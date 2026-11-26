# Working in Oldweb-kit

[Français](AGENTS.md)

- Read `repo-factory/AGENTS.md`, its compatibility playbook, the CMS instructions and the MMW v1 protocol before integration.
- Keep visual styles independent of functional kits; classify them by visual outcome.
- Do not modify content, URLs, permissions, authentication or active settings while installing the catalogue.
- MMW must not execute downloaded code; community features remain server-side.
- No GitHub Actions workflow for this kit at this stage. Local packaging and tests; one coherent batch per push, `[skip ci]`.
- Do not present design tokens as complete retro rendering or guestbook contracts as an implemented backend.
- Do not introduce dependencies for tasks covered by the Python standard library.
- The installer imports only the three known JSON style files and never overwrites an existing path. Changes to this rule require regression tests.
- No actual visitor messages, secrets, tokens or private addresses in fixtures.
- UI rendering requires a chosen visual direction, mobile and keyboard checks and screenshots; the normal version must be accessible.
