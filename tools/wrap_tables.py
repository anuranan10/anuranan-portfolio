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
