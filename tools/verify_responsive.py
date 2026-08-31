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
