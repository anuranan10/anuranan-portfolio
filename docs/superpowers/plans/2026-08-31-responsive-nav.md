# Responsive Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the portfolio usable on phones and tablets by replacing the cramped nav with a CSS-only hamburger below 768px, adding a tablet breakpoint, and stopping horizontal page overflow.

**Architecture:** All behavior comes from CSS. The menu toggle uses a hidden checkbox and a `<label>`, driven by `#nav-toggle:checked ~ .nav-links`. No JavaScript is added, consistent with `CLAUDE.md`. Nav markup is duplicated across 39 HTML files, so markup edits are performed by idempotent Python scripts that validate each file before touching it rather than by hand.

**Tech Stack:** HTML5, CSS3, Python 3.12 (build-time rewrite scripts only — not shipped to the browser), Chrome for layout verification.

## Global Constraints

- **No JavaScript.** No `<script>` tags, no event handlers, no JS files. Per `CLAUDE.md`.
- **No build step.** `style.css` remains the single shared stylesheet loaded directly by every page.
- **Desktop above 1024px must render identically to the current site.** This is a hard acceptance criterion, verified in Task 5.
- **Breakpoint boundaries are exact:** mobile is `@media (max-width: 768px)`; tablet is `@media (min-width: 769px) and (max-width: 1024px)`. 768px is mobile, not tablet.
- **The nav's nine links, their order, their `href` values, and their visible label text do not change.**
- **Bar height is 52px**, set explicitly. The value appears in `.nav-bar { height }` and in `.nav-links { max-height: calc(100vh - 52px) }`. These must stay in sync.
- Colors come from the existing palette: `#1f1f1f` nav background, `#ffffff` nav text, `#cfe3ff` focus ring.
- Python scripts live in `tools/` and must be safe to run twice (idempotent).

## File Structure

| File | Responsibility |
|---|---|
| `tools/verify_responsive.py` | **Create.** Structural test harness. Asserts nav shape, table wrapping, and CSS rules across all 39 pages. Run after every task. |
| `tools/rewrite_nav.py` | **Create.** One-purpose script: replaces the `<nav>` block in all 39 files. |
| `tools/wrap_tables.py` | **Create.** One-purpose script: wraps `<table>` elements in `.table-scroll`. |
| `style.css` | **Modify.** Add nav base rules, new tablet block, rewrite mobile nav rules, add `.table-scroll`, add `min-width: 0` fix. |
| `*.html` (39 files) | **Modify.** Nav block replaced (Task 2); tables wrapped in 11 of them (Task 3). |

Scripts are split by responsibility so a failure in table wrapping cannot corrupt nav markup, and either can be rerun independently.

Each task below leaves the site in a working, viewable state. Markup and its matching CSS always ship in the same commit — never a commit where markup has changed but its styles have not.

---

### Task 1: Verification harness

Builds the test that every later task is checked against. It must fail now and keep failing until Task 2 lands.

**Files:**
- Create: `tools/verify_responsive.py`

**Interfaces:**
- Consumes: nothing.
- Produces: a CLI returning exit code 0 on pass, 1 on failure. Later tasks run `python tools/verify_responsive.py` as their test step. Checks are grouped by name: `nav`, `tables`, `css`.

- [ ] **Step 1: Write the failing test harness**

Create `tools/verify_responsive.py`:

```python
"""Structural verification for the responsive nav work.

Run from the repo root:  python tools/verify_responsive.py
Exit code 0 = all checks pass, 1 = at least one failure.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

EXPECTED_LINKS = [
    ("index.html", "Home"),
    ("aerospace.html", "Aerospace"),
    ("cs.html", "Computer Science"),
    ("experience.html", "Work Experience"),
    ("lab-testing-experience.html", "Lab Testing Experience"),
    ("simulations.html", "Simulations"),
    ("highlights.html", "Highlights"),
    ("resume.html", "Resume"),
    ("contact.html", "Contact"),
]

NAV_RE = re.compile(r"<nav>.*?</nav>", re.DOTALL)
HREF_RE = re.compile(r'<a href="([^"]+)">([^<]*)</a>')
TABLE_RE = re.compile(r"<table[\s>]", re.IGNORECASE)
WRAPPED_TABLE_RE = re.compile(
    r'<div class="table-scroll">\s*<table[\s>]', re.IGNORECASE
)

failures = []


def fail(check, path, msg):
    failures.append(f"[{check}] {path}: {msg}")


def html_files():
    return sorted(p for p in ROOT.glob("*.html"))


def check_nav(path, html):
    nav = NAV_RE.search(html)
    if not nav:
        fail("nav", path.name, "no <nav>...</nav> block found")
        return
    block = nav.group(0)

    for needed in (
        'id="nav-toggle"',
        'class="nav-bar"',
        'class="nav-page"',
        'class="nav-links"',
        'for="nav-toggle"',
        'aria-label="Menu"',
    ):
        if needed not in block:
            fail("nav", path.name, f"missing {needed}")

    found = HREF_RE.findall(block)
    if found != EXPECTED_LINKS:
        fail("nav", path.name, f"link list changed: {found}")

    # The toggle must precede the links for the ~ sibling selector to work.
    if block.index('id="nav-toggle"') > block.index('class="nav-links"'):
        fail("nav", path.name, "nav-toggle must come before nav-links")


def check_tables(path, html):
    total = len(TABLE_RE.findall(html))
    wrapped = len(WRAPPED_TABLE_RE.findall(html))
    if total != wrapped:
        fail("tables", path.name, f"{total} tables, only {wrapped} wrapped")


def check_css():
    css = (ROOT / "style.css").read_text(encoding="utf-8")

    for needed in (
        ".nav-toggle",
        ".nav-bar",
        ".nav-page",
        ".nav-burger",
        ".nav-links",
        ".table-scroll",
        "@media (min-width: 769px) and (max-width: 1024px)",
    ):
        if needed not in css:
            fail("css", "style.css", f"missing rule/selector: {needed}")

    # The old rule is the direct cause of the oversized sticky mobile nav.
    if re.search(r"nav\s*\{[^}]*flex-direction:\s*column", css):
        fail("css", "style.css", "nav{flex-direction:column} must be removed")

    # Bar height and the menu's max-height must agree.
    if "calc(100vh - 52px)" not in css:
        fail("css", "style.css", "expected .nav-links max-height calc(100vh - 52px)")

    if "position: sticky" not in css:
        fail("css", "style.css", "nav should remain sticky")


def main():
    files = html_files()
    if len(files) != 39:
        fail("nav", "repo", f"expected 39 html files, found {len(files)}")

    for path in files:
        html = path.read_text(encoding="utf-8")
        check_nav(path, html)
        check_tables(path, html)

    check_css()

    if failures:
        print(f"FAIL - {len(failures)} problem(s):")
        for f in failures[:40]:
            print("  " + f)
        if len(failures) > 40:
            print(f"  ... and {len(failures) - 40} more")
        return 1

    print(f"PASS - {len(files)} files verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `python tools/verify_responsive.py`

Expected: exit code 1, output beginning `FAIL -`, listing missing `id="nav-toggle"` for all 39 files plus the missing CSS selectors. This confirms the harness detects the current, unfixed state.

- [ ] **Step 3: Commit the harness**

```bash
git add tools/verify_responsive.py
git commit -m "test: add structural verification for responsive nav work"
```

---

### Task 2: Nav markup and CSS

Markup and styles ship together so the site is never left with restyled markup and no styles.

**Files:**
- Create: `tools/rewrite_nav.py`
- Modify: all 39 `*.html` (nav block only)
- Modify: `style.css` (base nav rules, new tablet block, mobile nav rules)

**Interfaces:**
- Consumes: `tools/verify_responsive.py` from Task 1.
- Produces: the class names `.nav-toggle`, `.nav-bar`, `.nav-page`, `.nav-burger`, `.nav-links` in markup and CSS. Task 5 asserts against these exact names.

- [ ] **Step 1: Write the nav rewrite script**

Create `tools/rewrite_nav.py`:

```python
"""Replace the <nav> block in every page with the responsive version.

Safe to run more than once. Refuses to touch any file whose nav does not
match the known nine-link shape, and reports it instead of guessing.

Run from the repo root:  python tools/rewrite_nav.py
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

LINKS = [
    ("index.html", "Home"),
    ("aerospace.html", "Aerospace"),
    ("cs.html", "Computer Science"),
    ("experience.html", "Work Experience"),
    ("lab-testing-experience.html", "Lab Testing Experience"),
    ("simulations.html", "Simulations"),
    ("highlights.html", "Highlights"),
    ("resume.html", "Resume"),
    ("contact.html", "Contact"),
]

NAV_RE = re.compile(r"<nav>.*?</nav>", re.DOTALL)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
HREF_RE = re.compile(r'href="([^"]+)"')
SUFFIX = "| Anuranan Bharadwaj"


def page_name(path, html):
    """Derive the collapsed-bar label from the page's existing <title>."""
    if path.name == "index.html":
        return "Home"          # title does not follow the shared pattern
    m = TITLE_RE.search(html)
    if not m:
        return "Anuranan Bharadwaj"
    title = " ".join(m.group(1).split())
    if title.endswith(SUFFIX):
        title = title[: -len(SUFFIX)].strip()
    return title


def build_nav(name):
    links = "\n".join(
        f'      <a href="{href}">{label}</a>' for href, label in LINKS
    )
    return (
        "<nav>\n"
        '    <input type="checkbox" id="nav-toggle" class="nav-toggle">\n'
        '    <div class="nav-bar">\n'
        f'      <span class="nav-page">{name}</span>\n'
        '      <label for="nav-toggle" class="nav-burger" aria-label="Menu"></label>\n'
        "    </div>\n"
        '    <div class="nav-links">\n'
        f"{links}\n"
        "    </div>\n"
        "  </nav>"
    )


def main():
    changed, skipped, refused = 0, 0, []

    for path in sorted(ROOT.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        m = NAV_RE.search(html)
        if not m:
            refused.append((path.name, "no <nav> block"))
            continue

        block = m.group(0)

        if 'id="nav-toggle"' in block:
            skipped += 1          # already rewritten
            continue

        hrefs = HREF_RE.findall(block)
        if hrefs != [h for h, _ in LINKS]:
            refused.append((path.name, f"unexpected links {hrefs}"))
            continue

        new_html = html[: m.start()] + build_nav(page_name(path, html)) + html[m.end():]
        path.write_text(new_html, encoding="utf-8", newline="")
        changed += 1

    print(f"rewritten: {changed}   already done: {skipped}   refused: {len(refused)}")
    for name, why in refused:
        print(f"  REFUSED {name}: {why}")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run the rewrite**

Run: `python tools/rewrite_nav.py`

Expected: `rewritten: 39   already done: 0   refused: 0`. Any `REFUSED` line means stop and inspect that file — do not proceed.

- [ ] **Step 3: Spot-check two files**

Run: `sed -n '/<nav>/,/<\/nav>/p' index.html` and `sed -n '/<nav>/,/<\/nav>/p' aerospace.html`

Expected: `index.html` shows `<span class="nav-page">Home</span>`; `aerospace.html` shows `<span class="nav-page">Aerospace Projects</span>`. Both list the same nine links.

- [ ] **Step 4: Remove the two obsolete mobile nav rules**

In `style.css`, inside the `@media (max-width: 768px)` block, the current nav rule reads:

```css
    nav {
      flex-direction: column;
      align-items: center;
      gap: 0.5rem;
      padding: 1rem;
    }
```

Replace that entire rule with:

```css
    nav {
      flex-direction: row;
      align-items: stretch;
      flex-wrap: wrap;
      gap: 0;
      padding: 0;
    }
```

- [ ] **Step 5: Add base nav rules**

In `style.css`, immediately after the existing `nav a:hover` rule (around line 29), add:

```css
/* --- Responsive nav ------------------------------------------------ */
/* Hidden but focusable: clipped rather than display:none so the menu
   stays operable from the keyboard (Tab to it, Space to toggle). */
.nav-toggle {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    clip-path: inset(50%);
    white-space: nowrap;
}

/* Collapsed bar is mobile-only; hidden at tablet and desktop. */
.nav-bar {
    display: none;
}

.nav-links {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    align-items: center;
    flex: 1 1 100%;
}
```

Because `.nav-links` is the sole visible child of `nav` and reuses the same
`justify-content: space-around`, desktop rendering is unchanged.

- [ ] **Step 6: Add the tablet block**

In `style.css`, immediately **before** the `@media (max-width: 768px)` block, add:

```css
/* Tablet: keep one clean row instead of letting nine links wrap. */
@media (min-width: 769px) and (max-width: 1024px) {
    nav {
      padding: 0.75rem 0.5rem;
    }

    .nav-links {
      flex-wrap: nowrap;
      justify-content: center;
    }

    nav a {
      font-size: 0.85rem;
      margin: 0 0.4rem;
      white-space: nowrap;
    }
}
```

- [ ] **Step 7: Add the mobile nav rules**

In `style.css`, inside the `@media (max-width: 768px)` block, directly after the `nav` rule edited in Step 4, add:

```css
    .nav-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      height: 52px;          /* must match calc(100vh - 52px) below */
      box-sizing: border-box;
      padding: 0 0.5rem 0 1rem;
    }

    .nav-page {
      font-weight: bold;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      margin-right: 0.5rem;
    }

    /* Three bars drawn from two pseudo-elements: ::before carries the top
       bar plus a box-shadow copy for the middle, ::after is the bottom. */
    .nav-burger {
      position: relative;
      width: 44px;           /* 44px touch target */
      height: 44px;
      flex-shrink: 0;
      cursor: pointer;
    }

    .nav-burger::before,
    .nav-burger::after {
      content: "";
      position: absolute;
      left: 9px;
      width: 26px;
      height: 3px;
      border-radius: 2px;
      background: #fff;
      transition: top 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    }

    .nav-burger::before {
      top: 15px;
      box-shadow: 0 5.5px 0 #fff;   /* the middle bar */
    }

    .nav-burger::after {
      top: 26px;
    }

    /* Checked: collapse the three bars into an X. */
    .nav-toggle:checked ~ .nav-bar .nav-burger::before {
      top: 20px;
      box-shadow: none;
      transform: rotate(45deg);
    }

    .nav-toggle:checked ~ .nav-bar .nav-burger::after {
      top: 20px;
      transform: rotate(-45deg);
    }

    .nav-toggle:focus-visible ~ .nav-bar .nav-burger {
      outline: 2px solid #cfe3ff;
      outline-offset: -4px;
    }

    .nav-links {
      display: none;
      flex-direction: column;
      width: 100%;
      max-height: calc(100vh - 52px);   /* must match .nav-bar height */
      overflow-y: auto;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
    }

    .nav-toggle:checked ~ .nav-links {
      display: flex;
    }

    .nav-links a {
      margin: 0;
      padding: 0.85rem 1rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
```

- [ ] **Step 8: Run the harness**

Run: `python tools/verify_responsive.py`

Expected: still `FAIL`, but **only** `[tables]` failures remain — all `[nav]` and `[css]` checks now pass. If any `[nav]` or `[css]` line appears, fix it before committing.

- [ ] **Step 9: Commit**

```bash
git add tools/rewrite_nav.py style.css *.html
git commit -m "feat: add CSS-only hamburger nav and tablet breakpoint"
```

---

### Task 3: Scrollable data tables

**Files:**
- Create: `tools/wrap_tables.py`
- Modify: 11 `*.html` files containing tables
- Modify: `style.css` (add `.table-scroll`)

**Interfaces:**
- Consumes: `tools/verify_responsive.py` from Task 1.
- Produces: the `.table-scroll` wrapper class.

Affected files, 20 tables total: `AE315 Lab 04 - Forces and Moments on a Canard Delta Wing.html` (1), `AE417 Lab 06 - Rocket Thrust Measurement.html` (1), `AE443 Lab 01 - Servo Modeling.html` (1), `AE443 Lab 03 - SRV02 Position Control.html` (1), `AE443 Lab 05 - Speed Control.html` (1), `Aircraft Stability & Control Simulation.html` (4), `DC-8 PID Controller Design.html` (3), `NACA 2412 Airfoil CFD Analysis.html` (2), `Quanser Aero PID Control Design.html` (3), `TDRS-M Orbital Mechanics and Trajectory Design.html` (2), `Wind Tunnel Drag Study - Flap Deflection.html` (1).

- [ ] **Step 1: Write the table wrapping script**

Create `tools/wrap_tables.py`:

```python
"""Wrap every <table> in a horizontally scrollable container.

Keeps the page itself from scrolling sideways on phones while leaving
table markup untouched. Safe to run more than once.

Run from the repo root:  python tools/wrap_tables.py
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

TABLE_RE = re.compile(r"<table\b.*?</table>", re.DOTALL | re.IGNORECASE)
ALREADY_RE = re.compile(r'<div class="table-scroll">\s*$')


def main():
    total_wrapped, files_touched = 0, 0

    for path in sorted(ROOT.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        if "<table" not in html.lower():
            continue

        wrapped_here = 0
        out, pos = [], 0

        for m in TABLE_RE.finditer(html):
            preceding = html[: m.start()]
            # Skip if this table already sits inside a .table-scroll wrapper.
            if ALREADY_RE.search(preceding):
                continue
            out.append(html[pos:m.start()])
            out.append('<div class="table-scroll">\n')
            out.append(m.group(0))
            out.append('\n</div>')
            pos = m.end()
            wrapped_here += 1

        if wrapped_here:
            out.append(html[pos:])
            path.write_text("".join(out), encoding="utf-8", newline="")
            files_touched += 1
            total_wrapped += wrapped_here
            print(f"  {path.name}: wrapped {wrapped_here}")

    print(f"wrapped {total_wrapped} table(s) across {files_touched} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run it**

Run: `python tools/wrap_tables.py`

Expected: `wrapped 20 table(s) across 11 file(s)`, with per-file counts matching the list above.

- [ ] **Step 3: Confirm idempotency**

Run: `python tools/wrap_tables.py`

Expected: `wrapped 0 table(s) across 0 file(s)`. If it wraps again, the skip logic is broken — `git checkout -- *.html` and fix before continuing.

- [ ] **Step 4: Add the CSS**

In `style.css`, at the end of the file **outside** any media query (these rules apply at every width), add:

```css
/* Wide data tables scroll inside their own box so the page never
   scrolls horizontally. */
.table-scroll {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    max-width: 100%;
    margin-bottom: 1rem;
}
```

- [ ] **Step 5: Run the harness**

Run: `python tools/verify_responsive.py`

Expected: `PASS - 39 files verified`, exit code 0. All checks now green.

- [ ] **Step 6: Commit**

```bash
git add tools/wrap_tables.py style.css *.html
git commit -m "fix: make wide data tables scroll without moving the page"
```

---

### Task 4: Fix the `.project-image-cs` overflow

**Files:**
- Modify: `style.css` (mobile block)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: nothing consumed later.

`.project-image-cs` sets `min-width: 300px` (style.css:551) at every width. On a 320px viewport the content box is roughly 288px, so the element overflows and drags the page sideways.

- [ ] **Step 1: Add the override**

In `style.css`, inside the `@media (max-width: 768px)` block, the existing rule reads:

```css
    .project-image-cs {
      width: 100%;
      justify-content: center;
    }
```

Replace it with:

```css
    .project-image-cs {
      width: 100%;
      justify-content: center;
      min-width: 0;   /* overrides the 300px floor, which overflows a 320px screen */
    }
```

- [ ] **Step 2: Verify no regression**

Run: `python tools/verify_responsive.py`

Expected: `PASS - 39 files verified`.

- [ ] **Step 3: Commit**

```bash
git add style.css
git commit -m "fix: stop .project-image-cs overflowing narrow phone screens"
```

---

### Task 5: Browser verification

Structural checks cannot prove the layout is right. This task confirms actual rendering.

**Files:**
- No files modified. This task only observes and reports.

**Interfaces:**
- Consumes: the class names produced in Task 2 and Task 3.
- Produces: a pass/fail report. If anything fails, fix it and rerun the affected earlier task's test step.

Use the Chrome browser tools. Open the local file directly, e.g. `file:///C:/Users/anura/OneDrive%20-%20Embry-Riddle%20Aeronautical%20University/Desktop/Projects/Personal%20Website/index.html`.

- [ ] **Step 1: Check for horizontal overflow at every width**

For each width in **375, 800, 1024, 1440**, resize the window, then for each of `index.html`, `aerospace.html`, `cs.html`, `NACA 2412 Airfoil CFD Analysis.html`, and `DC-8 PID Controller Design.html`, evaluate:

```js
({
  w: window.innerWidth,
  scroll: document.documentElement.scrollWidth,
  client: document.documentElement.clientWidth,
  overflows: document.documentElement.scrollWidth > document.documentElement.clientWidth
})
```

Expected: `overflows: false` in all 20 combinations. If true, find the culprit with:

```js
[...document.querySelectorAll('*')]
  .filter(el => el.getBoundingClientRect().right > document.documentElement.clientWidth + 1)
  .slice(0, 5)
  .map(el => el.tagName + '.' + el.className)
```

- [ ] **Step 2: Confirm the menu toggles at 375px**

At 375px on `index.html`, evaluate:

```js
const cb = document.getElementById('nav-toggle');
const links = document.querySelector('.nav-links');
const before = getComputedStyle(links).display;
cb.click();
const after = getComputedStyle(links).display;
cb.click();
({ before, after, restored: getComputedStyle(links).display,
   count: links.querySelectorAll('a').length,
   page: document.querySelector('.nav-page').textContent })
```

Expected: `before: "none"`, `after: "flex"`, `restored: "none"`, `count: 9`, `page: "Home"`.

- [ ] **Step 3: Confirm the collapsed bar height**

At 375px, evaluate:

```js
({ bar: document.querySelector('.nav-bar').getBoundingClientRect().height,
   nav: document.querySelector('nav').getBoundingClientRect().height })
```

Expected: both `52`. This confirms the sticky nav no longer swallows the viewport, and that the `calc(100vh - 52px)` constant is correct.

- [ ] **Step 4: Confirm keyboard operability**

At 375px, evaluate:

```js
const cb = document.getElementById('nav-toggle');
cb.focus();
({ focused: document.activeElement === cb,
   visible: getComputedStyle(cb).display !== 'none' })
```

Expected: both `true`. A `display: none` checkbox is not focusable, so this guards the clip-rect approach.

- [ ] **Step 5: Confirm tablet renders one row**

At 1024px and again at 800px on `index.html`, evaluate:

```js
const tops = [...document.querySelectorAll('.nav-links a')]
  .map(a => Math.round(a.getBoundingClientRect().top));
({ tops, rows: new Set(tops).size,
   barHidden: getComputedStyle(document.querySelector('.nav-bar')).display })
```

Expected: `rows: 1` at both widths, and `barHidden: "none"`.

- [ ] **Step 6: Confirm desktop is unchanged**

At 1440px on `index.html` and `aerospace.html`, evaluate:

```js
const tops = [...document.querySelectorAll('.nav-links a')]
  .map(a => Math.round(a.getBoundingClientRect().top));
({ rows: new Set(tops).size,
   fontSize: getComputedStyle(document.querySelector('.nav-links a')).fontSize,
   barHidden: getComputedStyle(document.querySelector('.nav-bar')).display })
```

Expected: `rows: 1`, `fontSize: "16px"` (the unmodified base size), `barHidden: "none"`. Also take a screenshot and compare against `git stash`-ed original if any doubt remains.

- [ ] **Step 7: Confirm tables scroll locally**

At 375px on `NACA 2412 Airfoil CFD Analysis.html`, evaluate:

```js
const w = document.querySelector('.table-scroll');
({ scrollable: w.scrollWidth > w.clientWidth,
   pageOverflows: document.documentElement.scrollWidth > document.documentElement.clientWidth })
```

Expected: `pageOverflows: false`. `scrollable` may be either value depending on that table's width — the requirement is only that the page does not move.

- [ ] **Step 8: Report results**

Summarize each check as pass/fail with the measured numbers. Do not claim success for any check that was not actually run. If a check fails, report it plainly rather than adjusting the expectation.

---

## Self-Review

**Spec coverage:**

| Spec requirement | Task |
|---|---|
| Nav markup with checkbox toggle | 2 |
| Page name from `<title>`, `index.html` → "Home" | 2 (`page_name`) |
| Ellipsis truncation of long names | 2 (Step 7, `.nav-page`) |
| Desktop >1024px unchanged | 2 (Step 5), verified 5 (Step 6) |
| Tablet 769–1024px single row | 2 (Step 6), verified 5 (Step 5) |
| Mobile ≤768px hamburger | 2 (Steps 4, 7), verified 5 (Step 2) |
| Remove `nav{flex-direction:column}` | 2 (Step 4), asserted in harness |
| Sticky retained, 52px bar, bounded menu | 2 (Step 7), verified 5 (Step 3) |
| Keyboard focusable toggle | 2 (Step 5), verified 5 (Step 4) |
| 20 tables wrapped in `.table-scroll` | 3 |
| `.project-image-cs { min-width: 0 }` | 4 |
| No horizontal overflow at 4 widths | 5 (Step 1) |
| Out-of-scope items untouched | No task — correct, they are already handled |

No gaps.

**Placeholder scan:** No TBD/TODO. Every code step contains complete, runnable code. No "similar to Task N" references.

**Type consistency:** `EXPECTED_LINKS` in `verify_responsive.py` and `LINKS` in `rewrite_nav.py` hold identical data in the same order; both are checked against the same nine hrefs confirmed present in all 39 files. Class names `.nav-toggle`, `.nav-bar`, `.nav-page`, `.nav-burger`, `.nav-links`, `.table-scroll` are spelled identically in the harness, the rewrite script, the CSS, and the Task 5 browser assertions. The 52px constant appears in `.nav-bar { height }`, `.nav-links { max-height: calc(...) }`, the harness check, and Task 5 Step 3 — all consistent.

## Risks

The nav rewrite touches 39 files at once. `rewrite_nav.py` validates each file's link list before substituting and refuses rather than guessing, and every task is a separate commit, so `git revert` cleanly undoes any single stage.
