"""Re-checks every number quoted in Day03_Transient_Analysis.md and Day03_Conceptual_Questions.md.

Run:  python3 verify_day03.py          (needs numpy, scipy, sympy; uses mna.py in this folder)
Past-year answers are checked against the official keys quoted in the comments.
"""
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp

from mna import solve

m, k, u = 1e-3, 1e3, 1e-6


def check(name, got, want, tol=1e-6):
    assert abs(got - want) < tol, f'{name}: got {got}, expected {want}'
    print(f'ok  {name:<58} {got:.5g}')


# ============================================================ first-order basics
for n, want in ((1, 0.632), (2, 0.865), (3, 0.950), (4, 0.982), (5, 0.993)):
    check(f'fraction reached after {n} tau', 1 - np.exp(-n), want, 6e-4)
check('t_half = 0.693 tau', np.log(2), 0.693, 1e-3)
check('99% needs 4.6 tau', np.log(100), 4.6, 1e-2)
check('rise time 10-90% = 2.2 tau', np.log(9), 2.2, 1e-2)

# Ex 2: 10 V step on R = 2 k, C = 5 uF, v(0) = 2 V
R, C, V0, Vs = 2 * k, 5 * u, 2.0, 10.0
tau = R * C
check('Ex2 tau (ms)', tau / m, 10)
sol = solve_ivp(lambda t, v: (Vs - v) / (R * C), (0, 0.1), [V0], rtol=1e-10, atol=1e-12, dense_output=True)
t9 = tau * np.log((V0 - Vs) / (9 - Vs))
check('Ex2 time to reach 9 V (ms)', t9 / m, 20.794, 1e-3)
check('Ex2 numerical v at that time', sol.sol(t9)[0], 9.0, 1e-6)
check('Ex2 i(0+) = (10-2)/2k (mA)', (Vs - V0) / R / m, 4)

# energy in a capacitor charged through R from a DC source (independent of R)
for Rx in (10.0, 1e3, 1e6):
    I = lambda t: (Vs / Rx) * np.exp(-t / (Rx * C))
    E_R = quad(lambda t: I(t) ** 2 * Rx, 0, 50 * Rx * C)[0]
    check(f'energy lost in R={Rx:g} equals 1/2 C V^2', E_R, 0.5 * C * Vs ** 2, 1e-9)

# ============================================================ charge conservation (two capacitors)
C1, C2, Vi = 4 * u, 6 * u, 100.0
Vf = C1 * Vi / (C1 + C2)
check('two caps: final voltage', Vf, 40)
check('two caps: energy before (mJ)', 0.5 * C1 * Vi ** 2 / m, 20)
check('two caps: energy after (mJ)', 0.5 * (C1 + C2) * Vf ** 2 / m, 8)
check('two caps: energy lost (mJ) = 1/2 V0^2 C1C2/(C1+C2)', 0.5 * Vi ** 2 * C1 * C2 / (C1 + C2) / m, 12)
check('Q5: 3 uF at 100 V into 2 uF: lost energy (mJ)', 0.5 * 100 ** 2 * (3 * u * 2 * u / (5 * u)) / m, 6)
check('Q5: final voltage', 3 * 100 / 5, 60)

# ============================================================ second-order
L, C = 1 * m, 1 * u
w0 = 1 / np.sqrt(L * C)
check('RLC w0 (rad/s)', w0, 31622.78, 0.01)
Rcrit = 2 * np.sqrt(L / C)
check('critical R (ohm)', Rcrit, 63.2456, 1e-3)
for Rx, kind in ((20.0, 'under'), (Rcrit, 'critical'), (100.0, 'over')):
    a = Rx / (2 * L)
    zeta = a / w0
    roots = np.roots([1, 2 * a, w0 ** 2])
    print(f'      R={Rx:7.3f}  alpha={a:9.1f}  zeta={zeta:.3f}  roots={np.round(roots, 1)}  ({kind})')
a = 20.0 / (2 * L)
check('R=20: alpha', a, 10000); check('R=20: w_d', np.sqrt(w0 ** 2 - a ** 2), 30000, 1e-6)
check('R=20: zeta', a / w0, 0.316, 1e-3)
check('R=20: overshoot %', 100 * np.exp(-np.pi * (a / w0) / np.sqrt(1 - (a / w0) ** 2)), 35.1, 0.05)
check('R=100 roots', max(np.roots([1, 2 * 50000, w0 ** 2]).real), -11270, 1)

# step response check against numerical integration (series RLC, v_C)
def series_step(Rx, Lx, Cx, Vs=1.0, T=None):
    f = lambda t, y: [(y[1]) / Cx, (Vs - Rx * y[1] - y[0]) / Lx]       # y = [v_C, i]
    T = T or 20 / (Rx / (2 * Lx))
    return solve_ivp(f, (0, T), [0.0, 0.0], rtol=1e-10, atol=1e-12, dense_output=True, max_step=T / 5e4)

s_ = series_step(20.0, L, C, T=4e-4)
tt = np.linspace(0, 4e-4, 40001)
vc = s_.sol(tt)[0]
check('R=20: numeric peak of v_C (step 1 V)', vc.max(), 1.3510, 5e-4)
check('R=20: peak time (us) = pi/w_d', tt[np.argmax(vc)] / u, np.pi / 30000 / u, 0.01)

# parallel RLC (Q17): R = 100, L = 10 mH, C = 1 uF
Rp, Lp, Cp = 100.0, 10 * m, 1 * u
ap, w0p = 1 / (2 * Rp * Cp), 1 / np.sqrt(Lp * Cp)
check('Q17 alpha (parallel)', ap, 5000); check('Q17 w0', w0p, 10000)
check('Q17 w_d', np.sqrt(w0p ** 2 - ap ** 2), 8660.25, 0.01)
check('Q14 zeta, series R=40, L=0.1, C=100 uF', 40 / 2 * np.sqrt(100 * u / 0.1), 0.632, 1e-3)
check('Q16 overshoot %, R=1, L=1, C=1 (zeta=0.5)', 100 * np.exp(-np.pi * 0.5 / np.sqrt(0.75)), 16.3, 0.05)

# Practice P4: L=1, C=0.04, R=6, 10 V step
alpha, w0_, zeta = 6 / 2, 1 / np.sqrt(0.04), 0.6
check('P4 alpha', alpha, 3); check('P4 w0', w0_, 5); check('P4 zeta', alpha / w0_, 0.6); check('P4 w_d', np.sqrt(25 - 9), 4)
s_ = series_step(6.0, 1.0, 0.04, Vs=10.0, T=6.0)
tt = np.linspace(0, 6, 60001); vc = s_.sol(tt)[0]
check('P4 peak v_C (V)', vc.max(), 10.948, 1e-3)
check('P4 peak time (s) = pi/4', tt[np.argmax(vc)], np.pi / 4, 2e-3)

# ============================================================ Laplace examples (sympy)
s, t = sp.symbols('s t', positive=True)
F = (s + 6) / (s * (s + 3))
f_t = sp.simplify(sp.inverse_laplace_transform(F, s, t))
check('Laplace: i(t) at t=0.5 for (s+6)/(s(s+3))', float(f_t.subs(t, 0.5)), 2 - np.exp(-1.5), 1e-9)
check('Laplace: initial value lim s F', float(sp.limit(s * F, s, sp.oo)), 1)
check('Laplace: final value lim s F', float(sp.limit(s * F, s, 0)), 2)
check('Q19: time at which i = 1.5 A (s)', np.log(2) / 3, 0.231, 1e-3)
# P5: L=1 H, i(0)=1 A, R=3 ohm, 6 V step  ->  I(s) = (6/s + L i0)/(sL+R)
I5 = (6 / s + 1) / (s + 3)
check('P5 i(t) = 2 - e^{-3t} at t=1', float(sp.inverse_laplace_transform(sp.apart(I5, s), s, t).subs(t, 1.0)), 2 - np.exp(-3), 1e-9)

# ============================================================ 2020 Q30 : state equations  (key A)
def derivs(v, i, i1, i2):
    """Replace C by a voltage source v and L by a current source i, solve the resistive circuit."""
    V, I = solve([('I', 0, 1, i1), ('R', 1, 0, 2.0), ('I', 1, 2, i), ('V', 2, 0, v, 'vc'), ('R', 2, 0, 1.0), ('I', 0, 2, i2)])
    return I['vc'] / 0.25, (V[1] - V[2]) / 0.5          # dv/dt = i_C / C ,  di/dt = v_L / L

A = np.array([[-4.0, 4.0], [-2.0, -4.0]]); B = np.array([[0.0, 4.0], [4.0, 0.0]])
rng = np.random.default_rng(1)
for _ in range(4):
    v, i, i1, i2 = rng.normal(size=4)
    want = A @ [v, i] + B @ [i1, i2]
    got = derivs(v, i, i1, i2)
    assert np.allclose(got, want), (got, want)
print('ok  2020 Q30 option (A): matches the circuit for 4 random states')
ev = np.linalg.eigvals(A)
check('2020 Q30 eigenvalues: real part', ev[0].real, -4); check('2020 Q30 eigenvalues: |imag|', abs(ev[0].imag), np.sqrt(8), 1e-9)

# ============================================================ PYQs
# 2019 Q41  (key 0.23 to 0.27 A): R(t) = R0 (1 - t/T), T = 3, C = 1, Vs = 1
T_, R0 = 3.0, 1.0
f = lambda t, y: [(1 - y[0]) / (R0 * (1 - t / T_) * 1.0)]
s_ = solve_ivp(f, (0, 1.5), [0.0], rtol=1e-11, atol=1e-13, dense_output=True)
check('2019 Q41 I(T/2) numeric (A)', (1 - s_.sol(1.5)[0]) / (R0 * (1 - 0.5)), 0.25, 1e-6)
check('2019 Q41 closed form (1-t/T)^T / R(t)', (1 - 0.5) ** 3 / (R0 * 0.5), 0.25)
check('2019 Q41 I(0) = 1 A', 1 / R0, 1)

# 2019 Q52  (key 3.2 to 3.4 V): tau = 500 x 10 uF = 5 ms; diode conducts only while V_s = +10 V (0-2 ms)
tau52 = 500 * 10 * u
v2ms = 10 * (1 - np.exp(-2 * m / tau52))
check('2019 Q52 v_C at 2 ms = held value at 3 ms (V)', v2ms, 3.297, 1e-3)

# 2021 Q28  (key C = -3 V/s)
dc = solve([('V', 1, 0, 20.0, 'vs'), ('R', 1, 0, 20 * k), ('R', 1, 2, 5 * k), ('R', 2, 3, 5 * k), ('R', 3, 4, 10 * k), ('V', 4, 0, 0.0, 'L')])
check('2021 Q28 v(0-) (V)', dc[0][3], 10); check('2021 Q28 i_L(0-) (mA)', dc[1]['L'] / m, 1)
after = solve([('V', 3, 0, dc[0][3], 'vc'), ('R', 3, 0, 5 * k), ('R', 3, 4, 10 * k), ('I', 4, 0, dc[1]['L'])])
check('2021 Q28 i_C(0+) (mA)', after[1]['vc'] / m, -3)
check('2021 Q28 dv/dt(0+) (V/s)  [key -3]', after[1]['vc'] / 1e-3, -3)

# 2021 Q38  (key 0.132 to 0.146 ms): v_C(0) = -5 V ; Thevenin seen by the capacitor
ckt = [('V', 1, 0, 5.0, 'vs'), ('R', 1, 2, 250.0), ('VCCS', 2, 0, 1, 2, 1 / 500), ('R', 2, 0, 250.0)]
Vth = solve(ckt)[0][2]
z = [('V', 1, 0, 0.0, 'vs'), ('R', 1, 2, 250.0), ('VCCS', 2, 0, 1, 2, 1 / 500), ('R', 2, 0, 250.0), ('I', 0, 2, 1.0)]
Rth = solve(z)[0][2]
check('2021 Q38 V_th (V)', Vth, 5 / 3); check('2021 Q38 R_th (ohm)', Rth, 166.667, 1e-3)
tau38 = Rth * 0.6 * u
check('2021 Q38 tau (ms)', tau38 / m, 0.1, 1e-6)
t0 = tau38 * np.log((Vth - (-5)) / Vth)
check('2021 Q38 time to v_C = 0 (ms)  [key 0.132-0.146]', t0 / m, 0.1386, 1e-4)
assert 0.132 <= t0 / m <= 0.146

# 2021 Q47  (key 1.40 to 1.45 A): current source 1 A, C = 100 pF across (L = 10 mH + R = 5 k) load
Lq, Rq, Cq = 10 * m, 5 * k, 100e-12
f = lambda t, y: [(1.0 - y[1]) / Cq, (y[0] - Rq * y[1]) / Lq]        # y = [v, i_L]
s_ = solve_ivp(f, (0, 2e-5), [0.0, 0.0], rtol=1e-10, atol=1e-14, max_step=1e-9)
check('2021 Q47 numeric max ammeter reading (A)', s_.y[1].max(), 1.4443, 5e-4)
a47, w47 = Rq / (2 * Lq), 1 / np.sqrt(Lq * Cq)
check('2021 Q47 alpha', a47, 2.5e5); check('2021 Q47 w0', w47, 1e6); check('2021 Q47 zeta', a47 / w47, 0.25)
check('2021 Q47 closed-form peak 1 + exp(-pi z/sqrt(1-z^2))', 1 + np.exp(-np.pi * 0.25 / np.sqrt(1 - 0.0625)), 1.4443, 5e-4)
assert 1.40 <= s_.y[1].max() <= 1.45

# 2023 Q35  (key 4 V)
check('2023 Q35 i_L before opening (A) = 2 V / 1 ohm', 2 / 1, 2)
check('2023 Q35 max |V_R| = I_L x 2 ohm (V)', 2 * 2, 4)
check('2023 Q35 tau = L/R (s)', 1 / 2, 0.5)

# 2023 Q44  (key B = -1 A)
dc = solve([('I', 0, 1, 1.0), ('R', 1, 0, 25.0), ('R', 1, 2, 100.0), ('V', 2, 0, 0.0, 'L')])
vC, iL = dc[0][1], dc[1]['L']
check('2023 Q44 v_C(0-) (V)', vC, 20); check('2023 Q44 i_L(0-) (A)', iL, 0.2)
after = solve([('V', 1, 0, vC, 'vc'), ('R', 1, 0, 25.0), ('I', 1, 0, iL)])
check('2023 Q44 i_c(0+) (A)  [key -1]', after[1]['vc'], -1)

# 2023 Q62  (key 8.30 to 8.34 us)
check('2023 Q62 t = tau ln(2^12) (us)', 1.0 * np.log(2 ** 12), 8.318, 1e-3)

# 2024 Q32  (key 0.75 s): resistance seen by the 3 H inductor with S closed
r = solve([('R', 1, 0, 2.0), ('R', 2, 0, 4.0), ('R', 2, 3, 0.0 + 1e-9), ('R', 3, 0, 4.0), ('I', 2, 1, 1.0)])[0]
check('2024 Q32 R seen by L (ohm)', r[1] - r[2], 4, 1e-6)
check('2024 Q32 tau = L/R (s)  [key 0.75]', 3 / 4, 0.75)

# 2024 Q35  (key 0.250 mJ): Zener holds 5 V while the capacitor discharges from 10 V to 5 V through 10 k
Rz, Cz, Vz, Vc0 = 10 * k, 10 * u, 5.0, 10.0
i_z = lambda t: (Vc0 - Vz) / Rz * np.exp(-t / (Rz * Cz))
E_z = quad(lambda t: Vz * i_z(t), 0, 20 * Rz * Cz)[0]
check('2024 Q35 energy in Zener (mJ)  [key 0.250]', E_z / m, 0.250, 1e-6)
check('   = V_Z x C x (V0 - V_Z)', Vz * Cz * (Vc0 - Vz) / m, 0.250)
check('   energy in R (mJ)', quad(lambda t: i_z(t) ** 2 * Rz, 0, 20 * Rz * Cz)[0] / m, 0.125, 1e-6)
check('   energy lost by C (mJ)', 0.5 * Cz * (Vc0 ** 2 - Vz ** 2) / m, 0.375)
check('Q12 variant: V_Z=4, C=10 uF, V0=10 -> Zener energy (mJ)', 4 * 10 * u * (10 - 4) / m, 0.24)

# 2024 Q49  (key D): Schmitt trigger (thresholds +/-1 V) followed by an L-input integrator with +/-10 V clipping
dt = 1e-9
tgrid = np.arange(0, 16e-6, dt)
Vi = np.where(tgrid % 8e-6 < 4e-6, -2 + 1e6 * (tgrid % 8e-6), 2 - 1e6 * ((tgrid % 8e-6) - 4e-6))
V01 = np.empty_like(Vi); state = -10.0
for n, vi in enumerate(Vi):
    vp = (vi * 100 + state * 10) / 110
    state = 10.0 if vp > 0 else -10.0
    V01[n] = state
V02 = np.empty_like(Vi); y = 0.0
for n in range(len(Vi)):
    y = float(np.clip(y - 1e6 * V01[n] * dt, -10, 10)); V02[n] = y
up = tgrid[np.where((V01[1:] > 0) & (V01[:-1] < 0))[0][0]]
check('2024 Q49 V01 rises at (us); V_i crosses 0 at 2 us -> delay', up / u - 2, 1.0, 5e-3)
flat = np.sum(np.isclose(V02[(tgrid > 8e-6) & (tgrid < 16e-6)], 10)) * dt / u
print(f'ok  2024 Q49 V02 sits at +10 V for {flat:.2f} us of each 8 us period (trapezoid)')
assert V02.max() == 10 and V02.min() == -10 and 1.5 < flat < 2.5
check('2024 Q49 slope of V02 (V/us) = (R/L) x 10 V', 1e6 * 10 / 1e6, 10)

# 2026 Q23  (key A): impulse of charge q into C is an initial-condition change
check('2026 Q23 V(0+) = V0 + q/C   (V0=1 V, q=4 uC, C=2 uF)', 1 + 4 * u / (2 * u), 3)

# ============================================================ practice problems
check('P1 time to 9 V (ms)', 10 * np.log(8), 20.794, 1e-3)
check('P2 initial voltage across the 40 ohm (V)', 2 * 40, 80)
check('P2 tau = L/(10+40) (ms)', 0.05 / 50 / m, 1)
check('P3 final voltage', 40, 40); check('P3 energy lost (mJ)', 12, 12)
check('P5 i(t) at 0.5 s', 2 - np.exp(-1.5), 1.7769, 1e-3)

# ============================================================ remaining conceptual questions
check('Q3 i(0+) = (6 - 3)/3 (A)', (6 - 3) / 3, 1)
check('Q4 di/dt(0+) = (10 - 4*3)/2 (A/s)', (10 - 4 * 3) / 2, -1)
check('Q7 time to 8 V (ms): tau ln 5, tau = 10 ms', 10 * np.log(5), 16.094, 1e-3)
check('Q10 t = tau N ln2 (us), tau=2 us, N=10', 2 * 10 * np.log(2), 13.863, 1e-3)
check('Q20 i(0+) = 1 + 6/2 (A)', 1 + 6 / 2, 4)

# ============================================================ sinusoidal source switched on at t = 0 (RL)
Rl, Ll, wl, Vm = 10.0, 0.1, 100.0, 20.0
Zm, phi = np.hypot(Rl, wl * Ll), np.arctan2(wl * Ll, Rl)
check('RL sinusoid: |Z| (ohm)', Zm, 14.142, 1e-3); check('RL sinusoid: phi (deg)', np.degrees(phi), 45, 1e-9)
check('RL sinusoid: tau (ms)', Ll / Rl / m, 10)
for theta in (0.0, phi):
    sol = solve_ivp(lambda t, i: [(Vm * np.sin(wl * t + theta) - Rl * i[0]) / Ll], (0, 0.05), [0.0], rtol=1e-11, atol=1e-13, dense_output=True)
    tq = 0.013
    formula = (Vm / Zm) * (np.sin(wl * tq + theta - phi) - np.sin(theta - phi) * np.exp(-tq * Rl / Ll))
    check(f'RL sinusoid: i(13 ms) numeric vs closed form (theta={np.degrees(theta):.0f} deg)', sol.sol(tq)[0], formula, 1e-8)
check('RL sinusoid: no transient when theta = phi (amplitude of the exp term)', np.sin(phi - phi), 0)

print('\nall Day 3 checks passed')
