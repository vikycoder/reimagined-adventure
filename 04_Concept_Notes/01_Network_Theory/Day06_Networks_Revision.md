# Day 6 — Networks Revision: PYQ Map, Master Formula Sheet and Mock Test

**Covers:** everything from Days 1–5, tied together: what eight years of papers actually ask · the map of all 43 Networks questions · a cold re-solve list · one master formula sheet · a method chooser · exam-hall rules · the mixed concept check and the timed mock test
**Matches:** Day 6 of `03_Study_Plans/20_Day_Plan_Networks_Signals_Control.md` ("Revision + test … a timed 25–30 question set. Finish the Networks formula sheet")
**Time:** about 4½ hours
**Companions:** `Day06_Conceptual_Questions.md` (20 mixed questions) and `Day06_Mock_Test.md` (25 questions, 35 marks, 60 minutes)

Every number in the two question files is re-checked by `tools/verify_day06.py` (circuit answers come from a circuit solver or an ODE integration, not from the closed forms in the solutions). The map below is built by `tools/build_pyq_map.py` from the Day 1–5 notes and the official answer keys.

## How to use Day 6

| Step | What | Time |
|---|---|---|
| 1 | Read §1–§2: what the papers ask, and the map of all 43 questions | 20 min |
| 2 | **Cold re-solve** the 13 questions in §3 against the clock (no notes). Whatever you cannot finish in time goes on the error list | 45 min |
| 3 | Copy the master formula sheet (§4) **by hand** onto two pages. Copying by hand is the revision | 30 min |
| 4 | Read §5 (method chooser) and §6 (exam-hall rules) | 15 min |
| 5 | Take the 20 mixed conceptual questions | 40 min |
| 6 | Take the **timed mock test** (60 minutes, closed book) | 60 min |
| 7 | Mark it, fill the error log, redo every miss with the solution covered | 50 min |
| 8 | Skim the "mistakes that cost marks" checklist at the end of each of the Day 1 to Day 5 notes | 20 min |

---

## 1. What eight years of papers say

I read all eight papers (2019–2026) and kept the questions that are about circuits and network theory. Questions in other subjects that merely contain a circuit (op-amps, MOS, diodes, transmission lines) are **not** counted, and neither are the few Signals or Control questions that use an RLC circuit as a vehicle (for example 2021 Q33 on controllability).

| Year | Networks questions (number, marks) | Questions | Marks |
|---|---|---|---|
| 2019 | Q4 (1), Q30 (2), Q41 (2), Q52 (2) | 4 | 7 |
| 2020 | Q9 (1), Q15 (1), Q16 (1), Q28 (2), Q30 (2), Q46 (2) | 6 | 9 |
| 2021 | Q18 (1), Q19 (1), Q28 (2), Q29 (2), Q38 (2), Q47 (2) | 6 | 10 |
| 2022 | Q13 (1), Q14 (1), Q24 (1), Q38 (2), Q39 (2), Q54 (2) | 6 | 9 |
| 2023 | Q18 (1), Q32 (1), Q33 (1), Q35 (1), Q44 (2), Q62 (2) | 6 | 8 |
| 2024 | Q31 (1), Q32 (1), Q35 (1), Q49 (2), Q60 (2), Q62 (2) | 6 | 9 |
| 2025 | Q19 (1), Q20 (1), Q39 (2), Q40 (2) | 4 | 6 |
| 2026 | Q23 (1), Q30 (1), Q31 (1), Q39 (2), Q51 (2) | 5 | 7 |
| **Total** | | **43** | **65** |

| Topic (day) | Questions | Marks | Share of the marks |
|---|---|---|---|
| Circuit analysis (Day 1) | 8 | 8 | 12 % |
| Network theorems (Day 2) | 4 | 6 | 9 % |
| Transients (Day 3) | 13 | 22 | 34 % |
| AC steady state and resonance (Day 4) | 11 | 17 | 26 % |
| Two-port networks (Day 5) | 7 | 12 | 18 % |



What the numbers say:

- **4 to 6 Networks questions per paper, 6 to 10 marks** (mean 8.1 marks, about 8 % of the paper). They are all one- and two-mark questions; there is no three-mark Networks question.
- **Transients and AC steady state are 60 % of the marks** (22 + 17 of 65). If you have to prioritise, this is where.
- **Every year has a two-port question** (nine in total, 2019–2026), and the two-port topic is easy to master because the question types repeat (measure a parameter, convert, terminate).
- **Dependent sources** appear in 5 of the 43 questions (2021 Q29, 2021 Q38, 2024 Q31, 2024 Q60, 2024 Q62). If you can handle them, you take marks others lose.
- **21 of the 43 are numerical-answer (NAT) questions** and the other 22 are MCQ. There is no MSQ among them. NAT means no guessing and no options to check against, so unit and arithmetic discipline matters.
- I found **no question on mutual inductance or coupled inductors** in these eight papers, and the GATE 2027 EC syllabus does not list it.

---

## 2. The map of all 43 questions

Each row says where the question is solved. **Try each one from the paper first** (`02_Previous_Year_Papers/<year>/`).

### Day 1: Circuit analysis

| Question | Marks | Official answer | Concept it tests | Solved in |
|---|---|---|---|---|
| 2021 Q18 (NAT) | 1 | 0.5 A | Merge wire-connected nodes; parallel resistors; current source | [Day 1 §12](Day01_Circuit_Analysis_Fundamentals.md) |
| 2021 Q19 (NAT) | 1 | 1.0 V | Nodal analysis with two current sources | [Day 1 §12](Day01_Circuit_Analysis_Fundamentals.md) |
| 2022 Q13 (MCQ) | 1 | B: 0.75 × 10⁻³ A | Resistor in series with a current source | [Day 1 §12](Day01_Circuit_Analysis_Fundamentals.md) |
| 2022 Q14 (MCQ) | 1 | B: 0 A | One wire between separate networks | [Day 1 §12](Day01_Circuit_Analysis_Fundamentals.md) |
| 2023 Q32 (NAT) | 1 | 1.30 to 1.40 mA | Source transformation + nodal | [Day 1 §12](Day01_Circuit_Analysis_Fundamentals.md) |
| 2024 Q31 (NAT) | 1 | 2 mA | Dependent source (CCVS) | [Day 1 §12](Day01_Circuit_Analysis_Fundamentals.md) |
| 2025 Q19 (MCQ) | 1 | A: 20/3 V | Use only the part of the circuit you need | [Day 1 §12](Day01_Circuit_Analysis_Fundamentals.md) |
| 2026 Q30 (NAT) | 1 | 0.95 to 1.05 V | Symmetry and KCL; the battery drops out | [Day 1 §12](Day01_Circuit_Analysis_Fundamentals.md) |

### Day 2: Network theorems

| Question | Marks | Official answer | Concept it tests | Solved in |
|---|---|---|---|---|
| 2019 Q4 (MCQ) | 1 | B: 1 A | Reciprocity: the circuit values are decoys | [Day 2 §9](Day02_Network_Theorems.md) |
| 2020 Q9 (MCQ) | 1 | C: 3.6 V | Thevenin voltage by source transformation | [Day 2 §9](Day02_Network_Theorems.md) |
| 2022 Q54 (NAT) | 2 | 3.9 to 4.1 mA | A Thevenin line read from a measurement, then a load with a battery | [Day 2 §9](Day02_Network_Theorems.md) |
| 2024 Q62 (NAT) | 2 | 2.5 Ω | Maximum power when a dependent source is present: test source | [Day 2 §9](Day02_Network_Theorems.md) |

### Day 3: Transients

| Question | Marks | Official answer | Concept it tests | Solved in |
|---|---|---|---|---|
| 2019 Q41 (NAT) | 2 | 0.23 to 0.27 A | RC circuit with a *time-varying* resistor | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2019 Q52 (NAT) | 2 | 3.2 to 3.4 V | RC charging through an ideal diode: the capacitor holds | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2020 Q30 (MCQ) | 2 | A | State equations of an RLC circuit | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2021 Q28 (MCQ) | 2 | C: −3 V/s | `dv/dt` at 0⁺ by the 0⁺ method | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2021 Q38 (NAT) | 2 | 0.132 to 0.146 ms | First-order circuit with a dependent source | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2021 Q47 (NAT) | 2 | 1.40 to 1.45 A | Underdamped step response: the overshoot | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2023 Q35 (NAT) | 1 | 4 V | Opening a switch in an RL circuit | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2023 Q44 (MCQ) | 2 | B: −1 A | `i_C(0⁺)` after two switches operate | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2023 Q62 (NAT) | 2 | 8.30 to 8.34 µs | Acquisition time for N-bit accuracy | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2024 Q32 (NAT) | 1 | 0.75 s | Time constant from the resistance seen by L | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2024 Q35 (NAT) | 1 | 0.250 mJ | Energy in a Zener while a capacitor discharges | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2024 Q49 (MCQ) | 2 | D | Schmitt trigger and an op-amp integrator with an inductor | [Day 3 §8](Day03_Transient_Analysis.md) |
| 2026 Q23 (MCQ) | 1 | A | An impulse of current is an initial condition | [Day 3 §8](Day03_Transient_Analysis.md) |

### Day 4: AC steady state and resonance

| Question | Marks | Official answer | Concept it tests | Solved in |
|---|---|---|---|---|
| 2019 Q30 (MCQ) | 2 | C | Phasor solution of a delta of R with a star of C | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2020 Q16 (NAT) | 1 | 2.80 to 2.85 H | Recover `L` from the phase of an RL current | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2020 Q28 (MCQ) | 2 | C | Phasor network with two sources: node choice makes it easy | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2022 Q24 (MCQ) | 1 | C | Conduction and displacement current in a series loop | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2022 Q38 (MCQ) | 2 | A | Impedance locus of `R₁ + (R₂ ∥ C)` | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2022 Q39 (MCQ) | 2 | B | Lag or lead from a waveform | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2023 Q18 (MCQ) | 1 | D | `Q = ω₀L/R` of a series RLC | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2025 Q20 (MCQ) | 1 | A | Phasor currents from admittances | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2025 Q39 (MCQ) | 2 | A | Rms meter readings and resonance | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2026 Q31 (NAT) | 1 | 71.50 to 72.50 mW | An ideal source across a resonant tank | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |
| 2026 Q39 (MCQ) | 2 | B | Orthogonal branch currents | [Day 4 §8](Day04_Sinusoidal_Steady_State_and_Resonance.md) |

### Day 5: Two-port networks

| Question | Marks | Official answer | Concept it tests | Solved in |
|---|---|---|---|---|
| 2020 Q15 (NAT) | 1 | 48 Ω | Z-matrix: load for maximum power at port 2 | [Day 5 §7](Day05_Two_Port_Networks.md) |
| 2020 Q46 (NAT) | 2 | 0.80 | S₂₁ of an ideal 2:1 transformer | [Day 5 §7](Day05_Two_Port_Networks.md) |
| 2021 Q29 (MCQ) | 2 | C | Y-parameters of a circuit with a dependent source | [Day 5 §7](Day05_Two_Port_Networks.md) |
| 2023 Q33 (NAT) | 1 | 80 Ω | Y-matrix: load for maximum power at port 2 | [Day 5 §7](Day05_Two_Port_Networks.md) |
| 2024 Q60 (NAT) | 2 | 1.5 S | `y₂₁` with a dependent source | [Day 5 §7](Day05_Two_Port_Networks.md) |
| 2025 Q40 (MCQ) | 2 | A | Z-parameters of a resistive ladder | [Day 5 §7](Day05_Two_Port_Networks.md) |
| 2026 Q51 (MCQ) | 2 | D | ABCD parameters of a T network | [Day 5 §7](Day05_Two_Port_Networks.md) |

Cross-references: 2019 Q4 and 2022 Q54 are two-port questions too (reciprocity and a measured Thevenin line); they are solved in Day 2 and referred to again in Day 5.

---

## 3. Cold re-solve list (22 marks, 40 minutes)

At GATE's pace (180 minutes for 100 marks, that is 1.8 minutes per mark) these 13 questions take about 40 minutes. Do them **without** looking at the notes. They were chosen to cover every skill in the map.

| # | Question | Marks | Skill | Notes |
|---|---|---|---|---|
| 1 | 2024 Q31 | 1 | dependent source in a node equation | Day 1 |
| 2 | 2026 Q30 | 1 | symmetry and KCL | Day 1 |
| 3 | 2024 Q62 | 2 | maximum power with a dependent source (test source) | Day 2 |
| 4 | 2021 Q28 | 2 | `dv/dt` at `0⁺` | Day 3 |
| 5 | 2023 Q44 | 2 | `i_C(0⁺)` after two switches | Day 3 |
| 6 | 2021 Q47 | 2 | underdamped step response, overshoot | Day 3 |
| 7 | 2019 Q41 | 2 | time-varying resistor | Day 3 |
| 8 | 2020 Q28 | 2 | phasor network, choose the node well | Day 4 |
| 9 | 2022 Q38 | 2 | impedance locus | Day 4 |
| 10 | 2026 Q31 | 1 | ideal source across a resonant tank | Day 4 |
| 11 | 2020 Q15 | 1 | Z-parameters, maximum power at port 2 | Day 5 |
| 12 | 2021 Q29 | 2 | Y-parameters with a dependent source | Day 5 |
| 13 | 2025 Q40 | 2 | Z-parameters of a ladder (cascade) | Day 5 |

For each one you could not finish in the time: write the **reason** (idea missing, formula forgotten, sign or unit slip, arithmetic) in the error log of the mock test.

---

## 4. The master formula sheet (copy this by hand)

### A. Circuit analysis (Day 1)

```
KCL: Σ i_out = 0 (node or any closed surface)       KVL: Σ v = 0 (loop)
b = n + m − 1          independent KCL: n−1          independent KVL: b−n+1

PSC: current into + terminal → p = v·i is ABSORBED.   Σ p_absorbed = 0

R_series = ΣR      R_parallel = 1/Σ(1/R)     2 in parallel: R1R2/(R1+R2)
V-divider: V_R1 = V·R1/(R1+R2)      I-divider: I_R1 = I·R2/(R1+R2)

NODAL:   G·V = I_in           diag = ΣG at node;  off-diag = −G between;  RHS = source current INTO node
         floating V-source → supernode: ONE KCL + constraint (V_a − V_b = E)
MESH:    R·I = V_rise         diag = ΣR in mesh;  off-diag = −shared R;   RHS = source voltage RISE (all CW)
         shared I-source → supermesh: outer-loop KVL + constraint (I_a − I_b = I_s)
Dependent source: write as independent, add control-variable equation, move to LHS.
Self-controlled VCCS (i = g·v) = resistor 1/g;  self-controlled CCVS (v = r·i) = resistor r.

Choose:  nodal unknowns ≈ (n−1) − #V-sources ;  mesh unknowns ≈ m − #I-sources

SOURCE TRANSFORMATION:  Vs in series with R  ⇔  I = Vs/R in parallel with R
   (arrow toward the + end).  Not for ideal sources.  Keep the element you are asked about.
   R in series with ideal I-source: irrelevant to the rest.   R in parallel with ideal V-source: irrelevant to the rest.

Δ → Y:  R1 = Rb·Rc/S, R2 = Rc·Ra/S, R3 = Ra·Rb/S       (S = Ra+Rb+Rc)
Y → Δ:  Ra = (R1R2+R2R3+R3R1)/R1 (opposite terminal 1), etc.      Balanced: R_Y = R_Δ/3
Balanced bridge R1/R2 = R3/R4 → middle arm carries no current.
```

### B. Network theorems (Day 2)

```
LINEARITY      y = Σ k_i·s_i  (no constant).  Power is NOT linear.

SUPERPOSITION  one independent source at a time; V → short, I → open; KEEP dependent sources.
               different frequencies → add in the TIME domain.

THEVENIN       V_th = V_oc (load removed)        R_th = V_oc / I_sc        R_th = v_t / i_t  (test source, independent sources off)
NORTON         I_N = I_sc    R_N = R_th    V_th = I_N·R_th        ideal V source: no Norton;  ideal I source: no Thevenin
MILLMAN        V_node = (Σ V_k/R_k + Σ I_k) / Σ(1/R_k)

MAX POWER      R_L = R_th  →  P_max = V_th²/(4R_th),  v_L = V_th/2,  efficiency = 50%.   P/P_max = 4x/(1+x)², x = R_L/R_th
               R_th variable, R_L fixed  →  smallest R_th (zero) is best.
               load = R_f (fixed) + R_v:   max in R_v  →  R_v = R_th + R_f.
               AC: Z_L = Z_th*;   only R_L adjustable: R_L = √(R_th² + (X_th+X_L)²);   only |Z_L|: |Z_L| = |Z_th|

RECIPROCITY    linear + bilateral + no dependent sources:  y₁₂ = y₂₁,  z₁₂ = z₂₁.
               V at port 1 → short-circuit I at port 2  =  V at port 2 → short-circuit I at port 1.
               I at port 1 → open-circuit V at port 2   =  I at port 2 → open-circuit V at port 1.
               reciprocal ≠ symmetric.

UNIT-OUTPUT    assume the output, work back to the source, scale.
```

### C. Transients (Day 3)

```
CONTINUITY       v_C and i_L continuous; i_C, v_L, i_R, v_R may jump.   Impulse: ΔV = q/C,  ΔI = Φ/L.
0+ MODEL         C → source v_C(0-)  (short if 0 V);   L → source i_L(0-)  (open if 0 A).   dv/dt = i_C/C,  di/dt = v_L/L.
DC (t→∞, 0-)     C open, L short.

FIRST ORDER      x(t) = x(∞) + [x(0+) − x(∞)]·e^(−t/τ)     τ = R_th·C  or  L/R_th  (R_th seen by the element AFTER switching)
                 63.2% at τ, 95% at 3τ, 99.3% at 5τ;  t_half = 0.693τ;  t = τ·ln[(x0−x∞)/(x−x∞)];  N-bit: t = N·τ·ln2
                 charging C through R from a DC source: energy lost in R = ½CV² (independent of R)
TWO CAPACITORS   V = (C1V1 + C2V2)/(C1+C2);   energy lost = ½·(V1−V2)²·C1C2/(C1+C2)   (independent of R)
SINUSOID ON (RL) i = (Vm/|Z|)[sin(ωt+θ−φ) − sin(θ−φ)e^(−t/τ)],  no transient if θ = φ

SECOND ORDER     s² + 2αs + ω0² = 0,  ω0 = 1/√(LC)
                 series: α = R/2L, ζ = (R/2)√(C/L), R_crit = 2√(L/C)      parallel: α = 1/(2RC), ζ = (1/2R)√(L/C), R_crit = ½√(L/C)
                 ζ>1 over (real roots) | ζ=1 critical | ζ<1 under: ω_d = √(ω0²−α²), %OS = 100·e^(−πζ/√(1−ζ²)), t_p = π/ω_d, t_settle(2%) ≈ 4/α
                 larger R: series → more damped;  parallel → less damped.   Q = 1/(2ζ)
STATE            ẋ = Ax + Bu,  x = [v_C, i_L];  eigenvalues of A = roots of the characteristic equation

LAPLACE          L → sL + source L·i(0-) (aids i);   C → 1/(sC) + source v(0-)/s;   f(0+) = lim sF(s);   f(∞) = lim s→0 sF(s) (LHP poles only)
                 series RLC: V_C/V_s = 1/(LC s² + RC s + 1);   qδ(t) into C  ≡  initial voltage + q/C
```

### D. AC steady state and resonance (Day 4)

```
PHASOR        A cos(ωt+φ) ↔ A∠φ (peak),  sin → subtract 90°;   d/dt ↔ jω,  ∫ ↔ 1/jω.     one frequency only.
IMPEDANCE     Z_R = R,  Z_L = jωL,  Z_C = 1/(jωC) = −j/(ωC);   Y_C = jωC,  Y_L = −j/(ωL).   I lags V in L, leads V in C.

POWER (rms)   S = V I* = P + jQ;   P = VI cos φ = I²R;   Q = VI sin φ = I²X;   |S| = VI = √(P²+Q²);   pf = cos φ = P/|S|
              inductive: lagging, Q > 0;  capacitive: leading, Q < 0.   Σ S = 0 (P and Q separately); |S| does NOT add.
PF CORRECTION Q_C = P(tan φ1 − tan φ2),   C = Q_C/(ω V²);   P unchanged, line current falls.
MAX POWER     R_L, X_L both free: Z_L = Z_th*,  P = V²/(4R_th);   X_L fixed: R_L = √(R_th² + (X_th+X_L)²);   |Z_L| only: |Z_L| = |Z_th|.
NON-SINUSOIDAL  I_rms = √(I_0² + ½ΣI_k²);  P only from same-frequency pairs;  meters read rms.

SERIES RLC    ω0 = 1/√(LC);  Q = ω0L/R = 1/(ω0CR) = (1/R)√(L/C);  BW = ω0/Q = R/L;  |Z|min = R;  V_L = V_C = QV
              ω1,2 = ω0[√(1+1/(4Q²)) ∓ 1/(2Q)];  ω2 − ω1 = BW;  ω0 = √(ω1ω2);  |I| = I_max/√2 and phase ±45° at ω1, ω2
              |I|/I_max = 1/√(1 + Q²(x − 1/x)²),  x = ω/ω0
PARALLEL RLC  same ω0;  Q = R/(ω0L) = ω0RC;  BW = 1/(RC);  |Z|max = R;  I_L = I_C = QI_s;   source current (voltage source) is MINIMUM at resonance
TANK (coil R_L)  unity pf: ω_r = √(1/LC − R_L²/L²) (needs R_L < √(L/C));  Z_d = L/(C R_L) = Q²R_L;  max |Z| and 1/√(LC) are slightly different
LOCI          series R + jX: vertical line;  R ∥ C: semicircle of diameter R below the axis;  R₁ + (R₂ ∥ C): from R₁+R₂ (ω=0) to R₁ (ω=∞), diameter R₂
```

### E. Two-port networks (Day 5)

```
PORT CONVENTION  I1, I2 INTO the network;  load on port 2:  V2 = −Z_L·I2;  load current = −I2.
SETS             Z: V = Z·I (other port OPEN)   Y: I = Y·V (other port SHORT)   Y = Z⁻¹,  g = h⁻¹
                 h: [V1; I2] = h·[I1; V2]   (h11 = Vin/Iin, output shorted;  h21 = current gain, output shorted)
                 ABCD: [V1; I1] = [A B; C D]·[V2; −I2]   (A, C: port 2 open;  B, D: port 2 shorted)
T NETWORK        Z = [[Z1+Z3, Z3],[Z3, Z2+Z3]];   A = 1+Z1/Z3, B = Z1+Z2+Z1Z2/Z3, C = 1/Z3, D = 1+Z2/Z3
PI NETWORK       Y = [[Ya+Yc, −Yc],[−Yc, Yb+Yc]];  A = 1+Yb/Yc, B = 1/Yc, C = Ya+Yb+YaYb/Yc, D = 1+Ya/Yc
BLOCKS (ABCD)    series Z: [[1,Z],[0,1]];  shunt Y: [[1,0],[Y,1]];  ideal transformer V1 = nV2: [[n,0],[0,1/n]]
RECIPROCAL       z12 = z21;  y12 = y21;  h12 = −h21;  g12 = −g21;  AD − BC = 1     (AD−BC = z12/z21 = y12/y21 = −h12/h21)
SYMMETRIC        z11 = z22;  y11 = y22;  Δh = 1;  A = D
CONVERSIONS      y11 = z22/ΔZ, y12 = −z12/ΔZ;   A = z11/z21, B = ΔZ/z21, C = 1/z21, D = z22/z21;   z11 = A/C, z12 = ΔT/C, z21 = 1/C, z22 = D/C
                 y11 = D/B, y12 = −ΔT/B, y21 = −1/B, y22 = A/B;   h11 = ΔZ/z22, h21 = −z21/z22, h22 = 1/z22
INTERCONNECT     series-series: Z add;  parallel-parallel: Y add;  series-parallel: h add;  parallel-series: g add;  cascade: T = Ta·Tb (order!)
TERMINATED       Z_in  = z11 − z12z21/(z22+Z_L) = (A·Z_L+B)/(C·Z_L+D)         Z_out = z22 − z12z21/(z11+Z_s) = (D·Z_s+B)/(C·Z_s+A)
                 A_v = V2/V1 = Z_L/(A·Z_L+B) = −y21/(y22+Y_L) = −h21·Z_L/(h11+Δh·Z_L)          A_i = I_L/I1 = 1/(C·Z_L+D) = z21/(z22+Z_L)
MAX POWER AT PORT 2   V_th = z21·V_s/(z11+Z_s) = V_s/(A+C·Z_s);   Z_L = Z_out*;   P_max = V_th²/(4·R_out)
TRANSFORMER      V1 = nV2, I1 = −I2/n, Z_in = n²Z_L;   coupled coils: M = k√(L1L2), series ±: L1+L2±2M, Z = jω[[L1,M],[M,L2]], T-equiv (L1−M),(L2−M),M
```

### F. Links between the topics

```
THEVENIN ↔ TRANSIENT   τ = R_th·C  or  L/R_th, with R_th seen by the element AFTER the switching.
THEVENIN ↔ TWO-PORT    seen from port 2:  Z_out = z22 − z12·z21/(z11 + Z_s),  V_th = z21·V_s/(z11 + Z_s)  →  max power at port 2 (2020 Q15, 2023 Q33).
THEVENIN ↔ AC          Z_L = Z_th*  (both parts free);  only R_L free: R_L = |Z_th + jX_L|.
Q, ζ AND POLES         series or parallel RLC:  Q = 1/(2ζ),  α = ζ·ω0 = ω0/(2Q),  poles −α ± jω_d,  ω_d = ω0·√(1 − ζ²).
STATE ↔ POLES          eigenvalues of A = poles of the circuit (R = 6, L = 1, C = 0.04:  −3 ± j4).
PHASOR ↔ LAPLACE       put s = jω in an s-domain model and you get the phasor model;  sL → jωL,  1/(sC) → 1/(jωC).
POWER                  components at DIFFERENT frequencies (DC included): add the mean squares;  components at the SAME frequency: add the phasors first, then find the power.
LINEAR  ≠  POWER       superposition holds for v and i, never for p.
```

---

## 5. Method chooser: which tool for which question

| You see | Do this | Day |
|---|---|---|
| "number of independent equations", KCL, KVL | `n − 1` and `b − n + 1` | 1 |
| many nodes, voltage sources | nodal analysis with **supernodes**; or source transformation | 1 |
| a current source shared by two meshes | **supermesh**, or nodal if the nodes are fewer | 1 |
| a delta or a bridge | star–delta; check balance `R₁/R₂ = R₃/R₄` first | 1 |
| a dependent source | write it as independent, add the control equation; a self-controlled one is a resistor | 1 |
| "Thevenin", "Norton", "load for maximum power" | `V_oc` and `R_th`; with a dependent source use a **test source** or `V_oc/I_sc` | 2 |
| several sources, one quantity | superposition (keep dependent sources) or Millman | 2 |
| "switch at `t = 0`", "time constant", "settling" | `v_C(0⁻)`, `i_L(0⁻)`; `0⁺` model; `τ = R_thC` or `L/R_th`; `x∞ + (x₀ − x∞)e^(−t/τ)` | 3 |
| two storage elements, "overshoot", "damping" | `α`, `ω₀`, `ζ`; **series vs parallel** formula | 3 |
| impulse, ideal switch between capacitors | conservation of charge or flux (`ΔV = q/C`, `ΔI = Φ/L`) | 3 |
| "steady state", "phasor" | impedances at one frequency; different frequencies separately | 4 |
| "power factor", "kVA", "capacitor to correct" | `S = P + jQ`; `C = P(tan φ₁ − tan φ₂)/(ωV²)`; add `P` and `Q`, never `\|S\|` | 4 |
| "resonance", "Q", "bandwidth" | `ω₀`, `Q`, `BW`; check series or parallel and the source type | 4 |
| "two-port", Z, Y, h, ABCD | choose the set; open or short the other port; cascade = multiply | 5 |
| source at port 1 and load at port 2 | Thevenin at port 2: `Z_out`, `V_th` | 5 |

---

## 6. Exam-hall rules for Networks

1. **Units first.** Write the unit next to every number (kΩ, mA, µF, ms). Unit slips cost more NAT marks than concept slips.
2. **One sign convention per problem.** Mark the polarity of every voltage and the direction of every current before writing an equation; for two-ports, `I₁` and `I₂` point into the network.
3. **Do the quick marks first.** Formula-recall questions (a `Q`, a `ζ`, a two-port parameter, a time constant) take under a minute; do them before the multi-step circuit problems.
4. **Sanity-check every NAT answer** with a limiting case (does the voltage lie between the source voltages? is the time constant positive? is the power less than the maximum?).
5. **Check the circuit for the cheap trick:** a wire shorting a branch, a series resistor with a current source, a balanced bridge, a symmetric circuit, an ideal source across the element in question.
6. **MCQs carry a penalty:** −⅓ for one mark, −⅔ for two. When two options remain, compute rather than guess. NAT and MSQ carry no penalty.
7. **Leave the long ones for the second pass.** A two-mark question that does not start working in a minute is probably the wrong method.

---

## 7. The concept check and the mock test

1. **`Day06_Conceptual_Questions.md`**: 20 mixed questions (MCQ, MSQ, NAT) across Days 1–5, one idea each. Score 17 or more before the mock test.
2. **`Day06_Mock_Test.md`**: 25 questions, 35 marks, 60 minutes, closed book. The topic mix follows the past papers (transients and AC about 55 %, two-ports about 17 %, analysis and theorems the rest).

The mock test has a scoring table and an **error log**. Count the causes of the lost marks; the cause that appears twice or more is your next study target.

---

## 8. Self-test before you move to Day 7

You are ready if you can, **without looking**:

- [ ] write the formula sheet of §4 from memory for at least one topic (take the one you like least)
- [ ] pick the right method for each row of §5 without reading the "Do this" column
- [ ] solve the 13 cold questions of §3 within 45 minutes
- [ ] score at least 17/20 on the mixed questions and at least 24/35 on the mock test

**Day 7 preview:** Signals and Systems begins. Day 7 covers signal types and operations (shifting, scaling, even and odd parts, energy and power) and the system properties (linearity, time invariance, causality, stability, memory). Everything in Days 1–6 transfers: phasors, Laplace models and the first-order response are the same mathematics you will meet again as frequency response and impulse response.

---

## 9. Sources

This note contains no new theory. The formula sheets are the Day 1–5 sheets copied unchanged; their sources are listed at the end of each day note. The map is built from the PYQ tables of those notes and from the official answer keys in `02_Previous_Year_Papers/`. The 2019 and 2021 answer keys are scanned images with no text layer, so for those years the marks follow the 55-question layout (Q1–Q25 one mark, Q26–Q55 two marks), which reproduces the 2020 key exactly and agrees with the 2021 key pages I read. The classification of "Networks" questions is my own reading of the eight papers; a question that I classified differently from you would change the totals slightly but not the conclusions.
