"""Add the skip link and the <main> landmark to every page.

Both are accessibility structure, invisible to a mouse user:
  * the skip link is the first thing Tab reaches, letting keyboard users
    jump past the nine nav links straight to the content;
  * <main> marks where the content starts so a screen reader's
    "jump to main content" command has a target.

Safe to run more than once. Refuses to touch any file whose shape is not
the expected <body> ... </nav> ... <footer> and reports it instead of
guessing.

Run from the repo root:  python tools/add_landmarks.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SKIP_LINK = '  <a class="skip-link" href="#main-content">Skip to content</a>'
BODY_RE = re.compile(r"<body[^>]*>")
NAV_END = "</nav>"
FOOTER_RE = re.compile(r"[ \t]*<footer[\s>]")


def main():
    changed, skipped, refused = 0, 0, []

    for path in sorted(ROOT.glob("*.html")):
        with open(path, encoding="utf-8", newline="") as fh:
            html = fh.read()

        if 'id="main-content"' in html:
            skipped += 1               # already has the landmarks
            continue

        body = BODY_RE.search(html)
        if not body:
            refused.append((path.name, "no <body> tag"))
            continue

        nav_end = html.find(NAV_END)
        if nav_end == -1:
            refused.append((path.name, "no </nav>"))
            continue

        footer = FOOTER_RE.search(html, nav_end)
        if not footer:
            refused.append((path.name, "no <footer> after </nav>"))
            continue

        content_start = nav_end + len(NAV_END)
        content = html[content_start:footer.start()]
        if not content.strip():
            refused.append((path.name, "no content between </nav> and <footer>"))
            continue

        # 1. skip link as the very first thing inside <body>
        new = (
            html[:body.end()]
            + "\n" + SKIP_LINK
            + html[body.end():content_start]
        )
        # 2. wrap everything up to the footer in <main>.
        # tabindex="-1" makes <main> a valid focus target: without it some
        # browsers follow the skip link by scrolling but leave keyboard
        # focus stranded back in the nav.
        new += (
            '\n  <main id="main-content" tabindex="-1">'
            + content.rstrip()
            + "\n  </main>\n"
            + html[footer.start():]
        )

        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        changed += 1

    print(f"landmarks added: {changed}   already done: {skipped}   "
          f"refused: {len(refused)}")
    for name, why in refused:
        print(f"  REFUSED {name}: {why}")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
