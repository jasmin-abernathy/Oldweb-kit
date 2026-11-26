# Oldweb-kit — 2000s web design for Dendrila CMS

[Version française](README.fr.md)

An independent visual style kit for [Dendrila CMS](https://github.com/jasmin-abernathy/dendrila-cms), intended for future management through Mon Manager Web (MMW). Styles can be combined with existing functional kits without replacing their content.

## Delivered

- Three style definitions using the **actual CMS v1 format**: personal homepage, panel-based portal and illustrated blog.
- Pinned compatibility schemas with verified CMS provenance.
- Dependency-free validation, compilation of existing design tokens, deterministic ZIP packaging and checksum verification.
- Conservative local installation into `design-styles/`: no overwriting or automatic activation on a website.
- Retro block contracts, a compatible composition example, an MMW roadmap and UX/security documentation.
- Local tests of hostile archives, schema errors, collisions and installation. No GitHub Actions workflow.

**Current limitation: the tokens express a design direction, not the complete retro rendering.** The CMS compiler produces CSS variables; it does not create a 1999/2004/2008 layout. The inspected CMS does not yet provide a complete public-facing adapter or a style management API. The kit can be installed in its catalogue; rendering and selection from MMW still need integration. Community modules are described, not enabled or presented as implemented.

## Usage

Python 3.10+; no dependencies to install. From this repository:

```sh
python3 tools/oldweb.py validate
python3 -m unittest discover -s tests -v
python3 tools/oldweb.py compile oldweb-personal
python3 tools/oldweb.py build dist/oldweb-kit-0.1.0.zip
python3 tools/oldweb.py verify dist/oldweb-kit-0.1.0.zip
python3 tools/oldweb.py install dist/oldweb-kit-0.1.0.zip /path/to/dendrila-cms --dry-run
python3 tools/oldweb.py install dist/oldweb-kit-0.1.0.zip /path/to/dendrila-cms
```

For an English-language catalogue, build a separate archive:

```sh
python3 tools/oldweb.py build dist/oldweb-kit-0.1.0-en.zip --language en
python3 tools/oldweb.py verify dist/oldweb-kit-0.1.0-en.zip
```

Install that archive using the same commands. Only labels, descriptions and keywords differ. The default French archive remains byte-for-byte unchanged. The CMS currently accepts a single label per style; this is a choice at packaging time, not automatic runtime language switching.

Then, in the CMS with its PHP 8.5+ toolchain:

```sh
php bin/compile-design-style.php oldweb-personal
```

Installation does not change a site's composition, settings, database or authentication. If any of the three IDs already exists, the whole operation is refused. Future upgrades require an explicit migration; this installer does not replace existing styles.

## Proposed visual directions

| ID | Label | Intent |
| --- | --- | --- |
| `oldweb-personal` | Personal homepage — 2000s | Strong borders, visible links, personal identity |
| `oldweb-portal` | Panel-based portal — 2000s | Compact sections, news and neighbour links |
| `oldweb-blog` | Illustrated blog — 2000s | Articles, banner and archives |

1999/2004/2008 are mood references from the original 15 August discussions, not promises of historical reconstruction. Visual development should begin with three mock-ups and a chosen direction; these files do not make that choice for the project owner.

## Documentation

- [Installation and limitations](docs/INSTALLATION.en.md)
- [Verified compatibility and MMW protocol](docs/COMPATIBILITY.en.md)
- [Architecture](docs/ARCHITECTURE.en.md)
- [UX/UI](docs/UX-UI.en.md)
- [Retro modules](docs/MODULES.en.md)
- [Animated backdrops without Flash](docs/ANIMATED-BACKDROPS.en.md)
- [Integration plan](docs/INTEGRATION.en.md)
- [Project origins](docs/ORIGINS.en.md)
- [Local validation](docs/VALIDATION.en.md)
- [Contribution guidelines](AGENTS.en.md)
- [Licensing status](LICENSE.en.md)

Sources and scripts are intended for maintainers. The generated ZIP contains only a manifest, JSON styles and their checksums: no executable code is imported by the client or CMS.

## Feedback

Suggestions, bug reports and contributions are welcome through [GitHub Issues](https://github.com/jasmin-abernathy/Oldweb-kit/issues) and pull requests. Please read the licensing status before redistributing the kit.
