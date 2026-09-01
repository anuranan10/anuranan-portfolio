"""Generate the favicon set and the homepage Open Graph card.

Run from the repo root:  python tools/make_brand_assets.py

Outputs (all overwritten on each run, so this is safe to re-run):
  favicon.svg           vector icon, used by modern browsers
  favicon.png           32x32 raster fallback
  favicon.ico           legacy /favicon.ico request
  apple-touch-icon.png  180x180 iOS home-screen icon
  og-card.png           1200x630 link-preview card
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAVY = (0, 64, 128)
WHITE = (255, 255, 255)
BOLD = "C:/Windows/Fonts/arialbd.ttf"
REG = "C:/Windows/Fonts/arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, box, text, f, fill):
    l, t, r, b = draw.textbbox((0, 0), text, font=f)
    x = box[0] + (box[2] - box[0] - (r - l)) / 2 - l
    y = box[1] + (box[3] - box[1] - (b - t)) / 2 - t
    draw.text((x, y), text, font=f, fill=fill)


def icon(size):
    """Navy rounded square with white 'AB'."""
    img = Image.new("RGBA", (size * 4, size * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size * 4
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.18), fill=NAVY)
    centered(d, (0, int(s * 0.02), s, s), "AB", font(BOLD, int(s * 0.55)), WHITE)
    return img.resize((size, size), Image.LANCZOS)


def og_card():
    """1200x630 preview card: circular profile photo beside name and tagline."""
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(card)
    d.rectangle([0, H - 10, W, H], fill=(240, 163, 10))   # palette accent

    photo = Image.open(ROOT / "Folder" / "profile.jpg").convert("RGB")
    side = min(photo.size)
    photo = photo.crop((
        (photo.width - side) // 2, (photo.height - side) // 2,
        (photo.width + side) // 2, (photo.height + side) // 2,
    )).resize((360, 360), Image.LANCZOS)
    mask = Image.new("L", (1440, 1440), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 1439, 1439], fill=255)
    photo.putalpha(mask.resize((360, 360), Image.LANCZOS))
    card.paste(photo, (90, 135), photo)

    x = 520
    d.text((x, 210), "Anuranan Bharadwaj", font=font(BOLD, 58), fill=WHITE)
    d.text((x, 292), "Aerospace Engineering  |  Computer Science",
           font=font(REG, 32), fill=(207, 227, 255))
    d.text((x, 352), "Propulsion  ·  CFD  ·  Controls  ·  Structures",
           font=font(REG, 28), fill=(207, 227, 255))
    d.text((x, 424), "anuranan.info", font=font(BOLD, 30), fill=(240, 163, 10))
    return card


def main():
    (ROOT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        '  <rect width="64" height="64" rx="12" fill="#004080"/>\n'
        '  <text x="32" y="44" font-family="Arial, Helvetica, sans-serif"'
        ' font-size="34" font-weight="bold" fill="#ffffff"'
        ' text-anchor="middle">AB</text>\n'
        "</svg>\n",
        encoding="utf-8",
    )
    icon(32).save(ROOT / "favicon.png")
    icon(64).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    icon(180).convert("RGB").save(ROOT / "apple-touch-icon.png")
    og_card().save(ROOT / "og-card.png", optimize=True)

    for n in ("favicon.svg", "favicon.png", "favicon.ico",
              "apple-touch-icon.png", "og-card.png"):
        print(f"  wrote {n}  ({(ROOT / n).stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
