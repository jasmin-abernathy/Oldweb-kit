# Verified compatibility

[Français](COMPATIBILITY.md)

CMS inspected through direct GitHub access on 30 September 2026: commit `49f95c98a904fbb116e698006b42232c505bb65c` of `jasmin-abernathy/dendrila-cms`.

## Present

- `schemas/design-style.schema.json`, format 1, closed vocabulary and no additional fields.
- `schemas/site-composition.schema.json`: separate `functional_kit` and `design_style`.
- `src/Design/DesignStyleDefinition.php`: token and constraint validation.
- `src/Design/CssTokenCompiler.php`: ten CSS variables and reduced motion.
- `bin/compile-design-style.php`: reads from `design-styles/<id>/style.json`.
- Six initial presets, documentation and a gallery example.

All three styles use only this contract. Retro palettes, badges and compositions are not added as unknown fields in style.json: the schema would reject them. Extensions remain a separate contract to develop in the adapter.

## Not demonstrated / outstanding

The inspected tree and design files do not provide a complete public OldWeb renderer, package importer or MMW style-selection route. This kit adds a local import tool, not a new core API. No PHP 8.5 or actual MMW test was executed in that session; Python and consistency with inspected sources were checked locally.

## MMW v1

The current protocol supports `form`, `records`, `gallery`, `requests`, `calendar` and `dashboard`. `settings` is reserved. Available fields include `single_choice`, `boolean`, `text` and `url`; do not create an `oldweb` client type.

Style selection could be a `single_choice` field in a server-provided form. However, `update_fields` does not prove that a style publication API already exists. Add storage, permissions, revisions and preview before exposing the form. For an action on `records`, use only an authorised online server action (`allow_offline=false`). Older clients ignore unknown types; no mobile code extension is downloaded.

Schemas are pinned by SHA-256 in `compatibility/upstream.json`. The installer compares target CMS schemas against these copies and blocks any divergence. Compatibility does not rely on an invented version number.

### Dendrila, 19 November 2026

The installer also accepts the exact composition-schema checksum from Dendrila commit `e45aca880ee08e442094227cb710d524555b6be3`. That schema adds brand options and requires HTTPS for the logo. The composition supplied by the kit remains valid. Manifest checksums and existing 0.1.0 archives remain compatible. Other schema revisions still require verification before acceptance.
