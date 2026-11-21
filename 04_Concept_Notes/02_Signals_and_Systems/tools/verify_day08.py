"""Re-checks every number in Day08_Convolution_and_LTI_Systems.md and Day08_Conceptual_Questions.md.

Run:  python3 verify_day08.py            (needs numpy)

Continuous-time convolutions are evaluated by numerical integration, discrete-time ones with np.convolve, and the
system-property claims with the numerical property tests of signals_lib.py.  Past-year answers are checked against the keys.
"""
import numpy as np

import signals_lib as S

pi = np.pi
u = S.u


def check(name, got, want, tol=1e-6):
    assert abs(got - want) <= tol, f'{name}: got {got}, expected {want}'
    print(f'ok  {name:<74} {got:.6g}')


def checkv(name, got, want, tol=1e-9):
    assert np.allclose(got, want, atol=tol, rtol=0), f'{name}: got {got}, expected {want}'
    print(f'ok  {name}')


def conv_at(f, g, t, a=-10.0, b=70.0, n=4_000_001):
    """(f * g)(t) = int f(tau) g(t - tau) dtau by the trapezoid rule on [a, b]."""
    tau = np.linspace(a, b, n)
    return np.trapezoid(f(tau) * g(t - tau), tau)


# ====================================================================================== discrete-time convolution
y = np.convolve([1, 2, 3], [1, -1])
checkv('Ex1 {1,2,3} * {1,-1} = {1,1,1,-3}', y, [1, 1, 1, -3])
check('Q1 y[3] of {1,2,3} * {1,-1}', y[3], -3.0, 0)
check('   length rule: len(y) = len(x) + len(h) - 1', len(y), 3 + 2 - 1, 0)
xa, ha = np.array([2, -1, 3]), np.array([1, 4, -2])
check('Q3 sum of y = (sum x)(sum h) = 4 x 3', float(np.sum(np.convolve(xa, ha))), 12.0, 1e-12)
check('   same sum from the factors', float(np.sum(xa) * np.sum(ha)), 12.0, 1e-12)
# polynomial multiplication = convolution (the z-transform view)
checkv('   (1 + 2z + 3z^2)(1 - z) coefficients = convolution', np.polynomial.polynomial.polymul([1, 2, 3], [1, -1]), [1, 1, 1, -3])
# Q2: supports
nx = np.arange(0, 5); nh = np.arange(-1, 2)
ny = np.arange(nx[0] + nh[0], nx[-1] + nh[-1] + 1)
check('Q2 y has support from -1 ... to 5', float(ny[0]), -1.0, 0); check('Q2 ... last index', float(ny[-1]), 5.0, 0); check('   number of samples = 5 + 3 - 1', float(len(ny)), 7.0, 0)
# Q4: u[n] * (delta[n-2] + delta[n+1])  at n = 0
N = np.arange(-10, 11)
uu = (N >= 0).astype(float)
hh = ((N == 2) | (N == -1)).astype(float)
yy = np.convolve(uu, hh)                       # index offset 2*(-10)
n_out = np.arange(len(yy)) + 2 * N[0]
check('Q4 y[0] = u[-2] + u[1]', float(yy[n_out == 0][0]), 1.0, 0)
# Q5: step response -> impulse response
s_ = np.array([1, 3, 6, 6, 6])
h_ = np.diff(np.concatenate([[0], s_]))
checkv('Q5 h[n] = s[n] - s[n-1] = {1, 2, 3, 0, 0}', h_, [1, 2, 3, 0, 0]); check('Q5 h[2]', float(h_[2]), 3.0, 0)
# Q19: {1,1,1,1} * {1,1,1}
y19 = np.convolve([1, 1, 1, 1], [1, 1, 1])
checkv('Q19 {1,1,1,1} * {1,1,1} = {1,2,3,3,2,1}', y19, [1, 2, 3, 3, 2, 1]); check('Q19 y[3]', float(y19[3]), 3.0, 0)
# step response of h[n] = 0.5^n u[n]
nn = np.arange(0, 40)
hn = 0.5 ** nn
sn = np.cumsum(hn)
check('Ex2 step response of (0.5)^n u[n] at n = 5: 2(1 - 0.5^6)', sn[5], 2 * (1 - 0.5 ** 6), 1e-12)
check('   DC gain sum h = 2', float(np.sum(hn)), 2.0, 1e-9)
# Q14: s[n] = (1 - 0.5^{n+1}) u[n]  ->  h[3]
sq = np.where(nn >= 0, 1 - 0.5 ** (nn + 1.0), 0.0)
hq = np.diff(np.concatenate([[0.0], sq]))
check('Q14 h[0] = 0.5', hq[0], 0.5, 1e-12); check('Q14 h[3] = 0.5^4', hq[3], 0.0625, 1e-12)
check('   h[n] = 0.5^{n+1}: h[5]', hq[5], 0.5 ** 6, 1e-12)
# BIBO sums
check('Q13 sum |0.5^n u[n]| = 2', float(np.sum(0.5 ** np.arange(0, 80))), 2.0, 1e-12)
check('   sum 0.5^{|n|} = 3', float(np.sum(0.5 ** np.abs(np.arange(-80, 81)))), 3.0, 1e-12)
assert np.sum(2.0 ** np.arange(0, 60)) > 1e17
print('ok  sum 2^n u[n] diverges (unstable)')

# ====================================================================================== continuous-time convolution
a_, b_ = -3.0, 12.0
ts = [0.5, 1.0, 1.7, 2.5, 4.0]
rect01 = lambda s: np.where((s >= 0) & (s <= 1), 1.0, 0.0)
tri_exact = lambda t: np.where((t >= 0) & (t <= 1), t, np.where((t > 1) & (t <= 2), 2 - t, 0.0))
check('rect01 * rect01 at t = 0.5 (triangle)', conv_at(rect01, rect01, 0.5, -3, 4, 1_400_001), 0.5, 1e-3)
check('rect01 * rect01 at t = 1.5 (triangle)', conv_at(rect01, rect01, 1.5, -3, 4, 1_400_001), 0.5, 1e-3)
for t_ in (1.0, 2.5, 4.0):
    check(f'u * u at t = {t_} equals the ramp', conv_at(u, u, t_, -1, 8, 900_001), t_, 2e-3)
    check(f'e^-t u * u at t = {t_} equals 1 - e^-t', conv_at(lambda s: np.exp(-s) * u(s), u, t_, -1, 20, 2_100_001), 1 - np.exp(-t_), 2e-3)
    check(f'e^-t u * e^-2t u at t = {t_} equals e^-t - e^-2t', conv_at(lambda s: np.exp(-s) * u(s), lambda s: np.exp(-2 * s) * u(s), t_, -1, 20, 2_100_001), np.exp(-t_) - np.exp(-2 * t_), 2e-3)
check('e^-t u * e^-t u at t = 2 equals t e^-t', conv_at(lambda s: np.exp(-s) * u(s), lambda s: np.exp(-s) * u(s), 2.0, -1, 20, 2_100_001), 2 * np.exp(-2), 2e-3)
# Q6: x = 2 [u(t) - u(t - 2)]:  y = x * x has peak 2*2*2 = 8 at t = 2, support [0, 4]
x6 = lambda s: 2.0 * np.where((s >= 0) & (s < 2), 1.0, 0.0)
tt = np.linspace(0, 4, 17)
y6 = np.array([conv_at(x6, x6, t_, -2, 8, 1_000_001) for t_ in tt])
check('Q6 peak of x * x', y6.max(), 8.0, 2e-2); check('Q6 location of the peak', tt[np.argmax(y6)], 2.0, 1e-9)
check('Q6 y(4.5) = 0 (support ends at 4)', conv_at(x6, x6, 4.5, -2, 8, 1_000_001), 0.0, 1e-3)
# Q7: e^{-t} u * u at t = 1
check('Q7 (1 - e^-1)', 1 - np.exp(-1), 0.63212, 1e-5)
# Q8: rect(2) * rect(3): trapezoid, max = min(widths) = 2, support width 5
r2 = lambda s: np.where((s >= 0) & (s < 2), 1.0, 0.0); r3 = lambda s: np.where((s >= 0) & (s < 3), 1.0, 0.0)
tt8 = np.linspace(-1, 6, 29)
y8 = np.array([conv_at(r2, r3, t_, -3, 8, 1_100_001) for t_ in tt8])
check('Q8 maximum of rect(2) * rect(3)', y8.max(), 2.0, 3e-3)
check('   support: first and last nonzero t', float(tt8[y8 > 1e-2][0] - tt8[y8 > 1e-2][-1]), -4.5, 0.26)
check('   plateau width = |3 - 2| = 1: points at the maximum', float(np.sum(np.abs(y8 - 2.0) < 5e-3)) * 0.25, 1.0 + 0.25, 0.3)
# Q9: area rule: x = 3e^{-2t}u(t), h = 2 delta(t - 1) + 3[u(t) - u(t - 2)]
check('Q9 area of x', 3 / 2, 1.5); check('Q9 area of h = 2 + 3*2', 2 + 3 * 2, 8.0)
check('Q9 integral of y = 1.5 x 8', 1.5 * 8, 12.0)
# direct numerical check: y = 2 x(t - 1) + 3 (x * rect2); integrate on a grid
dt = 1e-3
tg = np.arange(-2, 60, dt)
xg = 3 * np.exp(-2 * tg) * (tg >= 0)
rg = np.where((tg >= 0) & (tg < 2), 1.0, 0.0)
yc = np.convolve(xg, rg) * dt
ty = np.arange(len(yc)) * dt + 2 * tg[0]
ysum = np.trapezoid(yc * 3, ty) + 2 * np.trapezoid(xg, tg)
check('Q9 numerical integral of y = x * h', ysum, 12.0, 3e-2)
# Q10 and 2024 Q21: time scaling x(at) * h(at) = (1/|a|) y(at)
xs = lambda s: np.exp(-s) * u(s)
hs = lambda s: u(s) - u(s - 1)
y_of = lambda t_: conv_at(xs, hs, t_, -5, 80, 3_000_001)
for a in (0.5, 2.0):
    xa_ = lambda s, a=a: xs(a * s); ha_ = lambda s, a=a: hs(a * s)
    for t_ in (1.0, 3.0, 4.5):
        lhs = conv_at(xa_, ha_, t_, -5, 80, 3_000_001)
        check(f'time scaling a = {a}: x(at) * h(at) at t = {t_} equals y(at)/|a|', lhs, y_of(a * t_) / abs(a), 3e-3)
check('2024 Q21 [key A]: for a = 0.5 the factor is 1/|a| = 2', 1 / 0.5, 2.0)
# shift property and delta
for t_ in (1.5, 3.0):
    check('shift property: x(t - 1) * h(t - 2) = y(t - 3) at t = %.1f' % t_, conv_at(lambda s: xs(s - 1), lambda s: hs(s - 2), t_, -5, 80, 3_000_001), y_of(t_ - 3), 3e-3)
# commutative, associative, distributive (numerical, discrete)
rng = np.random.default_rng(1)
p, q, r = rng.normal(size=5), rng.normal(size=4), rng.normal(size=3)
checkv('commutative p*q = q*p', np.convolve(p, q), np.convolve(q, p))
checkv('associative (p*q)*r = p*(q*r)', np.convolve(np.convolve(p, q), r), np.convolve(p, np.convolve(q, r)))
checkv('distributive p*(q + q2) = p*q + p*q2', np.convolve(p, q + q[::-1]), np.convolve(p, q) + np.convolve(p, q[::-1]))
# derivative property (x*h)' = x' * h on a fine grid
dt = 1e-3
tg = np.arange(-1, 15, dt)
xg = np.exp(-tg) * (tg >= 0) * 1.0
hg = np.where((tg >= 0) & (tg < 1), 1.0, 0.0)
yg = np.convolve(xg, hg)[: len(tg)] * dt
lhs = np.gradient(yg, dt)
rhs = np.convolve(np.gradient(np.exp(-tg) * (tg >= 0), dt), hg)[: len(tg)] * dt
check('derivative property (x*h)\' = x\' * h (median abs difference on t > 0.2)', float(np.median(np.abs(lhs - rhs)[int(1.2 / dt):])), 0.0, 5e-3)
# x * u = running integral
check('x * u is the running integral (e^-t u): value at t = 3', conv_at(xs, u, 3.0, -1, 10, 1_100_001), 1 - np.exp(-3), 2e-3)
# step response s = h * u and h = ds/dt (h = e^{-2t}u)
check('step response of e^{-2t}u at t = 1: (1 - e^-2)/2', conv_at(lambda s: np.exp(-2 * s) * u(s), u, 1.0, -1, 10, 1_100_001), (1 - np.exp(-2)) / 2, 2e-3)
check('   derivative of the step response at t = 1 equals h(1) = e^-2', ((1 - np.exp(-2 * 1.0001)) / 2 - (1 - np.exp(-2 * 0.9999)) / 2) / 2e-4, np.exp(-2), 1e-5)
# BIBO
tg = np.linspace(0, 40, 4_000_001)
check('BIBO: int |e^{-2t}u| = 1/2', np.trapezoid(np.exp(-2 * tg), tg), 0.5, 1e-6)
check('BIBO: int |e^{-|t|}| = 2', np.trapezoid(np.exp(-np.abs(np.linspace(-40, 40, 8_000_001))), np.linspace(-40, 40, 8_000_001)), 2.0, 1e-6)
check('BIBO: int_0^T |u| = T grows without bound (T = 1000)', np.trapezoid(np.ones(100001), np.linspace(0, 1000, 100001)), 1000.0, 1e-9)
# Q12: h = 3 e^{-2t} u(t), |x| <= 2  ->  max |y| = 2 * int|h| = 3
check('Q12 int |h| = 3 * 1/2', np.trapezoid(3 * np.exp(-2 * tg), tg), 1.5, 1e-5)
check('Q12 y for x = 2 (all t) after the transient', conv_at(lambda s: 3 * np.exp(-2 * s) * u(s), lambda s: 2.0 + 0 * s, 30.0, -1, 40, 2_100_001), 3.0, 1e-3)
# Q15: cascade of a delay and an exponential
check('Q15 h = delta(t - 1) * e^{-t}u(t) = e^{-(t-1)}u(t-1): value at t = 2', np.exp(-(2 - 1)), np.exp(-1), 1e-12)

# ====================================================================================== system properties (numerical tests)
A = lambda n: np.asarray(n)
delta = lambda n: np.where(np.asarray(n) == 0, 1.0, 0.0)


def fir(h):
    return lambda x: (lambda n: sum(v * x(A(n) - k) for k, v in h.items()))


# Q16: LTI followed by an added constant
h16 = {0: 1.0, 1: 0.5}
sys16 = lambda x: (lambda n: fir(h16)(x)(n) + 5.0)
p16 = S.dt_properties(sys16)
assert (not p16['linear']) and p16['ti']
print('ok  Q16 y = x*h + 5: non-linear and time-invariant', {k: bool(v) for k, v in p16.items()})
# 2025 Q17: y = h2 * (h1 * x + b delta) - b delta  with h2 != delta
h1, h2, b = {0: 1.0, 1: 0.5}, {0: 1.0, 2: 0.3}, 2.0
def sys_2025q17(x):
    inner = lambda n: fir(h1)(x)(n) + b * delta(n)
    return lambda n: fir(h2)(inner)(n) - b * delta(n)
p17 = S.dt_properties(sys_2025q17)
assert (not p17['linear']) and (not p17['ti'])
print('ok  2025 Q17 [key D]: non-linear and time-varying', {k: bool(v) for k, v in p17.items()})
# the zero-input response is the fixed signal b (h2 - delta)
zero_in = sys_2025q17(lambda n: 0.0 * A(n))(np.arange(-3, 6))
expected_offset = b * (np.array([h2.get(k, 0.0) for k in range(-3, 6)]) - np.array([1.0 if k == 0 else 0.0 for k in range(-3, 6)]))
checkv('   zero-input output equals the fixed signal b(h2[n] - delta[n])  (nonzero at n = 2)', zero_in, expected_offset)
# the same system with b = 0 is LTI
sys0 = lambda x: (lambda n: fir(h2)(lambda m: fir(h1)(x)(m))(n))
p0 = S.dt_properties(sys0)
assert p0['linear'] and p0['ti']
print('ok  with b = 0 the system is LTI', {k: bool(v) for k, v in p0.items()})


# 2026 Q47: acyclic interconnection of LTI blocks
def make_S(h1d, h2d):
    def system(x):
        a = lambda n: fir(h1d)(x)(n)
        v = lambda n: x(n) - a(A(n) - 1)
        w = lambda n: fir(h2d)(v)(n)
        return lambda n: a(n) - w(A(n) - 1)
    return system


p47 = S.dt_properties(make_S({0: 1.0, 1: 0.4}, {0: 0.5, 1: -0.2, 2: 0.1}))
assert p47['linear'] and p47['ti'] and p47['causal']
print('ok  2026 Q47 [key B] with causal h1, h2: linear, time-invariant and causal', {k: bool(v) for k, v in p47.items()})
p47n = S.dt_properties(make_S({-1: 1.0, 0: 0.4}, {0: 0.5, 1: -0.2}))
assert p47n['linear'] and p47n['ti'] and not p47n['causal']
print('ok  ... but with a non-causal h1 the SAME diagram is non-causal: "S is causal" is not necessarily true', {k: bool(v) for k, v in p47n.items()})

# ====================================================================================== eigenfunctions and frequency response
H = lambda h, W: sum(v * np.exp(-1j * W * k) for k, v in h.items())
check('Q17 |H(e^{j pi/2})| of h = {1, 2, 1}', abs(H({0: 1, 1: 2, 2: 1}, pi / 2)), 2.0, 1e-12)
check('   H(1) = sum h = 4 (DC gain)', abs(H({0: 1, 1: 2, 2: 1}, 0.0)), 4.0, 1e-12)
n_ = np.arange(0, 200)
x17 = np.cos(pi * n_ / 2)
y17 = np.convolve(x17, [1, 2, 1])[: len(n_)]
check('Q17 steady-state amplitude of the output (n >= 2)', np.max(np.abs(y17[2:])), 2.0, 1e-12)
check('   phase: output = 2 cos(pi n/2 - pi/2): max error', np.max(np.abs(y17[2:] - 2 * np.cos(pi * n_[2:] / 2 - pi / 2))), 0.0, 1e-12)
# 2019 Q29: y[n] = 0 for x[n] = c1 e^{-j pi n/2} + c2 e^{j pi n/2}, h = {1, a, b}
best = None
for a_t, b_t, lab in ((1, 1, 'A'), (0, -1, 'B'), (-1, 1, 'C'), (0, 1, 'D')):
    resid = max(abs(H({0: 1, 1: a_t, 2: b_t}, W)) for W in (pi / 2, -pi / 2))
    print(f'      option ({lab}) a = {a_t:>2}, b = {b_t:>2}: |H(e^(+-j pi/2))| = {resid:.3g}')
    if resid < 1e-12:
        best = lab
assert best == 'D'
print('ok  2019 Q29 [key D]: a = 0, b = 1 annihilates e^{+-j pi n/2}')
x29 = (0.7 - 0.2j) * np.exp(-1j * pi * n_ / 2) + (1.1 + 0.4j) * np.exp(1j * pi * n_ / 2)
y29 = x29[2:] + x29[:-2]                 # y[n] = x[n] + x[n-2]  (a = 0, b = 1)
check('   y[n] = x[n] + x[n - 2] is zero for every n (max |y|)', float(np.max(np.abs(y29))), 0.0, 1e-12)
# 2021 Q40: step response 2 d[n+1] + d[n] + d[n-1];  input (1/2)^n u[n];  y[0]
nrange = np.arange(-6, 10)
sd = np.zeros(len(nrange)); sd[nrange == -1] = 2; sd[nrange == 0] = 1; sd[nrange == 1] = 1
hd = np.diff(np.concatenate([[0.0], sd]))
checkv('2021 Q40 impulse response h = {2 at -1, -1 at 0, 0 at 1, -1 at 2}', [hd[nrange == k][0] for k in (-1, 0, 1, 2)], [2, -1, 0, -1])
xd = np.where(nrange >= 0, 0.5 ** np.maximum(nrange, 0), 0.0)
yd = np.convolve(hd, xd)
nd = np.arange(len(yd)) + 2 * nrange[0]
check('2021 Q40 [key 0.0 to 0.0]: y[0]', float(yd[nd == 0][0]), 0.0, 1e-12)
print('      y[-1], y[0], y[1], y[2] =', [round(float(yd[nd == k][0]), 4) for k in (-1, 0, 1, 2)])
check('   direct sum: 2 x[1] - x[0] - 0*x[-1] - x[-2]... = 2(1/2) - 1', 2 * 0.5 - 1.0, 0.0, 1e-12)

# 2022 Q33: e^{-t}u(t) * [u(t) - u(t - 2)]
x1 = lambda s: np.exp(-s) * u(s); x2 = lambda s: u(s) - u(s - 2)
for t_ in (1.0, 2.0, 5.0):
    exact = (1 - np.exp(-t_)) if t_ < 2 else np.exp(-t_) * (np.exp(2) - 1)
    check(f'2022 Q33 y({t_}) = piecewise closed form', conv_at(x1, x2, t_, -3, 40, 2_000_001), exact, 3e-3)
check('2022 Q33 [key 0.0]: y(30) -> 0', np.exp(-30) * (np.exp(2) - 1), 0.0, 1e-9)
check('   peak value 1 - e^-2 at t = 2', 1 - np.exp(-2), 0.86466, 1e-5)
# 2023 Q48
xq = [1, -1, 0, 2]; hq48 = [1, 0, -0.5]
y48 = np.convolve(xq, hq48)
checkv('2023 Q48 [key C]: y = d[n] - d[n-1] - (1/2)d[n-2] + (5/2)d[n-3] - d[n-5]', y48, [1, -1, -0.5, 2.5, 0, -1])
# DTFT check: Y = X H
Wg = np.linspace(-pi, pi, 7)
X = lambda W: 1 - np.exp(-1j * W) + 2 * np.exp(-3j * W)
Hh = lambda W: 1 - 0.5 * np.exp(-2j * W)
Y = sum(v * np.exp(-1j * Wg * k) for k, v in enumerate(y48))
checkv('   DTFT of y equals X(e^jW) H(e^jW)', Y, X(Wg) * Hh(Wg), 1e-12)
# 2023 Q58 : areas
check('2023 Q58 area of x1 (width 3)', 3.0, 3.0); check('2023 Q58 area of x2 = 1 + 2 + 2', 1 + 2 + 2, 5.0)
check('2023 Q58 [key 15]: integral of y = 3 x 5', 3 * 5, 15.0)
dt = 1e-3
tg = np.arange(-9, 9, dt)
x1g = np.where(np.abs(tg) < 1.5, 1.0, 0.0)
x2g = np.where(np.abs(tg) < 1.0, 1.0, 0.0) + (np.abs(tg + 3) < dt / 2) / dt + 2 * (np.abs(tg - 2) < dt / 2) / dt
yg = np.convolve(x1g, x2g) * dt
check('2023 Q58 numerical integral of y (impulses as narrow pulses of area 1)', float(np.sum(yg) * dt), 15.0, 3e-2)
# 2026 Q13: Laplace transform of u(t - 2) * t u(t)
tg = np.linspace(2, 80, 7_800_001)
xt = (tg - 2) ** 2 / 2
check('2026 Q13 x(t) = (t-2)^2/2 u(t-2); X(1.5) numerically', np.trapezoid(xt * np.exp(-1.5 * tg), tg), np.exp(-3) / 1.5 ** 3, 1e-6)
check('   e^{-2s}/s^3 at s = 1.5  [key D]', np.exp(-3) / 1.5 ** 3, 0.01475, 1e-5)

# ====================================================================================== standard results quoted in the note (section 2.2 and 3.2)
n30 = np.arange(0, 30)
ones30 = np.ones(30)
checkv('DT u * u = (n + 1) u[n]', np.convolve(ones30, ones30)[:30], n30 + 1.0)
ra, rb = 0.5, 0.25
y_ab = np.convolve(ra ** n30, rb ** n30)[:30]
checkv('DT a^n u * b^n u = (a^(n+1) - b^(n+1))/(a - b)   (a = 0.5, b = 0.25)', y_ab, (ra ** (n30 + 1) - rb ** (n30 + 1)) / (ra - rb), 1e-12)
check('   ... at n = 4 this is 0.12109375', y_ab[4], 0.12109375, 1e-12)
checkv('DT a^n u * a^n u = (n + 1) a^n u   (a = 0.5)', np.convolve(ra ** n30, ra ** n30)[:30], (n30 + 1) * ra ** n30, 1e-12)
checkv('DT a^n u * u = (1 - a^(n+1))/(1 - a) u   (a = 0.5)', np.convolve(ra ** n30, ones30)[:30], (1 - ra ** (n30 + 1)) / (1 - ra), 1e-12)
# support rule with offsets: x on [2, 6], h on [-3, 0]  ->  y on [-1, 6], 8 samples
check('support rule: first index 2 + (-3) = -1', 2 + (-3), -1, 0); check('   last index 6 + 0 = 6', 6 + 0, 6, 0)
check('   length 5 + 4 - 1 = 8 = 6 - (-1) + 1', len(np.convolve(np.ones(5), np.ones(4))), 8, 0)
# CT, general exponents
check('CT e^{-3t}u * e^{-t}u at t = 1.5 equals (e^{-t} - e^{-3t})/(3 - 1)', conv_at(lambda s: np.exp(-3 * s) * u(s), lambda s: np.exp(-s) * u(s), 1.5, -1, 20, 2_100_001), (np.exp(-1.5) - np.exp(-4.5)) / 2, 2e-3)
check('CT e^{-3t}u * u at t = 1.5 equals (1 - e^{-3t})/3', conv_at(lambda s: np.exp(-3 * s) * u(s), u, 1.5, -1, 20, 2_100_001), (1 - np.exp(-4.5)) / 3, 2e-3)
# rectangles of different heights and widths: heights 3 and 2, widths 1 and 2.5 -> plateau of height 3*2*1 = 6 on [1, 2.5]
rA = lambda s: 3.0 * np.where((s >= 0) & (s < 1.0), 1.0, 0.0); rB = lambda s: 2.0 * np.where((s >= 0) & (s < 2.5), 1.0, 0.0)
check('rect(3, width 1) * rect(2, width 2.5): plateau a*b*T1 = 6 at t = 1.7', conv_at(rA, rB, 1.7, -2, 8, 1_000_001), 6.0, 1e-2)
check('   ... still on the plateau at t = 2.4', conv_at(rA, rB, 2.4, -2, 8, 1_000_001), 6.0, 1e-2)
check('   ... rising edge at t = 0.5 gives 3*2*0.5 = 3', conv_at(rA, rB, 0.5, -2, 8, 1_000_001), 3.0, 1e-2)
check('   ... support ends at 1 + 2.5 = 3.5: value at 3.6 is 0', conv_at(rA, rB, 3.6, -2, 8, 1_000_001), 0.0, 1e-2)
# cascade and BIBO
checkv('cascade {1,1} * {1,1} = {1,2,1} (the filter of Q17)', np.convolve([1, 1], [1, 1]), [1, 2, 1])
rng2 = np.random.default_rng(7)
for _ in range(5):
    p1, p2 = rng2.normal(size=7), rng2.normal(size=6)
    assert np.sum(np.abs(np.convolve(p1, p2))) <= np.sum(np.abs(p1)) * np.sum(np.abs(p2)) + 1e-12
print('ok  cascade of stable systems is stable: sum|h1*h2| <= sum|h1| sum|h2| (5 random pairs)')
# the sinc is not absolutely integrable: the integral of |sinc| over [0, T] grows like (2/pi^2) ln T
dts = 0.005
ts_ = np.arange(0, 1e4, dts)
cum = np.cumsum(np.abs(np.sinc(ts_))) * dts
check('int_0^T |sinc| grows without bound: increase from T = 100 to T = 10^4 is (2/pi^2) ln 100', cum[-1] - cum[int(100 / dts)], (2 / pi ** 2) * np.log(100), 2e-2)
# 2026 Q47: overall impulse response  H = H1 - z^-1 H2 + z^-2 H1 H2
h1d, h2d = {0: 1.0, 1: 0.4}, {0: 0.5, 1: -0.2, 2: 0.1}
nidx = np.arange(-3, 12)
hS = make_S(h1d, h2d)(delta)(nidx)
pred = np.zeros(len(nidx))
for k, v in h1d.items(): pred[nidx == k] += v
for k, v in h2d.items(): pred[nidx == k + 1] -= v
h12 = np.convolve([1.0, 0.4], [0.5, -0.2, 0.1])
for k, v in enumerate(h12): pred[nidx == k + 2] += v
checkv('2026 Q47 impulse response of S equals h1[n] - h2[n-1] + (h1*h2)[n-2]', hS, pred, 1e-12)
print('      h_S[n] for n = 0..5:', [round(float(hS[nidx == k][0]), 4) for k in range(6)])

# ====================================================================================== practice problems P1 ... P6
yP1 = np.convolve([2, 1, 0, -1], [1, 3, 2])
checkv('P1 {2,1,0,-1} * {1,3,2} = {2,7,7,1,-3,-2} (n = -1..4)', yP1, [2, 7, 7, 1, -3, -2]); check('P1 sum = 2 x 6 = 12', float(np.sum(yP1)), 12.0, 1e-12)
xP2 = lambda s: np.exp(-2 * s) * u(s); hP2 = lambda s: u(s - 1) - u(s - 3)
for t_, want in ((2.0, (1 - np.exp(-2)) / 2), (3.0, (1 - np.exp(-4)) / 2), (5.0, (np.exp(-4) - np.exp(-8)) / 2)):
    check(f'P2 y({t_}) for e^-2t u * [u(t-1) - u(t-3)]', conv_at(xP2, hP2, t_, -2, 40, 2_100_001), want, 2e-3)
check('P2 peak value (1 - e^-4)/2 at t = 3', (1 - np.exp(-4)) / 2, 0.490842, 1e-6)
tP2 = np.linspace(1, 60, 5_900_001)
yP2 = np.where(tP2 < 3, (1 - np.exp(-2 * (tP2 - 1))) / 2, np.exp(-2 * tP2) * (np.exp(6) - np.exp(2)) / 2)
check('P2 area of y = (1/2)(2) = 1', np.trapezoid(yP2, tP2), 1.0, 1e-5)
# P4 (e): h = cos(t) u(t), input cos(t) u(t): the output (t cos t + sin t)/2 grows like t/2
check('P4 (e) response of cos(t)u(t) to cos(t)u(t) at t = 10 is (10 cos 10 + sin 10)/2', conv_at(lambda s: np.cos(s) * u(s), lambda s: np.cos(s) * u(s), 10.0, -1, 12, 2_200_001), (10 * np.cos(10) + np.sin(10)) / 2, 2e-3)
check('   ... and at t = 40 it has grown to (40 cos 40 + sin 40)/2', conv_at(lambda s: np.cos(s) * u(s), lambda s: np.cos(s) * u(s), 40.0, -1, 42, 4_300_001), (40 * np.cos(40) + np.sin(40)) / 2, 5e-3)
# 2021 Q40 trap: using the STEP response as if it were the impulse response gives y[0] = 2
check('2021 Q40 trap: using s[n] as h[n] would give y[0] = 2(1/2) + 1(1) + 1(0)', 2 * 0.5 + 1 * 1 + 1 * 0, 2.0)
check('P2 closed form for t >= 3 equals e^{-2t}(e^6 - e^2)/2 at t = 5', np.exp(-10) * (np.exp(6) - np.exp(2)) / 2, (np.exp(-4) - np.exp(-8)) / 2, 1e-12)
check('P3 (a) x(2t)*h(2t) at t = 0.5 is y(1)/2', 3 / 2, 1.5); check('P3 (c) area of h = 12 / 4', 12 / 4, 3.0)
check('P4 (a) sum |(-0.8)^n u[n]| = 5', float(np.sum(0.8 ** np.arange(0, 400))), 5.0, 1e-9)
tneg = np.linspace(-40, 0, 4_000_001)
check('P4 (b) int |e^t u(-t)| = 1', np.trapezoid(np.exp(tneg), tneg), 1.0, 1e-6)
tpos = np.linspace(0, 60, 6_000_001)
check('P4 (c) int t e^{-t} u(t) = 1', np.trapezoid(tpos * np.exp(-tpos), tpos), 1.0, 1e-6)
check('P4 (d) sum_{n<=-1} 2^n = 1', float(np.sum(2.0 ** (-np.arange(1, 80)))), 1.0, 1e-12)
check('P4 (e) int_0^T |cos t| = (2/pi) T for large T: T = 1000', np.trapezoid(np.abs(np.cos(np.linspace(0, 1000, 4_000_001))), np.linspace(0, 1000, 4_000_001)), 2000 / pi, 1.0)
sP5 = np.array([1, 3, 4, 4, 4, 4, 4])
hP5 = np.diff(np.concatenate([[0], sP5]))
checkv('P5 h[n] = s[n] - s[n-1] = {1,2,1,0,0,...}', hP5, [1, 2, 1, 0, 0, 0, 0])
yP5 = np.convolve(hP5[:3], [1, 1])
checkv('P5 response to the pulse {1,1} is {1,3,3,1}; y[2] = 3', yP5, [1, 3, 3, 1])
checkv('P5 same from s[n] - s[n-2]', (sP5 - np.concatenate([[0, 0], sP5[:-2]]))[:4], [1, 3, 3, 1])
checkv('P5 cascade of two copies {1,2,1} * {1,2,1} = {1,4,6,4,1}', np.convolve([1, 2, 1], [1, 2, 1]), [1, 4, 6, 4, 1]); check('P5 DC gain sum h = 4 = s[infinity]', float(np.sum(hP5)), 4.0, 0)
hP6 = {0: 1.0, 2: -1.0}
check('P6 |H(e^{j pi/2})| for h = delta[n] - delta[n-2]', abs(H(hP6, pi / 2)), 2.0, 1e-12); check('P6 angle of H(e^{j pi/2})', float(np.angle(H(hP6, pi / 2))), 0.0, 1e-12)
check('P6 H(1) = 0: DC is blocked', abs(H(hP6, 0.0)), 0.0, 1e-12); check('P6 H(e^{j pi}) = 0: the highest frequency is blocked too', abs(H(hP6, pi)), 0.0, 1e-12)
x6 = 3 * np.cos(pi * n_ / 2 + 0.3)
y6_ = np.convolve(x6, [1, 0, -1])[: len(n_)]
check('P6 steady-state output 6 cos(pi n/2 + 0.3): max error', float(np.max(np.abs(y6_[2:] - 6 * np.cos(pi * n_[2:] / 2 + 0.3)))), 0.0, 1e-12)
check('Ex 11: H(e^{j pi}) of {1,2,1} = 0 (the highest frequency is blocked)', abs(H({0: 1, 1: 2, 2: 1}, pi)), 0.0, 1e-12)
Wg2 = np.linspace(-pi, pi, 9)
checkv('Ex 11: H(e^{jW}) of {1,2,1} = e^{-jW} (2 + 2 cos W)', H({0: 1, 1: 2, 2: 1}, Wg2), np.exp(-1j * Wg2) * (2 + 2 * np.cos(Wg2)), 1e-12)

print('\nall Day 8 checks passed')
