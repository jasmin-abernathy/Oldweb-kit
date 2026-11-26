# Origins and decisions

[Français](ORIGINS.md)

A review of earlier discussions located an exchange on 15 August 2026: Jasmin requested a standalone CMS inspired by the web of the 1990s–2000s, called "OldWeb CMS" in the responses. Suggestions included 1999/2004/2008 themes, counters, guestbooks, 88×31 buttons, blinkies, GIFs, scrolling banners, webrings and galleries. Distinguish the original request from assistant proposals, which were not all approved.

On 30 September, Jasmin wanted to prepare this experience as an additional Dendrila CMS kit. The preference was a catalogue organised by visual outcome, independently of business purpose. The private Oldweb-kit repository was supplied and confirmed empty through direct GitHub access.

Decision at that stage: keep the complete experience in the Dendrila core rather than build a second standalone CMS. Separate style, blocks and community features. Downloads must remain lightweight and must not send dynamic code into MMW.

The initial design documents in `docs/` express the product target. README, INSTALLATION and COMPATIBILITY describe actually delivered capabilities and their limitations.

The commercial name confirmed on 30 September is **Dendrila CMS**. Repository paths, namespaces and `--mmw-*` variables are retained to match the inspected code; their migration is handled separately with compatibility. No temporary handoff between models is committed.
