# Retro animated backdrops — Flash without Flash (integration proposal)

[Français](ANIMATED-BACKDROPS.md)

Status: **specification and research, not yet integrated rendering**. This document prepares an optional extension to Oldweb-kit and the public **Dendrila CMS** adapter. It changes neither the v1 style schema, the v0.1 ZIP contents, nor published sites.

## Intent

Recover the creativity of 2000s Flash backgrounds without Flash Player, proprietary plugins, third-party scripts or automatic audio. Draw inspiration from the *principles* of Cargo/Ragekit backdrops without copying proprietary code, media or effects. Animations must not be mandatory to enjoy the OldWeb style.

### Effect families to consider

| Family | Rendering | Preferred technique | Fallback |
| --- | --- | --- | --- |
| Ripples / distortions | Image ripples with pointer movement or slowly | WebGL with audited local shader; possibly Canvas 2D | Static source image |
| Kaleidoscope / mirror | Texture symmetry and rotation | Local WebGL; simple CSS/SVG geometry if possible | Static image |
| Slitscan / scanning | Moving strips and offsets | WebGL or Canvas 2D according to measured GPU/CPU cost | Static image |
| Pixelation / dithering | Low-resolution retro aesthetic | CSS (image-rendering) / Canvas 2D before WebGL | Static image |
| Decorative video loop | Short silent source animation | MP4/H.264, WebM if useful, local poster, progressive HTTP streaming | Poster |
| Simple animated gradients | Organic or retro backgrounds | CSS/SVG first | Static gradient |

Do not promise WebGL is always lighter than video: compare **transferred bytes, CPU/GPU, battery and stability** on mobile.

## Trusted architecture

- The **Oldweb-kit style** remains declarative: effect name from a **closed list**, native media library ID, bounded parameters (intensity, speed, pointer response, framing), static poster reference and activation choice. No arbitrary GLSL, JS, HTML or CSS imported from the ZIP.
- The animation engine and shaders, if present, are **shipped and audited with Dendrila CMS**, not loaded from a theme URL or Cargo. No third-party dependency by default.
- Video backgrounds use local media-library files; no YouTube/Vimeo embedding by default, to avoid external requests and cookies.
- Reuse the CMS media pipeline and composition model; do not add fields to v1 schemas without versioning a compatible contract. No automatic changes to existing settings.
- Backgrounds are purely decorative, outside keyboard and screen-reader navigation, with independent text, navigation and links readable on a contrast layer.
- Limit active engines per page; keep the background static while not visible.

## Required behaviour and accessibility

1. **Animated background** disabled by default for existing styles; explicit administrator configuration, preview before publishing, rollback.
2. Local poster visible before initialisation and after any error, including unavailable WebGL or context loss.
3. Honour `prefers-reduced-motion: reduce`: static poster **without initialising the animation engine**. Likewise for accessible mode if animation is disabled.
4. Visible **Pause background / Resume** control if animation lasts longer than five seconds or repeats; keyboard-accessible state preserved during the visit.
5. Disable pointer-reactive effects on devices without a fine pointer; the background must never be necessary to understand content.
6. Deferred activation with `IntersectionObserver`, stop on hidden tab via `visibilitychange`, and cap frame rate and pixel density. No automatic audio or flashes/strobes.
7. Video: `muted playsinline loop` only when deliberately enabled; `poster`, `preload="none"` or `metadata` depending on tests; `object-fit: cover` for decoration. A poster does not reduce transferred bytes if preload already downloads the video.

## Editor workflow (to implement in the CMS)

`Appearance → Styles → 2000s web → Background`, then:

- **Static / Animated effect / Short video**
- select source media and static poster from the media library;
- closed preset list (ripple, kaleidoscope, scanning, pixelation);
- speed (slow/normal), intensity (gentle/strong), pointer response (yes/no);
- pause control and mobile/reduced-motion preview;
- warning about estimated transfer and energy cost, without invented numbers.

The CMS must retain a fully functional static version. Simply installing Oldweb-kit does not enable any animation.

## Inspecting Ragekit with WebInspector

Search **Elements**, excluding occurrences in the large generic CSS sheet: `[data-backdrop]`, `data-backdrop="..."`, `canvas`, `<video`, `<source`, `video_background`, `shader`, `src=`, `data-src`. A generic CSS property does not prove an effect is active.

Search **Network**: `_jsapps/backdrop`, `t/webgl`, `freight.cargo.site`, `interlace.png`, `.mp4`, `.webm`, `videoplayback`, `.frag`, `.vert`, `.glsl`. A `googlevideo.com/videoplayback` request may be from an unrelated YouTube embed. A `/t/webgl/` URL suggests a texture prepared for WebGL rendering, **not** the exact effect type.

Then verify the actually displayed element, MIME type, transferred weight, first-screen request count, poster, off-screen pause, mobile rendering and fallback without WebGL.

### Useful sources

- Inspected site: https://ragekit.org/ (inspection screenshots supplied on 19 November 2026).
- Cargo Backdrops documentation: https://cargo.site/docs (video and interactive backdrops).
- Cargo compatibility: https://cargo.site/docs/browser-support (some animations require WebGL).

## Confirmed observation on 19 November 2026

Inspection of the **page DOM (excluding CSS)** on Ragekit shows this in a `page-3` block:

```html
<div data-backdrop="ripple" style="">
  <canvas width="1219" height="0" class="displacement_canvas"></canvas>
</div>
```

**Established fact:** Ragekit configures at least one Cargo **Ripple** backdrop with a displacement Canvas. The network request `freight.cargo.site/w/2048/t/webgl/i` makes a WebGL texture plausible, but does not prove that this Canvas used WebGL or drew anything when captured (`height="0"`). No `<video>` element was found in the reported WebInspector searches, but that does not establish that video is absent from every page. The `googlevideo.com` streams may be embedded YouTube videos.

**Implication for P1:** implement an **original Ripple distortion** first, without copying Cargo's shader; a demonstrator with `canvas` and local poster, plus an explicit fallback when WebGL is unavailable. Then measure actual download and GPU costs.

## First prototype implemented in Dendrila (19 November 2026)

The first **original Ripple** is more than an idea: it is developed in [Dendrila PR #35](https://github.com/jasmin-abernathy/dendrila-cms/pull/35) (**unmerged draft** at that point):

- `public/assets/oldweb-ripple.js`: original WebGL 1 shader, slow and pointer-driven distortion, bounded frame rate and dimensions;
- `public/assets/oldweb-ripple.css`: backdrop, poster, accessible pause and reduced-motion behaviour;
- `src/Front/OldwebRippleBackdrop.php`: closed and validated configuration with local media;
- `PublicPageRenderer`: opt-in decoration injection only if `presentation['backdrop']` is supplied;
- `ReferenceSiteBuilder` and `bin/build-reference-site.php --ripple`: example with original SVG image and `ripple-preview.html` page;
- contract and regression tests added.

**Checks performed:** JS syntax parsed successfully and simulated WebGL availability, pause/resume, unavailable WebGL and reduced-motion cases. **Remaining:** PHP 8.5 tests, browser visual checks, performance measurements and integration with the Dendrila/MMW editor. No production site was modified.

Usage documentation: `dendrila-cms/docs/OLDWEB-RIPPLE.md`. The active renderer belongs to Dendrila; **Oldweb-kit keeps styles declarative** and must not include executable code in its ZIP.

## Phases and acceptance criteria

- [x] **P0a — Identification:** concrete effect confirmed on a Ragekit page, `data-backdrop="ripple"` and `<canvas class="displacement_canvas">` (WebInspector capture on 19 November 2026).
- [ ] **P0b — Rendering validation:** observe actual animation, exact Canvas context, media and transferred bytes; other Ragekit sections may use other backdrops.
- [ ] **P1 — Proof of concept:** original audited local effect, static poster, pause control and no third-party requests; standalone demo and measurements.
- [ ] **P2 — Dendrila API:** shared renderer, preset allowlist, parameter validation, media/asset pipeline, kit/engine separation.
- [ ] **P3 — Editor:** reversible selection and preview, publication/rollback, mobile.
- [ ] **P4 — Tests:** keyboard, contrast, reduced motion, no WebGL, context loss, hidden-tab pause, low-powered mobile, energy consumption and network budget.

**Budgets to test, not guaranteed:** keep initial static decoration within the existing 200 KB target; compare video qualities and durations, set limits from measurements. Any measured regression must allow disabling the effect without impacting content.
