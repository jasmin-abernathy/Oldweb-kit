import copy
import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('oldweb', SOURCE / 'tools/oldweb.py')
kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit)

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.archive = kit.build(self.root / 'kit.zip')
        self.cms = self.root / 'cms'
        (self.cms / 'schemas').mkdir(parents=True)
        (self.cms / 'design-styles').mkdir()
        for name in kit.expected_manifest()['schema_sha256']:
            (self.cms / 'schemas' / name).write_bytes((SOURCE / 'compatibility' / name).read_bytes())
        self.sentinel = self.cms / 'site-settings.json'
        self.sentinel.write_text('{"active_style":"quiet-elegant"}')
        self.before = self.sentinel.read_bytes()
    def tearDown(self):
        self.temp.cleanup()
    def hostile(self, transform):
        entries = list(kit.verify(self.archive).items())
        entries = transform(entries)
        bad = self.root / 'hostile.zip'
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(bad, 'w', zipfile.ZIP_DEFLATED) as z:
                for name, raw in entries:
                    z.writestr(name, raw)
        return bad
    def test_validate_all_styles_and_composition(self):
        self.assertEqual(len(kit.source_payload()), 5)
    def test_build_is_reproducible(self):
        second = kit.build(self.root / 'second.zip')
        self.assertEqual(self.archive.read_bytes(), second.read_bytes())
    def test_dry_run_is_read_only(self):
        self.assertEqual(kit.install(self.archive, self.cms, True), list(kit.IDS))
        self.assertEqual(list((self.cms / 'design-styles').iterdir()), [])
        self.assertEqual(self.sentinel.read_bytes(), self.before)
    def test_install_preserves_active_site(self):
        kit.install(self.archive, self.cms)
        for sid in kit.IDS:
            target = self.cms / 'design-styles' / sid
            self.assertTrue((target / '.oldweb-install.json').is_file())
            self.assertEqual((target / 'style.json').read_bytes(), (SOURCE / 'design-styles' / sid / 'style.json').read_bytes())
        self.assertEqual(self.sentinel.read_bytes(), self.before)
    def test_preflight_collision_does_not_partially_install(self):
        target = self.cms / 'design-styles' / kit.IDS[1]
        target.mkdir()
        (target / 'keep').write_text('unchanged')
        with self.assertRaises(kit.InvalidKit): kit.install(self.archive, self.cms)
        self.assertFalse((self.cms / 'design-styles' / kit.IDS[0]).exists())
        self.assertEqual((target / 'keep').read_text(), 'unchanged')
    def test_install_accepts_verified_current_cms_schema(self):
        schema = SOURCE / 'compatibility/site-composition-dendrila-2026-11-19.schema.json'
        (self.cms / 'schemas/site-composition.schema.json').write_bytes(schema.read_bytes())
        self.assertEqual(kit.install(self.archive, self.cms), list(kit.IDS))
        self.assertEqual(self.sentinel.read_bytes(), self.before)
    def test_schema_drift_blocks_install(self):
        (self.cms / 'schemas/design-style.schema.json').write_text('{}')
        with self.assertRaises(kit.InvalidKit): kit.install(self.archive, self.cms)
        self.assertEqual(list((self.cms / 'design-styles').iterdir()), [])
    def test_symlink_target_blocks_install(self):
        alias = self.root / 'alias'
        alias.symlink_to(self.cms, target_is_directory=True)
        with self.assertRaises(kit.InvalidKit): kit.install(self.archive, alias)
    def test_lock_blocks_install(self):
        lock = self.cms / 'design-styles/.oldweb-install.lock'
        lock.write_text('test')
        with self.assertRaises(kit.InvalidKit): kit.install(self.archive, self.cms)
        self.assertEqual(lock.read_text(), 'test')
    def test_failure_after_first_rename_rolls_back(self):
        original = kit.os.rename
        count = 0
        def failing(src, dest):
            nonlocal count
            count += 1
            if count == 2: raise OSError('simulated filesystem error')
            return original(src, dest)
        with patch.object(kit.os, 'rename', side_effect=failing):
            with self.assertRaises(OSError): kit.install(self.archive, self.cms)
        self.assertEqual(list((self.cms / 'design-styles').iterdir()), [])
        self.assertEqual(self.sentinel.read_bytes(), self.before)
    def test_path_traversal_and_code_refused(self):
        for name in ('../escape.json', '/absolute.json', 'run.php', 'design-styles/Oldweb-personal/style.json'):
            with self.subTest(name=name):
                bad = self.hostile(lambda entries: [(name, entries[0][1]), *entries[1:]])
                with self.assertRaises(kit.InvalidKit): kit.verify(bad)
    def test_duplicate_paths_refused(self):
        bad = self.hostile(lambda entries: [*entries, entries[0]])
        with self.assertRaises(kit.InvalidKit): kit.verify(bad)
    def test_tampered_bytes_refused(self):
        bad = self.hostile(lambda entries: [(n, r + b' ') if n.endswith('style.json') else (n,r) for n,r in entries])
        with self.assertRaises(kit.InvalidKit): kit.verify(bad)
    def test_symlink_member_refused(self):
        bad = self.root / 'symlink.zip'
        with zipfile.ZipFile(bad, 'w') as z:
            for name, raw in kit.verify(self.archive).items():
                info = zipfile.ZipInfo(name)
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                z.writestr(info, raw)
        with self.assertRaises(kit.InvalidKit): kit.verify(bad)
    def test_oversized_expansion_refused(self):
        bad = self.hostile(lambda entries: [(n, b'x' * (kit.MAX_FILE+1)) if n.endswith('style.json') else (n,r) for n,r in entries])
        with self.assertRaises(kit.InvalidKit): kit.verify(bad)
    def test_unknown_tokens_and_fields_refused(self):
        base = kit.parse_json((SOURCE / kit.STYLE_PATHS[0]).read_bytes())
        for change in ('token','field','boolean','id'):
            d = copy.deepcopy(base)
            if change == 'token': d['tokens']['layout']['content_width'] = 'url(https://tracker.invalid)'
            if change == 'field': d['custom_css'] = 'body{}'
            if change == 'boolean': d['constraints']['focus_visible'] = 1
            if change == 'id': d['id'] = '../escape'
            with self.subTest(change=change):
                with self.assertRaises(kit.InvalidKit): kit.validate_style(kit.json_bytes(d), kit.IDS[0])
    def test_duplicate_json_and_non_finite_refused(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'\xff'):
            with self.assertRaises(kit.InvalidKit): kit.parse_json(raw)
    def test_compile_scopes_variables_and_motion(self):
        css = kit.compile_style('oldweb-personal')
        self.assertIn('[data-design-style="oldweb-personal"]', css)
        self.assertIn('--mmw-content-max: 68rem;', css)
        self.assertIn('--mmw-radius: 0;', css)
        self.assertIn('--mmw-border-width: 2px;', css)
        self.assertIn('prefers-reduced-motion: reduce', css)
        self.assertNotIn('http', css)
        self.assertEqual(len(kit.MAPS), 10)
    def test_unknown_compile_id_refused(self):
        with self.assertRaises(kit.InvalidKit): kit.compile_style('../unsafe')
    def test_build_refuses_overwrite(self):
        before = self.archive.read_bytes()
        with self.assertRaises(kit.InvalidKit): kit.build(self.archive)
        self.assertEqual(self.archive.read_bytes(), before)

if __name__ == '__main__':
    unittest.main()
