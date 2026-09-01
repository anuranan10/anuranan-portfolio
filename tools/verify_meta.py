"""Structural verification for the page metadata.

Run from the repo root:  python tools/verify_meta.py
Exit code 0 = all checks pass, 1 = at least one failure.

Checks every page carries exactly one auto-generated metadata block, that
its description is a sane length, that Open Graph URLs are absolute, and
that every asset those tags point at actually exists on disk.
"""
import html
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://anuranan.info"

BLOCK_RE = re.compile(r"<!-- meta:auto -->(.*?)<!-- /meta:auto -->", re.DOTALL)
CONTENT_RE = re.compile(
    r'<meta (?:name|property)="([^"]+)" content="([^"]*)">'
)
LINK_RE = re.compile(r'<link rel="([^"]+)"[^>]*href="([^"]+)"')

REQUIRED_META = [
    "description",
    "og:type",
    "og:site_name",
    "og:title",
    "og:description",
    "og:url",
    "og:image",
    "twitter:card",
]
REQUIRED_ASSETS = [
    "favicon.svg",
    "favicon.png",
    "favicon.ico",
    "apple-touch-icon.png",
    "og-card.png",
]

failures = []


def fail(check, path, msg):
    failures.append(f"[{check}] {path}: {msg}")


def local_path(url):
    """Map an absolute site URL back to the file it should resolve to."""
    if not url.startswith(SITE + "/"):
        return None
    rel = urllib.parse.unquote(url[len(SITE) + 1:])
    return ROOT / rel if rel else ROOT / "index.html"


def check_page(path):
    text = path.read_text(encoding="utf-8")

    blocks = BLOCK_RE.findall(text)
    if len(blocks) != 1:
        fail("block", path.name, f"expected 1 meta:auto block, found {len(blocks)}")
        return
    block = blocks[0]

    if text.index("<!-- meta:auto -->") > text.index("</head>"):
        fail("block", path.name, "metadata block sits outside <head>")

    meta = {k: v for k, v in CONTENT_RE.findall(block)}
    for key in REQUIRED_META:
        if key not in meta:
            fail("meta", path.name, f"missing {key}")

    desc = html.unescape(meta.get("description", ""))
    if desc:
        if not 80 <= len(desc) <= 200:
            fail("meta", path.name, f"description is {len(desc)} chars (want 80-200)")
        if desc != meta.get("og:description", desc) and "og:description" in meta:
            if html.unescape(meta["og:description"]) != desc:
                fail("meta", path.name, "description and og:description differ")

    # Preview scrapers ignore relative paths, so these must be absolute.
    for key in ("og:url", "og:image"):
        val = meta.get(key)
        if val and not val.startswith("https://"):
            fail("meta", path.name, f"{key} is not absolute: {val}")

    # Every referenced asset must exist, or the preview silently breaks.
    for key in ("og:url", "og:image"):
        val = meta.get(key)
        if not val:
            continue
        target = local_path(val)
        if target is None:
            fail("asset", path.name, f"{key} is not on {SITE}: {val}")
        elif not target.exists():
            fail("asset", path.name, f"{key} points at a missing file: {val}")

    links = dict(LINK_RE.findall(block))
    for rel in ("canonical", "icon", "apple-touch-icon"):
        if rel not in links:
            fail("link", path.name, f"missing rel={rel}")

    for rel, href in links.items():
        if rel == "canonical":
            continue
        if not (ROOT / urllib.parse.unquote(href)).exists():
            fail("asset", path.name, f"rel={rel} points at missing {href}")


def check_assets():
    for name in REQUIRED_ASSETS:
        if not (ROOT / name).exists():
            fail("asset", "repo", f"missing generated asset {name}")


def main():
    files = sorted(ROOT.glob("*.html"))
    if len(files) != 39:
        fail("repo", "repo", f"expected 39 html files, found {len(files)}")

    for path in files:
        check_page(path)
    check_assets()

    if failures:
        print(f"FAIL - {len(failures)} problem(s):")
        for f in failures[:40]:
            print("  " + f)
        if len(failures) > 40:
            print(f"  ... and {len(failures) - 40} more")
        return 1

    print(f"PASS - metadata verified on {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
