# Next integration steps in Dendrila

[Français](INTEGRATION.md)

The kit is independent in `jasmin-abernathy/Oldweb-kit`. The core remains in `dendrila-cms` and the app in `lepotager-site-manager`.

## First delivered batch

Locally installable catalogue, three v1 definitions, compilation of closed tokens, reproducible archives and import pipeline tests. The Python compiler reproduces the ten mappings observed in the CMS compiler; the official PHP tool remains authoritative after installation.

## Visual rendering

1. Prepare three visual direction mock-ups from the UX brief, then choose a target.
2. Implement a trusted public adapter: semantic HTML, navigation, borders, secondary areas, gallery, 88×31 links and what's-new log.
3. Check mobile/desktop screenshots, keyboard, zoom, accessible mode and reduced motion; tokens alone are not a visual test.
4. Keep the public appearance isolated from MMW and administration.

## Publication and management

Reuse the CMS core for draft settings, authorised preview, server validation and versioned publication. Verify that offline changes cannot implicitly publish. Returning to a previous style must restore a coherent publication without deleting data. Do not change existing authentication.

## Blocks and modules

`contracts/retro-blocks.json` describes desired data; **it is not a file to import into the CMS schemas**. Connect buttons, links and galleries to the existing generic model. Guestbooks, counters and automatic webrings require a real backend, moderation, data controls and security tests; they are not necessary for the first rendering.

## Animated backdrops (optional, not yet integrated)

See [ANIMATED-BACKDROPS](ANIMATED-BACKDROPS.en.md) for the specification and integration plan. The first version remains static. Effects (video, Canvas/SVG/WebGL) are to be added **in a trusted Dendrila-side renderer** and configured through a versioned declarative contract with a poster, pause, reduced motion and a fallback without WebGL. Design ZIPs import no arbitrary scripts.

## Outstanding tests

- Run the PHP 8.5+ compiler on a target checkout with its autoloader.
- Integrate the pilot rendering and check content, URLs, SEO, forms and connectors.
- Test concurrent publication, idempotency and server rollback.
- Test the real MMW client against the same reference SHA.
- Measure page weight, requests and EcoIndex before announcing a score.

Do not enable a workflow for this kit while GitHub Actions usage is being conserved. Kit sources stay together; `dist/` is generated locally and excluded from Git.
