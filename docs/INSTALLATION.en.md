# Install the catalogue

[Français](INSTALLATION.md)

The tool is a maintainer CLI, not a web route. Do not expose it to visitors or construct a shell command from user input.

## Prerequisites

- Official Oldweb-kit repository source and a download authorised by the maintainer.
- Python 3.10+ for preparation. The target CMS requires PHP 8.5+ according to its composer.json; the Python CLI does not replace that requirement.
- CMS directory containing `schemas/design-style.schema.json`, `schemas/site-composition.schema.json` and `design-styles/`.
- Schemas matching the recorded snapshots exactly. Differences block installation: inspect upstream changes before updating the reference.
- Target paths must not be symlinks and no OldWeb style may already exist.

Run `validate`, `build`, `verify` and `install --dry-run` first, as shown in the [README](../README.md). A successful installation adds three directories under `design-styles/`, each containing `style.json` and a local `.oldweb-install.json` receipt.

Use `build ... --language en` to generate an English catalogue. The standard build keeps the original French style files. Both variants use the same v1 schemas and IDs and contain only the five allowed files. Choose the language before installation; changing an existing installation remains an explicit migration, not an overwrite. This does not translate the CMS interface itself.

The package is checked **before** writing into the CMS: only five predefined files are allowed. Malicious paths, duplicates, case collisions, symlinks, encrypted files, excessive size/count, an incorrect manifest and mismatched checksums are refused. JSON files are validated again before import. There is no general ZIP extraction: only known file contents are read.

The installer stages all styles under a local temporary directory and renames them. If an error occurs, it removes directories it just created to restore the previous state. This is not a durable transaction covering a sudden process termination or disk failure. A crash may leave a partially installed batch **without changing the active site**: inspect receipts before resuming.

## Trust and concurrency

SHA-256 verifies internal integrity, not the identity of the author. An attacker can rebuild a package with different checksums. Use an approved source and check the download; future public distribution should add a trust/signature chain.

An exclusive local lock prevents two installer instances from writing simultaneously. The CMS must be a checkout under the maintainer's control; the CLI does not claim to protect directories from another malicious process with the same privileges. A lock left after a crash is not removed automatically: check that no import is running before removing it.

## After installation

The catalogue is ready for the existing CMS compiler. The public site changes only once an adapter and its preview/publication cycle are implemented. `examples/site-composition.json` illustrates style selection but must not replace a real composition.

Reinstall/update is refused while a style exists. Do not automatically remove in-use styles. To deactivate, retain data and return to the previously published configuration through the future publication cycle. No publish button, data deletion or mock MMW manager is supplied.
