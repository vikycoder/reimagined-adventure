"""Tiny Modified Nodal Analysis solver used to verify the numbers in the Networks notes (DC and AC phasors).

Node 0 is ground. Elements:
  ('R', a, b, ohms)
  ('Z', a, b, z)                    complex impedance (phasor / AC analysis); source values may be complex too
  ('V', p, n, volts, name)          V(p) - V(n) = volts ; current var name flows p->n inside source
  ('I', a, b, amps)                 amps flow from node a, through the source, into node b
  ('VCCS', a, b, cp, cn, g)         g*(V(cp)-V(cn)) flows from a, through source, into b
  ('VCVS', p, n, cp, cn, k, name)   V(p)-V(n) = k*(V(cp)-V(cn))
  ('CCVS', p, n, ctrl, r, name)     V(p)-V(n) = r * I(ctrl)   (ctrl = name of a V source)
  ('CCCS', a, b, ctrl, beta)        beta*I(ctrl) flows from a, through source, into b
"""
import numpy as np


def solve(elements):
    nodes = sorted({x for e in elements for x in e[1:3]} - {0})
    for e in elements:
        if e[0] in ('VCCS', 'VCVS'):
            nodes = sorted(set(nodes) | ({e[3], e[4]} - {0}))
    idx = {n: i for i, n in enumerate(nodes)}
    vsrc = [e[-1] for e in elements if e[0] in ('V', 'VCVS', 'CCVS')]
    N = len(nodes) + len(vsrc)
    vidx = {name: len(nodes) + i for i, name in enumerate(vsrc)}
    cplx = any(e[0] == 'Z' or any(isinstance(x, complex) for x in e[3:]) for e in elements)
    dt = complex if cplx else float
    A = np.zeros((N, N), dtype=dt); z = np.zeros(N, dtype=dt)

    def add(r, c, v):
        if r is not None and c is not None:
            A[r, c] += v

    ni = lambda n: idx.get(n)  # None for ground
    for e in elements:
        t = e[0]
        if t in ('R', 'Z'):
            _, a, b, R = e; g = 1 / R
            add(ni(a), ni(a), g); add(ni(b), ni(b), g); add(ni(a), ni(b), -g); add(ni(b), ni(a), -g)
        elif t == 'I':
            _, a, b, I = e
            if ni(a) is not None: z[ni(a)] -= I
            if ni(b) is not None: z[ni(b)] += I
        elif t == 'VCCS':
            # current g*(Vcp-Vcn) leaves a, enters b  -> KCL rows (sum of currents leaving = 0)
            _, a, b, cp, cn, g = e
            add(ni(a), ni(cp), g); add(ni(a), ni(cn), -g)
            add(ni(b), ni(cp), -g); add(ni(b), ni(cn), g)
        elif t in ('V', 'VCVS', 'CCVS'):
            p, n = e[1], e[2]; k = vidx[e[-1]]
            add(ni(p), k, 1); add(ni(n), k, -1)
            add(k, ni(p), 1); add(k, ni(n), -1)
            if t == 'V':
                z[k] = e[3]
            elif t == 'VCVS':
                _, _, _, cp, cn, gain, _ = e
                add(k, ni(cp), -gain); add(k, ni(cn), gain)
            else:
                _, _, _, ctrl, r, _ = e
                A[k, vidx[ctrl]] -= r
        elif t == 'CCCS':
            _, a, b, ctrl, beta = e
            add(ni(a), vidx[ctrl], beta); add(ni(b), vidx[ctrl], -beta)
    x = np.linalg.solve(A, z)
    V = {n: x[idx[n]] for n in nodes}; V[0] = 0.0
    I = {name: x[vidx[name]] for name in vsrc}
    return V, I


if __name__ == '__main__':
    # sanity: 10 V across 2 ohm + 3 ohm divider
    V, I = solve([('V', 1, 0, 10, 'vs'), ('R', 1, 2, 2), ('R', 2, 0, 3)])
    assert abs(V[2] - 6) < 1e-9 and abs(I['vs'] + 2) < 1e-9, (V, I)
    # VCCS sanity: 1 A into node 1 with 1 ohm, VCCS 0.5*V1 drawn from node1 to ground
    V, _ = solve([('I', 0, 1, 1), ('R', 1, 0, 1), ('VCCS', 1, 0, 1, 0, 0.5)])
    assert abs(V[1] - 1 / 1.5) < 1e-9, V
    # AC sanity: 1 V (phasor) -> R=1k -> node 2 -> C=1uF to ground at w=1000 rad/s  =>  V2 = 1/(1 + jwRC) = 1/(1+1j)
    w, R, C = 1000.0, 1e3, 1e-6
    V, _ = solve([('V', 1, 0, 1 + 0j, 'vs'), ('R', 1, 2, R), ('Z', 2, 0, 1 / (1j * w * C))])
    assert abs(V[2] - 1 / (1 + 1j)) < 1e-12, V
    print('solver ok')
