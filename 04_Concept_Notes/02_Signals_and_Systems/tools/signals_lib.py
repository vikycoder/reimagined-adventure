"""Small numerical toolkit used to verify the Signals-and-Systems notes (Days 7 onwards).

Continuous-time signals are Python callables x(t) that accept numpy arrays; a *system* maps such a callable to another
callable.  The property testers do not prove anything: they look for counter-examples with concrete test inputs, which is
enough to confirm (or refute) the textbook classification of a given system.  Discrete-time versions follow the same pattern
with callables x(n) on integer arrays.
"""
import numpy as np

# ---------------------------------------------------------------------------------------------- standard signals
u = lambda t: np.where(np.asarray(t) >= 0, 1.0, 0.0)                  # unit step (value 1 at 0; irrelevant for integrals)
ramp = lambda t: np.asarray(t) * u(t)
rect = lambda t: np.where(np.abs(np.asarray(t)) < 0.5, 1.0, 0.0)      # unit-width rectangle
tri = lambda t: np.maximum(1 - np.abs(np.asarray(t)), 0.0)            # unit triangle (support [-1, 1])
sinc = np.sinc                                                         # numpy's sinc is sin(pi x)/(pi x)


def energy(x, a=-50.0, b=50.0, n=2_000_001):
    t = np.linspace(a, b, n)
    return np.trapezoid(np.abs(x(t)) ** 2, t)


def avg_power(x, T, a=0.0, n=200001):
    t = np.linspace(a, a + T, n)
    return np.trapezoid(np.abs(x(t)) ** 2, t) / T


def smallest_period(x, candidates, tol=1e-9):
    """Smallest candidate T with x(t + T) = x(t) on a fine random grid."""
    t = np.random.default_rng(0).uniform(-20, 20, 4000)
    for T in sorted(candidates):
        if np.max(np.abs(x(t + T) - x(t))) < tol:
            return T
    return None


def dt_smallest_period(x, Nmax=500):
    n = np.arange(-1000, 1000)
    for N in range(1, Nmax + 1):
        if np.max(np.abs(x(n + N) - x(n))) < 1e-9:
            return N
    return None


# ---------------------------------------------------------------------------------------------- continuous-time property testers
def _inputs():
    A = lambda t: np.asarray(t, dtype=float)
    g1 = lambda t: np.exp(-A(t) ** 2 / 4) * np.cos(3 * A(t))
    g2 = lambda t: np.exp(-(A(t) - 1) ** 2) * np.sin(2 * A(t)) + 0.3 * np.exp(-np.abs(A(t)))
    g3 = lambda t: np.cos(0.7 * A(t)) * np.exp(-np.abs(A(t)) / 3)
    return g1, g2, g3


def _eval(y, ts):
    return np.asarray(y(np.asarray(ts, dtype=float)), dtype=float)


TS = np.array([-3.3, -2.1, -0.9, -0.2, 0.4, 1.3, 2.2, 3.6])
TOL = 1e-6


def is_linear(system):
    x1, x2, _ = _inputs()
    a, b = 2.3, -1.7
    comb = lambda t: a * x1(t) + b * x2(t)
    return bool(np.max(np.abs(_eval(system(comb), TS) - a * _eval(system(x1), TS) - b * _eval(system(x2), TS))) < TOL)


def is_time_invariant(system):
    x1, _, x3 = _inputs()
    ok = True
    for x in (x1, x3):
        for t0 in (0.7, -1.3):
            shifted = lambda t, x=x, t0=t0: x(np.asarray(t, dtype=float) - t0)
            ok &= bool(np.max(np.abs(_eval(system(shifted), TS) - _eval(system(x), TS - t0))) < TOL)
    return ok


def is_causal(system):
    """Perturb the input only AFTER t_ref and watch whether any output at t <= t_ref changes."""
    x1, _, _ = _inputs()
    for t_ref in (-2.0, -0.5, 1.0, 3.0):
        bump = lambda t, t_ref=t_ref: np.where(np.asarray(t, dtype=float) > t_ref, np.exp(-(np.asarray(t, dtype=float) - t_ref)) * (np.asarray(t, dtype=float) - t_ref), 0.0)
        x2 = lambda t, bump=bump: x1(t) + bump(t)
        ts = t_ref - np.array([0.05, 0.3, 0.9, 1.7, 3.1, 5.3])
        if np.max(np.abs(_eval(system(x1), ts) - _eval(system(x2), ts))) > TOL:
            return False
    return True


def is_memoryless(system):
    """Two inputs that agree at t0 and differ elsewhere: a memoryless system gives equal outputs at t0."""
    x1, _, _ = _inputs()
    for t0 in (-1.9, -0.6, 0.8, 2.4):
        x2 = lambda t, t0=t0: x1(t) + (np.asarray(t, dtype=float) - t0) * np.exp(-(np.asarray(t, dtype=float) - t0) ** 2)
        if abs(_eval(system(x1), [t0])[0] - _eval(system(x2), [t0])[0]) > TOL:
            return False
    return True


def growth(system, T1=20.0, T2=200.0):
    """Largest |y| over [0, T] for a few BOUNDED inputs (|x| <= 1).  A ratio well above 1 between the long and the short window means unbounded."""
    # bounded inputs that start at t = 0, so an integrator's start-up offset does not hide its growth
    ins = [lambda t: u(t) * np.ones_like(np.asarray(t, dtype=float)), lambda t: u(t) * np.sin(np.asarray(t, dtype=float) ** 2),
           lambda t: u(t) * np.sign(np.sin(np.asarray(t, dtype=float)))]
    worst = 0.0
    for x in ins:
        y = system(x)
        s1 = np.max(np.abs(_eval(y, np.linspace(0, T1, 2001))))
        s2 = np.max(np.abs(_eval(y, np.linspace(0, T2, 20001))))
        worst = max(worst, s2 / max(s1, 1e-12))
    return worst


def is_bibo_stable(system):
    return growth(system) < 3.0


def properties(system):
    return dict(linear=is_linear(system), ti=is_time_invariant(system), causal=is_causal(system), memoryless=is_memoryless(system), stable=is_bibo_stable(system))


def _cumulative(x, lo=-400.0, hi=420.0, dt=1e-3):
    grid = np.arange(lo, hi + dt, dt)
    v = np.asarray(x(grid), dtype=float)
    C = np.concatenate([[0.0], np.cumsum((v[1:] + v[:-1]) / 2 * dt)])
    return lambda t: np.interp(np.asarray(t, dtype=float), grid, C)


def _accumulator(x):
    C = _cumulative(x)
    return lambda t: C(t)


def _window(x):
    C = _cumulative(x)
    return lambda t: C(t) - C(np.asarray(t, dtype=float) - 1.0)


A_ = lambda t: np.asarray(t, dtype=float)
H = 1e-6
CT_SYSTEMS = {
    'x(t - 2)':            lambda x: (lambda t: x(A_(t) - 2)),
    'x(t + 2)':            lambda x: (lambda t: x(A_(t) + 2)),
    'x(-t)':               lambda x: (lambda t: x(-A_(t))),
    'x(2t)':               lambda x: (lambda t: x(2 * A_(t))),
    'x(t/2)':              lambda x: (lambda t: x(A_(t) / 2)),
    'x(t^2)':              lambda x: (lambda t: x(A_(t) ** 2)),
    'x(e^t)':              lambda x: (lambda t: x(np.exp(A_(t)))),
    't x(t)':              lambda x: (lambda t: A_(t) * x(t)),
    'x(t)^2':              lambda x: (lambda t: x(t) ** 2),
    'x(t) + 1':            lambda x: (lambda t: x(t) + 1),
    '|x(t)|':              lambda x: (lambda t: np.abs(x(t))),
    'e^x(t)':              lambda x: (lambda t: np.exp(x(t))),
    'x(t) cos(2 pi t)':    lambda x: (lambda t: x(t) * np.cos(2 * np.pi * A_(t))),
    'dx/dt':               lambda x: (lambda t: (x(A_(t)) - x(A_(t) - H)) / H),
    'int_{-inf}^t x':      _accumulator,
    'int_{t-1}^t x':       _window,
}


# ---------------------------------------------------------------------------------------------- discrete-time property testers
def _dt_inputs():
    A = lambda n: np.asarray(n, dtype=float)
    g1 = lambda n: 0.9 ** np.abs(A(n)) * np.cos(0.7 * A(n))
    g2 = lambda n: (A(n) + 2) * 0.8 ** np.abs(A(n)) * np.sin(0.4 * A(n)) + 0.2 * 0.7 ** np.abs(A(n))
    g3 = lambda n: np.cos(0.5 * A(n)) * 0.85 ** np.abs(A(n))
    return g1, g2, g3


NS = np.array([-7, -5, -3, -2, -1, 0, 1, 2, 3, 5, 8])


def dt_is_linear(system):
    x1, x2, _ = _dt_inputs()
    a, b = 2.3, -1.7
    comb = lambda n: a * x1(n) + b * x2(n)
    return bool(np.max(np.abs(system(comb)(NS) - a * system(x1)(NS) - b * system(x2)(NS))) < TOL)


def dt_is_time_invariant(system):
    x1, _, x3 = _dt_inputs()
    ok = True
    for x in (x1, x3):
        for n0 in (2, -3):
            shifted = lambda n, x=x, n0=n0: x(np.asarray(n) - n0)
            ok &= bool(np.max(np.abs(system(shifted)(NS) - system(x)(NS - n0))) < TOL)
    return ok


def dt_is_causal(system):
    x1, _, _ = _dt_inputs()
    for n_ref in (-4, -1, 2, 5):
        bump = lambda n, n_ref=n_ref: np.where(np.asarray(n) > n_ref, 0.6 ** np.maximum(np.asarray(n, dtype=float) - n_ref, 0.0), 0.0)
        x2 = lambda n, bump=bump: x1(n) + bump(n)
        ns = np.arange(n_ref - 8, n_ref + 1)
        if np.max(np.abs(system(x1)(ns) - system(x2)(ns))) > TOL:
            return False
    return True


def dt_is_memoryless(system):
    x1, _, _ = _dt_inputs()
    for n0 in (-4, -1, 2, 5):
        x2 = lambda n, n0=n0: x1(n) + np.where(np.asarray(n) != n0, 0.5 ** np.abs(np.asarray(n, dtype=float) - n0), 0.0)
        if abs(system(x1)(np.array([n0]))[0] - system(x2)(np.array([n0]))[0]) > TOL:
            return False
    return True


def dt_growth(system, N1=200, N2=2000):
    step = lambda n: np.where(np.asarray(n) >= 0, 1.0, 0.0)
    ins = [lambda n: step(n), lambda n: step(n) * (-1.0) ** np.asarray(n, dtype=float), lambda n: step(n) * np.sign(np.sin(0.01 * np.asarray(n, dtype=float) ** 2 + 0.3))]
    worst = 0.0
    for x in ins:
        y = system(x)
        s1 = np.max(np.abs(y(np.arange(0, N1))))
        s2 = np.max(np.abs(y(np.arange(0, N2))))
        worst = max(worst, s2 / max(s1, 1e-12))
    return worst


def dt_properties(system):
    return dict(linear=dt_is_linear(system), ti=dt_is_time_invariant(system), causal=dt_is_causal(system), memoryless=dt_is_memoryless(system), stable=dt_growth(system) < 3.0)


def _dt_cumsum(x, lo=-3000, hi=3000):
    grid = np.arange(lo, hi + 1)
    C = np.cumsum(np.asarray(x(grid), dtype=float))
    return lambda n: C[np.asarray(n, dtype=int) - lo]


def _dt_runmax_abs(x, lo=-3000, hi=3000):
    grid = np.arange(lo, hi + 1)
    M = np.maximum.accumulate(np.abs(np.asarray(x(grid), dtype=float)))
    return lambda n: M[np.asarray(n, dtype=int) - lo]


def _expand(x):
    return lambda n: np.where(np.asarray(n) % 2 == 0, x(np.asarray(n) // 2), 0.0)


Ai = lambda n: np.asarray(n)
DT_SYSTEMS = {
    'x[n - 2]':             lambda x: (lambda n: x(Ai(n) - 2)),
    'x[n + 1]':             lambda x: (lambda n: x(Ai(n) + 1)),
    'x[-n]':                lambda x: (lambda n: x(-Ai(n))),
    'x[2n]':                lambda x: (lambda n: x(2 * Ai(n))),
    'x[n/2] (zero stuffed)': _expand,
    'n x[n]':               lambda x: (lambda n: Ai(n) * x(n)),
    'x[n] - x[n - 1]':      lambda x: (lambda n: x(n) - x(Ai(n) - 1)),
    '(x[n+1] + x[n-1])/2':  lambda x: (lambda n: (x(Ai(n) + 1) + x(Ai(n) - 1)) / 2),
    'sum_{k<=n} x[k]':      _dt_cumsum,
    'max_{k<=n} |x[k]|':    _dt_runmax_abs,
    'x[n]^2':               lambda x: (lambda n: x(n) ** 2),
    'x[n] x[n - 1]':        lambda x: (lambda n: x(n) * x(Ai(n) - 1)),
}
