"""
AE417 Labs 03-06: Re-extract images correctly and update HTML.
Fixes:
  - Lab03: include all 5 CFRP fiber microscopy images; complete stress-strain graphs
  - Lab04: include missing images (aircraft wing, thermography subject, radiography equip,
           calibration blocks); restructure into one section per NDE method
  - Lab05: include all 7 images; fix captions
  - Lab06: include all equipment photos + render vector graphs from page
"""

import fitz, re, os, sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE   = Path('C:/Users/anura/OneDrive - Embry-Riddle Aeronautical University/Desktop/Projects/Personal Website')
REPDIR = BASE / 'Reports' / 'AE 417'
FOLDER = BASE / 'Folder' / 'AE417'

ZOOM       = fitz.Matrix(2.5, 2.5)
MIN_AREA   = 20000   # display area threshold (skip tiny icons/lines)


# ── helper: extract all figure captions from a PDF ──────────────────────────
def get_all_captions(doc):
    """Returns dict {fig_key_str: caption_text} from full PDF text."""
    full = '\n'.join(p.get_text() for p in doc)
    caps = {}
    for m in re.finditer(
            r'[Ff]ig(?:ure)?\.?\s*([\d]+[a-zA-Z]?)[\.\:\s]\s*([^\n]{4,500})',
            full):
        k = m.group(1)
        if k not in caps:                     # keep first occurrence
            caps[k] = m.group(2).strip().rstrip(' ,.')
    return caps


# ── helper: extract raster images from a page ──────────────────────────────
def extract_raster(page, out_dir, fig_num, seen_xrefs):
    """Extract all qualifying raster images from page. Returns updated fig_num."""
    for img in page.get_images(full=True):
        xref = img[0]
        if xref in seen_xrefs:
            continue
        seen_xrefs.add(xref)
        rects = page.get_image_rects(xref)
        if not rects:
            continue
        r = rects[0]
        if r.width * r.height < MIN_AREA:
            continue
        pix = page.get_pixmap(matrix=ZOOM, clip=r, alpha=False)
        pix.save(str(out_dir / f'fig{fig_num:02d}.png'))
        fig_num += 1
    return fig_num


# ── helper: render a full page region as a PNG ──────────────────────────────
def render_region(page, rect, out_dir, fig_num):
    pix = page.get_pixmap(matrix=ZOOM, clip=rect, alpha=False)
    pix.save(str(out_dir / f'fig{fig_num:02d}.png'))
    return fig_num + 1


# ═══════════════════════════════════════════════════════════════════════════
# LAB 03 – Aluminum and Composite Tensile Testing
# ═══════════════════════════════════════════════════════════════════════════
def extract_lab03():
    out_dir = FOLDER / 'lab03'
    for f in out_dir.iterdir(): f.unlink()

    doc   = fitz.open(str(REPDIR / 'Lab-3-Main.pdf'))
    caps  = get_all_captions(doc)
    fn    = 1
    seen  = set()

    # Skip page 1 (logo only). Start from page 2.
    for pnum in range(1, doc.page_count):
        page = doc[pnum]
        page_h = page.rect.height

        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen: continue
            seen.add(xref)

            rects = page.get_image_rects(xref)
            if not rects: continue
            r = rects[0]
            if r.width * r.height < MIN_AREA: continue

            # Render the image as displayed (no rotation/distortion)
            pix = page.get_pixmap(matrix=ZOOM, clip=r, alpha=False)
            pix.save(str(out_dir / f'fig{fn:02d}.png'))
            fn += 1

    # For the stress-strain graphs (pp 16-18): each graph is stored as
    # two xrefs (top half + bottom half). Detect and merge by rendering
    # the combined bounding box for each page.
    # The merged graphs replace the split fig pairs already extracted.
    # -- Do this as a second pass, identifying split pairs by matching y-adjacency.
    # EASIER: just re-render each of pp 16-18 at the graph region.
    # Those pages have the graph in roughly the lower 60% of the page.

    doc.close()
    print(f'lab03: {fn-1} figs (raw extraction)')

    # Now build the caption assignment:
    # From the PDF: Fig 1-8 are equipment/specimens, Fig 9-13 are CFRP zooms,
    # Fig 14-16 are stress-strain graphs.
    # The extraction order (page order) matches the report figure order.
    # BUT: split graph halves create duplicates. We need to check and handle.
    return caps


def extract_lab03_v2():
    """Re-extraction for lab03 with split-graph merging and full caption mapping."""
    out_dir = FOLDER / 'lab03'
    for f in out_dir.iterdir(): f.unlink()

    doc     = fitz.open(str(REPDIR / 'Lab-3-Main.pdf'))
    caps    = get_all_captions(doc)
    fn      = 1
    seen    = set()

    # Per-page extraction
    for pnum in range(1, doc.page_count):
        page  = doc[pnum]

        # Collect all qualifying images on this page with their rects
        page_imgs = []
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen: continue
            rects = page.get_image_rects(xref)
            if not rects: continue
            r = rects[0]
            if r.width * r.height < MIN_AREA: continue
            seen.add(xref)
            page_imgs.append((xref, r))

        if not page_imgs: continue

        # Sort images top-to-bottom
        page_imgs.sort(key=lambda x: x[1].y0)

        # Check if this page has split halves (two images stacked vertically
        # with same width and total height ≈ normal single image)
        if len(page_imgs) == 2:
            r0, r1 = page_imgs[0][1], page_imgs[1][1]
            width_match = abs(r0.width - r1.width) < 10
            y_adjacent  = abs(r1.y0 - (r0.y0 + r0.height)) < 8
            both_wide   = r0.width > 200
            if width_match and y_adjacent and both_wide:
                # Merge into one combined rect
                merged = fitz.Rect(r0.x0, r0.y0, r1.x1, r1.y1)
                pix = page.get_pixmap(matrix=ZOOM, clip=merged, alpha=False)
                pix.save(str(out_dir / f'fig{fn:02d}.png'))
                fn += 1
                continue

        # Otherwise render each image individually
        for xref, r in page_imgs:
            pix = page.get_pixmap(matrix=ZOOM, clip=r, alpha=False)
            pix.save(str(out_dir / f'fig{fn:02d}.png'))
            fn += 1

    doc.close()
    print(f'lab03: {fn-1} figs')

    # Build fig→caption map:
    # Report order: Fig1 Specimens, Fig2 Specimens after, Fig3 Tinius Olsen,
    # Fig4 Experimental equipment, Fig5 Water sander, Fig6 Grinding machine,
    # Fig7 Hot glue gun, Fig8 Hand dryer,
    # Fig9-13 CFRP zooms 1-5, Fig14 Al stress-strain, Fig15 GFRP, Fig16 CFRP
    fig_order = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
    result = {}
    for i, k in enumerate(fig_order, 1):
        result[f'fig{i:02d}.png'] = caps.get(k, '')
    return result


# ═══════════════════════════════════════════════════════════════════════════
# LAB 04 – Nondestructive Evaluation
# ═══════════════════════════════════════════════════════════════════════════
def extract_lab04():
    out_dir = FOLDER / 'lab04'
    for f in out_dir.iterdir(): f.unlink()

    doc   = fitz.open(str(REPDIR / 'LAB-4_MAIN.pdf'))
    caps  = get_all_captions(doc)
    fn    = 1
    seen  = set()

    for pnum in range(1, doc.page_count):
        page = doc[pnum]
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen: continue
            rects = page.get_image_rects(xref)
            if not rects: continue
            r = rects[0]
            if r.width * r.height < MIN_AREA: continue
            seen.add(xref)
            pix = page.get_pixmap(matrix=ZOOM, clip=r, alpha=False)
            pix.save(str(out_dir / f'fig{fn:02d}.png'))
            fn += 1

    doc.close()
    print(f'lab04: {fn-1} figs')

    # Map extracted figs to report figures.
    # Report: Fig1 apparatus, Fig2 aircraft wing, Fig3 before inspection,
    # Fig4 during inspection, Fig5-8 surface damage details,
    # Fig9 thermography equip, Fig10 image subject, Fig11 active temp change,
    # Fig12 after temp change, Fig13 FLIR image, Fig14 residual heat,
    # Fig15 radiography equip, Fig16 X-ray computer, Fig17 X-ray weld,
    # Fig18 X-ray apple watch, Fig19 LP equipment, Fig20-24 LP process,
    # Fig25 ultrasonics equip, Fig26-28 calibration blocks, Fig29-32 A-scans
    # Total: 32 figures
    # Extracted (area>20000, skip p1): need to count
    fig_order = [str(i) for i in range(1, 33)]
    result = {}
    for i, k in enumerate(fig_order, 1):
        result[f'fig{i:02d}.png'] = caps.get(k, '')
    return result


# ═══════════════════════════════════════════════════════════════════════════
# LAB 05 – Vibration Testing of Beams
# ═══════════════════════════════════════════════════════════════════════════
def extract_lab05():
    out_dir = FOLDER / 'lab05'
    for f in out_dir.iterdir(): f.unlink()

    doc   = fitz.open(str(REPDIR / 'LAB-5-Main-1.pdf'))
    caps  = get_all_captions(doc)
    fn    = 1
    seen  = set()

    for pnum in range(1, doc.page_count):
        page = doc[pnum]
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen: continue
            rects = page.get_image_rects(xref)
            if not rects: continue
            r = rects[0]
            if r.width * r.height < MIN_AREA: continue
            seen.add(xref)
            pix = page.get_pixmap(matrix=ZOOM, clip=r, alpha=False)
            pix.save(str(out_dir / f'fig{fn:02d}.png'))
            fn += 1

    doc.close()
    print(f'lab05: {fn-1} figs')

    fig_order = ['1','2','3','4','5','6','7']
    result = {}
    for i, k in enumerate(fig_order, 1):
        result[f'fig{i:02d}.png'] = caps.get(k, '')
    return result


# ═══════════════════════════════════════════════════════════════════════════
# LAB 06 – Rocket Thrust Measurement
# ═══════════════════════════════════════════════════════════════════════════
def extract_lab06():
    out_dir = FOLDER / 'lab06'
    for f in out_dir.iterdir(): f.unlink()

    doc   = fitz.open(str(REPDIR / 'LAB-6-Main.pdf'))
    caps  = get_all_captions(doc)
    fn    = 1
    seen  = set()

    # Extract raster photos (Figs 1-8 on pages 4-8)
    for pnum in range(1, 9):
        page = doc[pnum]
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen: continue
            rects = page.get_image_rects(xref)
            if not rects: continue
            r = rects[0]
            if r.width * r.height < MIN_AREA: continue
            seen.add(xref)
            pix = page.get_pixmap(matrix=ZOOM, clip=r, alpha=False)
            pix.save(str(out_dir / f'fig{fn:02d}.png'))
            fn += 1

    # Render vector graph pages (pp 10-16):
    # p10 → Fig8 (cal) + Fig9 (B4-4)
    # p11 → Fig10 (E16-4) + Fig11 (C11-0)
    # p12 → Fig12 (A8-3)
    # p14 → Fig14 (B4-4) + Fig15 (E16-4)
    # p15 → Fig16 (C11-0) + Fig17 (C6-5)
    # p16 → Fig18 (A8-3)
    # Strategy: render each page, try to find graph region by text positions.
    # Graphs are typically the lower portion of the page when titles are above.
    # For simplicity: render each graph page, splitting into top/bottom
    # if two graphs present, or full-page crop of graph area.

    graph_pages = {
        9:  [('8',  'Voltage vs Time graph for Calibration test'),
             ('9',  'Voltage vs Time graph for B4-4 test')],
        10: [('10', 'Voltage vs Time graph for E16-4 test'),
             ('11', 'Voltage vs Time graph for C11-0 test')],
        11: [('12', 'Voltage vs Time graph for A803 test')],
        13: [('14', 'Thrust to time graph for B4-4 test'),
             ('15', 'Thrust to time graph for E16-4 test')],
        14: [('16', 'Thrust to time graph for C11-0 test'),
             ('17', 'Thrust to time graph for C6-5 test')],
        15: [('18', 'Thrust to time graph for A8-3 test')],
    }

    for pnum, fig_list in graph_pages.items():
        page = doc[pnum]
        pw   = page.rect.width
        ph   = page.rect.height

        if len(fig_list) == 1:
            # Single graph: render the whole page area below the page number
            graph_rect = fitz.Rect(0, 40, pw, ph - 40)
            pix = page.get_pixmap(matrix=ZOOM, clip=graph_rect, alpha=False)
            pix.save(str(out_dir / f'fig{fn:02d}.png'))
            fn += 1
        else:
            # Two graphs: split page roughly in half (vertically)
            half = ph / 2
            top_rect = fitz.Rect(0, 40,    pw, half)
            bot_rect = fitz.Rect(0, half,  pw, ph - 20)
            for rect in (top_rect, bot_rect):
                pix = page.get_pixmap(matrix=ZOOM, clip=rect, alpha=False)
                pix.save(str(out_dir / f'fig{fn:02d}.png'))
                fn += 1

    doc.close()
    print(f'lab06: {fn-1} figs')

    # Raster Figs 1-8 + vector graph figs 8-18 (no fig13 in extraction = 18 items - 1 missing)
    # Build caption map: figs 01-08 = report Figs 1-8, then graphs
    raster_keys  = ['1','2','3','4','5','6','7','8']
    graph_keys   = ['8','9','10','11','12','14','15','16','17','18']
    all_keys     = raster_keys + graph_keys
    result = {}
    for i, k in enumerate(all_keys, 1):
        result[f'fig{i:02d}.png'] = caps.get(k, '')
    return result


# ── Run extractions ─────────────────────────────────────────────────────────
print('Extracting lab03...')
cap03 = extract_lab03_v2()

print('Extracting lab04...')
cap04 = extract_lab04()

print('Extracting lab05...')
cap05 = extract_lab05()

print('Extracting lab06...')
cap06 = extract_lab06()

# Print results for verification
for lab, caps in [('lab03', cap03), ('lab04', cap04), ('lab05', cap05), ('lab06', cap06)]:
    print(f'\n--- {lab} ---')
    for fn, cap in sorted(caps.items()):
        p = FOLDER / lab / fn
        exists = '✓' if p.exists() else '✗'
        print(f'  {exists} {fn}: {cap[:80]}')

# Save captions for use by HTML update script
all_caps = {'lab03': cap03, 'lab04': cap04, 'lab05': cap05, 'lab06': cap06}
with open(BASE / 'ae417_caps_v2.json', 'w', encoding='utf-8') as f:
    json.dump(all_caps, f, ensure_ascii=False, indent=2)

print('\nDone.')
