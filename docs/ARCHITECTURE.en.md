# Proposed architecture

[Français](ARCHITECTURE.md)

## Three layers

| Layer | Responsibility | Distribution |
| --- | --- | --- |
| OldWeb style | Tokens, compositions, appearance of standard blocks, local assets | Downloaded design kit |
| OldWeb blocks | 88×31 buttons, neighbour links, what's-new log, retro gallery | Declarative data rendered by trusted components |
| Community modules | Guestbook, website network, possible statistics | Server code installed by the maintainer, separately from the kit |

A style creates neither accounts nor mandatory content. It does not change URLs, SEO fields, forms, permissions or business connectors. Deactivation preserves block data and renders it with a generic component or a preview warning; it does not delete it.

## Target download format

The minimal delivered format is described in [INSTALLATION](INSTALLATION.en.md): manifest, three JSON definitions and checksums. The assets and CSS described below are a future extension to audit; the v0.1 importer does not accept them.

Versioned archive: manifest, tokens, presets, audited CSS, approved assets, licence notices, documentation and checksums. No PHP, shell scripts, arbitrary JavaScript, SQL migrations or executable templates in a user-imported ZIP. Executable components belong to the already installed and audited engine.

If the current engine requires PHP templates, they must be a trusted extension supplied by the maintainer. The user's style ZIP remains declarative. Never claim that banning PHP alone makes imports secure.

The final manifest must declare the ID, kit version, format version, tested CMS version range, rendering adapter IDs/versions, required and optional blocks, allowed files, resource budget, licence and fallback behaviour. These versions are not specified here: they must come from inspected code.

## Installation and activation

1. Import into quarantine outside the public web root.
2. Check the signature from a trusted catalogue if available, provenance, compressed and expanded sizes, file count, duplicates, case collisions, absolute paths, directory traversal, symlinks and special names. Bound decompression time and space.
3. Validate the schema and actual file contents. Reject executable assets, active SVG and arbitrary HTML. Animated images need a static counterpart. Ban remote CSS imports, external URLs, remote fonts and constructs outside the permitted grammar; ideally compile tokens into trusted CSS.
4. Check engine capabilities. Block activation without a compatible adapter and explain what is missing. Missing optional features remain disabled.
5. Compute checksums and register an immutable package version. A checksum detects changes but does not authenticate the author.
6. Create a draft design configuration associated with the current content revision. Provide an authorised, non-indexable preview without exposing drafts via guessable URLs.
7. Atomically publish the content revision, design version and assets together. Reject publication based on stale revisions and offer to reload the preview. Use server-side idempotency keys and concurrency controls.
8. Keep the previous publication pointer for rollback. A rollback creates a new audited publication without rewriting historical revisions.

Installation, configuration, publication and module activation are distinct permissions to connect to the CMS's actual permission model. Offline mutations must not change the public design without revalidation.

## Rendering scope

The style applies to the public site. The administration area and MMW retain their navigation conventions and accessible components; only the name and previews identify the chosen style. Scope selectors under a dedicated website root, never to the administration document.

Preserve semantic structures: header/nav/main/aside/footer, one main heading, native links and labelled forms. Replace historical layout tables with modern rendering; real data tables remain tables.

Initial targets to measure, not observed results: kit CSS no more than 35 KB uncompressed; no third-party requests; no mandatory web font; initial decoration no more than 200 KB; no additional JavaScript for the first style. Editorial images use the existing media optimisation pipeline and explicit dimensions.

Functional kits, content and styles are separate objects. If a `design_styles` field already exists, inspect and reuse it instead of adding a second registry. Design exports should include media references and licences, never secrets or visitor data.
