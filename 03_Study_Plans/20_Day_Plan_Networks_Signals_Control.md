# 20-Day Plan: Network Theory, Signals & Systems, Control Systems

These three subjects are worth about 30–40 of the 85 technical marks in GATE EC.
The order matters: Networks introduces Laplace-domain circuits, Signals teaches transforms properly,
and Control is built on both.

**Notes** = `01_Notes/GateOPedia_EC_ShortNotes_PW_2022.pdf` (page numbers as printed in the notes).
**PYQs** = previous-year questions from `02_Previous_Year_Papers/` (2021–2026) plus an older topic-wise PYQ book if you have one.

## Daily routine (about 6 hours)

| Block | Time | What to do |
|---|---|---|
| 1. Warm-up | 30 min | Re-read your formula sheet and redo yesterday's wrong questions |
| 2. Concepts | 2–2.5 h | Read the day's notes pages; watch one lecture on any part that isn't clear |
| 3. Problems | 2.5–3 h | Solve PYQs on the day's topic. Attempt first, check the key, then study the solution |
| 4. Wrap-up | 30 min | Add new formulas to your one-page sheet; log every mistake and why it happened |

With only 3–4 hours a day, keep blocks 3 and 4 and shorten block 2. Problems matter more than reading.

---

## Days 1–6: Network Theory

| Day | Topics | Notes pages | Done |
|---|---|---|---|
| 1 | KCL/KVL, node and mesh analysis, supernode/supermesh, dependent sources, source transformation, star–delta (wye–delta) | 2.1 – 2.19. **Concept note:** `04_Concept_Notes/01_Network_Theory/Day01_Circuit_Analysis_Fundamentals.md` and `Day01_Conceptual_Questions.md` | ☐ |
| 2 | Superposition, Thevenin, Norton, maximum power transfer (DC), reciprocity | 2.30 – 2.34 | ☐ |
| 3 | Transients: RL, RC, RLC circuits, initial and final conditions, time constant, solving circuits with Laplace transform | 2.35 – 2.43 | ☐ |
| 4 | Sinusoidal steady state: phasors, impedance, complex power, power factor, AC maximum power transfer, series and parallel resonance, Q-factor | 2.44 – 2.57 | ☐ |
| 5 | Two-port networks (Z, Y, h, ABCD parameters, conversions, series/parallel/cascade connections), coupled inductors | 2.20 – 2.29, 2.58 – 2.61 | ☐ |
| 6 | **Revision + test:** every Networks PYQ from 2021–2026 not yet solved, then a timed 25–30 question set. Finish the Networks formula sheet | — | ☐ |

**High-frequency PYQ areas:** Thevenin with dependent sources, RLC transients, two-port parameters, resonance.

---

## Days 7–13: Signals & Systems

| Day | Topics | Notes pages | Done |
|---|---|---|---|
| 7 | Signal types and operations (shifting, scaling, even/odd, energy/power), system properties: linearity, time invariance, causality, stability, memory | 3.1 – 3.22 | ☐ |
| 8 | Convolution (continuous and discrete), impulse response, LTI system properties from h(t) / h[n] | 3.1 – 3.22 | ☐ |
| 9 | Continuous-time Fourier series: coefficients, symmetry, Parseval's theorem | 3.23 – 3.33 | ☐ |
| 10 | Fourier transform and its properties, sampling theorem, aliasing, reconstruction | 3.34 – 3.41, 3.65 – 3.68 | ☐ |
| 11 | Laplace transform: ROC, poles and zeros, causality and stability from ROC, frequency response. **Group delay and phase delay** (not in the notes, so use a lecture or textbook) | 3.42 – 3.50 | ☐ |
| 12 | Z-transform: ROC, inverse z-transform, discrete-time system analysis. DTFT | 3.51 – 3.64 | ☐ |
| 13 | DFT (N-point DFT, circular convolution). **FIR and IIR filter design** (window method, bilinear transform; not in the notes). Then a timed Signals PYQ set | 3.69 – 3.76 | ☐ |

**High-frequency PYQ areas:** convolution, system properties, Fourier transform properties, sampling, z-transform ROC, DFT.

---

## Days 14–19: Control Systems

| Day | Topics | Notes pages | Done |
|---|---|---|---|
| 14 | Transfer function, feedback principle, block diagram reduction, signal flow graph and Mason's gain formula | 4.1 – 4.7 | ☐ |
| 15 | Time response: first- and second-order systems, damping, rise time, peak overshoot, settling time | 4.8 – 4.26 | ☐ |
| 16 | Steady-state error (system type, error constants), Routh–Hurwitz stability | 4.27 – 4.37 | ☐ |
| 17 | Root locus: rules, breakaway points, imaginary-axis crossing, effect of adding poles and zeros | 4.38 – 4.45 | ☐ |
| 18 | Frequency response: Bode plot, polar plot, gain and phase margin, Nyquist criterion | 4.46 – 4.67 | ☐ |
| 19 | State-space model, state transition matrix, solution of state equation, controllability and observability. Lead/lag compensators and PID | 4.68 – 4.81 | ☐ |

**High-frequency PYQ areas:** second-order time response, Routh, root locus, Bode/Nyquist margins, state-space.

---

## Day 20: Combined test and review

| Part | What to do | Done |
|---|---|---|
| Test (3 h) | Timed mixed set of about 50 questions across all three subjects, using the GATE virtual calculator | ☐ |
| Analysis (2 h) | Mark every wrong or guessed question as one of: concept gap, formula forgotten, silly mistake, too slow | ☐ |
| Fix (1 h) | Re-study the two weakest topics. Add them to the warm-up list for the next phase | ☐ |

## Rules that keep the plan on track

- **Behind schedule?** Don't skip days to catch up. Cut the reading and keep the PYQs.
- **Topics marked "not in the notes"** need one extra source: a lecture or textbook chapter on just that topic.
- **Keep your formula sheets.** By Day 20 you should have one page each for Networks, Signals and Control, which you'll reuse in final revision.
