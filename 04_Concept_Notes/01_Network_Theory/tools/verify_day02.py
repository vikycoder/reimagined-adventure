"""Re-checks every number quoted in Day02_Network_Theorems.md and Day02_Conceptual_Questions.md.

Run:  python3 verify_day02.py          (needs numpy; uses mna.py in this folder)
Past-year answers are checked against the official keys quoted in the comments.
"""
import numpy as np

from mna import solve

k, m = 1e3, 1e-3


def check(name, got, want, tol=1e-6):
    assert abs(got - want) < tol, f'{name}: got {got}, expected {want}'
    print(f'ok  {name:<48} {got:.4f}')


def zero_sources(elems):
    """Turn OFF independent sources only (V -> short, I -> open). Dependent sources stay."""
    out = []
    for e in elems:
        if e[0] == 'V':
            out.append(('V', e[1], e[2], 0.0, e[4]))
        elif e[0] == 'I':
            out.append(('I', e[1], e[2], 0.0))
        else:
            out.append(e)
    return out


def thevenin(elems, a):
    """(V_oc, I_sc, R_th by test source) seen at node a with respect to ground."""
    V, _ = solve(elems)
    voc = V[a]
    _, I = solve(elems + [('V', a, 0, 0.0, 'short')])
    isc = I['short']                                  # current leaving terminal a into the short
    V2, _ = solve(zero_sources(elems) + [('I', 0, a, 1.0)])   # 1 A test current into a
    return voc, isc, V2[a]


# ---- sanity of the helper: 10 V behind 5 ohm -> Voc 10, Isc 2, Rth 5
voc, isc, rth = thevenin([('V', 1, 0, 10.0, 'v'), ('R', 1, 2, 5.0)], 2)
check('helper: Voc', voc, 10); check('helper: Isc', isc, 2); check('helper: Rth', rth, 5)

# ================= Section 2: superposition =================
# Ex 1: 12 V via 2 ohm, 6 ohm to ground, 3 A injected at X
full = [('V', 1, 0, 12.0, 'v'), ('R', 1, 2, 2.0), ('R', 2, 0, 6.0), ('I', 0, 2, 3.0)]
VX = solve(full)[0][2]
VX1 = solve([('V', 1, 0, 12.0, 'v'), ('R', 1, 2, 2.0), ('R', 2, 0, 6.0)])[0][2]            # current source opened
VX2 = solve([('V', 1, 0, 0.0, 'v'), ('R', 1, 2, 2.0), ('R', 2, 0, 6.0), ('I', 0, 2, 3.0)])[0][2]  # voltage source shorted
check('Ex1 V_X total', VX, 13.5); check('Ex1 V_X from 12 V alone', VX1, 9); check('Ex1 V_X from 3 A alone', VX2, 4.5)
check('Ex1 P total in 6 ohm', VX ** 2 / 6, 30.375)
check('Ex1 P1 + P2 (wrong)', VX1 ** 2 / 6 + VX2 ** 2 / 6, 16.875)
check('Ex1 cross term', 2 * VX1 * VX2 / 6, 13.5)

# Ex 2: CCVS (3 i, i = current in the 2 ohm) kept in every step
def ex2(vs, isrc, kill_dep=False):
    r = 0.0 if kill_dep else 3.0
    return solve([('V', 1, 0, vs, 'vs'), ('R', 1, 2, 2.0), ('V', 2, 3, 0.0, 'sense'), ('CCVS', 4, 3, 'sense', r, 'dep'),
                  ('R', 4, 0, 4.0), ('I', 0, 4, isrc)])[0][4]

check('Ex2 V_X total', ex2(10.0, 2.0), 32 / 3)
check('Ex2 V_X from 10 V alone (CCVS kept)', ex2(10.0, 0.0), 40 / 3)
check('Ex2 V_X from 2 A alone (CCVS kept)', ex2(0.0, 2.0), -8 / 3)
wrong = ex2(10.0, 0.0, True) + ex2(0.0, 2.0, True)
check('Ex2 wrong total if CCVS is shorted', wrong, 28 / 3)

# Ex 3: V_th, R_th, I_N and three loads
ex3 = [('V', 1, 0, 24.0, 'vs'), ('R', 1, 2, 6.0), ('R', 2, 0, 12.0), ('I', 0, 2, 2.0)]
voc, isc, rth = thevenin(ex3, 2)
check('Ex3 V_th', voc, 24); check('Ex3 R_th (test source)', rth, 4); check('Ex3 I_N = I_sc', isc, 6)
check('Ex3 V_oc / I_sc', voc / isc, 4)
for RL, iL in ((1.0, 4.8), (4.0, 3.0), (12.0, 1.5)):
    V = solve(ex3 + [('R', 2, 0, RL)])[0][2]
    check(f'Ex3 load current, R_L={RL:g}', V / RL, iL)
    check(f'   (Thevenin formula, R_L={RL:g})', voc / (rth + RL), iL)
check('Ex3 P at R_L=4 (max power)', 24 ** 2 / (4 * 4), 36)

# Ex 4: 6 ohm with a CCCS  beta*i  in parallel (i = current in the 6 ohm)
for beta, want in ((2.0, 2.0), (0.0, 6.0), (-0.5, 12.0), (-2.0, -6.0)):
    el = [('V', 1, 2, 0.0, 'sense'), ('R', 2, 0, 6.0), ('CCCS', 1, 0, 'sense', beta), ('I', 0, 1, 1.0)]
    check(f'Ex4 R_th for beta={beta:g}  (= 6/(1+beta))', solve(el)[0][1], want)
try:
    solve([('V', 1, 2, 0.0, 'sense'), ('R', 2, 0, 6.0), ('CCCS', 1, 0, 'sense', -1.0), ('I', 0, 1, 1.0)])
    raise AssertionError('beta=-1 should be singular (open circuit)')
except np.linalg.LinAlgError:
    print('ok  Ex4 beta=-1 is singular (R_th = infinity)')

# Ex 5: unit-output (proportionality) method on a ladder
lad = lambda vs: [('V', 1, 0, vs, 'vs'), ('R', 1, 2, 1.0), ('R', 2, 0, 3.0), ('R', 2, 3, 1.0), ('R', 3, 0, 4.0),
                  ('R', 3, 4, 1.0), ('R', 4, 0, 3.0)]
check('Ex5 I_L for 10 V', solve(lad(10.0))[0][4] / 3, 1)
check('Ex5 I_L for 30 V', solve(lad(30.0))[0][4] / 3, 3)

# ================= Section 5: maximum power table =================
for x, pr, eta in ((0.25, 0.64, 0.2), (0.5, 8 / 9, 1 / 3), (1.0, 1.0, 0.5), (2.0, 8 / 9, 2 / 3), (4.0, 0.64, 0.8)):
    check(f'P/Pmax at R_L/R_th={x:g}', 4 * x / (1 + x) ** 2, pr)
    check(f'efficiency at R_L/R_th={x:g}', x / (1 + x), eta)

# ================= Past-year questions =================
# 2019 Q4 (key B = 1 A): T network 1 ohm / R / 2 ohm
def q19(R, drive_port1):
    base = [('R', 1, 2, 1.0), ('R', 2, 0, R), ('R', 2, 3, 2.0)]
    if drive_port1:
        return solve(base + [('V', 1, 0, 5.0, 'src'), ('V', 3, 0, 0.0, 'sh')])[1]['sh']
    return solve(base + [('V', 3, 0, 5.0, 'src'), ('V', 1, 0, 0.0, 'sh')])[1]['sh']

check('2019 Q4 (a): short-circuit current at port 2, R=1', q19(1.0, True), 1)
check('2019 Q4 (b): short-circuit current at port 1, R=1  [key 1 A]', q19(1.0, False), 1)
for R in (0.5, 3.0, 10.0):
    check(f'2019 Q4 reciprocity holds for R={R:g}', q19(R, True), q19(R, False))

# 2020 Q9 (key C = 3.6 V)
q20 = [('I', 0, 1, 1.0), ('R', 1, 0, 1.0), ('V', 2, 1, 2.0, 'v2'), ('R', 2, 3, 2.0), ('I', 0, 3, 2.0), ('R', 3, 0, 2.0), ('R', 3, 4, 4.0)]
V = solve(q20)[0]
check('2020 Q9 V_TH  [key 3.6 V]', V[4], 3.6)
V2 = solve(zero_sources(q20) + [('I', 0, 4, 1.0)])[0]
check('2020 Q9 R_th', V2[4], 5.2)
check('2020 Q9 I_N = V_th/R_th', V[4] / V2[4], 0.6923, 1e-4)
check('2020 Q9 P_max = V_th^2/(4 R_th)', V[4] ** 2 / (4 * V2[4]), 0.6231, 1e-4)
# source-transformation shortcut used in the note: 3 V behind 3 ohm -> 1 A || 3 ohm, plus 2 A, shunt 2 ohm
check('2020 Q9 via transformations: (1+2) A x (3||2)', (1 + 2) * (3 * 2 / 5), 3.6)

# 2022 Q54 (key 3.9 to 4.1 mA): V2 = 5 - 250*(-I2) ; load: 1 kohm in series with 10 V (+ toward A)
vth, rth = 5.0, (5.0 - 4.0) / 4e-3
check('2022 Q54 R_th from the measured line', rth, 250)
A = np.array([[1.0, -250.0], [1.0, 1000.0]])          # V2 - 250*I2 = 5 ;  V2 + 1000*I2 = 10
V2, I2 = np.linalg.solve(A, [5.0, 10.0])
check('2022 Q54 I2 (mA)  [key 3.9-4.1]', I2 / m, 4.0)
check('2022 Q54 V2', V2, 6.0)

# 2024 Q62 (key 2.5 ohm): V_x = V(N) - V(M) across the 3 ohm (+ at the right); dependent source V_x in branch 2
def q24(RL=None, zero=False):
    el = [('V', 1, 0, 0.0 if zero else 50.0, 'vs'), ('R', 1, 2, 2.0), ('R', 2, 3, 3.0),
          ('VCVS', 4, 1, 3, 2, 1.0, 'dep'), ('R', 4, 3, 2.0)]
    if RL is not None:
        el.append(('R', 3, 0, RL))
    return el
voc, isc, rth = thevenin(q24(), 3)
check('2024 Q62 V_oc', voc, 50); check('2024 Q62 I_sc', isc, 20); check('2024 Q62 R_th (test source)  [key 2.5]', rth, 2.5)
check('2024 Q62 V_oc / I_sc', voc / isc, 2.5)
RLs = np.linspace(0.5, 6, 1101)
P = [solve(q24(r))[0][3] ** 2 / r for r in RLs]
check('2024 Q62 sweep: argmax R_L', RLs[int(np.argmax(P))], 2.5, 6e-3)
check('2024 Q62 P_max = V^2/(4R)', max(P), 250, 0.01)
# naive (wrong) R_th if the dependent source is set to zero: 2+3 in parallel with 2
check('2024 Q62 wrong R_th (dependent source dropped)', 5 * 2 / 7, 1.4286, 1e-4)

# 2020 Q15 (key 48) and 2023 Q33 (key 80): Thevenin resistance at port 2 of a two-port driven through 10 ohm
check('2020 Q15 Z_L = z22 - z12 z21/(z11+10)  [key 48]', 120 - 60 * 60 / (40 + 10), 48)
y11, y12, y21, y22 = 2e-2, -1e-2, -1e-2, (4 / 3) * 1e-2
check('2023 Q33 Z_L = 1/(y22 - y12 y21/(y11+1/10))  [key 80]', 1 / (y22 - y12 * y21 / (y11 + 0.1)), 80)

# ================= Practice problems =================
p1 = [('V', 1, 0, 24.0, 'v1'), ('R', 1, 3, 4.0), ('V', 2, 0, 12.0, 'v2'), ('R', 2, 3, 6.0), ('R', 3, 0, 12.0), ('I', 0, 3, 6.0)]
check('P1 V_X', solve(p1)[0][3], 28)
check('P1 from 24 V alone', solve([('V', 1, 0, 24.0, 'v1'), ('R', 1, 3, 4.0), ('V', 2, 0, 0.0, 'v2'), ('R', 2, 3, 6.0), ('R', 3, 0, 12.0)])[0][3], 12)
check('P1 from 12 V alone', solve([('V', 1, 0, 0.0, 'v1'), ('R', 1, 3, 4.0), ('V', 2, 0, 12.0, 'v2'), ('R', 2, 3, 6.0), ('R', 3, 0, 12.0)])[0][3], 4)
check('P1 from 6 A alone', solve([('V', 1, 0, 0.0, 'v1'), ('R', 1, 3, 4.0), ('V', 2, 0, 0.0, 'v2'), ('R', 2, 3, 6.0), ('R', 3, 0, 12.0), ('I', 0, 3, 6.0)])[0][3], 12)

p2 = [('V', 1, 0, 12.0, 'vs'), ('R', 1, 5, 2.0), ('V', 5, 2, 0.0, 'sense'), ('R', 2, 0, 4.0), ('CCCS', 2, 0, 'sense', 0.5)]
voc, isc, rth = thevenin(p2, 2)
check('P2 V_th', voc, 6); check('P2 R_th', rth, 2); check('P2 I_N', isc, 3)
check('P2 wrong R_th (dependent source ignored): 2||4', 2 * 4 / 6, 1.3333, 1e-4)

check('P3a P_max = V^2/(4R)', 20 ** 2 / (4 * 5), 20)
check('P3c R_L=20 ohm', 20 ** 2 * 20 / (5 + 20) ** 2, 12.8)
check('P3b fixed R_L=5, R_th -> 0', 20 ** 2 * 5 / (0 + 5) ** 2, 80)
check('P4a reciprocity: 4 V at port 2 -> I at port 1 (A)', 4 * (0.5 / 10), 0.2)
check('P4b reciprocity: 2 A at port 2 -> V1 (V)', 2 * (3 / 1), 6)
V = solve([('R', 1, 0, 6.0), ('VCCS', 0, 1, 1, 0, 0.25), ('I', 0, 1, 1.0)])[0][1]
check('P5 R_th (6 ohm || VCCS 0.25 v) = -12', V, -12)

# ================= Conceptual questions =================
check('Q4 power with both sources, 2 ohm, 3 A - 1 A', (3 - 1) ** 2 * 2, 8)
check('Q4 sum of the individual powers (wrong)', 3 ** 2 * 2 + 1 ** 2 * 2, 20)
check('Q5 output for (5, 15)', 5 / 10 * 4 + 15 / 5 * (-3), -7)
check('Q7 current in 6 ohm: Voc=12 V, Isc=3 A', 12 / (12 / 3 + 6), 1.2)
V = solve([('R', 1, 0, 4.0), ('VCCS', 0, 1, 1, 0, 0.5), ('I', 0, 1, 1.0)])[0][1]
check('Q9 R_th (4 ohm || VCCS 0.5 v injecting) = -4', V, -4)
r = np.roots([1e-3 * k, 1.0, -6.0])                      # v + 1000 * 1e-3 * v^2 = 6
check('Q10 nonlinear load voltage', max(r.real), 2)
check('Q10 its current (mA)', 1e-3 * 2 ** 2 / m, 4)
bridge = [('V', 1, 0, 18.0, 'vs'), ('R', 1, 2, 6.0), ('R', 2, 0, 12.0), ('R', 1, 3, 3.0), ('R', 3, 0, 9.0)]
Vb = solve(bridge)[0]
check('Q11 V_oc across detector terminals (V_c - V_d)', Vb[2] - Vb[3], -1.5)
Vt = solve(zero_sources(bridge) + [('I', 3, 2, 1.0)])[0]
check('Q11 R_th seen by the detector', Vt[2] - Vt[3], 6.25)
Vd = solve(bridge + [('R', 2, 3, 3.75)])[0]
check('Q11 |detector current| with 3.75 ohm', abs((Vd[2] - Vd[3]) / 3.75), 0.15)
Vs2 = solve([('V', 1, 0, 36.0, 'vs')] + bridge[1:])[0]
check('Q11 R_th unchanged for another supply (36 V)', (lambda V: V[2] - V[3])(solve(zero_sources([('V', 1, 0, 36.0, 'vs')] + bridge[1:]) + [('I', 3, 2, 1.0)])[0]), 6.25)
check('Q13 fixed R_L=10, V_th=20, R_th=2', 20 ** 2 * 10 / (2 + 10) ** 2, 27.78, 5e-3)
check('Q13 same at R_th=10 (matched, smaller)', 20 ** 2 * 10 / (10 + 10) ** 2, 10)
Rv = np.linspace(0.01, 40, 40000)
PRv = (30 / (4 + 6 + Rv)) ** 2 * Rv
check('Q15 argmax over R_v', Rv[int(np.argmax(PRv))], 10, 2e-3)
Pw = (30 / (4 + 6 + Rv)) ** 2 * (6 + Rv)
check('Q15 whole-load power is largest at R_v -> 0', Rv[int(np.argmax(Pw))], 0.01, 1e-9)
check('Q15 whole load: P(Rv=0)', (30 / 10) ** 2 * 6, 54)
RL = np.linspace(0.01, 20, 200000)
Zth = 3 + 4j
PRL = RL / ((3 + RL) ** 2 + 4 ** 2)
check('Q16 R_L maximising P (X_L = 0), Z_th = 3+j4', RL[int(np.argmax(PRL))], 5, 1e-3)
check('Q16 |Z_th|', abs(Zth), 5)
check('Q18 5 A', 25 * (2 / 10), 5)
check('Q19 15 V', 5 * (6 / 2), 15)
check('Q20 R_th from 8 V open / 6 V with 6 ohm', 6 * (8 - 6) / 6, 2)
check('Q20 P_max', 8 ** 2 / (4 * 2), 8)
check('Q12 load fraction at matching', 1 / (1 + 1), 0.5)
check('Q12 (alt) power in R_th at matching, V=24 R_th=8', (24 / 16) ** 2 * 8, 18)

print('\nall Day 2 checks passed')
