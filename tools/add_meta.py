"""Inject search and link-preview metadata into every page's <head>.

Adds a per-page meta description, Open Graph / Twitter card tags, and the
favicon links. Everything sits between marker comments, so re-running
replaces the block rather than duplicating it.

Run from the repo root:  python tools/add_meta.py
"""
import html
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://anuranan.info"
START = "  <!-- meta:auto -->"
END = "  <!-- /meta:auto -->"
BLOCK_RE = re.compile(
    re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.DOTALL
)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
IMG_RE = re.compile(r'<img[^>]+src="([^"]+)"', re.IGNORECASE)
SUFFIX = "| Anuranan Bharadwaj"

# One description per page, ~150-160 characters, written from the page's
# own content. These are what Google shows under the link and what a
# LinkedIn/Slack preview card uses as its subtitle.
DESCRIPTIONS = {
    "index.html":
        "Aerospace engineering graduate from Embry-Riddle specializing in "
        "turbomachinery and propulsion, with computer science work in "
        "simulation, controls, and software.",
    "aerospace.html":
        "Aerospace engineering projects spanning turbofan engine design, "
        "flight dynamics and control, wind tunnel testing, structural "
        "analysis, and orbital mechanics.",
    "cs.html":
        "Software projects including a Three.js interactive airport scene, a "
        "neural network built from scratch, an HFT backtesting engine, and a "
        "QR-based attendance platform.",
    "experience.html":
        "Turbomachinery software internship, reinforcement learning research, "
        "gas turbine lab research, and CubeSat flight software development at "
        "Embry-Riddle.",
    "lab-testing-experience.html":
        "Hands-on laboratory experimentation at Embry-Riddle across "
        "experimental aerodynamics, structures and instrumentation, and "
        "dynamics and control.",
    "simulations.html":
        "CFD and computational modeling work: OpenFOAM airfoil analysis, "
        "ANSYS Fluent pipe flow, FEMAP wing structural analysis, and aircraft "
        "stability simulation.",
    "highlights.html":
        "Undergraduate research presented at NCUR, conferences attended, and "
        "engineering experiences beyond the classroom at Embry-Riddle "
        "Aeronautical University.",
    "resume.html":
        "Download Anuranan Bharadwaj's resumes, tailored separately for "
        "aerospace engineering and software engineering opportunities.",
    "contact.html":
        "Get in touch with Anuranan Bharadwaj about aerospace and software "
        "engineering opportunities, research collaboration, and project work.",

    # Lab section index pages
    "experimental-aerodynamics-labs.html":
        "Five AE 315 wind tunnel experiments at Embry-Riddle: tunnel "
        "characterization, bluff-body flow, airfoil lift and drag, delta wing "
        "forces, and Schlieren imaging.",
    "structures-instrumentation-labs.html":
        "Six AE 417 experiments at Embry-Riddle covering honeycomb "
        "compression, strain gages, tensile testing, nondestructive "
        "evaluation, vibration, and rocket thrust.",
    "dynamics-control-labs.html":
        "Five AE 443 Quanser experiments at Embry-Riddle covering servo "
        "modeling, flexible link dynamics, position control, gyroscope "
        "control, and speed control.",

    # AE 315 - Experimental Aerodynamics
    "AE315 Lab 01 - Wind Tunnel Characterization.html":
        "Mapping the ERAU open-circuit wind tunnel: fan frequency versus "
        "freestream velocity and test-section uniformity, measured with a "
        "traverse pitot-static probe.",
    "AE315 Lab 02 - Flow Around Cylinders.html":
        "Pressure distribution around a circular cylinder in subsonic flow, "
        "capturing stagnation, boundary layer separation, and the turbulent "
        "wake of a bluff body.",
    "AE315 Lab 03 - Lift and Drag on Airfoils.html":
        "Measured lift and drag on a NACA 4412 airfoil across angle of "
        "attack, compared against ideal potential-flow theory to quantify "
        "viscous and stall effects.",
    "AE315 Lab 04 - Forces and Moments on a Canard Delta Wing.html":
        "Force and moment measurements on a canard delta wing, examining "
        "leading-edge vortex lift and the stability contribution of canard "
        "placement at high angles of attack.",
    "AE315 Lab 05 - Schlieren Imaging and Supersonic Wind Tunnels.html":
        "Schlieren visualization of shock waves in a supersonic wind tunnel, "
        "relating measured shock angles to compressible-flow theory and "
        "nozzle behavior.",

    # AE 417 - Structures and Instrumentation
    "AE417 Lab 01 - Honeycomb Compression Test.html":
        "Out-of-plane compression testing of aluminum honeycomb core per ASTM "
        "D7336, capturing elastic loading, cell-wall buckling, and "
        "densification, with microscopy of the failure surfaces.",
    "AE417 Lab 02 - Strain Gages.html":
        "Strain gage instrumentation and Wheatstone bridge measurement on "
        "loaded specimens, covering gage factor, bridge configuration, and "
        "experimental strain accuracy.",
    "AE417 Lab 03 - Aluminum and Composite Tensile Testing.html":
        "Tensile testing of aluminum alloy against fiber-reinforced "
        "composite, comparing modulus, strength, failure mode, and "
        "strength-to-weight for aerospace structures.",
    "AE417 Lab 04 - Nondestructive Evaluation.html":
        "Nondestructive evaluation of aerospace structures using borescope "
        "inspection, thermography, and radiography to locate subsurface "
        "damage without harming the part.",
    "AE417 Lab 05 - Vibration Testing of Beams.html":
        "Vibration testing of beams to identify natural frequencies, mode "
        "shapes, and damping, with measured results compared against "
        "analytical predictions.",
    "AE417 Lab 06 - Rocket Thrust Measurement.html":
        "Static test-stand measurement of a rocket motor thrust curve, "
        "including load cell calibration, peak and average thrust, total "
        "impulse, and burn duration.",

    # AE 443 - Dynamics and Control
    "AE443 Lab 01 - Servo Modeling.html":
        "First-order system identification of a Quanser SRV02 servo using the "
        "bump test method, extracting steady-state gain and time constant, "
        "then validating the model.",
    "AE443 Lab 02 - Flexible Link Modeling.html":
        "Modeling a servo-driven flexible link, capturing both rigid-body "
        "actuator motion and the structural vibration modes of the link in "
        "the equations of motion.",
    "AE443 Lab 03 - SRV02 Position Control.html":
        "Position control design for the Quanser SRV02 servo, tuned for step "
        "response performance and for steady-state tracking of ramp reference "
        "inputs.",
    "AE443 Lab 04 - Gyro Modeling and Control.html":
        "Modeling and active control of a gyroscope module, using gyroscopic "
        "precession dynamics to design a controller for platform "
        "stabilization and attitude hold.",
    "AE443 Lab 05 - Speed Control.html":
        "Frequency-domain design and comparison of speed controller "
        "architectures, evaluating step command tracking and disturbance "
        "rejection on a servo plant.",

    # Project detail pages
    "High-Bypass Turbofan Engine Senior Design.html":
        "Two-semester senior design of a high-bypass turbofan: thermodynamic "
        "cycle analysis, inlet sizing, turbomachinery component design, and "
        "combustor design.",
    "DC-8 PID Controller Design.html":
        "PID controller design for the DC-8, covering modal characterization "
        "from transfer functions plus angle-of-attack and forward-speed "
        "control loops.",
    "Quanser Aero PID Control Design.html":
        "Open-loop characterization and PID tuning of the Quanser Aero pitch "
        "axis, isolating each control action's effect and identifying the "
        "second-order system response.",
    "Aircraft Stability & Control Simulation.html":
        "Longitudinal, directional, and lateral stability analysis of an "
        "aircraft configuration, with hand calculations validated against "
        "Digital DATCOM predictions.",
    "Wind Tunnel Drag Study - Flap Deflection.html":
        "Wake survey drag measurement across flap deflection angles in a "
        "subsonic wind tunnel, quantifying the drag penalty of increasing "
        "high-lift device deployment.",
    "Aircraft Wing Structural Analysis.html":
        "Complete wing structural analysis workflow: 3D CAD assembly in "
        "Fusion 360 through finite element analysis in FEMAP and NX Nastran, "
        "with stress and displacement results.",
    "TDRS-M Orbital Mechanics and Trajectory Design.html":
        "TDRS-M mission trajectory design: LEO parking orbit propagation, "
        "Hohmann transfer to GTO, geostationary insertion with plane change, "
        "and GEO phasing maneuvers.",
    "NACA 2412 Airfoil CFD Analysis.html":
        "Steady RANS angle-of-attack sweep on a NACA 2412 airfoil in "
        "OpenFOAM, from attached flow through near-stall, deep stall, and "
        "bluff-body vortex shedding.",
    "Laminar Pipe Flow CFD Analysis.html":
        "Laminar incompressible pipe flow simulated end-to-end in ANSYS "
        "Fluent, covering geometry, meshing, boundary conditions, solving, "
        "and CFD-Post velocity and pressure results.",
    "Database Application for Aircraft Fleet Selection.html":
        "MATLAB decision support application that lets airline operators "
        "filter, compare, and visualize aircraft fleet options against a "
        "structured performance database.",
    "LEGO Airplane Design.html":
        "EGR 120 project: a LEGO Technic race plane measured by hand and "
        "modeled from scratch in CATIA, redesigned with twin propellers "
        "and tricycle gear, documented in a 17 sheet drawing package with "
        "GD&T.",
}

# Pages whose own imagery is not the best preview get the branded card.
FORCE_CARD = {"index.html", "resume.html", "contact.html", "experience.html"}


def url_for(rel):
    """Absolute, percent-encoded URL. Preview scrapers ignore relative paths."""
    if rel == "index.html":
        return f"{SITE}/"          # the homepage's canonical form is the root
    return f"{SITE}/{urllib.parse.quote(rel)}"


def og_image(path, body):
    if path.name in FORCE_CARD:
        return url_for("og-card.png")
    m = IMG_RE.search(body)
    if m and not m.group(1).startswith("http"):
        return url_for(urllib.parse.unquote(m.group(1)))
    return url_for("og-card.png")


def og_title(path, title):
    if path.name == "index.html":
        return title
    return title[: -len(SUFFIX)].strip() if title.endswith(SUFFIX) else title


def build(path, title, desc, image):
    e = html.escape
    lines = [
        START,
        f'  <meta name="description" content="{e(desc)}">',
        f'  <link rel="canonical" href="{url_for(path.name)}">',
        '  <link rel="icon" href="favicon.svg" type="image/svg+xml">',
        '  <link rel="icon" href="favicon.png" sizes="32x32">',
        '  <link rel="apple-touch-icon" href="apple-touch-icon.png">',
        '  <meta property="og:type" content="website">',
        '  <meta property="og:site_name" content="Anuranan Bharadwaj">',
        f'  <meta property="og:title" content="{e(og_title(path, title))}">',
        f'  <meta property="og:description" content="{e(desc)}">',
        f'  <meta property="og:url" content="{url_for(path.name)}">',
        f'  <meta property="og:image" content="{image}">',
        '  <meta name="twitter:card" content="summary_large_image">',
        END,
    ]
    return "\n".join(lines) + "\n"


def main():
    written, problems = 0, []

    for path in sorted(ROOT.glob("*.html")):
        # newline="" keeps existing line endings byte-for-byte
        # (Path.read_text gained a newline argument only in 3.13).
        with open(path, encoding="utf-8", newline="") as fh:
            text = fh.read()

        desc = DESCRIPTIONS.get(path.name)
        if not desc:
            problems.append((path.name, "no description written for this page"))
            continue

        m = TITLE_RE.search(text)
        if not m:
            problems.append((path.name, "no <title> found"))
            continue
        title = " ".join(html.unescape(m.group(1)).split())

        if "</head>" not in text:
            problems.append((path.name, "no </head> found"))
            continue

        text = BLOCK_RE.sub("", text)          # drop any previous block
        head, rest = text.split("</head>", 1)
        block = build(path, title, desc, og_image(path, rest))
        path.write_text(
            head.rstrip("\n") + "\n" + block + "</head>" + rest,
            encoding="utf-8", newline="",
        )
        written += 1

    print(f"metadata written: {written}   problems: {len(problems)}")
    for name, why in problems:
        print(f"  PROBLEM {name}: {why}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
