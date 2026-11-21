"""Re-checks every number in Day07_Signals_and_System_Properties.md and Day07_Conceptual_Questions.md.

Run:  python3 verify_day07.py            (needs numpy)
      python3 verify_day07.py --tables   also prints the system-property tables of the note as markdown

The classification tables of the note are the OUTPUT of numerical property tests (signals_lib.py), not hand-made.
Past-year answers are checked against the official keys quoted in the comments.
"""
import sys

import numpy as np

import signals_lib as S
from signals_lib import u

pi = np.pi


def check(name, got, want, tol=1e-6):
    assert abs(got - want) < tol, f'{name}: got {got}, expected {want}'
    print(f'ok  {name:<72} {got:.6g}')


# ====================================================================================== periodicity
def period_ct(x, step, tmax):
    return S.smallest_period(x, np.arange(step, tmax, step), tol=1e-7)


f19 = lambda t: 1 + 2 * np.cos(pi * t) + 3 * np.sin(2 * pi * t / 3) + 4 * np.cos(pi * t / 2 + pi / 4)
check('2019 Q21 fundamental period of 1 + 2cos(pi t) + 3 sin(2 pi t/3) + 4cos(pi t/2 + pi/4)  [key 12]', period_ct(f19, 0.01, 30), 12.0, 1e-9)
check('   component periods 2, 3, 4 -> lcm', np.lcm.reduce([2, 3, 4]), 12)
check('Ex1 cos(2 pi t) + cos(3 pi t): periods 1 and 2/3', period_ct(lambda t: np.cos(2 * pi * t) + np.cos(3 * pi * t), 0.01, 10), 2.0, 1e-9)
check('Q2 2cos(0.5 pi t) + 5 sin(0.75 pi t) + 1', period_ct(lambda t: 2 * np.cos(0.5 * pi * t) + 5 * np.sin(0.75 * pi * t) + 1, 0.01, 40), 8.0, 1e-9)
check('P1 cos(6 pi t) + sin(4 pi t) + cos(10 pi t + 1)', period_ct(lambda t: np.cos(6 * pi * t) + np.sin(4 * pi * t) + np.cos(10 * pi * t + 1), 0.01, 5), 1.0, 1e-9)
check('Q4 sin^2(3 pi t): period 1/3', S.smallest_period(lambda t: np.sin(3 * pi * t) ** 2, np.arange(1, 3001) / 3000.0, tol=1e-9), 1 / 3, 1e-9)
check('   identity sin^2 = (1 - cos 2x)/2 (max error)', np.max(np.abs(np.sin(np.linspace(0, 9, 1000)) ** 2 - (1 - np.cos(2 * np.linspace(0, 9, 1000))) / 2)), 0.0, 1e-12)
x6 = lambda t: np.cos(2 * pi * t / 6) + 0.5 * np.sin(4 * pi * t / 6)
check('Q5 base signal has period 6', period_ct(x6, 0.01, 12), 6.0, 1e-9)
check('Q5 x(3t - 1) has period 2', period_ct(lambda t: x6(3 * t - 1), 0.005, 12), 2.0, 1e-9)
check('cos(t) + cos(sqrt 2 t) is not periodic up to T = 400 (best error)', min(np.max(np.abs((lambda tt: np.cos(tt) + np.cos(np.sqrt(2) * tt))(np.linspace(0, 50, 2000) + T) - (lambda tt: np.cos(tt) + np.cos(np.sqrt(2) * tt))(np.linspace(0, 50, 2000))))
                                                                                    for T in np.arange(0.05, 400, 0.05)) > 1e-3, 1.0, 0.5)
# discrete time
check('DT cos(0.4 pi n): Omega/2pi = 1/5 -> N = 5', S.dt_smallest_period(lambda n: np.cos(0.4 * pi * np.asarray(n))), 5)
check('DT cos(3 pi n/7): 3/14 -> N = 14', S.dt_smallest_period(lambda n: np.cos(3 * pi * np.asarray(n) / 7)), 14)
check('DT sin(2 pi n/5): N = 5', S.dt_smallest_period(lambda n: np.sin(2 * pi * np.asarray(n) / 5)), 5)
check('Q3 cos(3 pi n/7) + sin(2 pi n/5): N = 70', S.dt_smallest_period(lambda n: np.cos(3 * pi * np.asarray(n) / 7) + np.sin(2 * pi * np.asarray(n) / 5), 200), 70)
check('   lcm(14, 5)', np.lcm(14, 5), 70)
assert S.dt_smallest_period(lambda n: np.cos(np.asarray(n, dtype=float)), 500) is None
print('ok  DT cos(n) has no period up to N = 500')
check('DT Omega and Omega + 2 pi are the same signal (max difference)', np.max(np.abs(np.cos(0.9 * np.arange(50)) - np.cos((0.9 + 2 * pi) * np.arange(50)))), 0.0, 1e-9)

# ====================================================================================== even / odd
t = np.linspace(-30, 30, 3_000_001)
H = np.where(t > 0, 1.0, np.where(t == 0, 0.5, 0.0))
x = np.exp(-t) * H
xr = np.exp(t) * (1 - H)
xe, xo = (x + xr) / 2, (x - xr) / 2
Ex = np.trapezoid(x ** 2, t)
check('Ex3 energy of e^{-t}u(t)', Ex, 0.5, 5e-5)
check('Ex3 energy of the even part', np.trapezoid(xe ** 2, t), 0.25, 5e-5); check('Ex3 energy of the odd part', np.trapezoid(xo ** 2, t), 0.25, 5e-5)
check('   E_x = E_even + E_odd', np.trapezoid(xe ** 2, t) + np.trapezoid(xo ** 2, t), Ex, 5e-5)
check('Q6 odd part of e^{-2t}u(t) at t = -0.5', 0.5 * (np.exp(-2 * -0.5) * (-0.5 >= 0) - np.exp(-2 * 0.5) * (0.5 >= 0)), -0.18394, 1e-5)
check('   even part of e^{-t}u(t) at t = -1 is e^{-1}/2', 0.5 * np.exp(-1), 0.18394, 1e-5)
pt = np.linspace(-3, 3, 7)
poly = lambda s: 1 + 2 * s + 3 * s ** 2 - s ** 3
check('P3 even part of 1 + 2t + 3t^2 - t^3 is 1 + 3t^2', np.max(np.abs((poly(pt) + poly(-pt)) / 2 - (1 + 3 * pt ** 2))), 0.0, 1e-12)
check('P3 odd part is 2t - t^3', np.max(np.abs((poly(pt) - poly(-pt)) / 2 - (2 * pt - pt ** 3))), 0.0, 1e-12)
g = np.linspace(-2, 2, 4001)
check('odd x odd is even (max asymmetry)', np.max(np.abs((g ** 3 * np.sin(g)) - (g ** 3 * np.sin(g))[::-1])), 0.0, 1e-12)
check('integral of an odd signal over [-a, a] is 0', np.trapezoid(g ** 3 * np.cos(g), g), 0.0, 1e-12)

# ====================================================================================== energy and power
tt = np.linspace(-60, 60, 6_000_001)
check('energy of e^{-t}u(t)', S.energy(lambda s: np.exp(-s) * u(s), -5, 60, 6_000_001), 0.5, 1e-5)
check('P2a energy of 3e^{-2t}u(t) = 9/4', S.energy(lambda s: 3 * np.exp(-2 * s) * u(s), -5, 40, 6_000_001), 2.25, 2e-4)
check('Q8 energy of 5e^{-t}u(t - 1) = 25e^{-2}/2', S.energy(lambda s: 5 * np.exp(-s) * u(s - 1), -5, 60, 6_000_001), 25 * np.exp(-2) / 2, 1e-4)
check('Q9 energy of e^{-3|t|} = 1/3', S.energy(lambda s: np.exp(-3 * np.abs(s)), -30, 30, 6_000_001), 1 / 3, 1e-6)
check('energy of sinc(t) = 1', S.energy(S.sinc, -2000, 2000, 8_000_001), 1.0, 2e-3)
check('power of u(t): (1/2T) int_{-T}^{T}', np.trapezoid(u(np.linspace(-1000, 1000, 2_000_001)) ** 2, np.linspace(-1000, 1000, 2_000_001)) / 2000, 0.5, 1e-5)
check('power of A cos(w t) is A^2/2 (A = 4)', S.avg_power(lambda s: 4 * np.cos(10 * s), 2 * pi / 10), 8.0, 1e-6)
check('P2b power of 6cos(50t) - 8sin(50t) = 50', S.avg_power(lambda s: 6 * np.cos(50 * s) - 8 * np.sin(50 * s), 2 * pi / 50), 50.0, 1e-6)
check('Q10 power of 4cos(10t) + 3sin(20t) + 2 = 8 + 4.5 + 4', S.avg_power(lambda s: 4 * np.cos(10 * s) + 3 * np.sin(20 * s) + 2, 2 * pi / 10, n=2_000_001), 16.5, 1e-6)
# the energy of r(t) and e^{t}u(t) grows without bound
for name, fx in (('r(t)', lambda s: s * u(s)), ('e^t u(t)', lambda s: np.exp(s) * u(s))):
    e1, e2 = S.energy(fx, -1, 10, 1_000_001), S.energy(fx, -1, 20, 1_000_001)
    assert e2 > 5 * e1; print(f'ok  {name}: energy grows without bound ({e1:.4g} -> {e2:.4g}), so it is not an energy signal; its average power also diverges')
# DT energy and power
n = np.arange(0, 4000)
check('DT energy of 0.5^n u[n] = 1/(1 - 0.25) = 4/3', np.sum(0.5 ** (2.0 * n)), 4 / 3, 1e-12)
check('DT power of u[n] = 1/2', np.sum(np.ones(2 * 10 ** 6 + 1)[: 10 ** 6 + 1]) / (2 * 10 ** 6 + 1), 0.5, 1e-5)

# ====================================================================================== standard signals and the impulse
eps = 1e-3
dlt = lambda s: np.exp(-s ** 2 / (2 * eps ** 2)) / (eps * np.sqrt(2 * pi))          # narrow Gaussian standing in for delta
s_ = np.linspace(-6, 6, 12_000_001)
check('Q11 int t^2 delta(2t - 4) dt = 2 (scaling property)', np.trapezoid(s_ ** 2 * dlt(2 * s_ - 4), s_), 2.0, 1e-3)
check('   delta(2t) integrates to 1/2', np.trapezoid(dlt(2 * s_), s_), 0.5, 1e-6)
check('Q12 int cos(pi t)[delta(t - 1) + delta(t + 1/3)] dt', np.trapezoid(np.cos(pi * s_) * (dlt(s_ - 1) + dlt(s_ + 1 / 3)), s_), -0.5, 1e-3)
check('   delta(-t) = delta(t): int t^2 delta(-t + 1) dt', np.trapezoid(s_ ** 2 * dlt(-s_ + 1), s_), 1.0, 1e-3)
check('Ex  int (t^2 + 1) delta(3t - 6) dt = 5/3', np.trapezoid((s_ ** 2 + 1) * dlt(3 * s_ - 6), s_), 5 / 3, 1e-3)
check('   delta(t^2 - 4) = [delta(t - 2) + delta(t + 2)]/4: int t delta(t^2 - 4)... = (2 - 2)/4 = 0 for f(t) = t', np.trapezoid(s_ * dlt(s_ ** 2 - 4), s_), 0.0, 5e-3)
check('   int e^{-t} delta(t^2 - 4) dt = (e^{-2} + e^{2})/4', np.trapezoid(np.exp(-s_) * dlt(s_ ** 2 - 4), s_), (np.exp(-2) + np.exp(2)) / 4, 5e-3)
check('ramp is the integral of the step: r(2) = 2', np.trapezoid(u(np.linspace(-5, 2, 700001)), np.linspace(-5, 2, 700001)), 2.0, 1e-4)
check('normalised sinc: zeros at the non-zero integers (max |sinc(k)|)', np.max(np.abs(S.sinc(np.arange(1, 10)))), 0.0, 1e-12)
check('integral of sinc over the real line is 1', np.trapezoid(S.sinc(np.linspace(-20000, 20000, 20_000_001)), np.linspace(-20000, 20000, 20_000_001)), 1.0, 2e-4)
nn = np.arange(-8, 9)
dn = (nn == 0).astype(float); un = (nn >= 0).astype(float)
check('DT: delta[n] = u[n] - u[n-1]', np.max(np.abs(dn - (un - np.concatenate([[0.0], un[:-1]])))), 0.0, 1e-12)
check('DT: u[n] = sum_{k<=n} delta[k]', np.max(np.abs(np.cumsum(dn) - un)), 0.0, 1e-12)

# ====================================================================================== operations on the time axis
xf = lambda s: np.where((s >= 0) & (s <= 1), s, np.where((s > 1) & (s <= 2), 1.0, 0.0))
check('Q13 y(t) = x(3 - 2t) at t = 1.25 (argument 0.5)', float(xf(3 - 2 * 1.25)), 0.5, 1e-12)
tg = np.linspace(-4, 5, 90001)
supp = lambda y: (tg[y > 0].min(), tg[y > 0].max())
y1 = xf(-2 * tg + 1)
check('Ex5 x(-2t + 1): left edge of the support', supp(y1)[0], -0.5, 2e-4); check('Ex5 x(-2t + 1): right edge of the support', supp(y1)[1], 0.5, 2e-4)
check('Ex5 same by "scale first, then shift": x(-2(t - 1/2))', np.max(np.abs(xf(-2 * (tg - 0.5)) - y1)), 0.0, 1e-12)
y2 = xf(3 - 2 * tg)
check('P4 x(3 - 2t): support starts at 0.5', supp(y2)[0], 0.5, 2e-4); check('P4 x(3 - 2t): support ends at 1.5', supp(y2)[1], 1.5, 2e-4)
check('P4 plateau (value 1) ends at t = 1 (argument 1)', float(xf(3 - 2 * 1.0)), 1.0, 1e-12)
# energy under a x(bt + c) = a^2 E / |b|
x_e = lambda s: np.where((s >= 0) & (s < 1), 2.0, 0.0)
tq = np.linspace(-5, 8, 13_000_001)
Ex_ = np.trapezoid(x_e(tq) ** 2, tq)
Ey_ = np.trapezoid((3 * x_e(-3 * tq + 5)) ** 2, tq)
check('2026 Q43 E[x]', Ex_, 4.0, 1e-3); check('2026 Q43 E[3x(-3t + 5)]', Ey_, 12.0, 1e-2); check('2026 Q43 ratio  [key C = 1/3]', Ex_ / Ey_, 1 / 3, 1e-3)
check('2026 Q43 formula a^2 E/|b|', 9 * 4 / 3, 12.0)
xp = lambda s: np.sqrt(5.0) * np.where(np.abs(s / 2) < 0.5, 1.0, 0.0)           # E = 5 * 2 = 10
check('Q15 energy of x', np.trapezoid(xp(tq) ** 2, tq), 10.0, 1e-3)
check('Q15 energy of -2x(0.5t - 3)  (= 4 * 10 / 0.5)', np.trapezoid((-2 * xp(0.5 * tq - 3)) ** 2, tq), 80.0, 1e-2)
check('   power is unchanged by time scaling: P of cos(3t) and of cos(6t)', S.avg_power(lambda s: np.cos(3 * s), 2 * pi / 3), S.avg_power(lambda s: np.cos(6 * s), 2 * pi / 6), 1e-9)
# discrete time operations
xd = np.zeros(8); xd[:4] = [1, 2, 3, 4]
xdn = lambda k: np.where((np.asarray(k) >= 0) & (np.asarray(k) < 4), np.array([1, 2, 3, 4])[np.clip(np.asarray(k), 0, 3)], 0)
ns = np.arange(-6, 12)
check('Q14 sum of y[n] = x[2n - 1]', float(np.sum(xdn(2 * ns - 1))), 6.0, 1e-12)
check('   x[2n] keeps 2 samples (1 and 3): sum', float(np.sum(xdn(2 * ns))), 4.0, 1e-12)
check('   x[n/2] zero-stuffed then x[2n] returns x[n] (max error)', np.max(np.abs(np.where((2 * ns) % 2 == 0, xdn((2 * ns) // 2), 0) - xdn(ns))), 0.0, 1e-12)

# ====================================================================================== system properties (numerical tests)
CT_EXPECT = {
    'x(t - 2)':         dict(linear=1, ti=1, causal=1, memoryless=0, stable=1),
    'x(t + 2)':         dict(linear=1, ti=1, causal=0, memoryless=0, stable=1),
    'x(-t)':            dict(linear=1, ti=0, causal=0, memoryless=0, stable=1),
    'x(2t)':            dict(linear=1, ti=0, causal=0, memoryless=0, stable=1),
    'x(t/2)':           dict(linear=1, ti=0, causal=0, memoryless=0, stable=1),
    'x(t^2)':           dict(linear=1, ti=0, causal=0, memoryless=0, stable=1),
    'x(e^t)':           dict(linear=1, ti=0, causal=0, memoryless=0, stable=1),
    't x(t)':           dict(linear=1, ti=0, causal=1, memoryless=1, stable=0),
    'x(t)^2':           dict(linear=0, ti=1, causal=1, memoryless=1, stable=1),
    'x(t) + 1':         dict(linear=0, ti=1, causal=1, memoryless=1, stable=1),
    '|x(t)|':           dict(linear=0, ti=1, causal=1, memoryless=1, stable=1),
    'e^x(t)':           dict(linear=0, ti=1, causal=1, memoryless=1, stable=1),
    'x(t) cos(2 pi t)': dict(linear=1, ti=0, causal=1, memoryless=1, stable=1),
    'dx/dt':            dict(linear=1, ti=1, causal=1, memoryless=0, stable=0),
    'int_{-inf}^t x':   dict(linear=1, ti=1, causal=1, memoryless=0, stable=0),
    'int_{t-1}^t x':    dict(linear=1, ti=1, causal=1, memoryless=0, stable=1),
}
DT_EXPECT = {
    'x[n - 2]':              dict(linear=1, ti=1, causal=1, memoryless=0, stable=1),
    'x[n + 1]':              dict(linear=1, ti=1, causal=0, memoryless=0, stable=1),
    'x[-n]':                 dict(linear=1, ti=0, causal=0, memoryless=0, stable=1),
    'x[2n]':                 dict(linear=1, ti=0, causal=0, memoryless=0, stable=1),
    'x[n/2] (zero stuffed)': dict(linear=1, ti=0, causal=0, memoryless=0, stable=1),
    'n x[n]':                dict(linear=1, ti=0, causal=1, memoryless=1, stable=0),
    'x[n] - x[n - 1]':       dict(linear=1, ti=1, causal=1, memoryless=0, stable=1),
    '(x[n+1] + x[n-1])/2':   dict(linear=1, ti=1, causal=0, memoryless=0, stable=1),
    'sum_{k<=n} x[k]':       dict(linear=1, ti=1, causal=1, memoryless=0, stable=0),
    'max_{k<=n} |x[k]|':     dict(linear=0, ti=1, causal=1, memoryless=0, stable=1),
    'x[n]^2':                dict(linear=0, ti=1, causal=1, memoryless=1, stable=1),
    'x[n] x[n - 1]':         dict(linear=0, ti=1, causal=1, memoryless=0, stable=1),
}
# extra systems used in the practice problems and questions
A_ = lambda s: np.asarray(s, dtype=float)
EXTRA_CT = {
    'x(t) + x(t + 1)':      (lambda x: (lambda s: x(A_(s)) + x(A_(s) + 1)), dict(linear=1, ti=1, causal=0, memoryless=0, stable=1)),
    'x(t) + x(-t)':         (lambda x: (lambda s: x(A_(s)) + x(-A_(s))), dict(linear=1, ti=0, causal=0, memoryless=0, stable=1)),
}
results = {}
for name, system in S.CT_SYSTEMS.items():
    p = S.properties(system)
    results[name] = p
    assert {k: int(v) for k, v in p.items()} == CT_EXPECT[name], (name, p, CT_EXPECT[name])
print(f'ok  all {len(S.CT_SYSTEMS)} continuous-time systems classified as expected by the numerical tests')
dt_results = {}
for name, system in S.DT_SYSTEMS.items():
    p = S.dt_properties(system)
    dt_results[name] = p
    assert {k: int(v) for k, v in p.items()} == DT_EXPECT[name], (name, p, DT_EXPECT[name])
print(f'ok  all {len(S.DT_SYSTEMS)} discrete-time systems classified as expected by the numerical tests')
for name, (system, want) in EXTRA_CT.items():
    p = S.properties(system)
    assert {k: int(v) for k, v in p.items()} == want, (name, p, want)
    print(f'ok  {name:<22}', {k: bool(v) for k, v in p.items()})
# P5 (a): int_{t-2}^{t+1} x : linear, TI, NON-causal, memory, stable   (checked with a cumulative-integral implementation)
def window_2_1(x):
    C = S._cumulative(x)
    return lambda s: C(np.asarray(s, dtype=float) + 1.0) - C(np.asarray(s, dtype=float) - 2.0)
p = S.properties(window_2_1)
assert {k: int(v) for k, v in p.items()} == dict(linear=1, ti=1, causal=0, memoryless=0, stable=1), p
print('ok  P5a  int_{t-2}^{t+1} x  ', {k: bool(v) for k, v in p.items()})
# P5 (b): y[n] = x[n] cos(0.2 pi n): linear, TV, causal, memoryless, stable
pb = S.dt_properties(lambda x: (lambda k: x(k) * np.cos(0.2 * pi * np.asarray(k, dtype=float))))
assert {k: int(v) for k, v in pb.items()} == dict(linear=1, ti=0, causal=1, memoryless=1, stable=1), pb
print('ok  P5b  x[n] cos(0.2 pi n) ', {k: bool(v) for k, v in pb.items()})
# a few more used in questions
pq = S.properties(lambda x: (lambda s: A_(s) * x(A_(s))))
print('ok  Q17 t x(t):', {k: int(v) for k, v in pq.items()}, '-> linear and time-varying')
assert pq['linear'] and not pq['ti']

# 2023 Q26 y(t) = x(e^t): argument e^t exceeds t for every t
tg2 = np.linspace(-30, 30, 100001)
check('2023 Q26 [key B]: e^t - t is positive for all t (min over the grid)', float(np.min(np.exp(tg2) - tg2)), 1.0, 1e-3)
print('ok  2023 Q26 y(t) = x(e^t) is non-causal and time-varying   [key B]')

# 2020 Q5: y[n] = max_{k<=n} |x[k]|
imp = (np.arange(-5, 15) == 0).astype(float)
yimp = np.maximum.accumulate(np.abs(imp))
checkm_ = np.max(np.abs(yimp - (np.arange(-5, 15) >= 0)))
check('2020 Q5 impulse response is u[n]  [key C]', checkm_, 0.0, 1e-12)
x1_, x2_ = (np.arange(-5, 15) == 0).astype(float), (np.arange(-5, 15) == 1).astype(float)
check('2020 Q5 additivity fails: y(x1 + x2) differs from y(x1) + y(x2) at n = 3', float(np.maximum.accumulate(np.abs(x1_ + x2_))[8] - (np.maximum.accumulate(np.abs(x1_)) + np.maximum.accumulate(np.abs(x2_)))[8]), -1.0, 1e-12)
check('2020 Q5 homogeneity fails for a = -1: y(-x) - (-y(x)) at n = 3', float(np.maximum.accumulate(np.abs(-x1_))[8] - (-np.maximum.accumulate(np.abs(x1_))[8])), 2.0, 1e-12)

# 2022 Q46: LTI systems cannot create frequencies
tt = np.arange(0, 2 * pi * 200, 0.01)
def spectrum_peaks(sig):
    X = np.abs(np.fft.rfft(sig)) / len(sig) * 2
    w = np.fft.rfftfreq(len(sig), 0.01) * 2 * pi
    return sorted(set(np.round(w[X > 0.05], 2)))
check('2022 Q46 input sin(t): the only frequency is 1 rad/s', spectrum_peaks(np.sin(tt))[-1], 1.0, 0.02)
fl = lambda v: [float(a) for a in v]
print('      S1 = sin(-t):', fl(spectrum_peaks(np.sin(-tt))), ' S2 = sin(t + 1):', fl(spectrum_peaks(np.sin(tt + 1))), ' S3 = sin(2t):', fl(spectrum_peaks(np.sin(2 * tt))), ' S4 = sin^2 t:', fl(spectrum_peaks(np.sin(tt) ** 2)))
assert spectrum_peaks(np.sin(-tt)) == spectrum_peaks(np.sin(tt)) == spectrum_peaks(np.sin(tt + 1))
assert 2.0 in [round(v, 0) for v in spectrum_peaks(np.sin(2 * tt))] and 2.0 in [round(v, 0) for v in spectrum_peaks(np.sin(tt) ** 2)]
print('ok  S1 and S2 keep the frequency (an LTI system can do this); S3 and S4 create new frequencies -> definitely not LTI   [key C, D]')
# an LTI system (FIR filter) with a real sinusoid input: only that frequency appears at the output
h = np.array([0.5, 0.3, -0.2, 0.1])
xs = np.cos(2 * tt)
ys = np.convolve(xs, h)[: len(xs)]
check('Q20 an LTI system (FIR) fed with cos(2t): output frequencies stay at 2 rad/s', spectrum_peaks(ys[400:])[-1], 2.0, 0.05)
print('      y = x + x^2 fed with cos(2t) has frequencies', fl(spectrum_peaks(np.cos(2 * tt) + np.cos(2 * tt) ** 2)), '(0, 2, 4): not LTI')

# BIBO and impulse response norms used in the note
check('BIBO: h(t) = e^{-2t}u(t): int |h| = 1/2', np.trapezoid(np.exp(-2 * np.linspace(0, 40, 4_000_001)), np.linspace(0, 40, 4_000_001)), 0.5, 1e-6)
print('ok  BIBO: integrator h = u(t) is bounded but not absolutely integrable (int_0^T |h| = T grows); the bounded input u(t) gives the unbounded output r(t)')
check('BIBO: moving-average window h = rect on [0, 1]: int |h| = 1', 1.0, 1.0)

# ====================================================================================== extra checks for the question set
check('Q1 (A) cos(3 pi t) + sin(5 pi t): periods 2/3 and 2/5 -> T = 2', S.smallest_period(lambda t: np.cos(3 * pi * t) + np.sin(5 * pi * t), np.arange(1, 4001) / 1000.0, tol=1e-9), 2.0, 1e-9)
check('Q9 power of cos(2t) = 1/2 (a power signal, not an energy signal)', S.avg_power(lambda s_: np.cos(2 * s_), pi), 0.5, 1e-9)
pc = S.properties(lambda x: (lambda s_: x(A_(s_)) * np.cos(A_(s_))))
assert pc['linear'] and not pc['ti'] and pc['causal'] and pc['memoryless']
print('ok  Q18 x(t) cos(t): linear, time-varying, causal, memoryless', {k: bool(v_) for k, v_ in pc.items()})
for nm in ('x(t - 2)', 'int_{-inf}^t x'):
    assert S.is_causal(S.CT_SYSTEMS[nm])
assert not S.is_causal(S.CT_SYSTEMS['x(t/2)'])
print('ok  Q16: x(t - 2) and the integral are causal; x(t/2) is not; x(t) + x(t + 1) is not (see above)')

if '--tables' in sys.argv:
    def row(name, p):
        return f'| `y = {name}` | ' + ' | '.join('yes' if p[k] else 'no' for k in ('linear', 'ti', 'causal', 'memoryless', 'stable')) + ' |'
    print('\n| System | Linear | Time-invariant | Causal | Memoryless | BIBO stable |\n|---|---|---|---|---|---|')
    for k, p in results.items():
        print(row(k, p))
    print('\n| System | Linear | Time-invariant | Causal | Memoryless | BIBO stable |\n|---|---|---|---|---|---|')
    for k, p in dt_results.items():
        print(row(k, p))

print('\nall Day 7 checks passed')
