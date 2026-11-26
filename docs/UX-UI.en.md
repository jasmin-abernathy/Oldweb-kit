# UX and UI direction

[Français](UX-UI.md)

## Catalogue by visual outcome

A "2000s web" entry in the visual catalogue, alongside "Image-focused" or "Simple and elegant". Dates are mood references, not business categories or guarantees of historical reconstruction.

| Direction to mock up | Visible outcome | Composition use |
| --- | --- | --- |
| Personal homepage, around 1999 | Strong borders, sidebar navigation, small badges, underlined links, customisable background | Personal presentation, links, journal and gallery |
| Panel-based portal, around 2004 | Banner, tabbed menus, compact modules and central news | Pages rich in sections and news |
| Illustrated blog, around 2008 | Illustrated banner, prominent articles, sidebar archives, visually distinct comments | Reading and regular publication |

These three directions are proposals to visualise and choose before coding the rendering. The first delivery should cover **one complete direction**; the other two follow validation. The CMS must allow the same style to be combined with different functional kits.

## Identity and readability

Keep genuine retro expressiveness: borders, panel hierarchy, badges, controlled density and clearly visible links. Avoid turning everything into large rounded cards on a modern landing page. Nostalgia does not justify tiny text, pop-ups, autoplay audio, flashing or unpredictable navigation.

Background, banner and badges are local assets selected from the media library; meaningful alt text for informative images, empty alt text for decoration. Packs must not copy historical brands or service images without a licence. System fonts by default, relative reading sizes and contrast checked against actual chosen colours.

Guided customisation: mood, palette, banner, reading width, density, borders and panel placement. No free-form CSS in the initial client workflow. If a colour makes text unreadable, show the result and suggest a correction with a preview; keep safeguards for interactive elements.

## Mobile

Semantic order: identity → navigation → main content → secondary panels → footer. A grid can position panels beside content on desktop without moving essential content in the DOM. On mobile, one column; compact keyboard-operable menu, visible focus and focus restoration after closing. The editor may reorder secondary panels without hiding essential content.

88×31 buttons retain their historical graphic dimensions; the enclosing link provides a larger touch target. Images do not overflow, text remains usable when zoomed and there is no horizontal page scrolling at 320 px. A real table may have its own labelled scrolling container.

## Motion

Initial version is static. Any GIFs are opt-in and accompanied by a fixed visual. "Reduce animations" replaces animated images with their static versions; `prefers-reduced-motion` also triggers replacement because CSS cannot pause a GIF. No flashing effects. A future scrolling banner must have a visible stop control, the same accessible text and a static version; never use marquee or blink elements.

Accessible mode is supplementary: the normal version must already be usable. It reduces textures and decoration, increases line spacing, reinforces contrast and preserves content and links.

## Owner workflow

1. Appearance → Styles → "2000s web" → kit details, compatibility and size.
2. Install without publishing: the old site is still served.
3. Select mood and settings. "Try with my content" opens a preview; no sample text overwrites the website.
4. Compare desktop/mobile, accessible mode and reduced motion. Provide a readable list of blocks with different fallbacks.
5. "Publish this style" shows the relevant revision. After publication: active status, date and control to return to the previous style.

A community module is configured elsewhere, under features: short explanation, retained data, moderation and permissions. The style never automatically enables a public guestbook.

## States to design

Download in progress, invalid archive, incompatible engine, missing optional dependency, expired preview, concurrent edit, publication success/failure, rollback completed, missing media, unknown block and MMW offline state. Errors preserve draft settings; never display "style active" before server confirmation.
