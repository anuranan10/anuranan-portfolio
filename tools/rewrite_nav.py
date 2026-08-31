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
