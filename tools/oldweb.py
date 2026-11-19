#!/usr/bin/env python3
"""Maintainer-only, dependency-free OldWeb catalogue tooling (Python >= 3.10)."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
IDS = ('oldweb-personal', 'oldweb-portal', 'oldweb-blog')
STYLE_PATHS = tuple(f'design-styles/{name}/style.json' for name in IDS)
ARCHIVE_PATHS = frozenset(('manifest.json', 'SHA256SUMS', *STYLE_PATHS))
MAX_FILE = 32768
MAX_ARCHIVE = 262144
MAX_TOTAL = 131072

class InvalidKit(ValueError):
    pass

def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def parse_json(raw):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise InvalidKit(f'Duplicate JSON key: {k}')
            result[k] = v
        return result
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                          parse_constant=lambda x: (_ for _ in ()).throw(InvalidKit('Non-finite JSON number')))
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise InvalidKit(f'Invalid JSON: {exc}') from exc

def validate_schema(schema, value, location='$'):
    """Closed subset covering the two pinned CMS schemas; never silently ignore keywords."""
    supported = {'$schema', 'title', 'description', 'type', 'required', 'properties',
                 'additionalProperties', 'enum', 'const', 'pattern', 'minLength',
                 'maxLength', 'minItems', 'maxItems', 'uniqueItems', 'items', 'format'}
    if set(schema) - supported:
        raise InvalidKit(f'Unsupported schema keywords at {location}')
    typ = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'boolean': bool}
    if typ and (typ not in types or type(value) is not types[typ]):
        raise InvalidKit(f'Wrong type at {location}: {typ}')
    if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']):
        raise InvalidKit(f'Wrong constant at {location}')
    if 'enum' in schema and value not in schema['enum']:
        raise InvalidKit(f'Unsupported value at {location}')
    if isinstance(value, str):
        if not schema.get('minLength', 0) <= len(value) <= schema.get('maxLength', len(value)):
            raise InvalidKit(f'Wrong text length at {location}')
        if 'pattern' in schema and re.search(schema['pattern'], value) is None:
            raise InvalidKit(f'Unsafe or invalid text at {location}')
        if schema.get('format') == 'uri' and not re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:\S+$', value):
            raise InvalidKit(f'Invalid URI at {location}')
    if type(value) is dict:
        props = schema.get('properties', {})
        if set(schema.get('required', ())) - set(value):
            raise InvalidKit(f'Missing fields at {location}')
        if schema.get('additionalProperties') is False and set(value) - set(props):
            raise InvalidKit(f'Unknown fields at {location}')
        for k, v in value.items():
            if k in props:
                validate_schema(props[k], v, location + '.' + k)
    if type(value) is list:
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', len(value)):
            raise InvalidKit(f'Wrong list length at {location}')
        if schema.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            raise InvalidKit(f'Duplicate list entries at {location}')
        for v in value:
            if 'items' in schema:
                validate_schema(schema['items'], v, location + '[]')

def schema_for(name, root=ROOT):
    return parse_json((root / 'compatibility' / name).read_bytes())

def validate_style(raw, expected_id, root=ROOT):
    data = parse_json(raw)
    validate_schema(schema_for('design-style.schema.json', root), data)
    if data['id'] != expected_id:
        raise InvalidKit('Style ID does not match its path')
    return data

def expected_manifest(root=ROOT):
    provenance = parse_json((root / 'compatibility/upstream.json').read_bytes())
    return {'package_format': 1, 'id': 'oldweb-kit', 'version': '0.1.0',
            'styles': list(IDS), 'schema_sha256': provenance['schemas'],
            'automatic_activation': False, 'contains_executable_code': False}

def source_payload(root=ROOT):
    provenance = parse_json((root / 'compatibility/upstream.json').read_bytes())
    for name, digest in provenance['schemas'].items():
        if hashlib.sha256((root / 'compatibility' / name).read_bytes()).hexdigest() != digest:
            raise InvalidKit('Pinned schema digest mismatch')
    payload = {'manifest.json': json_bytes(expected_manifest(root))}
    for name, path in zip(IDS, STYLE_PATHS):
        raw = (root / path).read_bytes()
        validate_style(raw, name, root)
        payload[path] = raw
    composition = parse_json((root / 'examples/site-composition.json').read_bytes())
    validate_schema(schema_for('site-composition.schema.json', root), composition)
    if composition['design_style'] not in IDS:
        raise InvalidKit('Example references an unknown style')
    payload['SHA256SUMS'] = ''.join(f'{hashlib.sha256(raw).hexdigest()}  {path}\n'
                                  for path, raw in sorted(payload.items())).encode('ascii')
    return payload

def build(destination, root=ROOT):
    payload = source_payload(root)
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise InvalidKit('Output already exists; choose a new filename')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'x', zipfile.ZIP_DEFLATED) as archive:
        for path, raw in sorted(payload.items()):
            info = zipfile.ZipInfo(path, (2026, 9, 30, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, raw)
    verify(destination, root)
    return destination

def verify(path, root=ROOT):
    path = Path(path)
    if path.stat().st_size > MAX_ARCHIVE:
        raise InvalidKit('Archive too large')
    try:
        with zipfile.ZipFile(path) as archive:
            entries = archive.infolist()
            names = [i.filename for i in entries]
            if len(names) != len(ARCHIVE_PATHS) or set(names) != ARCHIVE_PATHS:
                raise InvalidKit('Unexpected, missing or duplicate archive paths')
            if len(set(n.casefold() for n in names)) != len(names):
                raise InvalidKit('Case-colliding archive paths')
            if sum(i.file_size for i in entries) > MAX_TOTAL:
                raise InvalidKit('Expanded archive too large')
            payload = {}
            for info in entries:
                mode = info.external_attr >> 16
                if info.flag_bits & 1 or stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG)):
                    raise InvalidKit('Encrypted or non-regular archive member')
                if info.file_size > MAX_FILE:
                    raise InvalidKit('Archive member too large')
                with archive.open(info) as stream:
                    raw = stream.read(MAX_FILE + 1)
                if len(raw) > MAX_FILE or len(raw) != info.file_size:
                    raise InvalidKit('Incorrect archive member size')
                payload[info.filename] = raw
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError) as exc:
        raise InvalidKit(f'Unreadable archive: {exc}') from exc
    if parse_json(payload['manifest.json']) != expected_manifest(root):
        raise InvalidKit('Manifest differs from supported package contract')
    checksums = ''.join(f'{hashlib.sha256(raw).hexdigest()}  {name}\n'
                        for name, raw in sorted(payload.items()) if name != 'SHA256SUMS').encode('ascii')
    if payload['SHA256SUMS'] != checksums:
        raise InvalidKit('Checksum mismatch')
    for name, member in zip(IDS, STYLE_PATHS):
        validate_style(payload[member], name, root)
    return payload

def safe_existing(path):
    """Reject symlink components, including ancestors, in a maintainer-controlled checkout."""
    absolute = Path(os.path.abspath(path))
    if any(p.is_symlink() for p in (absolute, *absolute.parents)):
        raise InvalidKit(f'Symlink component in target: {path}')
    return absolute

def install(archive, cms, dry_run=False, root=ROOT):
    payload = verify(archive, root)
    cms = safe_existing(cms)
    catalogue = safe_existing(cms / 'design-styles')
    if not catalogue.is_dir():
        raise InvalidKit('Missing CMS design-styles directory')
    provenance = parse_json((root / 'compatibility/upstream.json').read_bytes())
    alternatives = provenance.get('compatible_install_schemas', {})
    for name, digest in expected_manifest(root)['schema_sha256'].items():
        path = safe_existing(cms / 'schemas' / name)
        compatible = {digest, alternatives.get(name, {}).get('sha256')}
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() not in compatible:
            raise InvalidKit('CMS schema differs from verified contract: ' + name)
    def check_targets():
        for name in IDS:
            target = catalogue / name
            if target.exists() or target.is_symlink():
                raise InvalidKit('Style already exists: ' + name)
    check_targets()
    if dry_run:
        return list(IDS)
    lock = catalogue / '.oldweb-install.lock'
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise InvalidKit('Another install or unresolved crash lock exists') from exc
    installed = []
    try:
        with os.fdopen(lock_fd, 'w') as stream:
            stream.write(str(os.getpid()))
        check_targets()
        with tempfile.TemporaryDirectory(prefix='.oldweb-stage-', dir=catalogue) as temporary:
            stage = Path(temporary)
            for name, member in zip(IDS, STYLE_PATHS):
                directory = stage / name
                directory.mkdir(mode=0o755)
                (directory / 'style.json').write_bytes(payload[member])
                (directory / '.oldweb-install.json').write_bytes(json_bytes({
                    'package': 'oldweb-kit', 'version': '0.1.0', 'id': name,
                    'style_sha256': hashlib.sha256(payload[member]).hexdigest()}))
            try:
                for name in IDS:
                    destination = catalogue / name
                    if destination.exists() or destination.is_symlink():
                        raise InvalidKit('Concurrent target appeared: ' + name)
                    os.rename(stage / name, destination)
                    installed.append(destination)
            except BaseException:
                for directory in reversed(installed):
                    shutil.rmtree(directory)
                raise
    finally:
        lock.unlink()
    return list(IDS)

# Maps from the inspected CMS CssTokenCompiler, pinned in compatibility/upstream.json.
MAPS = {
    '--mmw-content-max': ('layout.content_width', {'narrow':'48rem','medium':'68rem','wide':'84rem','full':'100%'}),
    '--mmw-section-gap': ('layout.section_spacing', {'compact':'2.5rem','balanced':'4rem','airy':'6rem'}),
    '--mmw-text-max': ('layout.text_column', {'narrow':'42rem','medium':'54rem','wide':'68rem'}),
    '--mmw-radius': ('surfaces.radius', {'none':'0','small':'0.35rem','medium':'0.8rem','large':'1.4rem'}),
    '--mmw-border-width': ('surfaces.borders', {'none':'0','subtle':'1px','present':'2px'}),
    '--mmw-shadow': ('surfaces.shadows', {'none':'none','subtle':'0 0.5rem 1.5rem rgb(0 0 0 / 0.08)'}),
    '--mmw-heading-scale': ('typography.scale', {'restrained':'1','balanced':'1.12','expressive':'1.28'}),
    '--mmw-media-emphasis': ('media.prominence', {'low':'0.75','medium':'1','high':'1.2'}),
    '--mmw-accent-strength': ('accent.usage', {'restrained':'0.35','balanced':'0.65','strong':'1'}),
    '--mmw-motion-duration': ('motion.level', {'none':'0ms','subtle':'160ms','expressive':'260ms'}),
}

def compile_style(name, root=ROOT):
    if name not in IDS:
        raise InvalidKit('Unknown style ID')
    data = validate_style((root / f'design-styles/{name}/style.json').read_bytes(), name, root)
    selector = f'[data-design-style="{name}"]'
    lines = [selector + ' {']
    for variable, (path, mapping) in MAPS.items():
        group, key = path.split('.')
        lines.append(f'  {variable}: {mapping[data["tokens"][group][key]]};')
    lines += ['}', '', '@media (prefers-reduced-motion: reduce) {',
              '  ' + selector + ' { --mmw-motion-duration: 0ms; }', '}']
    return '\n'.join(lines) + '\n'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('validate')
    compile_command = commands.add_parser('compile')
    compile_command.add_argument('style', choices=IDS)
    for command in ('build', 'verify'):
        commands.add_parser(command).add_argument('archive', type=Path)
    install_command = commands.add_parser('install')
    install_command.add_argument('archive', type=Path)
    install_command.add_argument('cms', type=Path)
    install_command.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'validate':
            source_payload()
            print('Styles and composition valid against pinned CMS schemas.')
        elif args.command == 'compile':
            print(compile_style(args.style), end='')
        elif args.command == 'build':
            print(build(args.archive))
        elif args.command == 'verify':
            verify(args.archive)
            print('Archive valid. Integrity is not proof of publisher identity.')
        else:
            styles = install(args.archive, args.cms, args.dry_run)
            print(('Would install: ' if args.dry_run else 'Installed into catalogue: ') + ', '.join(styles))
            print('No site was activated or modified.')
    except (InvalidKit, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
