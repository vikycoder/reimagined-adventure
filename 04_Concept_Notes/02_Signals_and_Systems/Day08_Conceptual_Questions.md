# Day 8 — 20 Conceptual Questions (Convolution and LTI Systems)

**Companion to:** `Day08_Convolution_and_LTI_Systems.md` (read §1–§6 first)
**Time:** 40 minutes, pencil and paper. No calculator needed except for the exponentials in Q7 and Q14.
**Format:** GATE style. Each question tests **one idea**, and the wrong options are the mistakes students actually make.

| Type | How it works | Self-score |
|---|---|---|
| **MCQ** | exactly one correct option | 1 mark if right |
| **MSQ** | one or more correct options; **no partial credit** | 1 mark only if your set is exactly right |
| **NAT** | type a number, no options | 1 mark if right |

Every number in the solutions is re-checked by `tools/verify_day08.py` (continuous-time convolutions by numerical integration, discrete-time ones with `np.convolve`, system properties with numerical tests), and each answer was also derived by hand. `∗` is convolution; `u(t)` and `u[n]` are unit steps.

## What is in the set

| # | Type | Concept | Level | Review in the Day 8 note |
|---|---|---|---|---|
| 1 | NAT | One sample of a discrete convolution | Easy | §2 |
| 2 | MCQ | Where the convolution is non-zero | Easy | §2 |
| 3 | NAT | The sum of a convolution | Easy | §2 |
| 4 | MCQ | Convolution with shifted impulses | Medium | §2 |
| 5 | NAT | Impulse response from the step response | Medium | §4 |
| 6 | NAT | Peak of a rectangle convolved with itself | Medium | §3 |
| 7 | MCQ | An exponential convolved with a step | Easy | §3 |
| 8 | NAT | Maximum of two rectangles convolved | Medium | §3 |
| 9 | NAT | The area of a convolution | Medium | §3 |
| 10 | MCQ | Convolving two time-scaled signals | Medium | §3 |
| 11 | MSQ | Causal and BIBO-stable impulse responses | Medium | §4 |
| 12 | NAT | The largest output of a stable system | Medium | §4 |
| 13 | MCQ | A causal, stable discrete-time `h[n]` | Medium | §4 |
| 14 | NAT | A sample of `h[n]` from the step response | Medium | §4 |
| 15 | MCQ | The impulse response of a cascade | Medium | §5 |
| 16 | MCQ | An LTI system plus a constant | Medium | §5 |
| 17 | NAT | A sinusoid through an FIR filter | Medium | §6 |
| 18 | MSQ | Properties of convolution | Medium | §3, §5 |
| 19 | NAT | A moving-sum filter | Easy | §2 |
| 20 | MCQ | A feedback-free network of LTI blocks | Medium | §5 |

---

## Part A: Discrete-time convolution

### Q1 · NAT
`x[n]` has the values 1, 2, 3 at `n = 0, 1, 2` and is zero elsewhere. `h[n]` has the values 1, −1 at `n = 0, 1` and is zero elsewhere. For `y[n] = x[n] ∗ h[n]`, the value `y[3]` is ______.

### Q2 · MCQ
`x[n]` is non-zero only for `0 ≤ n ≤ 4`, and `h[n]` is non-zero only for `−1 ≤ n ≤ 1`. The convolution `y[n] = x[n] ∗ h[n]` can be non-zero only for:

- (A) `−1 ≤ n ≤ 5`
- (B) `0 ≤ n ≤ 4`
- (C) `−1 ≤ n ≤ 6`
- (D) `0 ≤ n ≤ 6`

### Q3 · NAT
`x[n] = {2, −1, 3}` (values at `n = 0, 1, 2`) and `h[n] = {1, 4, −2}` (values at `n = 0, 1, 2`). For `y = x ∗ h`, the sum `Σₙ y[n]` is ______.

### Q4 · MCQ
`x[n] = u[n]` and `h[n] = δ[n − 2] + δ[n + 1]`. The value `y[0]` of `y = x ∗ h` is:

- (A) 0
- (B) 1
- (C) 2
- (D) 3

### Q5 · NAT
The step response of a discrete-time LTI system is `s[n] = 1, 3, 6, 6, 6, …` for `n = 0, 1, 2, 3, 4, …` (and 0 for `n < 0`). Its impulse response has `h[2] =` ______.

---

## Part B: Continuous-time convolution

### Q6 · NAT
`x(t) = 2[u(t) − u(t − 2)]`. The peak value of `y(t) = x(t) ∗ x(t)` is ______.

### Q7 · MCQ
For `x(t) = e^{−t}u(t)` and `h(t) = u(t)`, the value of `y(1)`, where `y = x ∗ h`, is:

- (A) 0.368
- (B) 1.368
- (C) 1
- (D) 0.632

### Q8 · NAT
`x₁(t) = u(t) − u(t − 2)` (a rectangle of width 2 and height 1) and `x₂(t) = u(t) − u(t − 3)` (width 3, height 1). The maximum value of `x₁(t) ∗ x₂(t)` is ______.

### Q9 · NAT
`x(t) = 3e^{−2t}u(t)` and `h(t) = 2δ(t − 1) + 3[u(t) − u(t − 2)]`. For `y = x ∗ h`, the value of `∫_{−∞}^{∞} y(t) dt` is ______.

### Q10 · MCQ
If `y(t) = x(t) ∗ h(t)`, then `x(2t) ∗ h(2t)` equals:

- (A) `y(2t)`
- (B) `2y(2t)`
- (C) `0.5·y(2t)`
- (D) `0.5·y(t)`

---

## Part C: Reading properties from the impulse response

### Q11 · MSQ
Select **all** impulse responses for which the LTI system is **both causal and BIBO stable**.

- (A) `h(t) = e^{−2t}u(t)`
- (B) `h(t) = e^{2t}u(t)`
- (C) `h(t) = e^{−|t|}`
- (D) `h(t) = δ(t − 3)`

### Q12 · NAT
An LTI system has `h(t) = 3e^{−2t}u(t)`. For every input with `|x(t)| ≤ 2`, the largest possible value of `|y(t)|` is ______.

### Q13 · MCQ
Which of the following impulse responses describes a **causal, BIBO-stable** discrete-time LTI system?

- (A) `h[n] = (0.5)ⁿ u[n]`
- (B) `h[n] = 2ⁿ u[n]`
- (C) `h[n] = (0.5)^{|n|}`
- (D) `h[n] = u[n]`

### Q14 · NAT
A discrete-time LTI system has the step response `s[n] = (1 − 0.5^{n+1})u[n]`. Its impulse response value `h[3]` is ______ (round off to four decimal places).

---

## Part D: Combining systems and frequency response

### Q15 · MCQ
Two LTI systems with `h₁(t) = δ(t − 1)` and `h₂(t) = e^{−t}u(t)` are connected in cascade. The impulse response of the cascade is:

- (A) `e^{−t}u(t − 1)`
- (B) `e^{−(t+1)}u(t + 1)`
- (C) `e^{−t}u(t) + δ(t − 1)`
- (D) `e^{−(t−1)}u(t − 1)`

### Q16 · MCQ
A discrete-time system computes `y[n] = (x ∗ h)[n] + 5`, where `h[n]` is a fixed FIR impulse response. The system is:

- (A) linear and time-invariant
- (B) linear and time-varying
- (C) non-linear and time-invariant
- (D) non-linear and time-varying

### Q17 · NAT
A discrete-time LTI system has `h[n] = {1, 2, 1}` (values at `n = 0, 1, 2`). The input is `x[n] = cos(πn/2)` for all `n`. The amplitude of the steady-state output is ______.

### Q18 · MSQ
Select **all** correct statements.

- (A) `x(t) ∗ h(t) = h(t) ∗ x(t)`.
- (B) `d/dt [x(t) ∗ h(t)] = [dx/dt] ∗ h(t)`.
- (C) `x(t) ∗ δ(t − t₀) = x(t)·δ(t − t₀)`.
- (D) Interchanging the order of two cascaded LTI systems does not change the overall impulse response.

### Q19 · NAT
`x[n] = {1, 1, 1, 1}` (values at `n = 0, …, 3`) and `h[n] = {1, 1, 1}` (values at `n = 0, 1, 2`). For `y = x ∗ h`, the value `y[3]` is ______.

### Q20 · MCQ
A discrete-time system is built only from LTI sub-systems (impulse responses `h₁` and `h₂`), unit delays, gains and adders, **with no feedback loop**. The overall system is necessarily:

- (A) causal
- (B) linear and time-invariant
- (C) time-varying
- (D) non-linear

---

## Score yourself

<details>
<summary><b>Answer key (open after you finish all 20)</b></summary>

| Q | Answer | Q | Answer |
|---|---|---|---|
| 1 | -3 (range -3 to -3) | 11 | A, D |
| 2 | A | 12 | 3 (range 3 to 3) |
| 3 | 12 (range 12 to 12) | 13 | A |
| 4 | B | 14 | 0.0625 (range 0.0624 to 0.0626) |
| 5 | 3 (range 3 to 3) | 15 | D |
| 6 | 8 (range 8 to 8) | 16 | C |
| 7 | D | 17 | 2 (range 2 to 2) |
| 8 | 2 (range 2 to 2) | 18 | A, B, D |
| 9 | 12 (range 12 to 12) | 19 | 3 (range 3 to 3) |
| 10 | C | 20 | B |

**How to read your score**

| Score | What to do |
|---|---|
| 17–20 | You are ready for Day 9 (continuous-time Fourier series). |
| 13–16 | Re-read the "Review" section for each question you missed, then redo only those questions tomorrow. |
| 12 or less | Re-read §2–§5 of the Day 8 note, redo the worked examples with the solution covered, then retake this set after 24 hours. |

Keep a note of **why** each miss happened: a flip or shift slip, a support or length slip, or a property mixed up (area, scaling, BIBO). Those are three different fixes.

</details>

## Solutions

<details>
<summary><b>Q1 · One sample of a discrete convolution</b></summary>

**Answer: −3.**

`y[3] = Σ_k x[k]h[3 − k]`. Only `k = 2` has both factors non-zero (`h[1] = −1`): `y[3] = x[2]·h[1] = 3 × (−1) =` **−3**. The whole convolution is `{1, 1, 1, −3}`.

*Review:* §2.
</details>

<details>
<summary><b>Q2 · Where the convolution is non-zero</b></summary>

**Answer: A.**

The starting indices add (`0 + (−1) = −1`) and so do the ending indices (`4 + 1 = 5`). The length is `5 + 3 − 1 = 7` samples, from `n = −1` to `n = 5`.

*Review:* §2.
</details>

<details>
<summary><b>Q3 · The sum of a convolution</b></summary>

**Answer: 12.**

Summing a convolution multiplies the sums (the **area rule**): `Σy = (Σx)(Σh) = (2 − 1 + 3)(1 + 4 − 2) = 4 × 3 =` **12**. There is no need to build the whole sequence. As a check, it is `y = {2, 7, −5, 14, −6}` (`y[1] = 2·4 + (−1)·1 = 7`, `y[2] = 2·(−2) + (−1)·4 + 3·1 = −5`, `y[3] = (−1)(−2) + 3·4 = 14`, `y[4] = 3·(−2) = −6`), and `2 + 7 − 5 + 14 − 6 = 12` ✓.

*Review:* §2.
</details>

<details>
<summary><b>Q4 · Convolution with shifted impulses</b></summary>

**Answer: B.**

`u[n] ∗ δ[n − k] = u[n − k]`, so `y[n] = u[n − 2] + u[n + 1]` and `y[0] = u[−2] + u[1] = 0 + 1 =` **1**.

*Review:* §2.
</details>

<details>
<summary><b>Q5 · Impulse response from the step response</b></summary>

**Answer: 3.**

`h[n] = s[n] − s[n − 1]`: `h[0] = 1`, `h[1] = 3 − 1 = 2`, `h[2] = 6 − 3 =` **3**, and `h[n] = 0` afterwards. (The step response is the running sum of `h`.)

*Review:* §4.
</details>

<details>
<summary><b>Q6 · Peak of a rectangle convolved with itself</b></summary>

**Answer: 8.**

The convolution of two identical rectangles of width 2 and height 2 is a **triangle** on `[0, 4]` whose peak (at `t = 2`, full overlap) is `height × height × width = 2 × 2 × 2 =` **8**.

*Review:* §3.
</details>

<details>
<summary><b>Q7 · An exponential convolved with a step</b></summary>

**Answer: D.**

Convolving with `u(t)` integrates: `y(t) = ∫₀^t e^{−τ}dτ = 1 − e^{−t}`, so `y(1) = 1 − e^{−1} =` **0.632**. (0.368 is `e^{−1}`, the value of the exponential itself.)

*Review:* §3.
</details>

<details>
<summary><b>Q8 · Maximum of two rectangles convolved</b></summary>

**Answer: 2.**

The convolution of two rectangles (heights 1) is a trapezoid whose maximum equals the **shorter width**: `min(2, 3) =` **2**. (It is non-zero for `0 < t < 5`, rises for 2 s, stays at 2 for `|3 − 2| = 1` s, and falls for 2 s.)

*Review:* §3.
</details>

<details>
<summary><b>Q9 · The area of a convolution</b></summary>

**Answer: 12.**

`∫y = (∫x)(∫h)`. `∫x = 3/2 = 1.5`. `∫h = 2 + 3 × 2 = 8` (an impulse of weight 2 plus a pulse of height 3 and width 2). So `∫y = 1.5 × 8 =` **12**.

*Review:* §3.
</details>

<details>
<summary><b>Q10 · Convolving time-scaled signals</b></summary>

**Answer: C.**

With `v = 2τ`, `∫x(2τ)h(2(t − τ))dτ = (1/2)∫x(v)h(2t − v)dv = (1/2)y(2t)`. In general `x(at) ∗ h(at) = y(at)/|a|`. Option (A) forgets the factor `1/|a|`, option (B) multiplies by 2 instead of dividing, and option (D) scales the time axis the wrong way (`y(t)` instead of `y(2t)`). The same rule with `a = 0.5` gives `2y(0.5t)`, which is 2024 Q21.

*Review:* §3.
</details>

<details>
<summary><b>Q11 · Causal and BIBO-stable impulse responses</b></summary>

**Answer: A, D.**

- **(A) Yes.** Zero for `t < 0`, and `∫|h| = 1/2`.
- **(B) No.** `e^{2t}u(t)` grows: `∫|h| = ∞`.
- **(C) No.** `e^{−|t|}` is non-zero for `t < 0`: stable (`∫|h| = 2`) but **non-causal**.
- **(D) Yes.** A pure delay of 3 s: causal, and `∫|δ| = 1`.

*Review:* §4.
</details>

<details>
<summary><b>Q12 · The largest output of a stable system</b></summary>

**Answer: 3.**

`|y(t)| ≤ M∫|h| = 2 × ∫₀^∞ 3e^{−2t}dt = 2 × 1.5 =` **3**, and the bound is reached by the input `x = 2` (for all time), whose output tends to `2 × 1.5`. This is why `∫|h|` is exactly the quantity that decides BIBO stability.

*Review:* §4.
</details>

<details>
<summary><b>Q13 · A causal, stable h[n]</b></summary>

**Answer: A.**

- **(A) Yes.** Zero for `n < 0`, and `Σ(0.5)ⁿ = 2 < ∞`.
- **(B) No.** `2ⁿu[n]` diverges.
- **(C) No.** `(0.5)^{|n|}` is stable (`Σ = 3`) but non-zero for `n < 0`: non-causal.
- **(D) No.** `u[n]` is the accumulator: `Σ|h| = ∞`.

*Review:* §4.
</details>

<details>
<summary><b>Q14 · A sample of h[n] from the step response</b></summary>

**Answer: 0.0625.**

`h[n] = s[n] − s[n − 1]`. For `n ≥ 1`: `(1 − 0.5^{n+1}) − (1 − 0.5ⁿ) = 0.5ⁿ − 0.5^{n+1} = 0.5^{n+1}`, and `h[0] = s[0] = 0.5` fits the same formula. So `h[3] = 0.5⁴ =` **0.0625**.

*Review:* §4.
</details>

<details>
<summary><b>Q15 · The impulse response of a cascade</b></summary>

**Answer: D.**

For LTI systems in cascade `h = h₁ ∗ h₂`. Convolving with `δ(t − 1)` delays the other signal by 1: `h(t) = e^{−(t−1)}u(t − 1)`. (A) delays only the step, not the exponential; (B) advances instead of delaying.

*Review:* §5.
</details>

<details>
<summary><b>Q16 · An LTI system plus a constant</b></summary>

**Answer: C.**

The LTI part is linear and time-invariant, but adding the constant 5 makes the zero input give a **non-zero** output, so the system is **not linear** (it is affine). A constant does not depend on the time origin, so delaying the input just delays the LTI part: the system is still **time-invariant**. (If the added signal were a fixed pulse that is **not** constant, the system would also become time-varying, as in 2025 Q17.)

*Review:* §5.
</details>

<details>
<summary><b>Q17 · A sinusoid through an FIR filter</b></summary>

**Answer: 2.**

The frequency response is `H(e^{jΩ}) = 1 + 2e^{−jΩ} + e^{−j2Ω}`. At `Ω = π/2`: `1 − 2j − 1 = −2j`, so `|H| = 2` and the phase is `−π/2`. The output is `2cos(πn/2 − π/2)`: amplitude **2**. (The DC gain `H(1) = 4` is not the relevant number.)

*Review:* §6.
</details>

<details>
<summary><b>Q18 · Properties of convolution</b></summary>

**Answer: A, B, D.**

- **(A) True** (commutative) and **(D) True** (so the order of cascaded LTI systems does not matter).
- **(B) True** (derivative property: `(x ∗ h)′ = x′ ∗ h = x ∗ h′`).
- **(C) False.** Convolution with `δ(t − t₀)` **shifts**: `x(t) ∗ δ(t − t₀) = x(t − t₀)`; the product `x(t)δ(t − t₀)` is something else (`x(t₀)δ(t − t₀)`).

*Review:* §3, §5.
</details>

<details>
<summary><b>Q19 · A moving-sum filter</b></summary>

**Answer: 3.**

`y[3] = x[1]h[2] + x[2]h[1] + x[3]h[0] = 1 + 1 + 1 =` **3**. The whole convolution is `{1, 2, 3, 3, 2, 1}`: a trapezoid.

*Review:* §2.
</details>

<details>
<summary><b>Q20 · A feedback-free network of LTI blocks</b></summary>

**Answer: B.**

Delays, gains, adders and LTI sub-systems are all linear and time-invariant, and without a feedback loop the interconnection is just their composition, so it is **LTI**. It is **not necessarily causal**: if `h₁` or `h₂` is non-causal the whole system is non-causal (the same diagram, fed with a non-causal `h₁`, gave a non-causal system in the numerical test). (This is 2026 Q47.)

*Review:* §5.
</details>
