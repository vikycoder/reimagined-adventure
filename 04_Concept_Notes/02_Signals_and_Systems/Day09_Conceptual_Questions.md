# Day 9 — 20 Conceptual Questions (Continuous-Time Fourier Series)

**Companion to:** `Day09_Fourier_Series.md` (read §1–§9 first)
**Time:** 40 minutes, pencil and paper. A calculator helps for Q6, Q8 and Q15.
**Format:** GATE style. Each question tests **one idea**, and the wrong options are the mistakes students actually make.

| Type | How it works | Self-score |
|---|---|---|
| **MCQ** | exactly one correct option | 1 mark if right |
| **MSQ** | one or more correct options; **no partial credit** | 1 mark only if your set is exactly right |
| **NAT** | type a number, no options | 1 mark if right |

Every number in the solutions is re-checked by `tools/verify_day09.py` (coefficients computed numerically from the waveforms, symmetry and property claims tested on example signals, the Gibbs constants by numerical integration), and each answer was also derived by hand. `c_k` always means the **exponential** coefficient in `x(t) = Σ c_k e^{jkω₀t}`, with `ω₀` the fundamental angular frequency, unless the question says otherwise.

## What is in the set

| # | Type | Concept | Level | Review in the Day 9 note |
|---|---|---|---|---|
| 1 | NAT | Reading a coefficient off a sum of sinusoids | Easy | §2 |
| 2 | MCQ | Trigonometric to exponential coefficients (the sign of a sine) | Easy | §2 |
| 3 | NAT | Power of a sum of harmonics | Easy | §6 |
| 4 | NAT | An inner product by orthogonality | Medium | §1 |
| 5 | MSQ | Orthogonality over half a period | Hard | §1 |
| 6 | NAT | A coefficient of a pulse train | Medium | §3 |
| 7 | MCQ | Where the pulse-train spectrum has its first null | Medium | §3 |
| 8 | NAT | A trigonometric coefficient of a rectified sine | Medium | §3 |
| 9 | MCQ | The spectrum of an impulse train | Easy | §3 |
| 10 | MSQ | A real, odd signal | Medium | §4 |
| 11 | MCQ | Half-wave symmetry | Medium | §4 |
| 12 | NAT | Parseval combined with half-wave symmetry | Hard | §4, §6 |
| 13 | MCQ | The effect of a time shift | Medium | §5 |
| 14 | MCQ | The effect of time scaling | Medium | §5 |
| 15 | NAT | Differentiation of a triangle wave | Hard | §3, §5 |
| 16 | NAT | Multiplication by a cosine | Medium | §5 |
| 17 | NAT | The value of the series at a jump | Easy | §7 |
| 18 | NAT | The Gibbs overshoot | Medium | §7 |
| 19 | MCQ | A periodic input through `h(t) = δ(t) − δ(t − 1)` | Hard | §8 |
| 20 | MCQ | Spectrum of a periodic signal | Easy | §9 |

---

## Part A: Coefficients, forms and orthogonality

### Q1 · NAT
`x(t) = 2 + 4cos(4πt) − 6sin(12πt)`. Its exponential Fourier series is written for the fundamental frequency of `x(t)`. The magnitude `|c₃|` is ______.

### Q2 · MCQ
`x(t) = 4 + 6cos(ω₀t) + 8sin(ω₀t)`. The exponential Fourier coefficient `c₁` is:

- (A) `3 + 4j`
- (B) `6 − 8j`
- (C) `3 − 4j`
- (D) `5`

### Q3 · NAT
`x(t) = 2 + 3cos(ω₀t) + 4sin(2ω₀t)`. Its average power is ______.

### Q4 · NAT
`x(t) = cos(2πt) + 2sin(2πt)` and `y(t) = 3cos(2πt) − sin(2πt)`. The value of `∫₀¹ x(t)y(t) dt` is ______.

### Q5 · MSQ
Let `θ = ω₀t`. Over the **half period** `0 ≤ θ ≤ π`, which of these pairs are orthogonal?

- (A) `cosθ` and `cos2θ`
- (B) `sinθ` and `sin2θ`
- (C) `sinθ` and `cos2θ`
- (D) `cosθ` and `sin2θ`

---

## Part B: Standard waveforms

### Q6 · NAT
A periodic pulse train has period 8 s: `x(t) = 5` for `|t| < 1 s` and `x(t) = 0` for `1 s < |t| < 4 s`. Its exponential Fourier coefficient `c₁` is ______ (round off to two decimal places).

### Q7 · MCQ
For the same pulse train (`x(t) = 5` for `|t| < 1 s`, `0` for `1 s < |t| < 4 s`, period 8 s), the smallest positive harmonic number `k` for which `c_k = 0` is:

- (A) 2
- (B) 4
- (C) 8
- (D) there is none

### Q8 · NAT
`x(t) = |sin(πt)|`. Its trigonometric Fourier series is `x(t) = a₀ + Σ [a_k cos(kω₀t) + b_k sin(kω₀t)]`, with `ω₀` the fundamental angular frequency of `x(t)`. The coefficient `a₁` is ______ (round off to two decimal places).

### Q9 · MCQ
`x(t) = Σ_{n=−∞}^{∞} 3δ(t − 5n)`. Its exponential Fourier coefficients are:

- (A) `c_k = 3` for all `k`
- (B) `c₀ = 0` and `c_k = 3/(5k)` for `k ≠ 0`
- (C) `c_k = (3/5)·sinc(k/5)`
- (D) `c_k = 3/5` for all `k`

---

## Part C: Symmetry

### Q10 · MSQ
`x(t)` is real, periodic and odd, with exponential coefficients `c_k`. Select **all** true statements.

- (A) `c₀ = 0`
- (B) every `c_k` is purely imaginary
- (C) `c_{−k} = c_k` for all `k`
- (D) its trigonometric series has cosine terms but no sine terms

### Q11 · MCQ
A real periodic signal with period `T₀` satisfies `x(t − T₀/2) = −x(t)`. Its Fourier series contains:

- (A) only odd harmonics (no DC term and no even harmonics)
- (B) only even harmonics (including DC)
- (C) only cosine terms
- (D) only sine terms

### Q12 · NAT
A real periodic signal `x(t)` with period `T₀` satisfies `x(t − T₀/2) = −x(t)`. Its average power is 30, and its exponential coefficients include `c₁ = 2 + 2j` and `c₃ = −1`. The total power in all harmonics with `|k| ≥ 5` is ______.

---

## Part D: Properties

### Q13 · MCQ
`x(t)` has period 8 s and the exponential coefficient `c₂ = 3`. The signal `y(t) = x(t − 1)` has the coefficient `d₂ =`

- (A) `−3j`
- (B) `3j`
- (C) `3e^{−jπ/4}`
- (D) `3`

### Q14 · MCQ
`f(t) = Σ c_k e^{j(2π/T₀)kt}` has period `T₀` and `c₃ = 1 − j`. The signal `y(t) = f(2t)` is expanded in its **own** fundamental frequency, `y(t) = Σ d_k e^{jk(2π/T_y)t}`. The coefficient `d₃` is:

- (A) `(1 − j)/2`
- (B) `2(1 − j)`
- (C) `0`
- (D) `1 − j`

### Q15 · NAT
`x(t)` is a triangular wave with period 2 s that varies linearly between `+1` (at `t = 0`) and `−1` (at `t = 1`). Its derivative `dx/dt` is a square wave. The amplitude of the fundamental (first-harmonic) component of `dx/dt` is ______ (round off to two decimal places).

### Q16 · NAT
`y(t)` has exponential coefficients `d₀ = 2`, `d_{±1} = 1`, `d_{±2} = 3`, and `d_k = 0` for `|k| ≥ 3`. The signal `z(t) = y(t)cos(ω₀t)` has the coefficient `e₁ =` ______.

---

## Part E: Convergence and the Gibbs phenomenon

### Q17 · NAT
`x(t) = t` for `0 ≤ t < 1`, repeated with period 1 (a sawtooth ramp). The value to which its Fourier series converges at `t = 3` is ______.

### Q18 · NAT
A square wave switches between `−2 V` and `+2 V`. Its Fourier series is truncated after a very large number of harmonics. The maximum value of the partial sum near a jump is approximately ______ V (round off to two decimal places).

---

## Part F: LTI systems and spectra

### Q19 · MCQ
A periodic signal `x(t)` with period `T₀ = 2 s` is applied to an LTI system with impulse response `h(t) = δ(t) − δ(t − 1)`. The output contains:

- (A) only the even harmonics (and DC) of the input
- (B) all the harmonics of the input, each doubled in amplitude
- (C) only the odd harmonics of the input, each doubled in amplitude
- (D) all the harmonics of the input, unchanged in amplitude

### Q20 · MCQ
A continuous-time signal is periodic. Its spectrum (its Fourier coefficients plotted against frequency) is:

- (A) continuous and periodic
- (B) discrete and aperiodic
- (C) continuous and aperiodic
- (D) discrete and periodic

---

## Score yourself

<details>
<summary><b>Answer key (open after you finish all 20)</b></summary>

| Q | Answer | Q | Answer |
|---|---|---|---|
| 1 | 3 (range 3 to 3) | 11 | A |
| 2 | C | 12 | 12 (range 12 to 12) |
| 3 | 16.5 (range 16.5 to 16.5) | 13 | A |
| 4 | 0.5 (range 0.5 to 0.5) | 14 | D |
| 5 | A, B | 15 | 2.55 (range 2.54 to 2.56) |
| 6 | 1.13 (range 1.12 to 1.13) | 16 | 2.5 (range 2.5 to 2.5) |
| 7 | B | 17 | 0.5 (range 0.5 to 0.5) |
| 8 | -0.42 (range -0.43 to -0.42) | 18 | 2.36 (range 2.34 to 2.38) |
| 9 | D | 19 | C |
| 10 | A, B | 20 | B |

**How to read your score**

| Score | What to do |
|---|---|
| 17–20 | You are ready for Day 10 (the Fourier transform and sampling). |
| 13–16 | Re-read the "Review" section for each question you missed, then redo only those questions tomorrow. |
| 12 or less | Re-read §1–§5 of the Day 9 note, redo the worked examples with the solution covered, then retake this set after 24 hours. |

Keep a note of **why** each miss happened: a sign or a factor of ½ (forms), a symmetry rule applied the wrong way round, a property mixed up (scaling, shift, derivative), or a missing negative `k` in Parseval. Those are four different fixes.

</details>

## Solutions

<details>
<summary><b>Q1 · Reading a coefficient off a sum of sinusoids</b></summary>

**Answer: 3.**

The frequencies `4π` and `12π` rad/s have greatest common divisor `4π`, so `ω₀ = 4π` (`T₀ = 0.5 s`) and the terms are the harmonics `k = 1` and `k = 3`. By Euler, `−6sin(12πt) = −6(e^{j12πt} − e^{−j12πt})/(2j) = 3j·e^{j12πt} − 3j·e^{−j12πt}`, so `c₃ = 3j` and `|c₃| =` **3**. (The other coefficients are `c₀ = 2`, `c_{±1} = 2`, `c_{−3} = −3j`, and zero elsewhere.)

*Review:* §2.
</details>

<details>
<summary><b>Q2 · Trigonometric to exponential coefficients</b></summary>

**Answer: C.**

Here `a₁ = 6` and `b₁ = 8`, and `c₁ = (a₁ − jb₁)/2 = (6 − 8j)/2 =` **3 − 4j**. Option (A) is `c_{−1}`, the conjugate: the sign of the sine term is the usual slip. (B) forgets the factor ½, and (D) is `|c₁|`.

*Review:* §2.
</details>

<details>
<summary><b>Q3 · Power of a sum of harmonics</b></summary>

**Answer: 16.5.**

Harmonics at different frequencies are orthogonal, so their powers add: `P = a₀² + ½(a₁² + b₂²) = 2² + 3²/2 + 4²/2 = 4 + 4.5 + 8 =` **16.5**. (A cosine and a sine of the same amplitude have the same power, `A²/2`.)

*Review:* §6.
</details>

<details>
<summary><b>Q4 · An inner product by orthogonality</b></summary>

**Answer: 0.5.**

Over one period the cross terms `cos·sin` integrate to zero, and `∫₀¹cos²(2πt)dt = ∫₀¹sin²(2πt)dt = ½`. So `∫₀¹xy dt = (1)(3)(½) + (2)(−1)(½) = 1.5 − 1 =` **0.5**.

*Review:* §1.1.
</details>

<details>
<summary><b>Q5 · Orthogonality over half a period</b></summary>

**Answer: A, B.**

Over half a period, two cosines (or two sines) with different integer harmonic numbers are still orthogonal: `∫₀^π cosθ cos2θ dθ = 0` and `∫₀^π sinθ sin2θ dθ = 0`. A sine and a cosine are orthogonal over half a period only when their harmonic numbers have the **same parity**; here 1 and 2 differ, and `∫₀^π sinθ cos2θ dθ = −2/3` and `∫₀^π cosθ sin2θ dθ = 4/3`. So (C) and (D) are **not** orthogonal. (Over a *full* period all four pairs would be orthogonal.)

*Review:* §1.1.
</details>

<details>
<summary><b>Q6 · A coefficient of a pulse train</b></summary>

**Answer: 1.13.**

`c_k = (A/(πk))sin(kω₀T₁)` with `A = 5`, `T₁ = 1 s` and `ω₀ = 2π/8 = π/4`. So `c₁ = (5/π)sin(π/4) = 1.5915 × 0.7071 = 1.1254 ≈` **1.13**. (The DC value `c₀ = 5 × 2/8 = 1.25` is a different coefficient.)

*Review:* §3.2.
</details>

<details>
<summary><b>Q7 · The first null of a pulse-train spectrum</b></summary>

**Answer: B.**

`c_k = (5/(πk))sin(kπ/4)` is zero when `kπ/4` is a non-zero multiple of `π`, that is `k = 4, 8, 12, …`, and the first is **`k = 4`**. In terms of the duty cycle: `2T₁/T₀ = ¼`, so the sinc envelope has its nulls on every fourth harmonic (the first null is at `1/(2T₁) = 0.5 Hz = 4f₀`). The coefficients before it are non-zero: `c₁ = 1.125`, `c₂ = 0.796`, `c₃ = 0.375`.

*Review:* §3.3.
</details>

<details>
<summary><b>Q8 · A trigonometric coefficient of a rectified sine</b></summary>

**Answer: −0.42.**

`|sin(πt)|` has period 1 (not 2), so `ω₀ = 2π`. For the full-wave rectified sine `c_k = 2/(π(1 − 4k²))`, so `c₁ = 2/(π(−3)) = −2/(3π)` and `a₁ = 2c₁ = −4/(3π) = −0.4244 ≈` **−0.42**. (Using `T₀ = 2` instead would give the wrong harmonic numbers.)

*Review:* §3.2.
</details>

<details>
<summary><b>Q9 · The spectrum of an impulse train</b></summary>

**Answer: D.**

`c_k = (1/T₀)∫_{T₀} x(t)e^{−jkω₀t}dt` with `T₀ = 5`: the impulse at `t = 0` gives `c_k = 3/5` for **every** `k`, a flat line spectrum of height (weight)/`T₀`. (A) forgets the factor `1/T₀`; (B) is the shape of a sawtooth's spectrum; (C) is the spectrum of a pulse of non-zero width.

*Review:* §3.2.
</details>

<details>
<summary><b>Q10 · A real, odd signal</b></summary>

**Answer: A, B.**

The average of an odd signal is zero, so `c₀ = 0`, and `c_{−k} = −c_k`. Combined with `c_{−k} = c_k*` for a real signal, this makes every `c_k` **purely imaginary** (`c_k = −jb_k/2`). So (A) and (B) are true. (C) is the property of an *even* signal, and (D) is backwards: an odd signal has **sine** terms only.

*Review:* §4.
</details>

<details>
<summary><b>Q11 · Half-wave symmetry</b></summary>

**Answer: A.**

The shifted signal has coefficients `c_k e^{−jkπ} = (−1)^k c_k`. Setting this equal to the coefficients of `−x(t)`, which are `−c_k`, forces `c_k = 0` for every **even** `k`, including `k = 0` (no DC). Only the odd harmonics remain. Both the ±A square wave (sines only) and the ±1 triangle wave (cosines only) have this symmetry, so (C) and (D) are not implied; (B) is the opposite.

*Review:* §4.
</details>

<details>
<summary><b>Q12 · Parseval combined with half-wave symmetry</b></summary>

**Answer: 12.**

Half-wave symmetry makes every even-`k` coefficient zero. A real signal has `c_{−k} = c_k*`, so the harmonics `k = ±1` carry `2|c₁|² = 2(2² + 2²) = 16` and `k = ±3` carry `2|c₃|² = 2(1) = 2`, together `18`. By Parseval the total power is 30, so the rest, the harmonics `|k| ≥ 5`, carry `30 − 18 =` **12**.

*Review:* §4, §6.
</details>

<details>
<summary><b>Q13 · The effect of a time shift</b></summary>

**Answer: A.**

A shift multiplies `c_k` by `e^{−jkω₀t₀}`. Here `ω₀ = 2π/8 = π/4`, `k = 2` and `t₀ = 1`, so the factor is `e^{−j2(π/4)(1)} = e^{−jπ/2} = −j`, and `d₂ =` **−3j** (magnitude 3, phase −90°). (C) uses `k = 1` instead of `k = 2`; (B) has the wrong sign; (D) forgets that a shift changes the phase.

*Review:* §5.
</details>

<details>
<summary><b>Q14 · The effect of time scaling</b></summary>

**Answer: D.**

`y(t) = f(2t) = Σ c_k e^{j(2π/T₀)k(2t)} = Σ c_k e^{jk(2ω₀)t}`. The coefficients are **unchanged**; they now belong to the new fundamental frequency `2ω₀`, and `y` has period `T₀/2`. So `d₃ = c₃ =` **1 − j**. (A) and (B) borrow the rule of the Fourier *transform*, where scaling does change the amplitude; (C) has no basis.

*Review:* §5.
</details>

<details>
<summary><b>Q15 · Differentiation of a triangle wave</b></summary>

**Answer: 2.55.**

The ±1 triangle with period 2 has `c_k = 4/(π²k²)` for odd `k` and `ω₀ = π`. Differentiation multiplies the coefficients by `jkω₀`: `d₁ = jπ · 4/π² = 4j/π`, so the first harmonic of `x′` has amplitude `2|d₁| = 8/π =` **2.55**. Check: the slope of the triangle is `±2`, so `x′` is a ±2 square wave, whose fundamental has amplitude `(4/π)(2) = 8/π`.

*Review:* §3.4, §5.
</details>

<details>
<summary><b>Q16 · Multiplication by a cosine</b></summary>

**Answer: 2.5.**

`cos(ω₀t) = (e^{jω₀t} + e^{−jω₀t})/2` shifts the spectrum by `±1` and halves it: `e_k = (d_{k−1} + d_{k+1})/2`. So `e₁ = (d₀ + d₂)/2 = (2 + 3)/2 =` **2.5**.

*Review:* §5.
</details>

<details>
<summary><b>Q17 · The value of the series at a jump</b></summary>

**Answer: 0.5.**

At `t = 3` the ramp jumps from `1` (just before) to `0` (just after). At a jump the series converges to the **midpoint** `(1 + 0)/2 =` **0.5**, whatever value is assigned to `x(3)` itself. (At a point of continuity such as `t = 3.25` the series converges to the signal value, `0.25`.)

*Review:* §7.
</details>

<details>
<summary><b>Q18 · The Gibbs overshoot</b></summary>

**Answer: 2.36.**

The first overshoot of the partial sums tends to `Si(π)/π − ½ = 0.0895` of the **jump size** and does not shrink as terms are added. The jump is `4 V`, so the peak is `2 + 0.0895 × 4 = 2.358 ≈` **2.36 V**. (Equivalently `2 × (2/π)Si(π) = 2 × 1.179`.)

*Review:* §7.
</details>

<details>
<summary><b>Q19 · A periodic input through a two-impulse filter</b></summary>

**Answer: C.**

With `T₀ = 2 s` we have `ω₀ = π`, and `H(jω) = 1 − e^{−jω}`. Each harmonic is multiplied by `H(jkπ) = 1 − e^{−jkπ} = 1 − (−1)^k`, which is `0` for even `k` (including DC) and `2` for odd `k`. The output `y(t) = x(t) − x(t − T₀/2)` has half-wave symmetry: **only the odd harmonics, doubled in amplitude**.

*Review:* §8.
</details>

<details>
<summary><b>Q20 · Spectrum of a periodic signal</b></summary>

**Answer: B.**

A periodic continuous-time signal is represented by a Fourier series: lines only at the harmonics `kω₀` (**discrete**), with coefficients that are in general non-zero for infinitely many `k` (**aperiodic**). *Periodic in one domain means discrete in the other.* A continuous, periodic spectrum belongs to a discrete-time aperiodic signal (DTFT), and a discrete, periodic one to a discrete-time periodic signal (DTFS). (This is 2023 Q29.)

*Review:* §9.
</details>
