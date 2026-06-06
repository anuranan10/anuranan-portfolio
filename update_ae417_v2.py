"""
Fix AE417 Labs 03-06: correct caption maps + update HTML.
"""
import re, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path('C:/Users/anura/OneDrive - Embry-Riddle Aeronautical University/Desktop/Projects/Personal Website')

# ── Corrected caption maps ────────────────────────────────────────────────
# lab03: 18 figs. Page trace shows:
#   fig01-02 (p6) = Figs 1,2 | fig03-05 (p7 wide strips) = Fig3 panels |
#   fig06 (p7 normal photo) = Fig4 | fig07-08 (p8) = Figs 5,6 |
#   fig09-10 (p9) = Figs 7,8 | fig11-15 (p13-15) = Figs 9-13 |
#   fig16-18 (p16-18 merged) = Figs 14-16

CAP03 = {
    'fig01.png': 'Specimens',
    'fig02.png': 'Specimens after tensile testing',
    'fig03.png': 'Tinius Olsen 150ST Electromechanical Universal Testing Machine',
    'fig04.png': 'Tinius Olsen 150ST Electromechanical Universal Testing Machine',
    'fig05.png': 'Tinius Olsen 150ST Electromechanical Universal Testing Machine',
    'fig06.png': 'Experimental equipment used - (1) Mass Scale, (2) Acetone, (3) Cyanoacrylate Adhesive, (4) MBond 200 Adhesive',
    'fig07.png': 'Water Lubricated Sander',
    'fig08.png': 'Grinding and Polishing Machine',
    'fig09.png': 'Hot Glue Gun',
    'fig10.png': 'Hand Dryer',
    'fig11.png': 'Zoomed picture number 1 of CFRP fibers',
    'fig12.png': 'Zoomed picture number 2 of CFRP fibers',
    'fig13.png': 'Zoomed picture number 3 of CFRP fibers',
    'fig14.png': 'Zoomed picture number 4 of CFRP fibers',
    'fig15.png': 'Zoomed picture number 5 of CFRP fibers',
    'fig16.png': 'Stress-strain graph for aluminum 2024 with yield and ultimate stress',
    'fig17.png': 'Stress-strain graph for GFRP',
    'fig18.png': 'Stress-strain graph for CFRP',
}

# lab04: 32 figs matching report Figs 1-32.  Patch missing Fig14 caption.
with open(BASE / 'ae417_caps_v2.json', encoding='utf-8') as f:
    _caps = json.load(f)

CAP04 = _caps['lab04'].copy()
CAP04['fig14.png'] = 'Residual Heat Left Behind From Hand Imprint'
CAP04['fig01.png'] = (
    'Apparatus Used: (1) – Ridgid Micro CA-150 Inspection Camera kit, '
    '(2) – Funai LED display with RCA cable, (3) – Borescope probe tip, '
    '(4) – Test Subject (Aircraft Wing Airfoil)')
CAP04['fig09.png'] = (
    'Equipment Used for Thermography: (1) – FLIR T440 Thermal Imaging Camera, '
    '(2) – Image subject (paper), (3) – Water spray bottle')
CAP04['fig15.png'] = (
    'Radiography equipment: (1) – Test subject, (2) – X-ray detector, '
    '(3) – X-ray system, (4) – Safety shielding')
CAP04['fig16.png'] = 'Radiography computer used to partner with X-ray system'
CAP04['fig25.png'] = (
    'Ultrasonics equipment: (1) – Portable Ultrasonic Inspection Device, '
    '(2) – 5 MHz piezoelectric transducer, (3) – Ultrasonic couplant, '
    '(4) – Aluminum calibration block (SCB)')

CAP05 = {
    'fig01.png': 'Al-6061-T651 Beam Samples (Long and Short)',
    'fig02.png': 'Aerospace Structures: Rib and Model Airplane',
    'fig03.png': 'Screws, Washers, Tube Spacers, and Phillips Head Screwdriver',
    'fig04.png': 'Calipers, Ruler, and Tape Measure',
    'fig05.png': 'Digital Oscilloscope and Sweep Sine Generator',
    'fig06.png': 'Digital Stroboscope with tripod, ICP® (integrated-circuit piezoelectric) accelerometer, and sensor signal conditioner',
    'fig07.png': 'Electrodynamic Shaker',
}

CAP06 = {
    'fig01.png': '(0) – Rolling equipment Cart, (1) – Personal computer and monitor, (2) – Digital Strain Indicator, (3) – TracerDAQ Data Acquisition Software, (4) – Cantilever beam with load cell',
    'fig02.png': 'Solid rocket plugs',
    'fig03.png': '(0) – Cantilever beam, (1) – Calibration masses, (2) – Aluminum strip, (3) – Motor mount hose clamp, (4) – Dashpot oil container',
    'fig04.png': 'Solid rocket igniters',
    'fig05.png': 'Solid rocket motors',
    'fig06.png': 'Equipment Cart moved Outdoors',
    'fig07.png': 'Calibration',
    'fig08.png': 'Experiment Setup including Cantilever Beam',
    # Rendered graphs
    'fig09.png': 'Voltage vs Time graph for Calibration test',
    'fig10.png': 'Voltage vs Time graph for B4-4 test',
    'fig11.png': 'Voltage vs Time graph for E16-4 test',
    'fig12.png': 'Voltage vs Time graph for C11-0 test',
    'fig13.png': 'Voltage vs Time graph for A8-3 test',
    'fig14.png': 'Thrust to time graph for B4-4 test',
    'fig15.png': 'Thrust to time graph for E16-4 test',
    'fig16.png': 'Thrust to time graph for C11-0 test',
    'fig17.png': 'Thrust to time graph for C6-5 test',
    'fig18.png': 'Thrust to time graph for A8-3 test',
}

# ── HTML figure builder ───────────────────────────────────────────────────
def fig_html(lab, fname, seq_n, cap_map):
    cap = cap_map.get(fname, '')
    alt = cap or fname
    label = f'Figure {seq_n}: {cap}' if cap else f'Figure {seq_n}'
    return (
        f'      <figure style="margin:0; text-align:center;">\n'
        f'        <img src="Folder/AE417/{lab}/{fname}" alt="{alt}" />\n'
        f'        <figcaption style="font-size:0.82em; color:#555; '
        f'margin-top:0.35rem; text-align:center; font-style:italic;">'
        f'{label}</figcaption>\n'
        f'      </figure>'
    )

def img_group(lab, fnames, counter, cap_map):
    """Return (html_string, new_counter)."""
    lines = ['    <div class="project-image-group">']
    for fn in fnames:
        lines.append(fig_html(lab, fn, counter, cap_map))
        counter += 1
    lines.append('    </div>')
    return '\n'.join(lines), counter


# ════════════════════════════════════════════════════════════════════════════
# LAB 03
# ════════════════════════════════════════════════════════════════════════════
def update_lab03():
    html_path = BASE / 'AE417 Lab 03 - Aluminum and Composite Tensile Testing.html'
    html = html_path.read_text(encoding='utf-8')

    # Section assignments:
    # 0-Overview: fig01, fig02  (specimens before/after)
    # 1-Approach: fig11-fig15   (5 CFRP fiber zooms)
    # 2-Key Results: fig16,17,18 (merged stress-strain graphs)
    # 3-MATLAB Code: fig06,07,08 (experimental equip, water sander, grinding)
    # 4-Takeaways: already removed in prior run (0 groups? check)
    assignments = {
        0: ['fig01.png', 'fig02.png'],
        1: ['fig11.png', 'fig12.png', 'fig13.png', 'fig14.png', 'fig15.png'],
        2: ['fig16.png', 'fig17.png', 'fig18.png'],
        3: ['fig06.png', 'fig07.png', 'fig08.png'],
    }

    pattern = re.compile(r'\s*<div class="project-image-group">.*?</div>', re.DOTALL)
    matches = list(pattern.finditer(html))
    print(f'lab03: {len(matches)} project-image-group divs found')

    counter = 1
    replacements = []
    for idx, m in enumerate(matches):
        if idx not in assignments or assignments[idx] is None:
            replacements.append((m.start(), m.end(), ''))
        else:
            new_g, counter = img_group('lab03', assignments[idx], counter, CAP03)
            replacements.append((m.start(), m.end(), new_g))

    for start, end, new_text in reversed(replacements):
        html = html[:start] + new_text + html[end:]

    html_path.write_text(html, encoding='utf-8')
    print('  Written: lab03')


# ════════════════════════════════════════════════════════════════════════════
# LAB 04 – full HTML rewrite of the section bodies
# ════════════════════════════════════════════════════════════════════════════
def update_lab04():
    html_path = BASE / 'AE417 Lab 04 - Nondestructive Evaluation.html'
    html = html_path.read_text(encoding='utf-8')

    # We'll replace the entire body content between </header> and the
    # back-link section, rebuilding all sections with per-method structure.

    counter = [1]   # mutable for nested use

    def ig(fnames):
        nonlocal counter
        g, counter[0] = img_group('lab04', fnames, counter[0], CAP04)
        return g

    new_body = f"""
  <section class="project-row">
    <div class="project-text">
      <h2>Experiment Overview</h2>
      <p>Every aircraft in service is inspected continuously using nondestructive evaluation (NDE) methods &mdash; techniques that find damage without harming the part being inspected. NDE is what allows airlines to operate aging aircraft safely and enables manufacturers to certify composite primary structures. This lab provided hands-on exposure to five complementary NDE techniques applied to real aerospace hardware: visual inspection (borescope), thermography, radiography, liquid penetrant, and ultrasonics.</p>
      <ul>
        <li><strong>Visual inspection</strong> &mdash; borescope examination of an aircraft wing airfoil interior for cracks near rivet holes</li>
        <li><strong>Thermography</strong> &mdash; FLIR T440 infrared camera detecting surface temperature gradients</li>
        <li><strong>Radiography</strong> &mdash; X-ray imaging of a welded aluminum plate to visualize internal structure</li>
        <li><strong>Liquid penetrant</strong> &mdash; fluorescent dye/developer revealing surface discontinuities under UV light</li>
        <li><strong>Ultrasonics</strong> &mdash; 5 MHz piezoelectric transducer mapping echo time-of-flight vs. thickness</li>
      </ul>
    </div>
{ig(['fig01.png'])}
  </section>

  <section class="project-row">
    <div class="project-text">
      <h2>Equipment &amp; Tools</h2>
      <ul>
        <li>Ridgid Micro CA-150 borescope inspection camera with Funai LED display and RCA cable</li>
        <li>FLIR T440 Thermal Imaging Camera</li>
        <li>X-ray system with digital flat-panel detector and imaging computer</li>
        <li>Liquid penetrant kit: SD-1 cleaner, ZL-60D fluorescent penetrant, ZP-9F developer, and 365 nm UV light</li>
        <li>Portable Quantum TE ultrasonic inspection device with 5 MHz piezoelectric transducer</li>
        <li>DeFelsko ultrasonic couplant and aluminum stepped calibration blocks (SCB)</li>
        <li>Aircraft wing airfoil section, aluminum pressure vessel, and welded aluminum plate</li>
      </ul>
    </div>
  </section>

  <section class="project-row">
    <div class="project-text">
      <h2>Visual Inspection &ndash; Borescope</h2>
      <p>A Ridgid Micro CA-150 borescope was inserted into the interior of a metallic aircraft wing airfoil section and navigated along the inner skin surface. Under the enhanced lighting of the borescope, <strong>visible scratches and cracks near the rivet holes</strong> were identified &mdash; the type of stress-concentration-driven fatigue damage that motivates maintenance inspection intervals for riveted structures. The borescope proved effective for hard-to-access interior surfaces that no standard optical tool could reach.</p>
    </div>
{ig(['fig02.png', 'fig03.png', 'fig04.png', 'fig05.png', 'fig06.png', 'fig07.png', 'fig08.png'])}
  </section>

  <section class="project-row">
    <div class="project-text">
      <h2>Thermography</h2>
      <p>The FLIR T440 camera imaged a paper subject before and after applying cold water droplets and a hand imprint. The camera resolved temperature differentials at the &plusmn;0.1&deg;C level, with cold water appearing as cool blue zones (22.2&deg;C) against the warm amber background (26.1&deg;C), and the hand imprint glowing red at 26.6&deg;C. This demonstrated how thermal gradients reveal material non-uniformities, disbonds, and coolant leaks in aerospace hardware.</p>
    </div>
{ig(['fig09.png', 'fig10.png', 'fig11.png', 'fig12.png', 'fig13.png', 'fig14.png'])}
  </section>

  <section class="project-row">
    <div class="project-text">
      <h2>Radiography</h2>
      <p>X-ray images of a welded aluminum plate revealed the weld bead geometry and internal profile useful for quality assurance. An Apple Watch image illustrated how overlapping components complicate defect discrimination in complex assemblies &mdash; a known limitation of 2D projection radiography. The X-ray system required a dedicated computer and shielded enclosure for operator safety.</p>
    </div>
{ig(['fig15.png', 'fig16.png', 'fig17.png', 'fig18.png'])}
  </section>

  <section class="project-row">
    <div class="project-text">
      <h2>Liquid Penetrant</h2>
      <p>A fluorescent dye was applied to an aluminum pressure vessel and allowed to dwell for ~10 minutes before being wiped and developed. Under UV illumination, <strong>at least eight discrete damage indications</strong> appeared as bright zones against the green developer background &mdash; scratches and cracks completely invisible under normal white light. This demonstrated the technique&rsquo;s superior sensitivity to shallow, tight surface discontinuities.</p>
    </div>
{ig(['fig19.png', 'fig20.png', 'fig21.png', 'fig22.png', 'fig23.png', 'fig24.png'])}
  </section>

  <section class="project-row">
    <div class="project-text">
      <h2>Ultrasonics</h2>
      <p>A 5 MHz piezoelectric transducer was coupled with ultrasonic couplant to stepped aluminum calibration blocks (SCB). As the probe moved from the thickest section (~24.96 mm) to the thinnest (~3.32 mm), echo spacing in the A-scan decreased proportionally, tracking known thickness steps with clear step-wise echo patterns. Ledge edges produced slight amplitude reduction from scattering, validating the technique&rsquo;s sensitivity to internal geometry changes &mdash; the same principle airlines use to monitor skin corrosion on aging aircraft from the outer surface.</p>
    </div>
{ig(['fig25.png', 'fig26.png', 'fig27.png', 'fig28.png', 'fig29.png', 'fig30.png', 'fig31.png', 'fig32.png'])}
  </section>

  <section class="project-row">
    <div class="project-text">
      <h2>Valuable Takeaways</h2>
      <ul>
        <li><strong>No single NDE method catches everything.</strong> Visual inspection misses subsurface cracks; ultrasonics misses surface-only defects; liquid penetrant only works on non-porous surfaces. Professional inspection programs layer multiple techniques &mdash; the same approach a licensed A&amp;P mechanic applies to airframe maintenance.</li>
        <li><strong>Liquid penetrant reveals defects invisible to the naked eye.</strong> Finding eight surface indications on a visually clean part is a powerful demonstration of why NDE is mandated in airframe certification and maintenance schedules.</li>
        <li><strong>Ultrasonic thickness gauging is the industry standard for corrosion monitoring.</strong> Echo time of flight scaling linearly with thickness &mdash; demonstrated on calibration blocks &mdash; is exactly how airlines measure skin thickness on aging aircraft from the outer surface without removing interior trim or insulation.</li>
        <li>Gained hands-on exposure to five certified NDE methods used in FAA-regulated maintenance and manufacturing, directly relevant to structural integrity engineering, quality assurance, and MRO roles.</li>
      </ul>
    </div>
  </section>
"""

    # Replace everything between </header> and the back-link section
    html = re.sub(
        r'(</header>).*?(<section style="padding: 1rem)',
        r'\1\n' + new_body.replace('\\', '\\\\') + r'\n  \2',
        html, flags=re.DOTALL
    )

    html_path.write_text(html, encoding='utf-8')
    print('  Written: lab04')


# ════════════════════════════════════════════════════════════════════════════
# LAB 05
# ════════════════════════════════════════════════════════════════════════════
def update_lab05():
    html_path = BASE / 'AE417 Lab 05 - Vibration Testing of Beams.html'
    html = html_path.read_text(encoding='utf-8')

    # Existing image groups:
    # 0-Overview (3 imgs): replace with fig01, fig06, fig07 (beams + stroboscope + shaker)
    # 1-Approach (4 imgs): replace with fig02, fig03, fig04, fig05 (rib+model, screws, calipers, oscilloscope)
    assignments = {
        0: ['fig01.png', 'fig06.png', 'fig07.png'],
        1: ['fig02.png', 'fig03.png', 'fig04.png', 'fig05.png'],
    }

    pattern = re.compile(r'\s*<div class="project-image-group">.*?</div>', re.DOTALL)
    matches = list(pattern.finditer(html))
    print(f'lab05: {len(matches)} project-image-group divs found')

    counter = 1
    replacements = []
    for idx, m in enumerate(matches):
        if idx not in assignments or assignments[idx] is None:
            replacements.append((m.start(), m.end(), ''))
        else:
            new_g, counter = img_group('lab05', assignments[idx], counter, CAP05)
            replacements.append((m.start(), m.end(), new_g))

    for start, end, new_text in reversed(replacements):
        html = html[:start] + new_text + html[end:]

    html_path.write_text(html, encoding='utf-8')
    print('  Written: lab05')


# ════════════════════════════════════════════════════════════════════════════
# LAB 06 – add graph sections and fix captions
# ════════════════════════════════════════════════════════════════════════════
def update_lab06():
    html_path = BASE / 'AE417 Lab 06 - Rocket Thrust Measurement.html'
    html = html_path.read_text(encoding='utf-8')

    # Current image groups after previous updates:
    # 0-Overview (3 imgs)
    # 1-Approach (4 imgs)
    # (Key Results had 1 img but was removed in previous run)
    # Need to add: Voltage vs Time graphs section + Thrust vs Time graphs section

    assignments = {
        0: ['fig01.png', 'fig05.png', 'fig06.png'],          # overview: cart, motors, cart outdoors
        1: ['fig02.png', 'fig03.png', 'fig04.png', 'fig07.png', 'fig08.png'],  # approach: plugs, cantilever, igniters, calibration, setup
    }

    pattern = re.compile(r'\s*<div class="project-image-group">.*?</div>', re.DOTALL)
    matches = list(pattern.finditer(html))
    print(f'lab06: {len(matches)} project-image-group divs found')

    counter = 1
    replacements = []
    for idx, m in enumerate(matches):
        if idx not in assignments or assignments[idx] is None:
            replacements.append((m.start(), m.end(), ''))
        else:
            new_g, counter = img_group('lab06', assignments[idx], counter, CAP06)
            replacements.append((m.start(), m.end(), new_g))

    for start, end, new_text in reversed(replacements):
        html = html[:start] + new_text + html[end:]

    # Now insert the two graph sections before the back-link section
    voltage_group, counter = img_group('lab06',
        ['fig09.png', 'fig10.png', 'fig11.png', 'fig12.png', 'fig13.png'],
        counter, CAP06)
    thrust_group, counter = img_group('lab06',
        ['fig14.png', 'fig15.png', 'fig16.png', 'fig17.png', 'fig18.png'],
        counter, CAP06)

    graph_sections = f"""
  <section class="project-row">
    <div class="project-text">
      <h2>Voltage vs. Time Results</h2>
      <p>Raw strain-gage voltage output recorded during each motor firing. The calibration test confirmed the linear voltage-to-force relationship. All five motors produced clear ignition spikes followed by a sustained plateau and a sharp burnout, consistent with black-powder propellant combustion behavior.</p>
    </div>
{voltage_group}
  </section>

  <section class="project-row">
    <div class="project-text">
      <h2>Thrust vs. Time Results</h2>
      <p>Voltage traces converted to thrust (N) using the calibration equation F = 32.931&times;V &minus; 40.732. Peak thrust, average thrust, burn time, and total impulse were extracted from each curve. The C6-5 was selected for comparison against Estes manufacturer specifications.</p>
    </div>
{thrust_group}
  </section>

"""
    # Insert before the back-link section
    html = html.replace(
        '\n  <section style="padding: 1rem 2rem 2rem;">\n    <p><a class="project-title-link" href="structures-instrumentation-labs.html">',
        graph_sections + '\n  <section style="padding: 1rem 2rem 2rem;">\n    <p><a class="project-title-link" href="structures-instrumentation-labs.html">'
    )

    html_path.write_text(html, encoding='utf-8')
    print('  Written: lab06')


# ── Run all updates ──────────────────────────────────────────────────────
print('Updating lab03...')
update_lab03()

print('Updating lab04...')
update_lab04()

print('Updating lab05...')
update_lab05()

print('Updating lab06...')
update_lab06()

print('\nAll HTML updates done.')
