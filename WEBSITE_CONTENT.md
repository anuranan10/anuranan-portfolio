# Anuranan Bharadwaj — Website Content (anuranan.info)

This document mirrors the full content of [anuranan.info](https://anuranan.info), Anuranan Bharadwaj's personal portfolio website. It walks through every page — the homepage bio, aerospace and computer science project pages, work experience, lab testing experience (all 16 individual lab reports across three ERAU courses), highlights, resume, and contact information — so that reading this file gives the same overall impression as browsing the live site.

---

## 1. Home / Bio

**Anuranan Bharadwaj — Aerospace Engineer**

Anuranan is an international student from India who recently graduated with a B.S. in Aerospace Engineering, with a minor in Computer Science, from Embry-Riddle Aeronautical University (ERAU).

His expertise centers on **turbomachinery and propulsion**, with a focus on blade aerodynamics, thermodynamic cycle analysis, and turbine performance characterization. This engineering foundation also extends into **structural analysis**, **flight dynamics and control**, and **experimental aerodynamics** — validating designs from first-principles models through wind tunnel and flight testing and instrumentation design. Beyond the core discipline, he has also developed skills on the **software and computer science** side, including building databases, web applications, AI research, and computational tools that support engineering analysis.

The homepage links out to five main sections:
- **Aerospace** — Design, simulation, and analysis projects spanning propulsion, structures, dynamics, and controls
- **Computer Science** — Software projects spanning web development, databases, and applied programming
- **Work Experience** — Internships, research roles, and leadership positions
- **Highlights** — Conferences, mentorships, and experiences beyond the classroom
- **Resume** — Downloadable resumes covering his full background

---

## 2. Aerospace Engineering Projects

The Aerospace Projects hub ("Hands-on experience in propulsion, flight dynamics, aerodynamics, structures, and orbital mechanics") organizes projects into discipline categories: Propulsion & Turbomachinery, Flight Dynamics & Controls, Experimental Aerodynamics, Structural Analysis, Orbital Mechanics, Systems & Decision Tools, and Engineering Design.

### Flagship Project: High-Bypass Turbofan Engine Senior Design

**AE 440, Senior Design, Spring 2026, ERAU**
**Role:** Team Lead — Inlet & Turbomachinery Design
**Tools:** MATLAB, AEDsys, Excel, CAD (Onshape), Sovran & Klomp Diffuser Maps

**Headline stats:** 11:1 bypass ratio · 196 kN takeoff thrust · 9 compressor/turbine stages (vs. 13–14 in the GE90) · 55:1 overall pressure ratio · 16 (g/s)/kN cruise TSFC

A four-person team (Anuranan Bharadwaj, Vincent Shi, Nicholas Pradilla, and Kalkamanali Satvaldy) led the end-to-end design of the **Atlas-85X**, a 74,770 lbf high-bypass, separate-exhaust turbofan for a 1,000,000 lb MTOW airlifter with a 6,940 nm range and 5,400 ft runway requirement.

**Cycle Analysis & Validation**
A custom MATLAB cycle analysis tool was built and validated against AEDsys with less than 1% error, then used to size the engine across takeoff, cruise, and loiter conditions.

**Inlet Design**
The inlet throat was sized for the cruise condition (M_th = 0.70), with average pressure recovery coefficient C̄p = 0.25, diffuser pressure ratio π_d = 0.960, area ratio A0/A1 = 0.90, and fan-face Mach number M2 = 0.55, using Sovran & Klomp diffuser maps.

**Turbomachinery**
- Single-stage fan: 38 rotor blades, 3.65 m diameter, π = 1.30, 2,200 RPM via a 3.2:1 reduction gearbox
- 3-stage low-pressure compressor (LPC): π = 3.5, η = 0.90, 7,000 RPM
- 6-stage high-pressure compressor (HPC): π = 15.7, η = 0.89, 13,000 RPM, blade speed 495 m/s
- 1-stage high-pressure turbine (HPT): 45/51 blades, T4 = 1,778 K, η = 0.96, 26.8 MW
- 2-stage low-pressure turbine (LPT): 18.9 MW, 7,000 RPM

The design uses 9 compressor stages plus 3 turbine stages, compared to 13–14 compressor stages and 8 turbine stages in the GE90/GE9X family — a major simplification enabled by the geared fan architecture.

**Combustor**
Annular combustor, length 0.41 m, diameter 0.67 m, L/D = 0.62, 4% pressure drop, 0.01 s residence time.

**Nozzles**
Both core and bypass streams use convergent-only nozzles. A trade study comparing convergent-divergent (CD) nozzles found only a 1.6% whole-engine performance gain versus a 7.7% core-only gain at BPR 11 — not enough to justify the added weight and complexity of a CD nozzle at this bypass ratio.

**Cruise Performance**
Net thrust = 67.3 kN (47.5 kN core + 179.1 kN bypass − 159.3 kN ram drag), specific thrust = 84 N/(kg/s), TSFC = 16 (g/s)/kN.

**Key Takeaways**
- Cycle validation before design: validating the MATLAB cycle tool against AEDsys before sizing components avoided compounding errors downstream.
- Stage count as a design variable: minimizing stage count (9 vs. 13–14+8 in legacy designs) directly reduces weight, cost, and maintenance burden.
- Gearbox enables fan efficiency: decoupling fan speed from LPC/LPT speed via the 3.2:1 gearbox lets each component operate near its efficiency optimum.
- Nozzle trade — CD not justified at BPR 11: the marginal whole-engine gain (1.6%) does not offset the added complexity of a convergent-divergent nozzle at this bypass ratio.

---

### Flight Dynamics & Controls

#### DC-8 PID Controller Design

**AE 432, Flight Dynamics and Control, Fall 2025, ERAU**
**Role:** Team Member — Flight Dynamics & PID Design
**Tools:** MATLAB, Transfer Function Analysis, Pole Placement, Characteristic Polynomial Matching, Final Value Theorem

**Headline stats:** 3 flight modes characterized · 4% AOA max overshoot · 1.614 rad/s short-period natural frequency · 0° angle-of-attack steady-state error

This project derived linearized longitudinal and lateral-directional transfer functions for the DC-8 and designed PID controllers to meet transient-response specifications, holding angle-of-attack overshoot under 4% with zero steady-state error.

**Transfer Functions Derived**
- Short Period: Δα(s)/Δδe(s) = (−0.04195s − 1.384) / (s² + 1.6815s + 2.616)
- Phugoid: ΔU(s)/ΔδT(s) = 12.9s / (s² + 0.02915s + 0.03326)
- Dutch Roll: ΔP(s)/Δδr(s) = (0.03379s − 0.3953) / (s² + 0.3794s + 0.7918)

**Mode Characteristics**

| Mode | Poles | ωₙ (rad/s) | ζ |
|---|---|---|---|
| Short Period | −0.8404 ± j1.3819 | 1.6144 | 0.5196 |
| Phugoid | −0.01455 ± j0.18179 | 0.1823 | 0.0798 |
| Dutch Roll | −0.1897 ± j0.8694 | 0.8899 | 0.2132 |

**Angle-of-Attack PID Controller**
Design target: Mp ≤ 5%, giving ζd = 0.6901, ωnd = 0.4347 rad/s, third pole p3 ≈ −3, and a desired characteristic equation s³ + 3.6s² + 1.989s + 0.567 = 0. Resulting gains: kP = 0.3718, kI = −0.4366, kD = −1.569.

Result: 4% overshoot (meets the ≤5% spec), settling time ts = 15s (does **not** meet the <10s spec), and 0° steady-state error (Final Value Theorem confirmed).

**Forward Speed PID Controller**
Design target: Mp ≤ 7%, giving ζd = 0.6461, ωnd = 0.3095, p3 ≈ −2, with gains kD = −0.075, kP = −7.364×10⁻³, kI = −2.381×10⁻³. ΔUss = 0 in theory, but the response showed large transients, indicating the forward-speed model was not well-conditioned for this controller design.

**Key Takeaways** (4 total) cover transfer function derivation from state-space models, the trade-off between meeting overshoot vs. settling-time specs simultaneously, the value of the Final Value Theorem for verifying steady-state behavior analytically, and the limits of pole-placement design when a plant model is poorly conditioned.

---

#### Quanser Aero PID Control Design

**AE 443, Experimental Dynamics & Control Laboratory, Spring 2026, ERAU**
**Role:** Team Member — PID Tuning & System Identification
**Tools:** MATLAB, Simulink, QUARC Real-Time Control, Transfer Function Analysis, Bode/Frequency Response

**Headline stats:** 4.12% final PID overshoot · 1.18s peak time · 87.5° phase margin · 2.18 rad/s identified natural frequency

This project tuned a PID pitch controller on a physical two-DOF Quanser Aero platform (pitch axis only) using real-time hardware-in-the-loop control via QUARC.

**Open-Loop Characterization**
Peak time tp = 1.694s, settling time Ts = 13.63s, percent overshoot PO = 68.96%, ζ = 0.1178, ωn = 1.865 rad/s.

**Gain Sensitivity Studies**
- kp swept 5–10: overshoot grows past 60% at higher gains
- kd swept 4–8: drives overshoot to 0% but increases peak time to ~2.6s
- ki swept 3–6: ki = 5 gave steady-state output yss = 0.2976 rad

**Final Tuned Controller**
kp = 8, kd = 3.1, ki = 5 → tp = 1.18s (marginally fails the <1.1s spec), PO = 4.12% (passes), yss = 0.2976 rad (passes, target 0.3).

**System Identification**
Second-order model fit: G(s) = 1.27332 / (s² + 0.10047s + 3.62403), giving ζ = 0.0452, ωn = 2.18 rad/s. Errors versus measured response: 0.14% (peak time), 3.48% (overshoot), 3.61% (steady-state).

**Analytical vs. Workbook Gains**
Theoretical PID gains: kd = 3.847, kp = 3.437, ki = 3.141. The workbook (course-provided) gains used for hardware were kp = 3.3739, kd = 3.7484, ki = 3.06, giving 0% overshoot but a slower peak time of 4.64s.

**Frequency Response**
Open-loop phase margin = 3.68° (near-unstable); PID-compensated phase margin = 87.5°, gain margin infinite for both, bandwidth = 19.32 rad/s.

**State-Space Model**
A = [[0,1],[−ωn², −2ζωn]], B = [[0],[ωn²]], C = [1,0], D = [0] — confirmed fully controllable and observable.

**Key Takeaways** (4 total) emphasize the gap between analytical and hardware-tuned gains, how derivative gain trades overshoot for speed, the importance of phase margin as a robustness metric, and the value of validated state-space models for downstream controller design.

---

#### Aircraft Stability & Control Simulation

**AE 413, Aircraft Stability and Control, Spring 2025, ERAU**
**Role:** Team Member — Stability Analysis & Simulation
**Tools:** MATLAB, Simulink, USAF DATCOM, FlightGear, Multhopp's Theory, Hand Calculations

**Headline stats:** Mach 0.6 design condition · 43.5% MAC neutral point · <3.5% error vs. DATCOM (Cnβ) · 3 simulated maneuvers

The team built a closed-loop 6-DOF flight simulation in MATLAB/Simulink for a general aviation aircraft (22 ft span, 121 ft² wing area, AR = 4, 4,000 lb gross weight, 6,500 ft altitude, α = 2°), comparing hand-calculated stability derivatives against USAF DATCOM predictions.

**Geometry**

| Surface | Root Chord | Tip Chord | Span | Area | MAC | AR | Sweep | Dihedral | Taper |
|---|---|---|---|---|---|---|---|---|---|
| Wing | 6.5 ft | 4.5 ft | 22 ft | 121 ft² | 5.561 ft | 4.0 | 11° | 3° | 0.692 |
| Horizontal Tail | 3.0 ft | 2.5 ft | 8 ft | 22 ft² | 2.758 ft | 2.909 | 10° | 8° | 0.833 |

Other parameters: CL0 = 0.143, CD0 = 0.017, CLα = 4.648/rad (0.0811/deg), Vstall = 163.8 ft/s, fuselage length = 27.708 ft.

**Longitudinal Stability**
Hand-calculated Cmα,fuselage (via Multhopp's method) = 0.4702/rad. Total hand-calc Cmα ≈ −1.35/rad vs. DATCOM's −0.293/rad — a large discrepancy attributed to limitations in DATCOM's tail-effectiveness modeling. Neutral point N0 = 0.435 (43.5% MAC).

**Directional & Lateral Stability**
- Directional: Cnβ (hand) = 0.189/rad vs. Cnβ (DATCOM) = 0.183/rad — agreement within 3.5%
- Lateral: Clβ (hand) = −0.1231/rad vs. Clβ (DATCOM) = −0.113/rad — difference of 0.01/rad

A comparison table also covers CLα, CL, CD, Vstall, downwash gradient dε/dα = 0.456 (hand) vs. 0.461 (DATCOM), and Cmδe = −0.01385/deg.

**Simulink Model**
Five lookup-table-driven derivatives (Cnr = −0.008426, Cnp = −0.0006962, Cmq = −0.1992, Clα = 0.08109, Cnβ = 0.003193 at α = 2°) feed a 6-DOF general aviation model linked to FlightGear for visualization.

**Simulated Maneuvers**
1. Level Flight: V = 654 ft/s, δe = −1.71°, Altitude = 6,500 ft
2. Pitch-Up: V = 630 ft/s, δe = +2°, Altitude = 6,530 ft
3. Right Bank: V = 654 ft/s, neutral controls

**Key Takeaways** (4 total) discuss the divergence between hand calculations and DATCOM for pitch stiffness, the strong agreement on directional derivatives, the value of FlightGear visualization for sanity-checking simulation results, and the overall workflow connecting hand analysis, DATCOM, and 6-DOF simulation.

---

### Experimental Aerodynamics

#### Wind Tunnel Drag Study — Flap Deflection

**AE 315, Experimental Aerodynamics, Spring 2025, ERAU**
**Role:** Team Member — Experimental Aerodynamics
**Tools:** MATLAB, Wake Survey (Pitot-Static Probe), DAQ/ADC, Servo Microcontroller, Trapezoidal Integration, Error Propagation (95% CI)

**Headline stats:** 5 flap deflection angles tested · 2.20 N peak drag (full flap, 50°) · 0.220 max Cd (50°) · <0.06 N uncertainty across all trials

A NACA 4412 wing with servo-actuated flaps was tested in the ERAU open-loop subsonic wind tunnel at flap deflections of 0°, 15°, 25°, 35°, and 50°, using two pitot-static probes (one stationary reference, one traversing through the wake) at Tamb = 294.15 K and Pamb = 102,268.94 Pa. The wing's structural attachment failed during installation and was re-secured with electrical tape — an acknowledged source of uncertainty in the results.

**Method**
Drag per unit span: D' = ρ∞ ∫ Uw(U∞ − Uw) dy, computed via trapezoidal integration of the wake velocity deficit. Drag coefficient: Cd = D' / (½ρU∞²c).

**Drag Force Summary**

| Flap Angle | Drag Force (N) | Uncertainty (±N) | Cd |
|---|---|---|---|
| 0° | 1.8824 | 0.0443 | 0.200 |
| 15° | 1.9636 | 0.0493 | 0.205 |
| 25° | 1.8328 | 0.0426 | 0.191 |
| 35° | 1.9277 | 0.0482 | 0.199 |
| 50° | 2.2000 | 0.0587 | 0.220 |

Drag rose 16.9% from 0° to 50° flap deflection. The 25° case showed an anomalous dip relative to the otherwise increasing trend.

**Key Takeaways** (4 total) cover the wake survey method as a reliable means of extracting drag from velocity-deficit profiles, the impact of structural mounting issues on data quality, the non-monotonic 25° anomaly as a reminder to scrutinize outliers, and the role of error propagation in establishing confidence in experimental drag measurements.

---

### Structural Analysis

#### Aircraft Wing Structural Analysis

**Structures, ERAU**
**Role:** Individual — CAD Modeling & FEA Simulation
**Tools:** Fusion 360, FEMAP, NX Nastran

**Headline stats:** >0.6 minimum Jacobian · 0.15 in peak tip displacement · full 3D assembly model · NX Nastran FEA solver

A complete wing assembly — front and rear spars, ribs, stringers, and skin panels — was modeled in Fusion 360 and transferred to FEMAP for finite element analysis. A distributed aerodynamic load was applied to the skin, with the wing root fixed as the boundary condition. The mesh combined shell elements (skin) with beam elements (spars/stringers), and all elements achieved a Jacobian quality metric above 0.6.

**Results**
- Peak tip displacement ≈ 0.15 in
- Highest von Mises stress occurred at the front spar root
- Skin stress was lower than spar cap stress throughout
- No meshing-artifact stress concentrations were observed

**Key Takeaways** (4 total): CAD quality directly controls FEA validity; spars dominate bending load paths; mesh refinement should be targeted at known stress risers (spar root); and Jacobian validation is a necessary quality-control step before trusting FEA results.

---

### Orbital Mechanics

#### TDRS-M Orbital Mechanics and Trajectory Design

**AE 313, Space Mechanics, Fall 2025, ERAU**
**Role:** Team Member — Trajectory Design & Orbital Mechanics Analysis
**Tools:** MATLAB, ode45, Vis-Viva Equation, Tsiolkovsky Rocket Equation, Hohmann Transfer Theory

**Headline stats:** 5.36 km/s total mission Δv · 5.48 hr LEO→GEO transfer time · 82% propellant mass fraction · 0.028 km/s phasing maneuver cost

This project simulated a full LEO-to-GEO transfer mission profile for the TDRS-M satellite, broken into four phases.

**Phase 1 — LEO Parking Orbit**
r0 = 6,678 km, Vcirc = 7.73 km/s, period T = 5,400s, integrated with ode45 (RelTol = AbsTol = 1e-9). Classical orbital elements: a = 6,678 km, e = 0, i = 28.5°.

**Phase 2 — Hohmann Transfer**
Transfer orbit semi-major axis at = 24,421 km, perigee velocity Vp,t = 10.15 km/s, apogee velocity Va,t = 1.61 km/s, transfer period Tt = 10.95 hr, transfer time tPA = 5.48 hr, Δv1 (LEO→GTO injection) = 2.42 km/s.

**Phase 3 — GEO Insertion + Plane Change**
Combining circularization and plane change at apogee (where velocity is only 3.07 km/s vs. 10.15 km/s at perigee) saves roughly 3.5 km/s compared to performing the plane change at perigee. Δvcirc = 1.46 km/s, Δvinc = 2·VGEO·sin(Δi/2) = 1.50 km/s, total mission Δv = 5.36 km/s.

Using the Tsiolkovsky rocket equation with m0 = 3,500 kg, Isp = 320s, exhaust velocity Ve = 3.139 km/s: mass ratio m0/mf = 5.53, final mass mf = 633 kg, propellant mass mp = 2,867 kg (82% of initial mass).

**Phase 4 — Phasing Maneuver**
For a 5° longitude offset: phasing orbit semi-major axis = 42,554 km, apogee radius ra = 42,943 km, duration 24.3 hr, Δv1 = Δv2 = 0.014 km/s, total = 0.028 km/s (less than 0.6% of total mission Δv).

**Δv Budget Summary**

| Maneuver | Δv (km/s) |
|---|---|
| LEO → GTO injection | 2.42 |
| GEO circularization | 1.46 |
| Plane change | 1.50 |
| **Total** | **5.36** |

**Real-World Comparison**
The simulated mission (5.36 km/s, 82% propellant fraction) used significantly more Δv and propellant than the real TDRS-M mission (~2.0 km/s, ~42% propellant), because the actual Delta IV Medium+ launch vehicle performs most of the inclination reduction during a supersynchronous GTO insertion — a strategy not modeled in this simplified simulation.

**Key Takeaways** (4 total) cover the efficiency of combining plane-change and circularization burns at apogee, the dominant cost of inclination changes in the Δv budget, the value of validating simulation results against real mission data, and the practical insight that launch vehicle trajectory design (supersynchronous GTO) can dramatically reduce spacecraft propellant requirements.

---

### Systems & Decision Tools

#### Database Application for Aircraft Fleet Selection

**MATLAB / Excel / Decision Support Systems, ERAU**
**Role:** Individual — Application Design & Development
**Tools:** MATLAB, MATLAB App Designer, Excel

**Headline stats:** 25% faster data retrieval · interactive GUI · live Excel data backend · multi-parameter filtering

A MATLAB App Designer GUI was built for querying and comparing aircraft by multiple performance parameters, featuring a filter panel, results table, and visualization panel. The application reads from an Excel backend via `readtable()`, decoupling data from application logic so records can be updated without code changes. Bar charts are used for small result sets and scatter plots for larger sets, and in-memory queries keep response times under 100ms — a roughly 25% improvement in data retrieval speed compared to manual spreadsheet workflows.

**Key Takeaways** (4 total): separating data from code simplifies maintenance; visualization type should match the size/shape of the result set; multi-parameter filtering helps expose design trade-offs; and in-memory queries are essential for keeping a GUI responsive.

---

### Engineering Design

#### LEGO Airplane Design & Engineering Documentation

**EGR 120: Introduction to Engineering, Spring 2023**
**Role:** Individual — 3D Design & Drawing Package
**Tools:** BrickLink Studio, SolidWorks, Rendering

**Headline stats:** EGR 120 · 17-page engineering drawing package · twin-engine configuration · T-tail empennage

A twin-engine LEGO airplane with a T-tail empennage and tricycle landing gear was designed in BrickLink Studio (using the real LEGO part library and connection logic) in a teal/orange/white color scheme, drawing inspiration from a reference LEGO Technic race plane. A photorealistic ray-traced rendering was composited onto a runway photo background.

**17-Page SolidWorks Drawing Package**
- Sheet 01/17: Full Assembly Isometric (1:1 scale)
- Sheet 02/17: Full Assembly Exploded View with 22 part callouts (1:2 scale)
- Sheet 08/17: Wing 1 Subassembly (1:1 scale)
- Sheet 13/17: Section A-A view (2:1 scale)
- Sheet 16/17: Support Element detail with H8/f7 tolerances (2:1 scale)

**Key Takeaways** (4 total): design constraints (limited part library) drive creativity; engineering drawings are a communication standard across disciplines; translating a 3D model to 2D views requires deliberate view selection; and rendering grounds a design in a realistic physical context.

---

## 3. Computer Science Projects

**Header:** "Computer Science Projects" — "Selected software projects built using Java, Python, MERN, C#, and more"

### 1. 3D Interactive Airport Scene (Three.js)
**Tags:** Three.js, WebGL, JavaScript, OrbitControls, Raycasting

A full interactive 3D airport scene featuring an aircraft, hangar, fuel truck, baggage carts, and light poles, rendered with real-time shadows. Includes a dual-camera system — orbit camera and a WASD first-person camera — with raycasting enabling click-based interactions (toggling lights, animating the hangar door open/closed). The scene uses a multi-light pipeline (directional, point, and spot lights with 2048×2048 shadow maps), a looping fuel truck animation, sine-wave-driven beacon lighting, atmospheric fog, and tarmac/grass textures.

### 2. Neural Network from Scratch — MNIST Digit Classifier
**Tags:** Python, NumPy, MNIST, Backpropagation, ReLU/Softmax

A two-layer feedforward neural network built using only NumPy (no ML frameworks), with a 784 → 10 (ReLU) → 10 (Softmax) architecture. Trained on 42,000 MNIST digit images, with 1,000 held out for evaluation. Implements manual backpropagation, one-hot label encoding, and gradient descent, achieving approximately 89% training accuracy after 500 iterations at a learning rate α = 0.1.

### 3. HFT Strategy Backtesting Engine
**Tags:** Python, Pandas, Matplotlib, RSI, Bollinger Bands

A Python backtesting engine for high-frequency trading strategies that combines RSI momentum signals, Bollinger Band mean-reversion signals, and stop-loss/take-profit logic. Ingests millisecond-resolution tick data via Pandas and provides Sharpe ratio analysis, drawdown tracking, and parameter sweeps visualized through multi-panel Matplotlib dashboards.

### 4. ClassConnect — QR-Based Attendance Platform (In Progress)
**Tags:** JavaScript, Firebase, Firestore, QR Code, HTML/CSS

A full-stack QR-based attendance platform using dynamically time-expiring QR codes to prevent fraudulent check-ins. The frontend is built with JavaScript/HTML/CSS, with a Firebase Cloud Functions and Firestore backend providing sub-second session validation and real-time dashboards. Results: attendance logging completes in under 30 seconds, 100% submission accuracy, and a 90% reduction in manual entry time.

### 5. Pharmaceutical Inventory System
**Tags:** Java, OOP, CLI

A modular Java inventory system applying object-oriented principles (encapsulation, inheritance, polymorphism) to separate stock, supplier, and transaction logic. Automated multi-step financial calculations cut input errors by 15% and improved processing speed by 25%, with real-time stock tracking.

### 6. Code Analysis Tool (CAT)
**Tags:** C#, .NET, WPF

A WPF desktop application built in C#/.NET that statically analyzes Java codebases — measuring lines of code, class counts, inheritance depth, and conditional branching complexity. Processes 10+ Java files in seconds, reducing manual code review time by 25% and improving analysis accuracy to 90%.

The CS page also includes a download button for the **Software Engineering Resume** (`AnurananBharadwaj_RESUME_SE.pdf`).

---

## 4. Work Experience

The Work Experience page header reads: "A blend of technical internships, teaching roles, and hands-on engineering leadership." It lists nine entries, most recent first:

### 1. Turbomachinery Software Intern — Concepts NREC
**Internship · January 2026 – April 2026**
- Extended Axcent's automated CFD testing framework from single-solver (pbCFD) to dual-solver support by integrating FINE/Turbo (Cadence Design Systems), modifying Python automation scripts and adapting API calls for solver-specific execution flows, data handling, and post-processing differences.
- Implemented a polling-based solver monitoring function that periodically checks simulation status and gates data processing until completion, resolving a robustness issue where the pipeline terminated before solver output was fully generated.
- Conducted a geometric consistency study of 20+ Axcent blade profiles applied to axial turbine configurations, extracting parameters (camber, max thickness, LE/TE radii, unguided turning angle) across CW/CCW orientations and SI/British unit systems — findings directly identified bugs in Axcent's blade geometry implementation.

### 2. Reinforcement Learning Research Assistant — Embry-Riddle Aeronautical University
**Research · July 2025 – April 2026**
- Contributing to an AI research project developing and evaluating Reinforcement Learning agents (SAC & DDPG) to autonomously control a vehicle in a custom driving simulator (CARLoS).
- Integrating prebuilt RL algorithms (Stable-Baselines3) into a Python-based, low-fidelity simulation environment by adapting agent-environment interactions and implementing Gym-style interfaces for training and evaluation.
- Benchmarking SAC and DDPG performance against reward convergence, policy stability, and generalization to unseen driving scenarios to inform future high-fidelity simulator integration.

### 3. Undergraduate Research Assistant – Gas Turbine Lab — Embry-Riddle Aeronautical University
**Research · May 2025 – April 2026**
- Built an Excel-Python computational tool implementing Aungier's deviation angle correlations with Mach-dependent branching (M=1, M>0.5, M≤0.5) across four blade rows (S1, R1, S2, R2) of a turbine cascade, using Python's `fsolve` to converge deviation angle and throat opening values through iterative root-finding.
- Automated multi-stage turbine parameter analysis in Python — reading inputs directly from Excel, reproducing Aungier-based calculations, and updating outputs on input changes — replacing manual Goal Seek iteration and enabling rapid aerodynamic design exploration.
- Designed and iteratively prototyped a custom five-arm pitot rake in PETG via 3D printing for the ERAU turbine cascade rig, progressing from a two-arm fit-check prototype to a final external-mount structure supporting five simultaneous pitot tube measurements, eliminating the need for repeated single-probe test runs.

### 4. C&DH Software Developer – Project COMET — Embry-Riddle Aeronautical University
**Design Team · April 2025 – April 2026**
- Designing and developing real-time flight software in C for a 12U CubeSat featuring mmWave inter-satellite communication, contributing to a scalable, low-latency space network architecture.
- Building modular applications within NASA's Core Flight System (cFS) on Ubuntu Linux to control satellite subsystem operations, implement automated fault-recovery algorithms, and manage various spacecraft modes.
- Contributing to the design of a high-throughput (500+ Mbps) autonomous satellite communication system as part of NASA's University Nanosatellite Program (UNP) launch competition.

### 5. Compressor Team Lead – Project Aether — ERAU Experimental Jet Engine Propulsion Club
**Design Team · January 2025 – April 2026**
- Designing the centrifugal impeller stage for a 300 kW turboshaft engine, defining blade geometry to meet target pressure ratio and mass flow specified by thermodynamic cycle analysis.
- Using CFTurbo to generate preliminary impeller blade profiles, meridional flow paths, and splitter vane configurations for initial aerodynamic evaluation.
- Coordinating with thermodynamic cycle analysts to reconcile impeller inlet/exit conditions with overall engine operating requirements.

### 6. Software Engineer Intern — ABH Software, Assam, India
**Internship · July 2024 – August 2024**
- Architected and prototyped a Local Business Management Platform covering inventory control, customer management, and sales tracking for small retail business deployment.
- Optimized SQL queries, enhancing data accuracy by 20% and reducing report processing time by 30%.
- Collaborated with cross-functional teams to implement Java-based features using Agile methodologies.

### 7. Teaching Assistant – EGR 115 (Intro to Computing for Engineers) — Embry-Riddle Aeronautical University
**Teaching · January 2024 – August 2025**
- Guided students through MATLAB programming, numerical methods, and algorithmic problem-solving.
- Provided structured feedback and one-on-one help sessions to improve students' coding proficiency and logic.
- Led collaborative lab sections, enhancing peer-to-peer learning and fostering computational thinking.

### 8. Peer Mentor – EGR 101 (Introduction to Engineering) — Embry-Riddle Aeronautical University
**Teaching · August 2023 – December 2023**
- Mentored first-year engineering students through academic and professional development, helping them navigate course expectations, campus resources, and the transition to university-level engineering coursework.
- Facilitated weekly group sessions covering study strategies, engineering discipline overviews, and problem-solving approaches aligned with EGR 101 course objectives.
- Provided one-on-one guidance to help students build early confidence in technical coursework and develop habits for long-term academic success.

### 9. Electrical Head – ERIC Oblique-Wing RC Aircraft — Embry-Riddle Inventors Club
**Design Team · August 2023 – May 2024**
- Led the design of custom PCBs, telemetry systems, and power distribution networks for an oblique-wing RC aircraft inspired by NASA AD-1.
- Integrated electrical components for real-time control, data logging, and sensor fusion.
- Presented intermediate prototype and roadmap to MicaPlex mentors for external development opportunities.

---

## 5. Lab Testing Experience

**Header:** "ERAU Lab Testing Experience" — "Hands-on experimentation across aerodynamics, structural mechanics, dynamics, and controls — Embry-Riddle Aeronautical University"

This section is a hub linking to three sub-hubs, each covering a different ERAU laboratory course.

### 5.1 Experimental Aerodynamics Lab (AE 315, Spring 2025)

**Sub-hub description:** "Five wind tunnel experiments spanning subsonic characterization, external flow over cylinders and airfoils, force and moment measurement on a canard-delta wing, and supersonic Schlieren imaging. Conducted in AE 315 at ERAU, Spring 2025, using pitot probes, pressure taps, a six-component force balance, and optical flow visualization."

#### Lab 01: Wind Tunnel Characterization
**Equipment:** ERAU open-circuit wind tunnel, traversing pitot-static probe (1–40 in.), analog manometer, ADC, MATLAB DAQ.

**Approach:** Airspeed computed via V = √(2q/ρ); the fan was swept from 0–25 Hz in 5 Hz steps. Turbulence intensity I = 100 × σV / V̄. Reynolds number per unit length computed via Sutherland's formula.

**Key Results:** Airspeed ranged from 2.89 m/s at 5 Hz to 18.2 m/s at 25 Hz, varying linearly with fan frequency. Re/l reached 1.21×10⁶ m⁻¹ at 25 Hz. Velocity uncertainty dropped from 0.42% at low speed to 0.056% at 18.2 m/s. Turbulence intensity increased near the tunnel ceiling, consistent with boundary layer growth.

**Valuable Takeaways** (4 total) cover the linear fan-frequency-to-airspeed relationship as a calibration tool, the importance of uncertainty quantification at varying operating points, the boundary-layer origin of near-wall turbulence increases, and the foundational role of tunnel characterization before any subsequent aerodynamic testing.

#### Lab 02: Flow Around Cylinders
**Equipment:** 1.4-inch aluminum cylinder, single static pressure port, 24 angular positions (0°–180°), differential pressure transducer.

**Approach:** Pressure coefficient Cp normalized against freestream dynamic pressure; compared to potential flow theory Cp = 1 − 4sin²θ. Drag coefficient Cd computed via trapezoidal integration of Cp·cosθ.

**Key Results:** Measured Cp matched potential flow theory below ~40° but diverged sharply past 40° due to boundary layer separation. Both test conditions were subcritical (Re < 300,000): Cd = 1.31 at 10 m/s (Re ≈ 23,515) and Cd = 1.42 at 15 m/s (Re ≈ 35,272) — the higher Reynolds number delayed separation but produced a wider wake and higher overall drag.

**Valuable Takeaways** (4 total) discuss the divergence from potential flow as direct evidence of boundary layer separation, the counterintuitive Cd increase with Reynolds number in the subcritical regime, the value of pressure-tap data for mapping flow topology, and MATLAB's role in automating Cp/Cd computation across angular sweeps.

#### Lab 03: Lift and Drag on Airfoils
**Equipment:** NACA 4412 airfoil, 6-inch chord, 18 static pressure taps (10 upper, 8 lower), 76-position traversing wake probe, freestream velocity 15 m/s, angle of attack swept −3° to 12°.

**Approach:** Lift coefficient Cl = (1/c)∫(Cp,lower − Cp,upper)dx; drag computed from wake momentum deficit; pitching moments computed about both the leading edge and the quarter-chord.

**Key Results:** Cl increased linearly with angle of attack but remained below the potential-flow prediction. Cm,LE became more negative with increasing AoA, while Cm,c/4 stayed approximately constant at −0.09, confirming the quarter-chord as the aerodynamic center. Zero-lift angle of attack = −3.31°. Peak lift-to-drag ratio occurred near 9° AoA, and the drag polar was bowl-shaped rather than the typical "fishhook" shape, partly due to elevated drag at −3° AoA.

**Valuable Takeaways** (4 total) cover the experimental confirmation of the aerodynamic center concept, the systematic under-prediction by potential flow theory due to viscous effects, the use of wake surveys for drag extraction, and the practical interpretation of drag polar shape.

#### Lab 04: Forces and Moments on a Canard-Delta Wing
**Equipment:** ERAU Micaplex closed-circuit wind tunnel, 75/100 fps test speeds, canard-delta model (wing area Sw = 242.01 in², span bw = 24.5 in, chord cw = 9.88 in), WAFBC six-component force balance, image-invert tare method, angle of attack swept −4° to 34° in 2° increments, tested at 0° and 10° yaw.

**Approach:** CL = Lift/(q·Sw), CD = Drag/(q·Sw), Cm = Pitch/(q·Sw·cw); a quadratic fit CD = CD0 + K·CL² separated parasitic drag from induced drag.

**Key Results:** CL increased nearly linearly up to about 25° AoA, then rolled off gradually rather than stalling abruptly — consistent with vortex-lift breakdown rather than conventional stall. Higher Reynolds number (100 fps) produced higher CL and lower CD. A 10° yaw angle had negligible effect on lift but increased side force and yawing moment.

**Best CL/CD Summary**

| Condition | Best CL/CD | At AoA |
|---|---|---|
| 75 fps, 0° yaw | 4.21 | 12° |
| 100 fps, 0° yaw | 3.77 | 12° |
| 75 fps, 10° yaw | 3.19 | 12° |
| 100 fps, 10° yaw | 2.67 | 12° |

**Valuable Takeaways** (4 total) cover vortex-lift behavior on delta wings, the influence of Reynolds number on aerodynamic efficiency, the relatively small effect of yaw on lift, and the use of image-invert tare methods to remove balance/support interference from force measurements.

#### Lab 05: Schlieren Imaging and Supersonic Wind Tunnels
**Equipment:** ERAU blowdown supersonic wind tunnel, convergent-divergent nozzle (throat area = 0.765 in², half-angle ≈ 4.8°), 13 static pressure taps (1.5–19.5 in), Schlieren optics.

**Approach:** Nozzle pressure ratio NPR = P0/Pexit; shock strength S = Pafter/Pbefore; choked-flow mass rate computed from isentropic flow theory.

**Key Results:** A normal shock was confirmed between the 9.5 in and 10.5 in tap positions, matching the location visible in the Schlieren image. NPR = 3.932, exceeding the critical value and confirming choked, shocked flow. Shock strength S = 1.614 (a 61.4% pressure jump across the shock). Mass flow rate = 6.10 lbm/s.

**Valuable Takeaways** (4 total) cover the direct correspondence between Schlieren imagery and pressure-tap-derived shock location, the use of NPR to predict choking and shock formation, isentropic-flow-based mass flow calculations, and the broader value of optical flow visualization for validating quantitative measurements.

---

### 5.2 Dynamics & Control Lab (AE 443, Spring 2026)

**Sub-hub description:** "Experimental investigation of dynamic systems and closed-loop control design. Labs cover system identification, controller tuning, and performance evaluation of physical test rigs including motor-driven and electromechanical platforms. Results are compared against simulation models developed in MATLAB and Simulink."

#### Lab 01: Servo Modeling
This lab identified a first-order transfer function model (steady-state gain K and time constant τ) for the Quanser SRV02 servo-motor using a bump test and iterative model validation.

**Approach:** A square-wave voltage (amplitude 1.5V, offset 2.0V, frequency 0.4 Hz) was applied via Simulink's "Monitor & Tune" mode. Steady-state gain K = (yss − y0)/(umax − umin); time constant τ identified at the 63.2% step-response crossing. Multiple (K, τ) pairs were tested in simulation until simulated and measured responses converged.

**Key Results**

| Source | K (rad/s/V) | τ (s) |
|---|---|---|
| Nominal (theoretical) | 1.53 | 0.0253 |
| Bump test | 1.7866 | 0.048 |
| Model validation (best fit) | 1.68 | 0.044 |

The bump test gave Ke,b = (6.051 − 0.691)/(3.5 − 0.5) = 1.787 rad/s/V and τe,b = 1.298 − 1.25 = 0.048s. The nominal model under-predicted steady-state speed and over-predicted response speed due to unmodeled friction and parameter uncertainty in the gear train. The validated model (K = 1.68, τ = 0.044) produced a near-exact overlay with the measured response.

**Valuable Takeaways** (4 total): experimental system identification outperforms purely theoretical modeling; K and τ independently control "how far" and "how fast" the response goes; model validation is inherently iterative; and the lab provided foundational experience with MATLAB/Simulink hardware-in-the-loop testing via QUARC.

#### Lab 02: Flexible Link Modeling
This lab derived equations of motion for the SRV02 rotary flexible link system via the Euler-Lagrange method, identified link stiffness from a free-oscillation test, and validated a 4-state state-space model.

**Approach:** The system Lagrangian L = T − V was formed from the kinetic energy of the servo base and flexible link plus the elastic potential energy of the link spring. Euler-Lagrange equations produced coupled second-order ODEs, rewritten in state-space form with states x = [θ, α, θ̇, α̇]. Link stiffness was identified from a free-oscillation decay test: Ks = Jl·ωn², where Jl = mlLl²/3 (ml = 0.065 kg, Ll = 0.419 m).

**Key Results:** From peak amplitudes O1 = 20.48° at t = 0.244s and O3 = 9.70° at t = 0.924s: Tosc = 0.34s, ωd = 18.48 rad/s, ζ = 0.034, giving ωn = 18.49 rad/s and Ks = 1.30 N·m/rad. Open-loop poles: P1 = 0 (marginally stable), P2,3 = −8.16 ± 22.52i (stable oscillatory), P4 = −24.01 (stable). Simulated and measured servo angle responses agreed closely; the flexible link angle matched the correct oscillation frequency but showed slight amplitude discrepancy from unmodeled structural damping.

**Valuable Takeaways** (4 total): a marginally stable open-loop system (pole at the origin) requires feedback control; structural stiffness can be identified from a simple free-oscillation/logarithmic-decrement test; the state-space A matrix derived from Lagrangian mechanics directly informs stability, controllability, and observability; and the lab connected Lagrangian mechanics, linear systems theory, and hardware validation end-to-end.

#### Lab 03: SRV02 Position Control
This lab designed a PV controller meeting second-order transient specs, demonstrated its ramp-tracking steady-state error, and added an integral term (PIV) to eliminate it.

**Approach:** Target specs tp = 0.20s, PO = 5% mapped to ζ = 0.69, ωn = 21.7 rad/s, giving kp = τωn²/K = 7.82 V/rad and kv = (2ζωnτ − 1)/K = −0.157 V·s/rad. Since PV control makes the position loop Type-1, a ramp input produces a predictable steady-state error ess = R(1 + Kkv)/(Kkp) = 0.214 rad. Adding ki = 38.9 V/(rad·s) upgraded the controller to PIV.

**Key Results**

| Test | tp (s) | PO (%) | ess (rad) |
|---|---|---|---|
| Step sim (PV) | 0.194 | 5.0 | 0 |
| Step impl (PV) | 0.170 | 7.86 | 0.004 |
| Ramp sim (PV) | — | — | 0.213 |
| Ramp impl (PV) | — | — | 0.186 |
| Ramp sim (PIV) | — | — | 0.005 |
| Ramp impl (PIV) | — | — | 0.007 |

The hardware step response (PO = 7.86%) slightly exceeded the 5% design spec due to friction and encoder quantization noise. PIV reduced ramp steady-state error from ~0.19 rad to ~0.007 rad — a 97% reduction from a single integral term.

**Valuable Takeaways** (4 total): transient specs map directly to controller gains via ζ and ωn; the "type number" of a system determines what reference inputs it can track without error (Type 1 vs. Type 2); hardware always differs from simulation, and explaining the gap is a hallmark of competent control engineering; and the lab built proficiency in the full MATLAB/Simulink hardware-in-the-loop workflow.

#### Lab 04: Gyro Modeling and Control
This lab modeled an open-loop gyroscope, designed a PI controller to regulate deflection angle, and compared controlled vs. uncontrolled behavior under disturbance.

**Approach:** The open-loop plant is first order: α(s)/Vm(s) = (K/Gg)/(τs + 1), with K = 1.53 rad/s/V, τ = 0.9s, Gg = 5.20 1/(rad·s). Closing the loop with a PI controller and matching to a standard second-order form (ζ = 1.05, ωn = 3.61 rad/s) gave kp = Gg(2ζωnτ − 1)/K = 19.79 and ki = Ggτωn²/K = 39.86. Experimental open-loop time constant: τexp = 0.87s (vs. theoretical 0.9s).

**Key Results**
- Open-loop: theoretical αss = 8.43° vs. measured peak of only 2.8° (66.8% error) due to unmodeled gyroscopic coupling, friction, and sensor noise.
- Closed-loop tracking: α converged to 1.997° (ess = 0.003° ≈ 0), confirming the PI integral term eliminated steady-state error despite model inaccuracy.
- PI ON, disturbance: motor voltage actively opposed base rotation, holding deflection near 0° (ess = 0°).
- PI OFF, disturbance: deflection reached ±7.4° and took ~20 seconds to passively damp out.
- Routh-Hurwitz: both open-loop (single pole at −1.11) and closed-loop (kp = 19.79, ki = 39.86) configurations are stable.

**Valuable Takeaways** (4 total): passive gyroscopic stability alone is insufficient for precision heading control — active feedback is essential (the operating principle behind gimbal stabilizers and the Hubble Space Telescope's pointing system); a PI controller converts a passive gyroscope into an actively stabilized platform; feedback control can be robust even when the open-loop model has large errors (66.8% in this case); and the lab gave hands-on experience with multi-physics PI design and the Routh-Hurwitz stability criterion.

#### Lab 05: Speed Control
This lab designed and compared a PI controller and a lead compensator for SRV02 motor speed regulation, using both Bode analysis and time-domain step response testing.

**Approach:** The augmented plant Pi(s) = K/[s(τs+1)] was analyzed via Bode plot. Its magnitude rolls off at −20 dB/decade from the origin pole, steepening to −40 dB/decade above ω = 1/τ = 39.4 rad/s. Phase starts at −90° and approaches but never reaches −180°, giving infinite gain margin. Phase margin = 87.8° at the gain crossover of 1.53 rad/s.

**Key Results**

| Controller / Test | tp (s) | PO (%) | ess (rad/s) |
|---|---|---|---|
| PI — simulation | 0.04 | 4.4 | 0 |
| PI — hardware | 0.034 | 23.8 | −3.2×10⁻⁴ |
| Lead — simulation | 0.04 | 2.0 | 0 |
| Lead — hardware | 0.03 | 44.4 | −0.0012 |

Both controllers met simulation specs, with the lead compensator showing marginally lower simulated overshoot (2% vs. 4.4%). On hardware, however, PI overshoot (23.8%) was far more moderate than lead's (44.4%) — the lead compensator's derivative-like action amplified encoder quantization noise into large velocity spikes at step transitions. Measured PI peak-to-peak ripple was 1.16 rad/s vs. a theoretical estimate of 0.525 rad/s.

**Valuable Takeaways** (4 total): simulation performance does not guarantee hardware performance — noise sensitivity invisible in simulation can dominate on real hardware; frequency-domain stability margins (87.8° phase margin) quantify robustness to real-world uncertainty; controller selection must account for the physical system's noise characteristics, not just its theoretical transient response; and the lab completed a full frequency-domain design cycle from Bode analysis through hardware validation.

---

### 5.3 Structures & Instrumentation Lab (AE 417, Fall 2025)

**Sub-hub description:** "Hands-on structural testing and sensor-based data acquisition covering material characterization, load-deflection behavior, and failure analysis. Labs include strain gauge instrumentation, calibration procedures, and experimental validation of structural models under static and dynamic loading conditions."

#### Lab 01: Honeycomb Compression Test
Aluminum honeycomb core was tested in out-of-plane compression per ASTM D 7336/D 7336M-07, using a Tinius Olsen 150ST universal testing machine, to characterize its three-stage crush behavior (linear elastic, progressive cell-wall buckling plateau, and densification).

**Approach:** Four teams each measured five nominally identical specimens (foil thickness, cell size, dimensions, mass); the specimen closest to the cross-team mean was selected for testing to minimize variability. Stress was computed as force divided by cross-sectional area, strain as displacement divided by original height. Energy absorbed was the area under the stress-strain curve, computed by splitting the curve into two geometric regions. Post-test microscopy documented cell-wall buckling at multiple magnifications.

**Key Results**
- Peak stress σpeak = 4.5 MPa (653 psi), crush stress σcrush = 1.87 MPa (270 psi) — close to manufacturer specs of 620 psi peak / 300 psi crush for the target 5056 alloy at 4.3 pcf density.
- Energy absorbed ≈ 798.9 MPa·cm³ over the full crush stroke (specimen volume 492.8 cm³).
- Specimen density 4.6 pcf, cell size 6.11 mm — identified as a 5056 Alloy Hexagonal Aluminum Honeycomb, designation ¼-5056-0.002.
- Microscopy confirmed progressive cell-wall buckling and folding; even as sections failed, buckled walls reinforced adjacent sections, explaining the near-constant plateau force.

**Microscopy Findings:** Close-up images showed bent, buckled cell walls with periodic fold lines — the signature of progressive axial crushing in thin-walled metallic structures. Top-view images revealed collapsed hexagonal geometry with cell walls folded inward against neighbors rather than fracturing, consistent with ductile aluminum behavior.

**Valuable Takeaways** (4 total): the flat plateau on the stress-strain curve represents the sustained energy absorption that makes honeycomb cores irreplaceable in crash structures (floor panels, helicopter seats, crumple zones); the three-stage crush curve is itself a design tool for selecting density and cell size; standardized testing (ASTM D 7336) ensures results are comparable to manufacturer data; and the lab provided hands-on experience with universal testing machines, multi-team specimen selection, and materials microscopy.

#### Lab 02: Strain Gages
This lab covered the full strain-gage installation workflow on an Al 6061-T6511 beam and a Nomex/CFRP sandwich beam, deriving Young's modulus for each from bending tests.

**Approach:** Surfaces were degreased, sanded (320/400 grit), conditioned with M-Prep Conditioner A, and bonded with M-Bond 200 adhesive per Vishay bulletin B-127-14. A 120Ω foil strain gage (GF = 2) was installed and connected via banana plug to a digital multimeter. Beams were cantilevered ("diving board" configuration) and loaded with 1, 2, and 3 kg masses. Strain ε = (ΔR/R)/GF; bending stress σ = My/I (aluminum) or σ = M/(h·tf·b) (sandwich beam); Young's modulus E = σ/ε.

**Key Results**
- Aluminum beam resistance changed by ~0.08Ω per kg of load in both tension and compression — nearly symmetric responses validating correct gage installation.
- E_Al = 84 GPa vs. handbook value of 69 GPa for 6061-T651 (17.9% error), attributed to minor gage misalignment and surface-prep variability.
- E_honeycomb = 74 GPa for the Nomex/CFRP sandwich beam — within the expected 70–120 GPa range for woven carbon-fiber facing skins.
- At identical loads, the honeycomb beam strained less than the aluminum beam, confirming higher effective bending stiffness per unit cross-section.

**Valuable Takeaways** (4 total): strain gage installation is a high-precision craft where surface prep, alignment, and bonding all introduce error (the 17.9% modulus error directly demonstrates this); sandwich beams demonstrate why composite structures are so weight-efficient; symmetric tension/compression responses are the signature of proper gage installation; and the lab built practical proficiency in the full strain-gage workflow — surface prep, bonding, soldering, Wheatstone bridge measurement, and MATLAB analysis.

#### Lab 03: Aluminum and Composite Tensile Testing
Three materials — Al-2024-T351, GFRP, and CFRP — were pulled to fracture using a Tinius Olsen 150ST with an LVDT extensometer, to quantify the strength/stiffness/weight trade-offs between aluminum and composites.

**Approach:** Each rod was sanded, cleaned with acetone, and fitted with 6061-T6 aluminum gripping tubes. Young's modulus was averaged from five points in the elastic region of the stress-strain curve; ultimate stress was the maximum recorded value; aluminum yield stress was found via the 0.2% offset method. For CFRP, the stress-strain method underestimated E by ~49%, so an independent estimate was obtained via the rule of mixtures (Ec = EmVm + EfVf), with fiber volume fraction Vf measured from polished cross-section microscopy.

**Key Results**
- Al-2024-T351: E = 693 MPa (note: the page text uses MPa for these values), σu = 497 MPa, σy = 361 MPa — percent differences vs. handbook of 1.3%, 1.4%, and 2.7%, confirming reliable test execution for ductile metals.
- GFRP: E = 373.9 MPa, σu = 469 MPa — only 0.4% error vs. handbook E.
- CFRP stress-strain E = 1,118.6 MPa showed ~49% error vs. handbook; rule-of-mixtures E = 126,984 MPa (Vf ≈ 55%) agreed within 6%, confirming the stress-strain method cannot capture CFRP modulus accurately and metallography-based analysis is required.
- Strength-to-weight ratios: Al-2024 = 178,777, GFRP = 250,482, CFRP = 717,297 MPa·mm³/g — CFRP outperforms aluminum by roughly 4× on this metric.

**Valuable Takeaways** (4 total): no single test method works for all materials — the stress-strain approach worked for aluminum and GFRP but failed for CFRP, requiring rule-of-mixtures plus microstructural analysis; CFRP's specific-strength advantage (717,297 vs. 178,777 for aluminum) is the driving force behind composite-heavy aircraft like the 787 and A350; brittle (GFRP/CFRP) vs. ductile (Al-2024) failure modes drive damage-tolerance and inspection requirements; and the lab covered the complete tensile-test workflow including specimen prep, extensometer use, and metallography cross-validation.

#### Lab 04: Methods for Nondestructive Evaluation
Five complementary NDE techniques were applied to real aerospace hardware: visual inspection (borescope), thermography, radiography, liquid penetrant, and ultrasonics.

**Visual Inspection (Borescope):** A Ridgid Micro CA-150 borescope was inserted into a metallic aircraft wing airfoil section, revealing visible scratches and cracks near the rivet holes — the type of stress-concentration-driven fatigue damage that motivates riveted-structure inspection intervals.

**Thermography:** A FLIR T440 camera imaged a paper subject before and after applying cold water droplets and a hand imprint, resolving temperature differences at the ±0.1°C level (cold water at 22.2°C against a 26.1°C background, hand imprint at 26.6°C), demonstrating how thermal gradients reveal disbonds and material non-uniformities.

**Radiography:** X-ray imaging of a welded aluminum plate revealed weld bead geometry and internal profile. An Apple Watch X-ray illustrated how overlapping components complicate defect discrimination — a known limitation of 2D projection radiography.

**Liquid Penetrant:** Fluorescent dye applied to an aluminum pressure vessel, after a ~10-minute dwell and developer application, revealed at least eight discrete damage indications under UV light — scratches and cracks completely invisible under normal white light.

**Ultrasonics:** A 5 MHz piezoelectric transducer coupled to stepped aluminum calibration blocks tracked thickness from ~24.96 mm down to ~3.32 mm, with echo spacing decreasing proportionally and ledge edges producing slight amplitude reduction from scattering — the same principle airlines use to monitor skin corrosion from the outer surface.

**Valuable Takeaways** (4 total): no single NDE method catches everything — professional inspection programs layer multiple techniques, just as licensed A&P mechanics do; liquid penetrant reveals defects invisible to the naked eye, justifying its mandate in airframe certification; ultrasonic thickness gauging is the industry standard for corrosion monitoring; and the lab gave hands-on exposure to five FAA-relevant NDE methods applicable to structural integrity, QA, and MRO roles.

#### Lab 05: Vibration Testing of Beams
Resonance frequencies and mode shapes of two aluminum beams (short, 761 mm, and long, 1275 mm, both Al-6061-T651) were measured using an electrodynamic shaker, motivated by the principle of resonance that destroyed the Tacoma Narrows Bridge and drives flutter clearance testing.

**Approach:** Each beam was clamped to an electrodynamic shaker; sine generator frequency was swept from zero until large-amplitude oscillation indicated resonance. Resonance was captured simultaneously via three instruments: the sine generator readout (FSSG), a digital oscilloscope reading the ICP accelerometer (Fpiezo), and a digital stroboscope flash rate that visually "froze" the beam (Fstrobe). Nodal positions were measured with a ruler under strobe illumination. Theoretical frequencies were computed from the Euler-Bernoulli beam equation using eigenvalues λL = 1.88, 4.69, 7.85, and 11.00 for modes 1–4.

**Key Results**
- Short beam (761 mm) frequencies: Mode 1 = 6.5 Hz, Mode 2 = 40.1 Hz, Mode 3 = 111.5 Hz.
- Long beam (1275 mm) frequencies: Mode 1 = 2.4 Hz, Mode 2 = 14.5 Hz, Mode 3 = 40.9 Hz, Mode 4 = 80.1 Hz.
- Percent difference from theory: 9.5–11.6% for the short beam, 5.3–8.0% for the long beam — longer beams behave more like ideal Euler-Bernoulli beams since clamping/root effects are proportionally smaller.
- At Mode 1 of the short beam, FSSG and Fpiezo differed by 13.6% (the piezo oscilloscope struggles below ~10 Hz); all three methods converged to <3% agreement at higher modes.
- Nodal positions matched theoretical predictions within 3.32% for both beams across all modes.

**Lab footage:** two videos showing the beams vibrating at resonance and stroboscope-based mode shape identification.

**Valuable Takeaways** (4 total): resonance frequencies can be identified experimentally with high confidence (validating ground vibration tests performed before any aircraft's first flight); measurement instrument selection matters at low frequencies (the piezo's 13.6% error at Mode 1); resonance avoidance directly drives structural design decisions (avoiding overlap with engine RPM, blade-passing frequency, etc.); and the lab built proficiency with electrodynamic shakers, ICP accelerometers, stroboscopes, and oscilloscopes.

#### Lab 06: Rocket Thrust Measurement
A strain-gage cantilever beam load cell was built and calibrated, then used to record thrust-time profiles for five Estes solid rocket motors (A8-3, B4-4, C6-5, C11-0, E16-4) and compare them against manufacturer specifications.

**Approach:** A half-bridge strain-gage load cell on an aluminum cantilever beam was statically calibrated using 1, 2, and 3 kg masses, producing the linear calibration equation F = 32.931 × V − 40.732 (N). This equation converted all voltage-time recordings to thrust-time curves. Total impulse was computed via trapezoidal integration; average thrust as It/tb. Each motor was mounted nozzle-down with a color-coded igniter plug, and data acquisition began ~3 seconds before ignition to capture a baseline.

**Live Firing Footage:** A video shows a solid rocket motor firing during the outdoor test session, with the ignition spike, thrust plateau, and burnout clearly visible.

**Key Results — C6-5 Comparison vs. Estes Specs**

| Parameter | Measured | Estes Spec | % Diff |
|---|---|---|---|
| Peak thrust (N) | 13.55 | 15.3 | 12.1% |
| Burn time (s) | 2.1 | 1.6 | 27.0% |
| Total impulse (N·s) | 8.53 | 10.0 | 15.9% |
| Delay time (s) | 4.8 | 5.0 | 4.1% |

The 27% burn-time deviation was the largest discrepancy, attributed to ignition delays, beam damping from the oil-bath dashpot, and manufacturing tolerances in hobby-grade motors. Higher-impulse motors (C11-0, E16-4) produced peak thrusts of ~30 N with sharp ignition spikes.

All five motors showed the characteristic black-powder thrust profile: a sharp ignition spike, sustained plateau, and abrupt burnout — visible in both the voltage-vs-time and thrust-vs-time plots for each motor.

**Valuable Takeaways** (4 total): static calibration is the foundation of any force measurement system — a poorly calibrated load cell produces precise-looking but systematically wrong data; real motors deviate from specifications in ways that matter (a 27% burn-time error means a vehicle reaches altitude 27% later than planned, motivating test-before-fly requirements from CubeSat kick stages to large SRBs); the thrust curve encodes impulse (area), vehicle dynamics (shape), and structural loads (peak); and the lab gave end-to-end instrumentation experience from calibration through live-fire data acquisition to propulsion parameter extraction.

---

## 6. Highlights

**Header:** "Highlights" — "Conferences attended, research presented, and experiences beyond the classroom"

### 1. NCUR 2026 — "Turbine Aerodynamics and Performance Characterization"
**National Conference on Undergraduate Research, Richmond, Virginia, May 2026** (with K. Satvaldy & V. Shi)

Presented original undergraduate research at one of the largest undergraduate research conferences in the United States, hosted by Virginia Commonwealth University. Represented ERAU among a university-wide delegation, sharing work on a Python-based computational framework for turbine blade aerodynamics analysis and multi-point pressure characterization.

### 2. FURC — "Turbine Aerodynamics and Performance Characterization"
**Florida Undergraduate Research Conference, University of North Florida, Jacksonville, Spring 2026** (with K. Satvaldy & V. Shi)

Presented at the Florida state-level undergraduate research conference hosted at UNF — the first public presentation of this research before advancing to the national stage at NCUR. Shared findings on computational turbine design tools with students and faculty researchers from across Florida.

### 3. ERAU Math Department Student Worker — "Mathematical Methods for Engineering and Physics" Online Textbook
**Embry-Riddle Aeronautical University, Mathematics Department, Daytona Beach, FL, Aug 2025 – May 2026**

Assisted a Mathematics Department professor in developing an online textbook covering vector calculus, series, and differential equations. Wrote and formatted chapters in LaTeX, refined explanations, structured examples, and ensured mathematical accuracy and clarity to produce a professional, accessible learning resource for future engineering and physics students.

### 4. Boeing Career Mentorship Program — Class of 2025
**Boeing, Mar 2025 – Oct 2025**

Selected as a mentee for the 2025 Boeing Career Mentorship Program cohort. Participated in resume reviews, mock interviews, professional development sessions, and technical mentoring with Boeing engineers to prepare for internships and full-time aerospace career pathways.

### 5. Honeywell Aerospace Mentorship — 2024 Cohort
**Honeywell Aerospace, Sep 2024 – Mar 2025**

Selected for the 2024 Honeywell Aerospace Mentorship cohort. Participated in professional development sessions and technical mentoring with Honeywell engineers to prepare for internships and full-time aerospace career pathways.

---

## 7. Resume

**Header:** "Resume" — "Download or view tailored resumes for Aerospace and Software Engineering opportunities"

### Aerospace Engineering Resume
"Focused on aircraft systems, propulsion, structural analysis, and engineering leadership."
File: `AnurananBharadwaj_RESUME_AE.pdf`

### Software Engineering Resume
"Highlights experience in Java, C#, Python, full-stack development, and project-based software solutions."
File: `AnurananBharadwaj_RESUME_SE.pdf`

---

## 8. Contact

**Header:** "Contact Me" — "I'm open to collaboration and opportunities in aerospace and software engineering. Feel free to reach out!"

- **Email:** bharadwajanuranan@gmail.com
- **Phone (U.S.):** +1 (215) 397-5806
- **Phone (India):** +91 76370 13316
- **LinkedIn:** [linkedin.com/in/anuranan-bharadwaj](https://linkedin.com/in/anuranan-bharadwaj)
- **GitHub:** [github.com/anuranan10](https://github.com/anuranan10)

The same phone, email, LinkedIn, and GitHub links also appear in the footer of every page on the site.
