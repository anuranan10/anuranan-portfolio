---
name: ae315-lab-pages
description: Design spec for AE 315 lab index page and 5 individual lab detail pages
metadata:
  type: project
---

# AE 315 Lab Pages Design

## Goal

Replace the placeholder `lab-testing-experience.html` with an index page matching the
`aerospace.html` layout (clickable project-row cards). Create 5 individual lab detail pages
linked from that index.

## Files to Create / Modify

| File | Action |
|---|---|
| `lab-testing-experience.html` | Overwrite — new index page |
| `AE315 Lab 01 - Wind Tunnel Characterization.html` | New |
| `AE315 Lab 02 - Flow Around Cylinders.html` | New |
| `AE315 Lab 03 - Lift and Drag on Airfoils.html` | New |
| `AE315 Lab 04 - Forces and Moments on a Canard Delta Wing.html` | New |
| `AE315 Lab 05 - Schlieren Imaging and Supersonic Wind Tunnels.html` | New |

## Index Page — `lab-testing-experience.html`

### Header
- `<h1>` AE 315: Experimental Aerodynamics Labs
- `<p>` Hands-on wind tunnel testing, force measurement, and flow visualization — Embry-Riddle Aeronautical University, Spring 2025

### Layout
5 `<section class="project-row">` blocks, one per lab.
Each block:
- **Left** `<div class="project-text">`: `<h2><a class="project-title-link" href="DETAIL_PAGE">Title</a></h2>` + one `<p>` summary (2–3 sentences).
- **Right** `<div class="project-image-group">`: 3 `<div class="project-image-note">` placeholder notes.

### Lab summaries

**Lab 01 — Wind Tunnel Characterization**
Characterized the ERAU open-circuit wind tunnel by mapping airspeed across fan frequencies (5–25 Hz) and probe heights (1–40 in) using a traverse pitot-static probe. Demonstrated a direct correlation between fan frequency and freestream velocity (up to 18.2 m/s) and quantified turbulence intensity growth with height. Uncertainty was propagated and visualized in MATLAB.

Image notes: "Airspeed vs Fan Frequency" | "Height vs Airspeed profile" | "Height vs Turbulence Intensity"

**Lab 02 — Flow Around Cylinders**
Measured circumferential surface pressure distributions on a 1.4-inch cylinder at 10 m/s (Re ≈ 23,515) and 15 m/s (Re ≈ 35,272) to extract Cp, Cd, and drag force. Compared experimental Cp profiles to potential flow theory; both regimes were subcritical, with Cd increasing from 1.31 to 1.42 as velocity rose.

Image notes: "Cp vs Cylinder Angle plot" | "Cd vs Reynolds Number" | "Drag force comparison table"

**Lab 03 — Lift and Drag on Airfoils**
Evaluated aerodynamic performance of a NACA 4412 airfoil at 15 m/s across angles of attack from −3° to 12° using 18 surface pressure taps and a traversing pitot-static wake survey. Extracted Cl, Cd, and moment coefficients (leading edge and quarter chord) and compared to panel code predictions. Zero-lift angle of attack was determined to be −3.31°.

Image notes: "Cp distribution for all AoA" | "CL vs Angle of Attack" | "Drag Polar"

**Lab 04 — Forces and Moments on a Canard Delta Wing**
Used the ERAU Micaplex Wind Tunnel force balance to measure all six aerodynamic loads on a canard-delta wing at 75 fps and 100 fps with 0° and 10° yaw angles. Applied aerodynamic tares for data correction and analyzed lift, drag, side force, and pitching/rolling/yawing moments against angle of attack. Best CL/CD of 4.21 achieved at 12° AoA.

Image notes: "Lift Coefficient vs AoA" | "Drag Polar (CL vs CD)" | "Lift-to-Drag Ratio vs AoA"

**Lab 05 — Schlieren Imaging & Supersonic Wind Tunnels**
Operated the ERAU supersonic wind tunnel and used Schlieren photography to visualize a shock wave between nozzle positions 9.5–10.5 inches. Computed nozzle pressure ratio (NPR = 3.932), shock strength (1.614), and mass flow rate (6.10 lbm/s) from static pressure tap data.

Image notes: "Schlieren image of shock wave" | "Static pressure distribution along nozzle" | "Pressure vs position plot"

---

## Detail Page Structure (applied to all 5 labs)

Each detail page uses the standard nav + footer from other pages.

### Header
`<h1>` = full lab title (e.g., "Lab 01: Wind Tunnel Characterization")
`<p>` = one-line course context (e.g., "AE 315 · Experimental Aerodynamics · Spring 2025 · ERAU")

### Section 1 — Overview
`<h2>` Lab Overview
Bullet list:
- Course / date / section info
- Lab objective (1–2 sentences)
- Equipment / instrumentation used

### Section 2 — Methodology
`<h2>` Procedure & Methodology
Prose paragraphs covering experimental procedure, test conditions, data acquisition approach.
Use `<!-- insert figure: [description] here -->` comments where report figures belong.

### Section 3 — Key Results
`<h2>` Results & Analysis
Bullet list of key numerical outcomes (e.g., "Cd = 1.31 at 10 m/s", "NPR = 3.932").
`<!-- insert figure: X here -->` comments for each plot.

### Section 4 — Code
`<h2>` MATLAB Code
One `<pre><code>` block with a short representative excerpt from the MATLAB code.
A note: `<!-- full MATLAB code to be embedded here -->`.

### Section 5 — Back link
`<p><a class="project-title-link" href="lab-testing-experience.html">← Back to Lab Testing Experience</a></p>`

---

## Lab-Specific Content

### Lab 01 — Wind Tunnel Characterization
- Date: February 7, 2025
- Instrumentation: traverse pitot-static probe, analog manometer, ADC, MATLAB DAQ
- Test conditions: T = 21.5°C, P = 30.3 inHg, ρ = 1.213 kg/m³
- Experiment A: Fan frequency swept 0–25 Hz at fixed probe height
- Experiment B: Probe height swept 1–40 in at 15 Hz (≈10 m/s)
- Key results: 
  - Airspeed ranges 2.89–18.2 m/s over 5–25 Hz
  - Re/L ranges 192,508–1,212,334 (1/m)
  - Turbulence intensity increases with height; speed decreases near ceiling
  - Velocity uncertainty <0.1% at higher speeds
- Figures: Airspeed vs Fan Speed (Fig 2), Height vs Airspeed (Fig 3), Height vs Turbulence Intensity (Fig 4)

### Lab 02 — Flow Around Cylinders
- Date: February 27, 2025
- Cylinder diameter: 1.4 in; 24 angular positions measured
- Test conditions: T = 24°C, P = 30.4 inHg, ρ = 1.207 kg/m³
- Two velocities: 10 m/s (Re ≈ 23,515) and 15 m/s (Re ≈ 35,272)
- Key results:
  - Both regimes subcritical (Re < 300,000)
  - Cd = 1.3055 at 10 m/s, Cd = 1.4239 at 15 m/s
  - Higher velocity → later flow separation from cylinder
  - Cp agrees with potential flow near stagnation; diverges past ~40°
- Figures: Cp vs Angle (Fig 1), Cd vs Re (Fig 2)

### Lab 03 — Lift and Drag on Airfoils (NACA 4412)
- Date: March 28, 2025
- Airfoil: NACA 4412, 6-inch chord, 18 static pressure taps
- Test speed: 15 m/s; AoA: −3°, 0°, 3°, 6°, 9°, 12°
- Test conditions: T = 22°C, P = 30.1 inHg, ρ = 1.203 kg/m³
- Key results:
  - Cl increases linearly with AoA; below panel code due to viscosity
  - Cd increases with AoA; drag polar bowl-shaped
  - Cm,LE becomes more negative with increasing AoA
  - Cm,c/4 near constant; close to potential flow
  - Peak L/D at ~9° AoA
  - Zero-lift AoA = −3.31°
- Figures: Wake profiles (Fig 2), Cp distribution (Fig 3), Cl vs AoA (Fig 4), Cd vs AoA (Fig 5), Cm,LE (Fig 6), Cm,c/4 (Fig 7), Drag Polar (Fig 8), L/D vs AoA (Fig 9)

### Lab 04 — Forces and Moments on a Canard Delta Wing
- Date: April 4, 2025
- Tunnel: ERAU Micaplex closed-circuit wind tunnel
- Model: canard-delta wing; Sw = 242.01 in², cw = 9.88 in, bw = 24.5 in
- Test matrix: 75 fps / 100 fps × 0° / 10° yaw; AoA −4° to 34° (2° steps)
- Test conditions: P = 102,438 Pa, T = 295.15 K, ρ = 1.205 kg/m³
- Aerodynamic tares applied (image + invert method)
- Key results:
  - CL linear to ~25° AoA; flow separation above that
  - Higher Re → lower Cd (better flow attachment)
  - Best CL/CD = 4.21 at 12° AoA (75 fps, 0° yaw)
  - 10° yaw: negligible effect on lift; increases side force and yaw moment
  - Cm rises with pitch angle; higher at higher Re
- Figures: Lift (F1), Drag (F2), Side Force (F3), Pitching (F4), Rolling (F5), Yawing (F6), CL (F7), CD (F8), Drag Polar (F9), L/D (F10), Cm (F11)

### Lab 05 — Schlieren Imaging & Supersonic Wind Tunnels
- Date: April 18, 2025
- Tunnel: ERAU supersonic wind tunnel (blowdown, air-driven)
- Components documented: dryer, compressor, storage tank, main valve, regulator, nozzle, Schlieren system, silencer
- Throat area: Ath = 0.765 in²; nozzle half-angle: ~4.8°
- 13 pressure taps at positions: 1.5–19.5 inches along nozzle floor
- Key results:
  - Shock wave located between 9.5 and 10.5 inches
  - NPR = 3.932 (flow is shocked; NPR > critical value)
  - Shock strength = 1.6142 (moderate)
  - Mass flow rate = 6.1036 lbm/s
  - Pressure drops continuously in diverging section then spikes at shock
- Figures: Schlieren images (F2.1, F2.2), Pressure vs position (F3.1), Pressure vs row points (F3.2)

---

## CSS / Styling Notes

- All pages use `style.css` unchanged — no new classes needed
- Image placeholders use `<div class="project-image-note">` (existing class)
- Code blocks: `<pre style="background:#f4faff; padding:1rem; border-radius:6px; overflow-x:auto;"><code>` (inline style, no new CSS class)
- Detail pages use alternating `project-row` sections (no alternating background — existing CSS handles this)

## Constraints

- No JavaScript
- No new CSS classes
- Nav and footer duplicated identically across all new files (same pattern as all other pages)
- All links relative (no absolute paths)
