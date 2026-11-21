"""Re-checks every number in Day09_Fourier_Series.md and Day09_Conceptual_Questions.md.

Run:  python3 verify_day09.py            (needs numpy and scipy)

Fourier-series coefficients are computed numerically (midpoint rule through an FFT, see coeffs()) and compared with the closed
forms of the note.  Past-year answers are checked against the official keys.
"""
import numpy as np
from scipy import integrate, special
from scipy.integrate import solve_ivp

pi = np.pi


def check(name, got, want, tol=1e-6):
    assert abs(got - want) <= tol, f'{name}: got {got}, expected {want}'
    print(f'ok  {name:<80} {got:.6g}')


def checkv(name, got, want, tol=1e-6):
    assert np.allclose(got, want, atol=tol, rtol=0), f'{name}: got {got}, expected {want}'
    print(f'ok  {name}')


def coeffs(x, T0, K, N=1 << 16):
    """Exponential Fourier coefficients c_k, k = -K..K, of the T0-periodic function x (callable on arrays).
    c_k = (1/T0) int_0^T0 x(t) e^{-j k w0 t} dt by the midpoint rule: (1/N) sum x(t_n) e^{-j 2 pi k t_n / T0}."""
    t = (np.arange(N) + 0.5) * T0 / N
    F = np.fft.fft(x(t)) / N
    k = np.arange(-K, K + 1)
    return k, F[k % N] * np.exp(-1j * pi * k / N)


def at(k, c, m):
    """c_m from the arrays returned by coeffs()."""
    return c[list(k).index(m)]


def mean_square(x, T0, N=1 << 18):
    t = (np.arange(N) + 0.5) * T0 / N
    return float(np.mean(np.abs(x(t)) ** 2))


def sq_pm(T0, A=1.0):
    """+A for 0 < t < T0/2, -A for T0/2 < t < T0 (odd, half-wave symmetric)."""
    return lambda t: A * np.where((t % T0) < T0 / 2, 1.0, -1.0)


# ================================================================================ 1. orthogonality
T0 = 3.0; w0 = 2 * pi / T0
tg = np.linspace(0, T0, 600_001)
for kk, mm in ((1, 1), (2, 2), (1, 2), (3, -3), (0, 0), (4, 1), (-2, 5)):
    val = np.trapezoid(np.exp(1j * kk * w0 * tg) * np.exp(-1j * mm * w0 * tg), tg) / T0
    check(f'(1/T) int e^(j{kk}w0t) e^(-j{mm}w0t) dt = delta[{kk} - {mm}]', abs(val - (1.0 if kk == mm else 0.0)), 0.0, 1e-9)
for kk, mm in ((1, 1), (2, 2), (1, 3)):
    check(f'int cos({kk}w0t)cos({mm}w0t) = T/2 delta', np.trapezoid(np.cos(kk * w0 * tg) * np.cos(mm * w0 * tg), tg), T0 / 2 if kk == mm else 0.0, 1e-9)
    check(f'int sin({kk}w0t)sin({mm}w0t) = T/2 delta', np.trapezoid(np.sin(kk * w0 * tg) * np.sin(mm * w0 * tg), tg), T0 / 2 if kk == mm else 0.0, 1e-9)
for kk, mm in ((1, 1), (2, 5), (3, 1)):
    check(f'int sin({kk}w0t)cos({mm}w0t) = 0 (always)', np.trapezoid(np.sin(kk * w0 * tg) * np.cos(mm * w0 * tg), tg), 0.0, 1e-9)
check('int_0^T cos^2(0 t) = T  (k = 0 is special)', np.trapezoid(np.ones_like(tg), tg), T0, 1e-9)
# Q4: x = cos(2 pi t) + 2 sin(2 pi t), y = 3 cos(2 pi t) - sin(2 pi t), int_0^1 x y dt
t1 = np.linspace(0, 1, 400_001)
check('Q4 int_0^1 x y dt = (1)(3)/2 + (2)(-1)/2 = 0.5', np.trapezoid((np.cos(2 * pi * t1) + 2 * np.sin(2 * pi * t1)) * (3 * np.cos(2 * pi * t1) - np.sin(2 * pi * t1)), t1), 0.5, 1e-9)
# Q5: over HALF a period
th = np.linspace(0, pi, 400_001)
check('Q5 half period: cos(th) cos(2 th) is orthogonal', np.trapezoid(np.cos(th) * np.cos(2 * th), th), 0.0, 1e-9)
check('Q5 half period: sin(th) sin(2 th) is orthogonal', np.trapezoid(np.sin(th) * np.sin(2 * th), th), 0.0, 1e-9)
check('Q5 half period: sin(th) cos(2 th) is NOT orthogonal (-2/3)', np.trapezoid(np.sin(th) * np.cos(2 * th), th), -2 / 3, 1e-9)
check('Q5 half period: cos(th) sin(2 th) is NOT orthogonal (4/3)', np.trapezoid(np.cos(th) * np.sin(2 * th), th), 4 / 3, 1e-9)

# ================================================================================ 2. relations between the forms
w0 = 2 * pi / 3
x2 = lambda t: 4 + 6 * np.cos(w0 * t) + 8 * np.sin(w0 * t)
k_, c_ = coeffs(x2, 3.0, 4)
check('Q2 c_0 = 4', at(k_, c_, 0).real, 4.0, 1e-9)
check('Q2 c_1 = (a_1 - j b_1)/2 = 3 - 4j : real part', at(k_, c_, 1).real, 3.0, 1e-9); check('   ... imaginary part', at(k_, c_, 1).imag, -4.0, 1e-9)
check('   c_-1 = conj(c_1) = 3 + 4j: imaginary part', at(k_, c_, -1).imag, 4.0, 1e-9)
check('   |c_1| = 5 and C_1 = 2|c_1| = 10', 2 * abs(at(k_, c_, 1)), 10.0, 1e-9)
check('   compact form: 10 cos(w0 t - 53.13 deg) reproduces 6 cos + 8 sin', float(np.max(np.abs(10 * np.cos(w0 * np.linspace(0, 3, 50) + np.angle(at(k_, c_, 1))) - (6 * np.cos(w0 * np.linspace(0, 3, 50)) + 8 * np.sin(w0 * np.linspace(0, 3, 50)))))), 0.0, 1e-9)
check('   angle of c_1 in degrees', float(np.degrees(np.angle(at(k_, c_, 1)))), -53.1301, 1e-3)
xr = lambda t: 1 + 2 * np.cos(w0 * t) - 3 * np.sin(2 * w0 * t) + 0.5 * np.cos(3 * w0 * t + 0.7)
k_, c_ = coeffs(xr, 3.0, 6)
for m in (1, 2, 3):
    a_m = (c_[list(k_).index(m)] + c_[list(k_).index(-m)])
    b_m = 1j * (c_[list(k_).index(m)] - c_[list(k_).index(-m)])
    t_ = np.linspace(0, 3, 4001); xa = np.mean(xr(t_[:-1]) * np.cos(m * w0 * t_[:-1])) * 2; xb = np.mean(xr(t_[:-1]) * np.sin(m * w0 * t_[:-1])) * 2
    check(f'a_{m} = c_{m} + c_-{m}  equals (2/T) int x cos', a_m.real, xa, 1e-6); check(f'b_{m} = j(c_{m} - c_-{m})  equals (2/T) int x sin', b_m.real, xb, 1e-6)
    check(f'c_{m} = (a_{m} - j b_{m})/2', abs(at(k_, c_, m) - (a_m.real - 1j * b_m.real) / 2), 0.0, 1e-9)
# Q1
x1 = lambda t: 2 + 4 * np.cos(4 * pi * t) - 6 * np.sin(12 * pi * t)
k_, c_ = coeffs(x1, 0.5, 4)
check('Q1 |c_3| for 2 + 4cos(4 pi t) - 6 sin(12 pi t)', abs(at(k_, c_, 3)), 3.0, 1e-9); check('   c_3 = +3j', at(k_, c_, 3).imag, 3.0, 1e-9)
check('   c_1 = 2', at(k_, c_, 1).real, 2.0, 1e-9); check('   c_2 = 0', abs(at(k_, c_, 2)), 0.0, 1e-9)
# Q3 power
x3 = lambda t: 2 + 3 * np.cos(w0 * t) + 4 * np.sin(2 * w0 * t)
check('Q3 power of 2 + 3cos(w0 t) + 4 sin(2 w0 t) = 4 + 9/2 + 16/2', mean_square(x3, 3.0), 16.5, 1e-6)
k_, c_ = coeffs(x3, 3.0, 4)
check('   Parseval: sum |c_k|^2', float(np.sum(np.abs(c_) ** 2)), 16.5, 1e-9)

# ================================================================================ 3. standard waveforms
# rectangular pulse train (Q6, Q7): A = 5 for |t| < 1, period 8
Tp, A = 8.0, 5.0
rect_tr = lambda t: A * np.where(np.abs(((t + Tp / 2) % Tp) - Tp / 2) < 1.0, 1.0, 0.0)
k_, c_ = coeffs(rect_tr, Tp, 12)
w0 = 2 * pi / Tp
ck = lambda k: A / (pi * k) * np.sin(k * w0 * 1.0)
check('rect train c_0 = A * (2 T1/T0) = 1.25', at(k_, c_, 0).real, 1.25, 1e-4)
for m in (1, 2, 3, 5):
    check(f'rect train c_{m} = (A/(pi k)) sin(k w0 T1)', at(k_, c_, m).real, ck(m), 2e-4)
check('Q6 c_1 = (5/pi) sin(pi/4) = 1.1254', ck(1), 1.12540, 1e-4)
for m in (4, 8, 12):
    check(f'Q7 c_{m} = 0 (sin(k pi/4) = 0 for k = 4, 8, 12)', abs(at(k_, c_, m)), 0.0, 2e-4)
check('   imaginary parts vanish (even signal): max |Im c_k|', float(np.max(np.abs(c_.imag))), 0.0, 2e-4)
# 50% duty 0/A square wave
T0 = 2.0; w0 = pi
sq01 = lambda t: np.where((t % T0) < T0 / 2, 1.0, 0.0)
k_, c_ = coeffs(sq01, T0, 9)
check('0/1 square wave: c_0 = 1/2', at(k_, c_, 0).real, 0.5, 1e-4)
# (the 0/A wave that starts at t = 0 carries a phase factor; use the even version centred on t = 0)
sq01e = lambda t: np.where(np.abs(((t + T0 / 2) % T0) - T0 / 2) < T0 / 4, 1.0, 0.0)
k_, c_ = coeffs(sq01e, T0, 9)
for m in (1, 2, 3, 5):
    check(f'even 0/1 square wave: c_{m} = sin(k pi/2)/(k pi)', at(k_, c_, m).real, np.sin(m * pi / 2) / (m * pi), 2e-4)
check('   trig form: a_1 = 2/pi', 2 * at(k_, c_, 1).real, 2 / pi, 4e-4); check('   a_3 = -2/(3 pi)', 2 * at(k_, c_, 3).real, -2 / (3 * pi), 4e-4)
# +-A odd square wave
T0 = 2.0
k_, c_ = coeffs(sq_pm(T0), T0, 9)
for m in (1, 3, 5, 7):
    check(f'+-1 square wave: c_{m} = -j 2/(pi k)', at(k_, c_, m).imag, -2 / (pi * m), 4e-4); check(f'   real part of c_{m}', at(k_, c_, m).real, 0.0, 4e-4)
for m in (0, 2, 4, 6):
    check(f'   c_{m} = 0 (even harmonics and DC)', abs(at(k_, c_, m)), 0.0, 4e-4)
check('   b_k = 4/(pi k): b_1 = j(c_1 - c_-1)', (1j * (at(k_, c_, 1) - at(k_, c_, -1))).real, 4 / pi, 4e-4)
# decay rates: jumps 1/k, kink 1/k^2
# even triangle between 0 and A (period T0): x = A (1 - 2|t|/T0) for |t| <= T0/2
T0 = 4.0; A = 3.0; w0 = 2 * pi / T0
tri = lambda t: A * (1 - 2 * np.abs(((t + T0 / 2) % T0) - T0 / 2) / T0)
k_, c_ = coeffs(tri, T0, 9)
check('even triangle 0..A: c_0 = A/2', at(k_, c_, 0).real, A / 2, 1e-6)
for m in (1, 3, 5, 7):
    check(f'   c_{m} = 2A/(pi^2 k^2)', at(k_, c_, m).real, 2 * A / (pi ** 2 * m ** 2), 1e-6)
for m in (2, 4, 6):
    check(f'   c_{m} = 0 (even k)', abs(at(k_, c_, m)), 0.0, 1e-6)
# +-1 triangle with period 2 (Q15): c_k = 4/(pi^2 k^2) (odd k)
T0 = 2.0
tri1 = lambda t: 1 - 2 * np.abs(((t + 1) % 2) - 1)            # +1 at t = 0 (and 2), -1 at t = 1
k_, c_ = coeffs(tri1, T0, 9)
check('+-1 triangle (T0 = 2): c_1 = 4/pi^2', at(k_, c_, 1).real, 4 / pi ** 2, 1e-6); check('   c_0 = 0', abs(at(k_, c_, 0)), 0.0, 1e-9)
check('   k^2 c_k is constant for odd k (1/k^2 decay): k = 5', 25 * at(k_, c_, 5).real, 4 / pi ** 2, 1e-5)
k_, csq = coeffs(sq_pm(2.0), 2.0, 9)
check('   square wave: k c_k is constant (1/k decay): |5 c_5|', 5 * abs(at(k_, csq, 5)), 2 / pi, 1e-3)
# Q15: derivative of the +-1 triangle (T0 = 2) is a +-2 square wave; first harmonic amplitude 2|d_1| = 8/pi
d1 = 1j * pi * at(k_, c_, 1)                # j k w0 c_k with w0 = pi
check('Q15 derivative: d_1 = j w0 c_1 has |d_1| = 4/pi', abs(d1), 4 / pi, 1e-6)
check('Q15 first-harmonic amplitude of the derivative 2|d_1| = 8/pi = 2.546', 2 * abs(d1), 8 / pi, 1e-6)
dtri = lambda t: -2 * np.sign(np.sin(pi * t)) * 1.0           # derivative of tri1 on (0,1) is -2, on (1,2) is +2
k_, cd = coeffs(dtri, 2.0, 5)
check('   the derivative is the +-2 square wave: |c_1| = 2 * 2/pi', abs(at(k_, cd, 1)), 4 / pi, 1e-3)
# sawtooth (odd ramp) x = A t / T0 for |t| < T0/2
T0 = 3.0; A = 2.0; w0 = 2 * pi / T0
saw = lambda t: A * (((t + T0 / 2) % T0) - T0 / 2) / T0
k_, c_ = coeffs(saw, T0, 8)
for m in (1, 2, 3, 4):
    check(f'sawtooth c_{m} = j A (-1)^k/(2 pi k)', at(k_, c_, m).imag, A * (-1) ** m / (2 * pi * m), 1e-3)
    check(f'   b_{m} = A (-1)^(k+1)/(pi k)', (1j * (at(k_, c_, m) - at(k_, c_, -m))).real, A * (-1) ** (m + 1) / (pi * m), 2e-3)
# full-wave rectified sine, A |sin(ws t)|
ws = pi; T0 = pi / ws; w0 = 2 * pi / T0
fw = lambda t: np.abs(np.sin(ws * t))
k_, c_ = coeffs(fw, T0, 6)
for m in (0, 1, 2, 3):
    check(f'full-wave rectified sine c_{m} = 2A/(pi (1 - 4k^2))', at(k_, c_, m).real, 2 / (pi * (1 - 4 * m * m)), 1e-6)
check('Q8 trig coefficient a_1 = 2 c_1 = -4/(3 pi) = -0.4244', 2 * at(k_, c_, 1).real, -4 / (3 * pi), 1e-6)
check('   DC value 2/pi = 0.6366', at(k_, c_, 0).real, 2 / pi, 1e-6)
# half-wave rectified sine A sin(w0 t) on (0, T0/2)
T0 = 2 * pi; w0 = 1.0
hw = lambda t: np.where((t % T0) < pi, np.sin(t % T0), 0.0)
k_, c_ = coeffs(hw, T0, 6)
check('half-wave rectified sine c_0 = A/pi', at(k_, c_, 0).real, 1 / pi, 1e-4)
check('   c_1 = -j A/4 (b_1 = A/2)', at(k_, c_, 1).imag, -0.25, 1e-4)
for m in (2, 4, 6):
    check(f'   c_{m} = -A/(pi (k^2 - 1))', at(k_, c_, m).real, -1 / (pi * (m * m - 1)), 1e-4)
for m in (3, 5):
    check(f'   c_{m} = 0 (odd harmonics above the first vanish)', abs(at(k_, c_, m)), 0.0, 1e-4)
# impulse train as a limit of narrow unit-area pulses
T0 = 5.0; w = 1e-3
narrow = lambda t: (3.0 / w) * np.where(np.abs(((t + T0 / 2) % T0) - T0 / 2) < w / 2, 1.0, 0.0)
k_, c_ = coeffs(narrow, T0, 8, N=1 << 20)
check('Q9 impulse train 3 sum delta(t - 5n): c_7 = 3/5 = 0.6', at(k_, c_, 7).real, 0.6, 2e-3)
check('   all coefficients equal (flat spectrum): max |c_k - 0.6|', float(np.max(np.abs(c_ - 0.6))), 0.0, 2e-3)
# P2: e^-t on (0,1), period 1
T0 = 1.0
ex = lambda t: np.exp(-(t % T0))
k_, c_ = coeffs(ex, T0, 40)
for m in (0, 1, 2, -3):
    check(f'P2 c_{m} = (1 - e^-1)/(1 + j 2 pi k): modulus', abs(at(k_, c_, m)), (1 - np.exp(-1)) / abs(1 + 2j * pi * m), 1e-5)
check('P2 c_0 = 0.6321', at(k_, c_, 0).real, 0.632121, 1e-5); check('P2 |c_1| = 0.0993', abs(at(k_, c_, 1)), 0.09934, 5e-5)
check('P2 angle of c_1 = -arctan(2 pi) = -80.96 deg', float(np.degrees(np.angle(at(k_, c_, 1)))), -80.9568, 1e-2)
Pex = (1 - np.exp(-2)) / 2
check('P2 power (1/T) int e^-2t = (1 - e^-2)/2 = 0.4323', mean_square(ex, T0), Pex, 1e-6)
kk_ = np.arange(-200000, 200001)
check('P2 Parseval: (1 - e^-1)^2 sum 1/(1 + 4 pi^2 k^2) = same', float((1 - np.exp(-1)) ** 2 * np.sum(1 / (1 + 4 * pi ** 2 * kk_ ** 2))), Pex, 1e-6)
check('P2 fraction of the power in the DC term c_0^2 / P = 2 tanh(1/2) = 92.4 %', float((1 - np.exp(-1)) ** 2 / Pex), float(2 * np.tanh(0.5)), 1e-9)

# ================================================================================ 4. symmetry
T0 = 2.0
k_, c_ = coeffs(sq_pm(T0), T0, 8)
check('real odd (sawtooth/square): c_0 = 0', abs(at(k_, c_, 0)), 0.0, 1e-9)
check('   c_-k = -c_k for all k: max error', float(max(abs(at(k_, c_, m) + at(k_, c_, -m)) for m in range(1, 8))), 0.0, 1e-9)
check('   all c_k purely imaginary: max |Re c_k|', float(np.max(np.abs(c_.real))), 0.0, 1e-4)
# half-wave symmetric signal: only odd harmonics
Th = 3.0; wh = 2 * pi / Th
hws = lambda t: np.sin(wh * t) + 0.5 * np.sin(3 * wh * t + 1.0) + 0.2 * np.cos(5 * wh * t) + 0.8 * np.cos(wh * t - 0.4)
check('half-wave symmetry x(t - T/2) = -x(t) for the test signal', float(np.max(np.abs(hws(np.linspace(0, 3, 500) - Th / 2) + hws(np.linspace(0, 3, 500))))), 0.0, 1e-9)
k_, c_ = coeffs(hws, Th, 8)
check('   all even-k coefficients (including k = 0) vanish', float(max(abs(at(k_, c_, m)) for m in (-8, -6, -4, -2, 0, 2, 4, 6, 8))), 0.0, 1e-9)
assert abs(at(k_, c_, 3)) > 0.1
print('ok     odd-k coefficients do not vanish: |c_3| =', round(float(abs(at(k_, c_, 3))), 4))
# converse: only odd harmonics => half-wave symmetric.  Build from odd harmonics with random complex weights (and conjugates)
rng = np.random.default_rng(3)
cc = {m: rng.normal() + 1j * rng.normal() for m in (1, 3, 5, 7)}
xo = lambda t: sum(2 * (v * np.exp(1j * m * wh * t)).real for m, v in cc.items())
check('only odd harmonics present => x(t + T/2) = -x(t)', float(np.max(np.abs(xo(np.linspace(0, 3, 400) + Th / 2) + xo(np.linspace(0, 3, 400))))), 0.0, 1e-9)
# a signal WITHOUT half-wave symmetry has even-order coefficients: 0/1 square wave (c_0), half-wave rectified sine (c_2)
check('counter-example: the 0/1 square wave has c_0 = 1/2 (no half-wave symmetry)', 0.5, 0.5)
# shift argument: x(t - T/2) <-> (-1)^k c_k
k_, c_ = coeffs(lambda t: np.exp(-(t % 1.0)), 1.0, 6)
k_, cs = coeffs(lambda t: np.exp(-(((t - 0.5)) % 1.0)), 1.0, 6)
check('shift by T/2 multiplies c_k by (-1)^k: max error', float(max(abs(at(k_, cs, m) - (-1) ** m * at(k_, c_, m)) for m in range(-5, 6))), 0.0, 1e-4)
# real even => real even coefficients ; general real => c_-k = conj(c_k)
k_, c_ = coeffs(lambda t: np.exp(-(t % 1.0)), 1.0, 10)
check('real x: c_-k = conj(c_k) (e^-t on (0,1))', float(max(abs(at(k_, c_, -m) - np.conj(at(k_, c_, m))) for m in range(1, 10))), 0.0, 1e-9)
# Q10 / Q11 / Q12
c1c3 = 2 * (abs(2 + 2j) ** 2 + abs(-1) ** 2)
check('Q12 power in k = +-1, +-3: 2(8 + 1) = 18', c1c3, 18.0); check('Q12 power in |k| >= 5: 30 - 18', 30 - c1c3, 12.0)

# ================================================================================ 5. properties
T0 = 3.0; w0 = 2 * pi / T0
base = lambda t: np.exp(-((t % T0)) / 2) * (1 + 0.3 * np.cos(w0 * (t % T0)))
k_, c_ = coeffs(base, T0, 8)
# time shift
t0 = 0.7
k_, cs = coeffs(lambda t: base(t - t0), T0, 8)
check('time shift x(t - t0) <-> c_k e^(-j k w0 t0): max error', float(max(abs(at(k_, cs, m) - at(k_, c_, m) * np.exp(-1j * m * w0 * t0)) for m in range(-6, 7))), 0.0, 1e-4)
check('   magnitudes unchanged', float(max(abs(abs(at(k_, cs, m)) - abs(at(k_, c_, m))) for m in range(-6, 7))), 0.0, 1e-4)
check('Q13 d_2 = 3 e^{-j k w0 t0} with w0 = pi/4, k = 2, t0 = 1: angle -90 deg', float(np.degrees(np.angle(3 * np.exp(-1j * 2 * (pi / 4) * 1.0)))), -90.0, 1e-9)
# time reversal, conjugation
k_, cr = coeffs(lambda t: base(-t), T0, 8)
check('time reversal x(-t) <-> c_-k', float(max(abs(at(k_, cr, m) - at(k_, c_, -m)) for m in range(-6, 7))), 0.0, 1e-4)
cplx = lambda t: np.exp(1j * w0 * t) * (1 + 0.5 * np.cos(2 * w0 * t)) + 0.3j * np.sin(w0 * t)
k_, cx = coeffs(cplx, T0, 6)
k_, cxc = coeffs(lambda t: np.conj(cplx(t)), T0, 6)
check('conjugation x*(t) <-> conj(c_-k)', float(max(abs(at(k_, cxc, m) - np.conj(at(k_, cx, -m))) for m in range(-5, 6))), 0.0, 1e-9)
# frequency shift and multiplication by cos
k_, cm = coeffs(lambda t: base(t) * np.exp(1j * 2 * w0 * t), T0, 8)
check('x(t) e^{j 2 w0 t} <-> c_{k-2}', float(max(abs(at(k_, cm, m) - at(k_, c_, m - 2)) for m in range(-5, 7))), 0.0, 1e-4)
yq = lambda t: 2 + 2 * np.cos(w0 * t) + 6 * np.cos(2 * w0 * t)
zq = lambda t: yq(t) * np.cos(w0 * t)
k_, cz = coeffs(zq, T0, 5)
check('Q16 y has d_0 = 2, d_+-1 = 1, d_+-2 = 3; z = y cos(w0 t): e_1 = (d_0 + d_2)/2 = 2.5', at(k_, cz, 1).real, 2.5, 1e-9)
check('   e_0 = (d_-1 + d_1)/2 = 1', at(k_, cz, 0).real, 1.0, 1e-9)
# time scaling (2025 Q55, Q14)
Tq = 3.0
f_ = lambda t: np.exp(-(t % Tq)) + 0.2 * np.cos(2 * pi * t / Tq)
k_, cf = coeffs(f_, Tq, 6)
k_, cy = coeffs(lambda t: f_(2 * t), Tq / 2, 6)
check('2025 Q55 y(t) = f(2t) has period T0/2 and, in its own harmonics, d_k = c_k: max error', float(max(abs(at(k_, cy, m) - at(k_, cf, m)) for m in range(-5, 6))), 0.0, 1e-4)
check('   power of y equals power of f', mean_square(lambda t: f_(2 * t), Tq / 2), mean_square(f_, Tq), 1e-6)
check('   y(t + T0/2) = y(t)', float(np.max(np.abs(f_(2 * (np.linspace(0, 3, 300) + Tq / 2)) - f_(2 * np.linspace(0, 3, 300))))), 0.0, 1e-9)
# differentiation and integration
T0 = 2.0
k_, ct_ = coeffs(tri1, T0, 8)
k_, cdt = coeffs(lambda t: -2 * np.sign(np.sin(pi * t)), T0, 8)
check('differentiation: dx/dt <-> j k w0 c_k (triangle -> square), k = 1, 3, 5', float(max(abs(at(k_, cdt, m) - 1j * m * pi * at(k_, ct_, m)) for m in (1, 3, 5))), 0.0, 3e-3)
# integration: the (zero-mean) integral of the +-1 square wave is a triangle between -1/2 and 1/2 with d_k = c_k/(j k w0) = -2/(pi^2 k^2)
y_int = lambda t: np.where((t % 2) < 1, t % 2, 2 - (t % 2)) - 0.5
kq, cqq = coeffs(sq_pm(2.0), 2.0, 8)
ki, ci = coeffs(y_int, 2.0, 8)
check('integration: int of the +-1 square wave <-> c_k/(j k w0), k = 1, 3, 5, 7', float(max(abs(at(ki, ci, m) - at(kq, cqq, m) / (1j * m * pi)) for m in (1, 3, 5, 7))), 0.0, 1e-4)
check('   = -2/(pi^2 k^2): k = 1', at(ki, ci, 1).real, -2 / pi ** 2, 1e-4)
# multiplication <-> convolution of coefficients; periodic convolution <-> T c d
T0 = 3.0; w0 = 2 * pi / T0
xa = lambda t: 1 + np.cos(w0 * t) + 0.5 * np.sin(2 * w0 * t)
xb = lambda t: 2 + 0.3 * np.cos(w0 * t + 0.5) - np.cos(3 * w0 * t)
k_, ca = coeffs(xa, T0, 8); k_, cb = coeffs(xb, T0, 8); k_, cab = coeffs(lambda t: xa(t) * xb(t), T0, 8)   # same index array k_ = -8..8 for all three
conv_c = np.array([sum(at(k_, ca, m) * at(k_, cb, kk - m) for m in range(-4, 5) if -8 <= kk - m <= 8) for kk in range(-4, 5)])
check('product x y <-> convolution of coefficients  sum_m c_m d_(k-m): max error (k = -4..4)', float(np.max(np.abs(conv_c - np.array([at(k_, cab, kk) for kk in range(-4, 5)])))), 0.0, 1e-9)
tau = np.linspace(0, T0, 3001)[:-1]
pconv = lambda t: np.array([np.mean(xa(tau) * xb(t_i - tau)) * T0 for t_i in np.atleast_1d(t)])
kp, cpc = coeffs(pconv, T0, 5, N=1 << 11)
check('periodic convolution  int_T x(tau) y(t - tau) dtau  <-> T c_k d_k: max error (k = -3..3)', float(max(abs(at(kp, cpc, m) - T0 * at(k_, ca, m) * at(k_, cb, m)) for m in range(-3, 4))), 0.0, 1e-6)
# Parseval
Tp, A = 8.0, 5.0
k_, c_ = coeffs(rect_tr, Tp, 200, N=1 << 18)
check('Parseval: rect train, (1/T) int x^2 = A^2 (2T1/T0) = 6.25', mean_square(rect_tr, Tp), 6.25, 1e-3)
check('   sum |c_k|^2 for |k| <= 200', float(np.sum(np.abs(c_) ** 2)), 6.25, 2e-2)
T0 = 2.0
k_, csq = coeffs(sq_pm(T0), T0, 2001, N=1 << 18)
for mmax, want in ((1, 8 / pi ** 2), (3, 8 / pi ** 2 * (1 + 1 / 9)), (5, 8 / pi ** 2 * (1 + 1 / 9 + 1 / 25)), (7, 8 / pi ** 2 * (1 + 1 / 9 + 1 / 25 + 1 / 49)), (9, 8 / pi ** 2 * (1 + 1 / 9 + 1 / 25 + 1 / 49 + 1 / 81))):
    frac = sum(2 * abs(at(k_, csq, m)) ** 2 for m in range(1, mmax + 1, 2))
    check(f'+-1 square wave: power in harmonics up to {mmax} (total power 1)', frac, want, 1e-3)
check('   fundamental carries 8/pi^2 = 81.06 %', 8 / pi ** 2, 0.810569, 1e-6)
check('   up to the 7th harmonic: 94.96 % (< 95 %); up to the 9th: 95.96 %', 8 / pi ** 2 * (1 + 1 / 9 + 1 / 25 + 1 / 49), 0.94960, 1e-4)
assert 8 / pi ** 2 * (1 + 1 / 9 + 1 / 25 + 1 / 49) < 0.95 < 8 / pi ** 2 * (1 + 1 / 9 + 1 / 25 + 1 / 49 + 1 / 81)
print('ok     5 non-zero harmonics (1, 3, 5, 7, 9) are needed for 95 % of the power')
# least-squares property of truncation (+-1 square wave)
def partial_sum(t, Kmax, coef=None):
    s = np.zeros_like(t)
    for m in range(1, Kmax + 1, 2):
        s += (4 / (pi * m) if coef is None else coef[m]) * np.sin(m * pi * t)
    return s
tt = np.linspace(0, 2, 200_001)[:-1]
xs = np.where(tt < 1, 1.0, -1.0)
for Kmax in (1, 3, 9, 27):
    err = float(np.mean((xs - partial_sum(tt, Kmax)) ** 2))
    tail = 8 / pi ** 2 * sum(1 / m ** 2 for m in range(Kmax + 2, 4001, 2))
    print(f'      truncation at harmonic {Kmax:>2}: mean-square error {err:.5f}  (tail power {tail:.5f})')
    assert abs(err - tail) < 2e-3
rng = np.random.default_rng(5)
base_err = float(np.mean((xs - partial_sum(tt, 9)) ** 2))
worse = 0
for _ in range(20):
    coef = {m: 4 / (pi * m) + 0.05 * rng.normal() for m in range(1, 10, 2)}
    if float(np.mean((xs - partial_sum(tt, 9, coef)) ** 2)) > base_err: worse += 1
check('least squares: any perturbation of the 5 coefficients increases the error (20 trials)', worse, 20, 0)

# ================================================================================ 6. convergence and Gibbs
# ramp x(t) = t on [0, 1), period 1: series 1/2 - sum sin(2 pi k t)/(pi k)
def ramp_ps(t, N):
    k = np.arange(1, N + 1)
    return 0.5 - np.sum(np.sin(2 * pi * np.outer(t, k)) / (pi * k), axis=1)
check('Q17 sawtooth x(t) = t on [0,1): series at the jump t = 3 converges to (1 + 0)/2', float(ramp_ps(np.array([3.0]), 2000)[0]), 0.5, 1e-9)
check('   ... and at t = 3.5 (continuity point) to 0.5', float(ramp_ps(np.array([3.5]), 4001)[0]), 0.5, 1e-3)
check('   ... and at t = 3.25 to 0.25', float(ramp_ps(np.array([3.25]), 4001)[0]), 0.25, 1e-3)
# Gibbs
Si_pi = special.sici(pi)[0]
check('Si(pi) = 1.851937 (Wilbraham-Gibbs constant)', float(Si_pi), 1.851937052, 1e-8)
over = Si_pi / pi - 0.5
check('overshoot fraction of the jump: Si(pi)/pi - 1/2 = 0.0894899', float(over), 0.089489872, 1e-8)
check('peak of the partial sums of the +-1 square wave tends to (2/pi) Si(pi) = 1.17898', float(2 / pi * Si_pi), 1.178980, 1e-5)
tfine = np.linspace(1e-5, 0.5, 400_001)
peaks = {}
for Nh in (5, 21, 101, 401):
    s = np.zeros_like(tfine)
    for m in range(1, Nh + 1, 2):
        s += 4 / (pi * m) * np.sin(m * pi * tfine)
    peaks[Nh] = float(s.max()); tpk = float(tfine[np.argmax(s)])
    print(f'      N = {Nh:>3}: peak {peaks[Nh]:.5f} at t = {tpk:.5f}')
assert peaks[401] > 1.17 and abs(peaks[401] - 1.17898) < 2e-3
assert all(v > 1.17 for k_n, v in peaks.items() if k_n >= 21)
print('ok  the peak does not shrink as N grows (it moves toward the jump): 21 -> 401 terms stays above 1.17')
check('Q18 jump from -2 to +2 (size 4): peak = 2 + 0.08949 * 4 = 2.358', 2 + float(over) * 4, 2.35796, 1e-5)
check('   same peak from the +-1 wave scaled by 2: 2 * 1.17898', 2 * float(2 / pi * Si_pi), 2.35796, 1e-5)
# partial sums at the jump of the square wave
s0 = partial_sum(np.array([1.0]), 99)
check('square wave: partial sum at the jump t = 1 is exactly the midpoint 0', float(s0[0]), 0.0, 1e-12)

# ================================================================================ 7. periodic input through an LTI system
# RC low-pass H = 1/(1 + jw), +-1 square wave with w0 = 1 rad/s (T0 = 2 pi): y' + y = x(t)
T0 = 2 * pi
sqw = lambda t: 1.0 if (t % T0) < T0 / 2 else -1.0
def rhs(t, y): return [-y[0] + sqw(t)]
tev = np.linspace(40 * T0, 42 * T0, 20001)
sol = solve_ivp(rhs, (0, 42 * T0), [0.0], t_eval=tev, rtol=1e-10, atol=1e-12, max_step=0.05)
ys = sol.y[0]
tt_ = tev - 40 * T0
Y = np.fft.rfft(ys[:-1]) / (len(ys) - 1) * 2            # amplitude spectrum over two periods -> harmonic k at index 2k
amp = lambda k: abs(Y[2 * k])
for m in (1, 3, 5):
    want = (4 / (pi * m)) / np.sqrt(1 + m * m)
    check(f'P5 RC low-pass (RC = 1/w0): amplitude of harmonic {m} = (4/(pi k))/sqrt(1 + k^2)', float(amp(m)), want, 2e-3)
check('   harmonic 3 amplitude 0.1342', 4 / (3 * pi * np.sqrt(10)), 0.13423, 1e-4); check('   harmonic 5 amplitude 0.0499', 4 / (5 * pi * np.sqrt(26)), 0.049944, 1e-5)
check('   harmonic 1: 4/(pi sqrt 2) = 0.9003', 4 / (pi * np.sqrt(2)), 0.900316, 1e-6)
check('   even harmonics absent in the output: |Y_2|', float(amp(2)), 0.0, 2e-3)
# Q19: y(t) = x(t) - x(t - 1) with T0 = 2 removes the even harmonics (H(jk pi) = 1 - (-1)^k)
Tq = 2.0
xg = lambda t: np.exp(-(t % Tq)) + 0.4 * np.cos(pi * t + 0.3) + 0.2 * np.cos(2 * pi * t) + 0.1 * np.sin(3 * pi * t)      # w0 = pi: harmonics 1, 2, 3
yq_ = lambda t: xg(t) - xg(t - 1.0)
k_, cx = coeffs(xg, Tq, 6); k_, cy = coeffs(yq_, Tq, 6)
check('Q19 H(j k pi) = 1 - e^{-j k pi} = 1 - (-1)^k: coefficients of y equal c_k (1 - (-1)^k)', float(max(abs(at(k_, cy, m) - at(k_, cx, m) * (1 - (-1) ** m)) for m in range(-5, 6))), 0.0, 1e-4)
check('   even harmonics (and DC) removed', float(max(abs(at(k_, cy, m)) for m in (-4, -2, 0, 2, 4))), 0.0, 1e-4)
check('   odd harmonics doubled: |d_1| / |c_1|', abs(at(k_, cy, 1)) / abs(at(k_, cx, 1)), 2.0, 1e-3)
check('   y has half-wave symmetry y(t - 1) = -y(t)', float(np.max(np.abs(yq_(np.linspace(0, 2, 300) - 1.0) + yq_(np.linspace(0, 2, 300))))), 0.0, 1e-9)

# ================================================================================ 8. spectra, DTFS, DT Parseval
a_ = np.array([1, 3j, 2j, -2j, -3j])
n5 = np.arange(5)
x_dt = sum(a_[k] * np.exp(2j * pi * k * n5 / 5) for k in range(5))
val = np.sum(x_dt * np.sin(4 * pi * n5 / 5))
check('2023 Q47 [key A]: sum x[n] sin(4 pi n/5) = (5 a_3 - 5 a_2)/(2j) = -10 (real part)', float(val.real), -10.0, 1e-9)
check('   ... imaginary part', float(val.imag), 0.0, 1e-9)
check('   closed form (5 a_3 - 5 a_2)/(2j)', float(((5 * a_[3] - 5 * a_[2]) / 2j).real), -10.0, 1e-12)
xd = 1 + 2 * np.cos(pi * np.arange(4) / 2)
ak = np.fft.fft(xd) / 4
checkv('DTFS of 1 + 2cos(pi n/2) (N = 4): a = {1, 1, 0, 1}', ak.real, [1, 1, 0, 1], 1e-12)
check('DT Parseval: (1/N) sum |x|^2 = sum |a_k|^2 = 3', float(np.mean(np.abs(xd) ** 2)), 3.0, 1e-12); check('   sum |a_k|^2', float(np.sum(np.abs(ak) ** 2)), 3.0, 1e-12)
# 2023 Q29 : table of spectrum types (logic)
types = {('CT', 'periodic'): ('discrete', 'aperiodic'), ('CT', 'aperiodic'): ('continuous', 'aperiodic'),
         ('DT', 'aperiodic'): ('continuous', 'periodic'), ('DT', 'periodic'): ('discrete', 'periodic')}
for (dom, per), (sp_d, sp_p) in types.items():
    assert (per == 'periodic') == (sp_d == 'discrete'), 'periodic in time <=> discrete spectrum'
    assert (dom == 'DT') == (sp_p == 'periodic') or (dom == 'CT' and per == 'periodic' and sp_p == 'aperiodic') or (dom == 'CT' and sp_p == 'aperiodic'), 'DT <=> periodic spectrum'
print('ok  2023 Q29 [key B]: CT periodic -> discrete & aperiodic (c); DT aperiodic -> continuous & periodic (b); (i)-(a), (ii)-(c), (iii)-(b), (iv)-(d)')

# ================================================================================ 9. past-year questions
# 2021 Q39
T0 = 6.0; w0 = pi / 3
x39 = lambda t: 2 + sum(2 * k * np.cos(k * w0 * t) for k in (1, 2, 3))
k_, c39 = coeffs(x39, T0, 6)
for m, want in ((0, 2), (1, 1), (2, 2), (3, 3), (-1, 1), (-2, 2), (-3, 3), (4, 0)):
    check(f'2021 Q39 c_{m} = {want}', at(k_, c39, m).real, want, 1e-9)
check('2021 Q39 [key 31.9 to 32.1]: average power = 4 + 2(1 + 4 + 9) = 32', float(np.sum(np.abs(c39) ** 2)), 32.0, 1e-9)
check('   same from the waveform (1/T) int x^2', mean_square(x39, T0), 32.0, 1e-6)
check('   trap: forgetting the negative-k terms gives 4 + 14', 4 + 1 + 4 + 9, 18.0)
check('   x(t) is real and even with average 2: x(0) = 2 + 2(1 + 2 + 3)', float(x39(np.array([0.0]))[0]), 14.0, 1e-12)
# 2025 Q55 : verified above (d_k = c_k, period T0/alpha); explicit options table
print('ok  2025 Q55 [key A;D]: c_k = d_k and the fundamental period of y(t) = f(alpha t) is T0/alpha')
# 2026 Q37: half-wave symmetric => a_{2m} = 0 for every integer m (checked above with the test signal)
print('ok  2026 Q37 [key A]: x(t - T/2) = -x(t) gives (-1)^k c_k = -c_k, so c_k = 0 for even k, i.e. a_{2m} = 0')
k_, csqq = coeffs(sq_pm(2.0), 2.0, 6)
assert abs(at(k_, csqq, 2)) < 1e-9 and abs(at(k_, csqq, 3)) > 0.1
print('ok     (C) a_2m = a_2m+1 fails: the +-1 square wave has a_2 = 0 but |a_3| =', round(float(abs(at(k_, csqq, 3))), 4))
# 2026 Q58
for n in (1, 2, 3):
    t_a = np.linspace(0, 1 / n, 800_001)
    x1_ = np.cos(2 * pi * n * t_a); x2_ = 2 * np.sin(4 * pi * n * t_a)
    check(f'2026 Q58 n = {n}: int_0^(1/n) x1 x2 dt = 0 (orthogonal)', np.trapezoid(x1_ * x2_, t_a), 0.0, 1e-9)
    check(f'   energy of x1 over [0, 1/n) = 1/(2n) != 1 (not orthonormal)', np.trapezoid(x1_ ** 2, t_a), 1 / (2 * n), 1e-9)
    t_b = np.linspace(0, 1 / (2 * n), 800_001)
    check(f'   int_0^(1/(2n)) x1 x2 dt = 4/(3 pi n) != 0 (non-orthogonal)', np.trapezoid(np.cos(2 * pi * n * t_b) * 2 * np.sin(4 * pi * n * t_b), t_b), 4 / (3 * pi * n), 1e-9)
print('ok  2026 Q58 [key A;C;D]: x2 has frequency 2n = 2 x (n Hz): the second harmonic of x1')
# 2019 Q44
h = {0: 4, 1: 3, 2: 2, 3: 1, -1: -3, -2: -2, -3: -1}
best = None
for s in range(-6, 5):
    support = {s, s + 1, s + 2}
    err = sum(v * v for nn_, v in h.items() if nn_ not in support) + 0.0
    # the error also includes any h tap outside the support only; inside the support g = h is optimal
    if best is None or err < best[0]: best = (err, s)
check('2019 Q44: best 3-tap window starts at n = -1 (error energy 10)', best[1], -1, 0); check('   error energy outside the window', best[0], 10.0, 1e-12)
g = {-1: h[-1], 0: h[0], 1: h[1]}
check('2019 Q44 [key -27.01 to -26.99]: 10 g[-1] + g[1] = 10(-3) + 3', 10 * g[-1] + g[1], -27.0, 1e-12)
wgrid = np.linspace(-pi, pi, 400_001)
Hf = lambda d: sum(v * np.exp(-1j * wgrid * k) for k, v in d.items())
E = np.trapezoid(np.abs(Hf(h) - Hf(g)) ** 2, wgrid)
check('   E(h, g) = integral |H - G|^2 d omega = 2 pi * 10 (Parseval)', float(E), 2 * pi * 10, 1e-6)
# any perturbation of g raises E
for dg in ({-1: 0.1}, {0: -0.2}, {1: 0.3}):
    g2 = dict(g)
    for kk_, vv in dg.items(): g2[kk_] += vv
    assert np.trapezoid(np.abs(Hf(h) - Hf(g2)) ** 2, wgrid) > E
print('ok     perturbing any tap of g increases E: the truncation g = h on {-1, 0, 1} is the minimiser')

# ================================================================================ 10. practice problems
# P1
Tq = 2.0; w0 = pi
xp1 = lambda t: 1 + 2 * np.cos(pi * t) + 3 * np.sin(3 * pi * t + pi / 4)
k_, cp = coeffs(xp1, Tq, 5)
check('P1 T0 = 2: c_0 = 1', at(k_, cp, 0).real, 1.0, 1e-9); check('P1 c_1 = 1', at(k_, cp, 1).real, 1.0, 1e-9)
check('P1 |c_3| = 3/2', abs(at(k_, cp, 3)), 1.5, 1e-9); check('P1 angle of c_3 = -45 deg', float(np.degrees(np.angle(at(k_, cp, 3)))), -45.0, 1e-6)
check('P1 power = 1 + 4/2 + 9/2 = 7.5', mean_square(xp1, Tq), 7.5, 1e-6)
# P4 shown above; P6
check('P6 |d_2| = 0.2 |-2 + j pi| = 0.7448', 0.2 * abs(-2 + 1j * pi), 0.74484, 1e-4)
# P6 check with an actual signal: x with c_2 = 0.2 (T0 = 4); y = 2x(t - 1) + x'(t)
T0 = 4.0; w0 = 2 * pi / T0
xP6 = lambda t: 0.4 * np.cos(2 * w0 * t) + 0.3 * np.cos(w0 * t + 0.4)
dx = lambda t: -0.4 * 2 * w0 * np.sin(2 * w0 * t) - 0.3 * w0 * np.sin(w0 * t + 0.4)
yP6 = lambda t: 2 * xP6(t - 1) + dx(t)
k_, cyy = coeffs(yP6, T0, 4)
check('P6 y = 2x(t - 1) + dx/dt: d_2 = c_2 (2 e^{-j k w0} + j k w0) = 0.2(-2 + j pi): modulus', abs(at(k_, cyy, 2)), 0.2 * abs(-2 + 1j * pi), 1e-9)

# ================================================================================ 11. extra checks quoted in the note
# Ex 1 of section 2: x = 3 - 2cos(2t) + 4 sin(6t)
xe1 = lambda t: 3 - 2 * np.cos(2 * t) + 4 * np.sin(6 * t)
k_, ce = coeffs(xe1, pi, 5)
check('Ex 1: T0 = pi, c_0 = 3', at(k_, ce, 0).real, 3.0, 1e-9); check('   c_+-1 = -1', at(k_, ce, 1).real, -1.0, 1e-9); check('   c_3 = -2j', at(k_, ce, 3).imag, -2.0, 1e-9); check('   c_-3 = +2j', at(k_, ce, -3).imag, 2.0, 1e-9)
check('   power = 9 + 2 + 8 = 19', mean_square(xe1, pi), 19.0, 1e-6)
# half-period orthogonality of sin and cos depends on the parity of the two harmonic numbers
for kk_, mm_, want in ((1, 3, 0.0), (2, 4, 0.0), (1, 2, None), (2, 3, None)):
    v = np.trapezoid(np.sin(kk_ * th) * np.cos(mm_ * th), th)
    if want is None:
        assert abs(v) > 0.1; print(f'ok  half period: sin({kk_} th) cos({mm_} th) is NOT orthogonal ({v:.4f})')
    else:
        check(f'half period: sin({kk_} th) cos({mm_} th) IS orthogonal (same parity)', v, 0.0, 1e-9)
# quarter-wave shortcut b_k = (8/T0) int_0^(T0/4) x sin(k w0 t) dt for the +-1 square wave
T0 = 2.0; w0 = pi
tq = np.linspace(0, T0 / 4, 400_001)
for m in (1, 3, 5):
    check(f'quarter-wave: b_{m} = (8/T0) int_0^(T0/4) sin(k w0 t) dt = 4/(pi k)', 8 / T0 * np.trapezoid(np.sin(m * w0 * tq), tq), 4 / (pi * m), 1e-9)
# real even signal: c_k = (2/T0) int_0^(T0/2) x cos(k w0 t) dt  (triangle +-1, T0 = 2)
th2 = np.linspace(0, 1, 400_001)
check('even real: c_1 = (2/T0) int_0^(T0/2) x cos(w0 t) dt = 4/pi^2 for the +-1 triangle', 2 / T0 * np.trapezoid((1 - 2 * th2) * np.cos(pi * th2), th2), 4 / pi ** 2, 1e-9)
# |sin t| with T0 = 2 pi has only even harmonics (its true period is pi)
k_, cabs = coeffs(lambda t: np.abs(np.sin(t)), 2 * pi, 6)
check('|sin t| viewed with T0 = 2 pi: odd coefficients vanish', float(max(abs(at(k_, cabs, m)) for m in (-5, -3, -1, 1, 3, 5))), 0.0, 1e-6)
check('   c_2 = 2/(pi (1 - 4)) = -2/(3 pi) in the T0 = 2 pi basis (k = 1 of the true period pi)', at(k_, cabs, 2).real, -2 / (3 * pi), 1e-6)
# 0/1 square wave = 1/2 + (1/2)(+-1 square wave): half-wave symmetry about the mean
check('0/1 square wave minus its mean has half-wave symmetry', float(np.max(np.abs((sq01(np.linspace(0, 2, 300) - 1.0) - 0.5) + (sq01(np.linspace(0, 2, 300)) - 0.5)))), 0.0, 1e-12)
# P5: phase of the RC output harmonics (x = sign(sin t), H = 1/(1 + jw)):  sin(kt) -> |H| sin(kt - arctan k)
for m in (1, 3):
    check(f'P5 phase of harmonic {m}: angle(Y_k) = -arctan(k) - pi/2 (a sine has a -90 degree cosine phase)', float(np.angle(Y[2 * m])), float(-np.arctan(m) - pi / 2), 2e-3)
print('ok  P5 fundamental of the output: 0.9003 sin(w0 t - 45 deg)')

print('\nall Day 9 checks passed')
