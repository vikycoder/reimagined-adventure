# Day 7 — 20 Conceptual Questions (Signals and System Properties)

**Companion to:** `Day07_Signals_and_System_Properties.md` (read §1–§6 first)
**Time:** 40 minutes, pencil and paper. A scientific calculator helps for Q8 and Q10.
**Format:** GATE style. Each question tests **one idea**, and the wrong options are the mistakes students actually make.

| Type | How it works | Self-score |
|---|---|---|
| **MCQ** | exactly one correct option | 1 mark if right |
| **MSQ** | one or more correct options; **no partial credit** | 1 mark only if your set is exactly right |
| **NAT** | type a number, no options | 1 mark if right |

Every number in the solutions is re-checked by `tools/verify_day07.py` (the property questions use its numerical tests), and each answer was also derived by hand. `u(t)` is the unit step, `x[n]` a discrete-time signal.

## What is in the set

| # | Type | Concept | Level | Review in the Day 7 note |
|---|---|---|---|---|
| 1 | MSQ | Which signals are periodic | Easy | §2.1 |
| 2 | NAT | Period of a sum of sinusoids | Medium | §2.1 |
| 3 | MCQ | Period of a discrete-time sum | Medium | §2.1 |
| 4 | NAT | Period of a squared sinusoid | Medium | §2.1 |
| 5 | MCQ | Period after scaling and shifting | Medium | §2.1 |
| 6 | NAT | The odd part of a causal signal | Easy | §2.2 |
| 7 | MSQ | Parity rules | Easy | §2.2 |
| 8 | NAT | Energy of a shifted exponential | Medium | §2.3 |
| 9 | MCQ | Which one is an energy signal | Easy | §2.3 |
| 10 | NAT | Power of a sum of sinusoids with a DC term | Medium | §2.3 |
| 11 | NAT | An impulse with a scaled argument | Medium | §3 |
| 12 | MCQ | The sifting property | Medium | §3 |
| 13 | NAT | A value of `x(3 − 2t)` | Medium | §4 |
| 14 | MCQ | Decimation of a discrete-time signal | Medium | §4 |
| 15 | NAT | Energy after scaling and reversal | Hard | §2.3 |
| 16 | MSQ | Which systems are causal | Easy | §5.2 |
| 17 | MCQ | Linear and time-invariant? `t·x(t)` | Medium | §5.3, §5.4 |
| 18 | MCQ | Which system is time-invariant | Medium | §5.4 |
| 19 | MSQ | Which systems are BIBO unstable | Medium | §5.5 |
| 20 | MCQ | An output that proves the system is not LTI | Hard | §6 |

---

## Part A: Classification and periodicity

### Q1 · MSQ
Select **all** periodic signals.

- (A) `x(t) = cos(3πt) + sin(5πt)`
- (B) `x(t) = cos(t) + cos(√2·t)`
- (C) `x[n] = cos(0.4πn)`
- (D) `x[n] = cos(n)`

### Q2 · NAT
The fundamental period of `x(t) = 2cos(0.5πt) + 5sin(0.75πt) + 1` is ______ s.

### Q3 · MCQ
The fundamental period of the discrete-time signal `x[n] = cos(3πn/7) + sin(2πn/5)` is:

- (A) 5
- (B) 14
- (C) 35
- (D) 70

### Q4 · NAT
The fundamental period of `x(t) = sin²(3πt)` is ______ s (round off to three decimal places).

### Q5 · MCQ
A signal `x(t)` has fundamental period 6 s. The fundamental period of `y(t) = x(3t − 1)` is:

- (A) 7/3 s
- (B) 2 s
- (C) 6 s
- (D) 18 s

---

## Part B: Even and odd parts, energy and power

### Q6 · NAT
The odd part of `x(t) = e^{−2t}u(t)`, evaluated at `t = −0.5`, is ______ (round off to two decimal places).

### Q7 · MSQ
Select **all** correct statements.

- (A) The product of two odd signals is even.
- (B) The derivative of an even signal is even.
- (C) An odd signal that is defined at `t = 0` has `x(0) = 0`.
- (D) Every signal can be written as the sum of an even signal and an odd signal.

### Q8 · NAT
The energy of `x(t) = 5e^{−t}u(t − 1)` is ______ (round off to two decimal places).

### Q9 · MCQ
Which one of the following is an **energy** signal?

- (A) `u(t)`
- (B) `cos(2t)`
- (C) `e^{−3|t|}`
- (D) `t·u(t)`

### Q10 · NAT
The average power of `x(t) = 4cos(10t) + 3sin(20t) + 2` is ______ W (for a 1 Ω resistor).

---

## Part C: Impulse and time-axis operations

### Q11 · NAT
The value of `∫_{−∞}^{∞} t²·δ(2t − 4) dt` is ______.

### Q12 · MCQ
The value of `∫_{−∞}^{∞} cos(πt)·[δ(t − 1) + δ(t + 1/3)] dt` is:

- (A) −0.5
- (B) −1.5
- (C) 0.5
- (D) 1.5

### Q13 · NAT
A signal is `x(t) = t` for `0 ≤ t ≤ 1`, `x(t) = 1` for `1 < t ≤ 2`, and `0` otherwise. Then `y(t) = x(3 − 2t)` has `y(1.25) =` ______.

### Q14 · MCQ
A discrete-time signal has `x[0] = 1`, `x[1] = 2`, `x[2] = 3`, `x[3] = 4` and is zero elsewhere. For `y[n] = x[2n − 1]`, the sum `Σₙ y[n]` is:

- (A) 10
- (B) 4
- (C) 2
- (D) 6

### Q15 · NAT
A signal `x(t)` has energy 10. The energy of `y(t) = −2x(0.5t − 3)` is ______.

---

## Part D: System properties

### Q16 · MSQ
Select **all** causal systems.

- (A) `y(t) = x(t − 2)`
- (B) `y(t) = x(t/2)`
- (C) `y(t) = ∫_{−∞}^{t} x(τ)dτ`
- (D) `y(t) = x(t) + x(t + 1)`

### Q17 · MCQ
The system `y(t) = t·x(t)` is:

- (A) linear and time-invariant
- (B) non-linear and time-invariant
- (C) linear and time-varying
- (D) non-linear and time-varying

### Q18 · MCQ
Which one of the following systems is **time-invariant**?

- (A) `y(t) = x²(t)`
- (B) `y(t) = x(t²)`
- (C) `y(t) = x(t)·cos t`
- (D) `y(t) = x(−t)`

### Q19 · MSQ
Select **all** BIBO-**unstable** systems.

- (A) `y(t) = ∫_{−∞}^{t} x(τ)dτ`
- (B) `y(t) = ∫_{t−1}^{t} x(τ)dτ`
- (C) `y(t) = t·x(t)`
- (D) `y(t) = e^{x(t)}`

### Q20 · MCQ
A system is excited with the input `cos(2t)`. For which of the following outputs can you conclude that the system is **not** LTI?

- (A) `3cos(2t − 1)`
- (B) `−cos(2t)`
- (C) `cos(2t) + cos(4t)`
- (D) `0`

---

## Score yourself

<details>
<summary><b>Answer key (open after you finish all 20)</b></summary>

| Q | Answer | Q | Answer |
|---|---|---|---|
| 1 | A, C | 11 | 2 (range 2 to 2) |
| 2 | 8 (range 8 to 8) | 12 | A |
| 3 | D | 13 | 0.5 (range 0.5 to 0.5) |
| 4 | 0.333 (range 0.332 to 0.334) | 14 | D |
| 5 | B | 15 | 80 (range 80 to 80) |
| 6 | -0.18 (range -0.19 to -0.18) | 16 | A, C |
| 7 | A, C, D | 17 | C |
| 8 | 1.69 (range 1.68 to 1.70) | 18 | A |
| 9 | C | 19 | A, C |
| 10 | 16.5 (range 16.5 to 16.5) | 20 | C |

**How to read your score**

| Score | What to do |
|---|---|
| 17–20 | You are ready for Day 8 (convolution and LTI systems). |
| 13–16 | Re-read the "Review" section for each question you missed, then redo only those questions tomorrow. |
| 12 or less | Re-read §2–§5 of the Day 7 note, redo the worked examples with the solution covered, then retake this set after 24 hours. |

Keep a note of **why** each miss happened: concept gap, a scaling or shifting slip, or a definition mixed up (energy/power, linear/affine). Those are three different fixes.

</details>

## Solutions

<details>
<summary><b>Q1 · Which signals are periodic</b></summary>

**Answer: A, C.**

- **(A) Periodic.** The periods are `2π/3π = 2/3 s` and `2π/5π = 2/5 s`; their ratio `5/3` is rational, and `3 × 2/3 = 5 × 2/5 =` **2 s**.
- **(B) Not periodic.** The periods are `2π` and `2π/√2`, whose ratio `√2` is irrational.
- **(C) Periodic.** `Ω₀/2π = 0.4π/2π = 1/5`, so `N = 5`.
- **(D) Not periodic.** `Ω₀/2π = 1/(2π)` is irrational. A discrete-time sinusoid is periodic only if `Ω₀/2π` is rational.

*Review:* §2.1.
</details>

<details>
<summary><b>Q2 · Period of a sum</b></summary>

**Answer: 8 s.**

The DC term and the amplitudes do not matter. The periods are `2π/0.5π = 4 s` and `2π/0.75π = 8/3 s`. Their ratio `4/(8/3) = 3/2` is rational, and `lcm = 3 × 8/3 = 2 × 4 =` **8 s**. (In frequencies: `0.25 Hz` and `0.375 Hz` have GCD `0.125 Hz`, so `T = 8 s`.) Taking the largest period (4 s) is the usual wrong answer.

*Review:* §2.1.
</details>

<details>
<summary><b>Q3 · Period of a discrete-time sum</b></summary>

**Answer: D.**

`cos(3πn/7)`: `Ω₀/2π = 3/14`, so `N₁ = 14`. `sin(2πn/5)`: `Ω₀/2π = 1/5`, so `N₂ = 5`. The sum has period `lcm(14, 5) =` **70**. (35 comes from reading the 7 in the denominator as the period; 14 and 5 are the periods of the parts.)

*Review:* §2.1.
</details>

<details>
<summary><b>Q4 · Period of a squared sinusoid</b></summary>

**Answer: 0.333 s.**

`sin²(3πt) = (1 − cos 6πt)/2`, whose period is `2π/6π = 1/3 s`. Squaring **halves** the period of `sin(3πt)` (which is `2/3 s`).

*Review:* §2.1.
</details>

<details>
<summary><b>Q5 · Period after scaling and shifting</b></summary>

**Answer: B.**

Time scaling by 3 divides the period: `6/3 = 2 s`. The shift by `1/3` (since `3t − 1 = 3(t − 1/3)`) does not change the period. (A) adds the shift to the period; (C) ignores the scaling; (D) multiplies instead of dividing.

*Review:* §2.1.
</details>

<details>
<summary><b>Q6 · The odd part of a causal signal</b></summary>

**Answer: −0.18.**

`x_o(t) = ½[x(t) − x(−t)]`. At `t = −0.5`: `x(−0.5) = 0` (causal) and `x(0.5) = e^{−1}`, so `x_o(−0.5) = ½(0 − 0.368) = −0.184`. (The even part at the same point is `+0.184`: the two parts cancel for `t < 0` so that their sum, `x(−0.5)`, is zero.)

*Review:* §2.2.
</details>

<details>
<summary><b>Q7 · Parity rules</b></summary>

**Answer: A, C, D.**

- **(A) True.** Odd × odd is even; so is even × even.
- **(B) False.** The derivative of an even signal is **odd** (and the derivative of an odd signal is even).
- **(C) True.** If `x` is odd and defined at 0, then `x(0) = −x(0)`, so `x(0) = 0`.
- **(D) True.** `x = ½[x(t) + x(−t)] + ½[x(t) − x(−t)]`, and the decomposition is unique.

*Review:* §2.2.
</details>

<details>
<summary><b>Q8 · Energy of a shifted exponential</b></summary>

**Answer: 1.69.**

`E = ∫₁^∞ 25e^{−2t}dt = 25e^{−2}/2 = 1.69`. (The signal starts at `5e^{−1} = 1.84`, not at 5, because the exponential `e^{−t}` is not shifted along with the step. Writing `E = 25/2 = 12.5` forgets the factor `e^{−2}`.)

*Review:* §2.3.
</details>

<details>
<summary><b>Q9 · Energy signals</b></summary>

**Answer: C.**

`e^{−3|t|}`: `E = 2∫₀^∞ e^{−6t}dt = 1/3`, finite, and `P = 0`: an energy signal. `u(t)` (`P = ½`) and `cos(2t)` (`P = ½`) are **power** signals with infinite energy. `t·u(t)` has infinite energy **and** infinite power: neither.

*Review:* §2.3.
</details>

<details>
<summary><b>Q10 · Power of a sum of sinusoids</b></summary>

**Answer: 16.5 W.**

Components at different frequencies (0, 10 and 20 rad/s) do not interact, so the powers add: `4²/2 + 3²/2 + 2² = 8 + 4.5 + 4 = 16.5 W`. Adding the amplitudes first, `(4 + 3 + 2)²/2`, is wrong.

*Review:* §2.3.
</details>

<details>
<summary><b>Q11 · An impulse with a scaled argument</b></summary>

**Answer: 2.**

`δ(2t − 4) = δ(2(t − 2)) = ½δ(t − 2)`. So `∫t²·½δ(t − 2)dt = ½ × 2² =` **2**. (Forgetting the `1/|a| = ½` gives 4.)

*Review:* §3.
</details>

<details>
<summary><b>Q12 · The sifting property</b></summary>

**Answer: A.**

Each impulse picks the value of `cos(πt)` at its location: `cos(π·1) + cos(π·(−1/3)) = −1 + 0.5 =` **−0.5**.

*Review:* §3.
</details>

<details>
<summary><b>Q13 · A value of x(3 − 2t)</b></summary>

**Answer: 0.5.**

`y(1.25) = x(3 − 2 × 1.25) = x(0.5)`, and on `[0, 1]` the signal is `x(t) = t`, so `y(1.25) = 0.5`. (Check with the edges: `y` lives on `[0.5, 1.5]`, equals 1 on `[0.5, 1]`, then falls linearly to 0, so at `t = 1.25` it is halfway: 0.5.)

*Review:* §4.
</details>

<details>
<summary><b>Q14 · Decimation</b></summary>

**Answer: D.**

`y[n] = x[2n − 1]` reads `x` at odd indices only: `n = 1 ⇒ x[1] = 2`, `n = 2 ⇒ x[3] = 4`, and the other values (`x[−1]`, `x[5]`, …) are 0. The sum is `2 + 4 =` **6**. The even-indexed samples (1 and 3) are discarded.

*Review:* §4.
</details>

<details>
<summary><b>Q15 · Energy after scaling and reversal</b></summary>

**Answer: 80.**

`E_y = a²E_x/|b|` with `a = −2`, `b = 0.5`: `E_y = 4 × 10/0.5 =` **80**. The shift by 3 and the sign of `a` do not matter; stretching time by 2 doubles the energy. (Using `×|b|` instead of `÷|b|` gives 20.)

*Review:* §2.3.
</details>

<details>
<summary><b>Q16 · Causal systems</b></summary>

**Answer: A, C.**

- **(A) Causal.** It looks 2 s into the past.
- **(B) Not causal.** For `t < 0`, `t/2 > t` (at `t = −4` it needs `x(−2)`).
- **(C) Causal.** The integral up to `t` uses only the past.
- **(D) Not causal.** It uses `x(t + 1)`.

*Review:* §5.2.
</details>

<details>
<summary><b>Q17 · t·x(t)</b></summary>

**Answer: C.**

**Linear:** `t(a x₁ + b x₂) = a·t x₁ + b·t x₂`. **Time-varying:** the response to `x(t − t₀)` is `t·x(t − t₀)`, but `y(t − t₀) = (t − t₀)·x(t − t₀)`. (It is also causal, memoryless and BIBO-*unstable*.)

*Review:* §5.3, §5.4.
</details>

<details>
<summary><b>Q18 · Time-invariant systems</b></summary>

**Answer: A.**

`y = x²` is a memoryless function of `x` alone, with no explicit `t`: the response to `x(t − t₀)` is `x²(t − t₀) = y(t − t₀)`. The others are time-varying: `x(t²)` and `x(−t)` change the argument in a way that is not a shift, and `x(t)cos t` has an explicit `t`. (`y = x²` is non-linear, but the question asks only about time invariance.)

*Review:* §5.4.
</details>

<details>
<summary><b>Q19 · BIBO-unstable systems</b></summary>

**Answer: A, C.**

- **(A) Unstable.** The integrator turns the bounded step `u(t)` into the unbounded ramp.
- **(B) Stable.** `|y| ≤ ∫_{t−1}^{t}|x| ≤ M`.
- **(C) Unstable.** The bounded input `x = 1` gives `y = t`.
- **(D) Stable.** If `|x| ≤ M` then `e^{−M} ≤ y ≤ e^{M}`.

*Review:* §5.5.
</details>

<details>
<summary><b>Q20 · An output that proves the system is not LTI</b></summary>

**Answer: C.**

An LTI system turns `cos(2t)` into `|H(j2)|cos(2t + ∠H(j2))`: the **same frequency**, with a new amplitude and phase. (A) `3cos(2t − 1)` is possible (gain 3, phase −1 rad), (B) `−cos(2t)` is possible (gain 1, phase π), and (D) `0` is possible (`H(j2) = 0`, e.g. a notch filter). But **(C) contains 4 rad/s**, a frequency the input does not have, so the system cannot be LTI.

*Review:* §6.
</details>
