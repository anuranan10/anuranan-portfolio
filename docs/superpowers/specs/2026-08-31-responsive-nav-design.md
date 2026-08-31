# Responsive Navigation and Small-Screen Layout Fixes

**Date:** 2026-08-31
**Status:** Approved for planning

## Problem

The site renders well on desktop but degrades on phones and tablets.

**Tablet (769–1024px).** `style.css` has exactly one media query, at `max-width: 768px`. Nothing covers the tablet range, so an iPad renders all nine nav links at full desktop font and `margin: 0 1rem`. The nine labels plus margins exceed 1024px, so `flex-wrap: wrap` breaks them into ragged rows distributed by `justify-content: space-around`. This is the crowding reported by the user.

**Phone (≤768px).** `nav` is set to `flex-direction: column` (style.css:789) while remaining `position: sticky` (style.css:15). Nine stacked full-width links produce a sticky bar that occupies most of the viewport and never scrolls away.

**Secondary issues.**

- 20 data tables across 11 project pages have no responsive handling and force horizontal scrolling of the whole page.
- `.project-image-cs` retains `min-width: 300px` (style.css:551) at all widths. On a 320px viewport the available content box is roughly 288px, so the element overflows.

Note: all 39 HTML files already carry a correct viewport meta tag. That is not a contributing cause.

## Constraints

- Pure HTML5 + CSS3. **No JavaScript**, per `CLAUDE.md`. The chosen menu uses the CSS checkbox technique and introduces no scripts.
- No build step. `style.css` is the single shared stylesheet.
- Nav markup is duplicated across all 39 HTML files and must be edited in each.
- Desktop rendering above 1024px must remain visually identical.

## Decisions

Settled with the user during brainstorming:

| Question | Decision |
|---|---|
| Mobile nav pattern | CSS-only hamburger (checkbox technique) |
| Hamburger threshold | Phones only (<768px); tablets keep a tightened single row |
| Collapsed bar label | Current page name |
| Table behavior | Horizontal scroll within the table's own container |

## Design

### Nav markup

Replaces the existing `<nav>` block in all 39 files:

```html
<nav>
  <input type="checkbox" id="nav-toggle" class="nav-toggle">
  <div class="nav-bar">
    <span class="nav-page">PAGE NAME</span>
    <label for="nav-toggle" class="nav-burger" aria-label="Menu"></label>
  </div>
  <div class="nav-links">
    <a href="index.html">Home</a>
    <a href="aerospace.html">Aerospace</a>
    <a href="cs.html">Computer Science</a>
    <a href="experience.html">Work Experience</a>
    <a href="lab-testing-experience.html">Lab Testing Experience</a>
    <a href="simulations.html">Simulations</a>
    <a href="highlights.html">Highlights</a>
    <a href="resume.html">Resume</a>
    <a href="contact.html">Contact</a>
  </div>
</nav>
```

The nine links, their order, their `href` values, and their label text are unchanged.

Toggling is driven by `#nav-toggle:checked ~ .nav-links { display: flex; }`.

The checkbox is hidden with a clip rectangle rather than `display: none`, so it remains keyboard-focusable and Space toggles the menu. The `<label>` provides the pointer target.

### Page name derivation

`PAGE NAME` is each file's existing `<title>` with the trailing `" | Anuranan Bharadwaj"` removed. This is mechanical for 38 of 39 files.

`index.html` is the sole exception — its title is `"Anuranan Bharadwaj | Aerospace & CS Portfolio"`, which does not fit the pattern. It gets the literal string `Home`.

Existing HTML entities in titles (`&amp;`, `&mdash;`) are carried through unchanged, since the destination is also HTML.

Long names are not shortened by hand. `.nav-page` applies `overflow: hidden; text-overflow: ellipsis; white-space: nowrap;` so the longest case — "Lab 04: Forces and Moments on a Canard Delta Wing" — truncates visually.

### Breakpoints

Three tiers. Boundaries are stated precisely because 768px is the existing query edge and must not become ambiguous:

- Mobile: `@media (max-width: 768px)` — the existing block. 768px itself is mobile.
- Tablet: `@media (min-width: 769px) and (max-width: 1024px)` — new block.
- Desktop: everything above 1024px, i.e. the unwrapped base rules.

**Above 1024px — unchanged.** `.nav-bar` is `display: none`. `.nav-links` renders as the current flex row with today's font size and margins. No visual change from the current site.

**769–1024px (new).** `.nav-bar` stays hidden and `.nav-links` stays a row, but `nav a` drops to `font-size: 0.85rem` and `margin: 0 0.4rem`, with `justify-content: center`. This fits all nine links on one line instead of wrapping.

**768px and below.** `.nav-bar` becomes visible as a flex row (page name left, burger right). `.nav-links` is `display: none` until the checkbox is checked, then `display: flex` with `flex-direction: column`.

The existing `nav { flex-direction: column; }` rule at style.css:789 is **removed**. That rule applied the column layout to the nav container itself and is the direct cause of the oversized sticky bar.

### Sticky behavior

`position: sticky` is retained at all widths. Collapsed, the mobile bar is a fixed 52px — set explicitly via `.nav-bar { height: 52px; box-sizing: border-box; }` rather than left to content height, so the value below is exact and not an estimate. Stickiness is now useful rather than obstructive.

When expanded, `.nav-links` receives `max-height: calc(100vh - 52px)` and `overflow-y: auto`, guaranteeing the open menu can never exceed the viewport regardless of how many links exist. The two 52px values must stay in sync; if the bar height changes, the `calc()` changes with it.

### Tables

Each of the 20 `<table>` elements is wrapped:

```html
<div class="table-scroll">
  <table> ... </table>
</div>
```

`.table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; max-width: 100%; }`

Table internals — columns, headers, cell content — are not modified. The page body no longer scrolls horizontally; the table scrolls within its own box.

Affected files (20 tables across 11 files):

- `AE315 Lab 04 - Forces and Moments on a Canard Delta Wing.html` (1)
- `AE417 Lab 06 - Rocket Thrust Measurement.html` (1)
- `AE443 Lab 01 - Servo Modeling.html` (1)
- `AE443 Lab 03 - SRV02 Position Control.html` (1)
- `AE443 Lab 05 - Speed Control.html` (1)
- `Aircraft Stability & Control Simulation.html` (4)
- `DC-8 PID Controller Design.html` (3)
- `NACA 2412 Airfoil CFD Analysis.html` (2)
- `Quanser Aero PID Control Design.html` (3)
- `TDRS-M Orbital Mechanics and Trajectory Design.html` (2)
- `Wind Tunnel Drag Study - Flap Deflection.html` (1)

### Overflow fix

`.project-image-cs` gains `min-width: 0` inside the `max-width: 768px` block, overriding the `min-width: 300px` at style.css:551.

### Explicitly out of scope

- `.ae-featured-images img` and `.ae-card-images img` (`width: 340px`, style.css:702 and :755) are **already** overridden in the existing mobile block at style.css:878–888. No change.
- `.about { text-align: justify }` is **already** overridden to `center` at style.css:815. No change.
- Consolidating the duplicated nav across 39 files is a pre-existing architectural property, not introduced here, and is not addressed. Flagged to the user separately.

## Verification

Render pages in Chrome at 375px (phone), 800px (tablet), 1024px (tablet upper edge), and 1440px (desktop). 768px is deliberately not a tablet test width — it falls in the mobile tier.

1. **No horizontal overflow.** At each width, `document.documentElement.scrollWidth <= document.documentElement.clientWidth`. Check `index.html`, `aerospace.html`, `cs.html`, and at least two table-bearing project pages.
2. **Menu toggles.** At 375px, the collapsed bar shows the correct page name; tapping the burger reveals all nine links; tapping again collapses.
3. **Keyboard access.** At 375px, the toggle is reachable by Tab and operable with Space.
4. **Desktop unchanged.** At 1440px, `index.html` and `aerospace.html` are visually identical to the pre-change site.
5. **Tablet single row.** At 1024px and 800px, nav links occupy exactly one row with no wrapping. Measured by confirming every `nav a` shares the same `offsetTop`.
6. **Tables scroll locally.** On a table page at 375px, the table scrolls horizontally while the page does not.

## Risks

Editing 39 files mechanically risks inconsistency if any nav block deviates from the expected shape. The rewrite script must verify each file's nav matches the known pattern before substituting, and report any file it declines to touch rather than silently skipping or partially editing it.
