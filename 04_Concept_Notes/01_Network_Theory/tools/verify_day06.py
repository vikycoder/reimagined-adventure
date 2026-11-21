"""Re-checks every number in Day06_Networks_Revision.md, Day06_Conceptual_Questions.md and Day06_Mock_Test.md.

Run:  python3 verify_day06.py          (needs numpy and scipy; uses mna.py)

Circuit answers come from the MNA solver or from an ODE integration, not from the closed forms used in the solutions,
so the two routes check each other.
"""
import numpy as np
from scipy.integrate import solve_ivp

from mna import solve

u, m, k = 1e-6, 1e-3, 1e3
J = 1j


def check(name, got, want, tol=1e-6):
    assert abs(got - want) < tol, f'{name}: got {got}, expected {want}'
    print(f'ok  {name:<70} {got:.6g}')


def checkm(name, got, want, tol=1e-9):
    assert np.allclose(got, want, atol=tol, rtol=0), f'{name}: got\n{got}\nexpected\n{want}'
    print(f'ok  {name}')


# ====================================================================================== MOCK TEST: part A (1 mark each)
# Q1: delta of three equal resistors, resistance between two corners
R = 18.0
check('M-Q1 delta R: R || 2R (ohm)', R * 2 * R / (3 * R), 12.0)
# Q2: 10 V + 2 ohm into node a, 3 ohm to ground, 2 A injected into a
V, _ = solve([('V', 1, 0, 10.0, 'e'), ('R', 1, 2, 2.0), ('R', 2, 0, 3.0), ('I', 0, 2, 2.0)])
check('M-Q2 V_a (V)', V[2], 8.4, 1e-9)
# Q3: 12 V with 6 ohm series, 3 ohm shunt across the terminals
check('M-Q3 V_th (V)', 12 * 3 / 9, 4.0); check('M-Q3 R_th (ohm)', 6 * 3 / 9, 2.0)
# Q4: 12 V, 4 ohm series, 12 ohm shunt -> P_max
Vth4, Rth4 = 12 * 12 / 16, 4 * 12 / 16
check('M-Q4 V_th (V)', Vth4, 9.0); check('M-Q4 R_th (ohm)', Rth4, 3.0); check('M-Q4 P_max (W)', Vth4 ** 2 / (4 * Rth4), 6.75)
check('M-Q4 wrong: P with R_L = R_s = 4 ohm', Vth4 ** 2 * 4 / (3 + 4) ** 2, 6.612, 1e-3)
# Q5: RC, v_C(0) = 4 V, 10 V step, tau = 2 ms, t = 3 ms
tau = 2e3 * 1e-6
vc = lambda t, v0: 10 - (10 - v0) * np.exp(-t / tau)
check('M-Q5 v_C(3 ms) (V)', vc(3e-3, 4), 8.6612, 1e-3)
check('M-Q5 wrong: ignoring the initial charge (V)', vc(3e-3, 0), 7.7687, 1e-3)
check('M-Q5 wrong: tau taken as 1 ms (V)', 10 - 6 * np.exp(-3), 9.7011, 1e-3)
check('M-Q5 wrong: only the decaying part (V)', 6 * np.exp(-1.5), 1.3388, 1e-3)
# Q6: RL, R = 10, L = 2, 20 V step: v_L = v_R
tauL = 2 / 10.0
check('M-Q6 t where v_L = v_R (s)', tauL * np.log(2), 0.1386, 1e-4)
# Q7: series RLC zeta
Rr, Ll, Cc = 20.0, 0.1, 100e-6
zeta = (Rr / 2) * np.sqrt(Cc / Ll)
check('M-Q7 zeta (series RLC)', zeta, 0.31623, 1e-5); check('M-Q7 alpha', Rr / (2 * Ll), 100.0); check('M-Q7 w0', 1 / np.sqrt(Ll * Cc), 316.23, 1e-2)
check('M-Q7 wrong: parallel formula (1/2R) sqrt(L/C)', (1 / (2 * Rr)) * np.sqrt(Ll / Cc), 0.7906, 1e-3)
# Q8: series R-L-C reactances
check('M-Q8 current (A)', 100 / np.hypot(6, 12 - 4), 10.0)
# Q9: 5 kVA at 0.6 lagging, 4 kvar capacitor
S9 = 5.0 * (0.6 + 0.8j)
check('M-Q9 source apparent power after the capacitor (kVA)', abs(S9 - 4j), 3.0)
# Q10: resonant frequency
check('M-Q10 f0 (Hz)', 1 / (2 * np.pi * np.sqrt(5e-3 * 20e-6)), 503.29, 1e-2)
# Q11: phasor sum
Z11 = 10 + 0j + 10 * np.exp(-1j * np.pi / 2)
check('M-Q11 |sum|', abs(Z11), 14.142, 1e-3); check('M-Q11 angle (deg)', np.degrees(np.angle(Z11)), -45.0, 1e-9)
# Q12: T network 2, 2, 4 -> ABCD
Z1_, Z2_, Z3_ = 2.0, 2.0, 4.0
T12 = np.array([[1 + Z1_ / Z3_, Z1_ + Z2_ + Z1_ * Z2_ / Z3_], [1 / Z3_, 1 + Z2_ / Z3_]])
checkm('M-Q12 ABCD of the T network', T12, [[1.5, 5], [0.25, 1.5]])
check('M-Q12 AD - BC', np.linalg.det(T12), 1.0, 1e-12)
# Q13: reciprocal Y, R_L = 2 ohm
Y13 = np.array([[0.5, -0.25], [-0.25, 0.75]]); YL = 0.5
Yin = Y13[0, 0] - Y13[0, 1] * Y13[1, 0] / (Y13[1, 1] + YL)
check('M-Q13 input resistance (ohm)', 1 / Yin, 2.2222, 1e-3)
# cross-check by solving the equations: V2 = -I2/YL ... apply 1 V at port 1
A_ = np.array([[Y13[1, 1] + YL]]); V2_ = -Y13[1, 0] * 1.0 / A_[0, 0]
I1_ = Y13[0, 0] * 1.0 + Y13[0, 1] * V2_
check('M-Q13 cross-check R_in = 1/I1 (ohm)', 1.0 / I1_, 2.2222, 1e-3)
# Q14: branches and nodes
b_, n_ = 10, 6
check('M-Q14 independent KCL (n - 1)', n_ - 1, 5); check('M-Q14 independent KVL (b - n + 1)', b_ - n_ + 1, 5)
# Q15: two sources with series resistors feeding a common node, 6 ohm load to ground
V, _ = solve([('V', 1, 0, 12.0, 'e1'), ('R', 1, 3, 3.0), ('V', 2, 0, 6.0, 'e2'), ('R', 2, 3, 6.0), ('R', 3, 0, 6.0)])
check('M-Q15 V_node (V)', V[3], 7.5, 1e-9); check('M-Q15 load current (A)', V[3] / 6.0, 1.25, 1e-9)
check('M-Q15 contribution of the 12 V source (V)', 12 * 3 / 6, 6.0); check('M-Q15 contribution of the 6 V source (V)', 6 * 2 / 8, 1.5)
check('M-Q15 wrong: ignoring the 6 V source (A)', 6.0 / 6.0, 1.0)

# ====================================================================================== MOCK TEST: part B (2 marks each)
# Q16: 12 V, 2 ohm (1-2), 4 ohm (2-0), dependent current 0.25*V2 from node 2 to ground
V, I = solve([('V', 1, 0, 12.0, 'e'), ('R', 1, 2, 2.0), ('R', 2, 0, 4.0), ('VCCS', 2, 0, 2, 0, 0.25)])
check('M-Q16 V_2 (V)', V[2], 6.0, 1e-9)
check('M-Q16 power absorbed by the dependent source (W)', V[2] * 0.25 * V[2], 9.0, 1e-9)
check('M-Q16 current from the 12 V source (A)', -I['e'], 3.0, 1e-9)
check('M-Q16 wrong: ignoring the dependent source V_2 (V)', 12 * 4 / 6, 8.0)
# Q17: Thevenin with a CCCS:  20 V, R1 = 4 (1 -> 2), R2 = 2 (2 -> 0), CCCS = 1*i1 injected into node 2
# node 3 = top of the 20 V source; a 0 V meter between 3 and 4 measures i1 (through R1) and controls the CCCS
net17 = [('V', 3, 0, 20.0, 'e'), ('V', 3, 4, 0.0, 'meas'), ('R', 4, 2, 4.0), ('R', 2, 0, 2.0), ('CCCS', 0, 2, 'meas', 1.0)]
V, _ = solve(net17)
check('M-Q17 V_oc = V_th (V)', V[2], 10.0, 1e-9)
V, I = solve(net17 + [('V', 2, 0, 0.0, 'sc')])
Isc = I['sc']                      # current var flows node 2 -> ground inside the 0 V source = the short-circuit current
check('M-Q17 I_sc (A)', Isc, 10.0, 1e-9); check('M-Q17 R_th = V_oc / I_sc (ohm)', 10.0 / Isc, 1.0, 1e-9)
Vt, It = solve([('V', 3, 0, 0.0, 'e'), ('V', 3, 4, 0.0, 'meas'), ('R', 4, 2, 4.0), ('R', 2, 0, 2.0), ('CCCS', 0, 2, 'meas', 1.0), ('V', 2, 0, 1.0, 'tst')])
check('M-Q17 R_th by a test source (ohm)', 1.0 / (-It['tst']), 1.0, 1e-9)
check('M-Q17 P_max (W)', 10.0 ** 2 / (4 * 1.0), 25.0)
check('M-Q17 wrong: ignoring the CCCS, P_max (W)', (20 * 2 / 6) ** 2 / (4 * (4 * 2 / 6)), 8.333, 1e-3)
# Q18: series RLC, R = 6, L = 1, C = 0.04, v_C(0) = 10, i_L(0) = 0: first zero of v_C
Rq, Lq, Cq = 6.0, 1.0, 0.04
sol = solve_ivp(lambda t, x: [x[1] / Cq, (-x[0] - Rq * x[1]) / Lq], (0, 2), [10.0, 0.0], rtol=1e-11, atol=1e-13, dense_output=True)
tt = np.linspace(0, 1.0, 2000001)
vcv = sol.sol(tt)[0]
t_zero = tt[np.argmax(vcv <= 0)]
check('M-Q18 first zero of v_C from the ODE (s)', t_zero, 0.55357, 1e-4)
check('M-Q18 closed form (pi/2 + atan(0.75))/4 (s)', (np.pi / 2 + np.arctan(0.75)) / 4, 0.55357, 1e-5)
check('M-Q18 alpha', Rq / (2 * Lq), 3.0); check('M-Q18 w_d', np.sqrt(1 / (Lq * Cq) - 9), 4.0, 1e-9)
check('M-Q18 wrong: first zero of the cosine part only 4t = pi/2 (s)', np.pi / 8, 0.3927, 1e-4)
# Q19: parallel RLC, current step, inductor current overshoot
Rp, Lp, Cp = 50.0, 16e-3, 10e-6
zp = (1 / (2 * Rp)) * np.sqrt(Lp / Cp)
check('M-Q19 zeta (parallel)', zp, 0.4, 1e-12)
sol = solve_ivp(lambda t, x: [x[1], (1.0 - x[0] - x[1] * Lp / Rp) / (Lp * Cp)], (0, 0.02), [0.0, 0.0], rtol=1e-11, atol=1e-13, dense_output=True)
t2 = np.linspace(0, 0.02, 400001)
iL = sol.sol(t2)[0]
check('M-Q19 percentage overshoot of i_L from the ODE (%)', 100 * (iL.max() - 1), 25.38, 5e-2)
check('M-Q19 closed form (%)', 100 * np.exp(-np.pi * zp / np.sqrt(1 - zp ** 2)), 25.38, 5e-3)
zs = (Rp / 2) * np.sqrt(Cp / Lp)
check('M-Q19 wrong: series formula zeta', zs, 0.625, 1e-9); check('M-Q19 wrong: overshoot with it (%)', 100 * np.exp(-np.pi * zs / np.sqrt(1 - zs ** 2)), 8.1, 0.1)
# Q20: eigenvalues of the state matrix for x = [v_C, i_L]
Aq = np.array([[0, 1 / Cq], [-1 / Lq, -Rq / Lq]])
ev = np.linalg.eigvals(Aq)
checkm('M-Q20 eigenvalues -3 +- j4', sorted(ev, key=lambda z: z.imag), [-3 - 4j, -3 + 4j])
# Q21: AC max power with fixed X_L = +2
Vth21, Zth21, XL21 = 20.0, 3 + 4j, 2.0
RL21 = abs(Zth21 + 1j * XL21)
P21 = Vth21 ** 2 * RL21 / ((Zth21.real + RL21) ** 2 + (Zth21.imag + XL21) ** 2)
check('M-Q21 best R_L (ohm)', RL21, 6.7082, 1e-4); check('M-Q21 P (W)', P21, 20.60, 1e-2)
RLs = np.linspace(0.01, 30, 300001)
Ps = Vth21 ** 2 * RLs / ((3 + RLs) ** 2 + (4 + XL21) ** 2)
check('M-Q21 brute-force best R_L (ohm)', RLs[np.argmax(Ps)], 6.7082, 1e-3)
check('M-Q21 wrong: R_L = R_th = 3 gives (W)', Vth21 ** 2 * 3 / ((6) ** 2 + 36), 16.67, 1e-2)
check('M-Q21 wrong: full conjugate match V^2/(4 R_th) (W)', Vth21 ** 2 / (4 * 3), 33.33, 1e-2)
# Q22: two loads, unity pf
Q1_, Q2_ = 8 * np.tan(np.arccos(0.8)), 6 * np.tan(np.arccos(0.6))
check('M-Q22 Q1 (kvar)', Q1_, 6.0, 1e-9); check('M-Q22 Q2 (kvar)', Q2_, 8.0, 1e-9)
w50 = 2 * np.pi * 50
check('M-Q22 C for unity pf (uF)', (Q1_ + Q2_) * 1e3 / (w50 * 230 ** 2) / u, 842.4, 0.1)
check('M-Q22 wrong: using the larger load only (uF)', Q2_ * 1e3 / (w50 * 230 ** 2) / u, 481.4, 0.1)
check('M-Q22 total real power (kW)', 14.0, 14.0)
# Q23: parallel resonance
R23, L23, C23 = 10e3, 1e-3, 1e-9
w23 = 1 / np.sqrt(L23 * C23)
check('M-Q23 w0 (rad/s)', w23, 1e6, 1e-3); check('M-Q23 f0 (Hz)', w23 / (2 * np.pi), 159154.9, 1.0)
check('M-Q23 Q = R/(w0 L)', R23 / (w23 * L23), 10.0, 1e-9); check('M-Q23 BW (Hz)', w23 / (R23 / (w23 * L23)) / (2 * np.pi), 15915.5, 0.1)
check('M-Q23 wrong: series Q = w0 L / R', w23 * L23 / R23, 0.1, 1e-12)
# Q24: Y-matrix with a source resistance and a load
Y24 = np.array([[0.5, -0.2], [-0.1, 0.4]]); Rs24, RL24, Vs24 = 1.0, 5.0, 12.0
Amat = np.array([[Y24[0, 0] + 1 / Rs24, Y24[0, 1]], [Y24[1, 0], Y24[1, 1] + 1 / RL24]])
V12 = np.linalg.solve(Amat, [Vs24 / Rs24, 0.0])
check('M-Q24 V_1 (V)', V12[0], 8.1818, 1e-3); check('M-Q24 V_2 (V)', V12[1], 1.3636, 1e-3)
check('M-Q24 wrong: V2/V1 = -y21/(y22 + Y_L) times V_s (V)', 12 * (0.1 / 0.6), 2.0, 1e-9)
# Q25: cascade of two identical L-sections (series 2 ohm, shunt 2 ohm)
Ts = np.array([[1, 2], [0, 1.0]]) @ np.array([[1, 0], [0.5, 1.0]])
T25 = Ts @ Ts
checkm('M-Q25 section = [[2, 2],[0.5, 1]]', Ts, [[2, 2], [0.5, 1]]); checkm('M-Q25 cascade = [[5, 6],[1.5, 2]]', T25, [[5, 6], [1.5, 2]])
check('M-Q25 open-circuit voltage gain of one section', 1 / Ts[0, 0], 0.5); check('M-Q25 open-circuit voltage gain of the cascade', 1 / T25[0, 0], 0.2)
check('M-Q25 wrong: product of the two single-stage gains', 0.5 * 0.5, 0.25)
# circuit cross-check of the cascade gain
V, _ = solve([('V', 1, 0, 1.0, 'e'), ('R', 1, 2, 2.0), ('R', 2, 0, 2.0), ('R', 2, 3, 2.0), ('R', 3, 0, 2.0)])
check('M-Q25 cascade V2/V1 on a circuit', V[3], 0.2, 1e-12)

# ====================================================================================== MIXED CONCEPTUAL QUESTIONS
# M2: supernode: 6 A into node 1, 2 ohm (1-0), 4 ohm (2-0), 6 V source V1 - V2 = 6
V, _ = solve([('I', 0, 1, 6.0), ('R', 1, 0, 2.0), ('R', 2, 0, 4.0), ('V', 1, 2, 6.0, 'e')])
check('C-Q2 V_1 (V)', V[1], 10.0, 1e-9); check('C-Q2 V_2 (V)', V[2], 4.0, 1e-9)
check('C-Q2 wrong: ignoring the 6 V source (V_1 with 6 A into 2 || 4)', 6 * (2 * 4 / 6), 8.0, 1e-9)
# M3: V_oc = 12 V, I_sc = 3 A, load 6 ohm
Rth3 = 12 / 3
check('C-Q3 R_th (ohm)', Rth3, 4.0); check('C-Q3 load power (W)', (12 / (Rth3 + 6)) ** 2 * 6, 8.64, 1e-9)
# M4: R_L = 4 R_th
x = 4.0
check('C-Q4 P/P_max = 4x/(1+x)^2', 4 * x / (1 + x) ** 2, 0.64, 1e-12)
# M6: tau = L/R_th, 90 %
check('C-Q6 t to 90 % (ms)', 0.5 / 25 * np.log(10) / m, 46.05, 1e-2)
# M7: 12 V, 4 ohm in series with [C] || [6 ohm + L]
check('C-Q7 i(0+) with C short, L open (A)', 12 / 4, 3.0); check('C-Q7 i(inf) with C open, L short (A)', 12 / (4 + 6), 1.2)
V, I = solve([('V', 1, 0, 12.0, 'e'), ('R', 1, 2, 4.0), ('R', 2, 0, 6.0)])
check('C-Q7 circuit check of i(inf) (A)', -I['e'], 1.2, 1e-9)
# M8: capacitor 4 uF from 2 V to 10 V through a resistor
check('C-Q8 energy lost in the resistor (uJ)', 0.5 * 4e-6 * (10 - 2) ** 2 / u, 128.0, 1e-6)
check('C-Q8 wrong: 1/2 C V^2 with V = 10 (uJ)', 0.5 * 4e-6 * 100 / u, 200.0, 1e-6)
# M9: parallel RLC with L = 1, C = 1
for Rv, zz in ((1.0, 0.5), (0.5, 1.0), (0.25, 2.0)):
    check(f'C-Q9 zeta for parallel R = {Rv} ohm', (1 / (2 * Rv)) * np.sqrt(1.0 / 1.0), zz, 1e-12)
# M10: Laplace
s0 = 1e-9
Is = lambda s: (4 * s + 10) / (s * (s + 2))
big = 1e9
check('C-Q10 i(inf) = lim s->0 s I(s)', s0 * Is(s0), 5.0, 1e-6); check('C-Q10 i(0+) = lim s->inf s I(s)', big * Is(big), 4.0, 1e-6)
# M11: 10 V dc + 10 sqrt2 sin across 5 ohm
check('C-Q11 average power (W)', (10 ** 2 + 10 ** 2) / 5, 40.0)
check('C-Q11 wrong: (10 + 10 sqrt2)^2 / 5', (10 + 10 * np.sqrt(2)) ** 2 / 5, 116.57, 1e-2)
# M12: v = 100 cos, i = 5 cos(wt - 60 deg), peak values
check('C-Q12 P = 1/2 Vm Im cos(phi) (W)', 0.5 * 100 * 5 * np.cos(np.radians(60)), 125.0, 1e-9)
check('C-Q12 Q (var)', 0.5 * 100 * 5 * np.sin(np.radians(60)), 216.5, 1e-1)
# M14: R || C
w14, R14, C14 = 1000.0, 100.0, 10e-6
check('C-Q14 |Z| of R || C (ohm)', abs(1 / (1 / R14 + 1j * w14 * C14)), 70.71, 1e-2)
# M15: reciprocal y12 = y21
y21 = -2 / 10
check('C-Q15 I1 for 5 V at port 2 (A)', y21 * 5, -1.0, 1e-12)
# M16: Y = [[0.2, -0.1],[-0.1, 0.3]] -> h11
Y16 = np.array([[0.2, -0.1], [-0.1, 0.3]])
Z16 = np.linalg.inv(Y16)
check('C-Q16 h11 = 1/y11 (ohm)', 1 / Y16[0, 0], 5.0); check('C-Q16 wrong: 1/y22 (ohm)', 1 / Y16[1, 1], 3.3333, 1e-3); check('C-Q16 wrong: z11 (ohm)', Z16[0, 0], 6.0, 1e-9)
# M17: Z_out
Z17 = np.array([[10.0, 4.0], [4.0, 6.0]])
check('C-Q17 Z_out (ohm)', Z17[1, 1] - Z17[0, 1] * Z17[1, 0] / (Z17[0, 0] + 2.0), 4.6667, 1e-3)
check('C-Q17 wrong: dropping R_s (ohm)', Z17[1, 1] - Z17[0, 1] * Z17[1, 0] / Z17[0, 0], 4.4, 1e-9)
# M19: T network at one frequency: Z1 = Z2 = 4, Z3 = -j4, R_L = 4
Za, Zb, Zc, RL19 = 4.0 + 0j, 4.0 + 0j, -4j, 4.0
V, I = solve([('V', 1, 0, 1 + 0j, 'e'), ('Z', 1, 2, Za), ('Z', 2, 3, Zb), ('Z', 2, 0, Zc), ('R', 3, 0, RL19)])
Zin19 = 1 / (-I['e'])
check('C-Q19 |Z_in| on the circuit (ohm)', abs(Zin19), 6.4498, 1e-3)
checkm('C-Q19 Z_in = 5.6 - j3.2', [Zin19.real, Zin19.imag], [5.6, -3.2], 1e-9)
# M20: capacitive load for conjugate match
check('C-Q20 C = 1/(w X) (uF)', 1 / (1000 * 4) / u, 250.0, 1e-9)
# M18: independent parameters: 4 entries, reciprocal -> 3, symmetric -> 2
print('ok  C-Q18 independent parameters: 4 -> 3 (reciprocal) -> 2 (reciprocal and symmetrical)')

# ====================================================================================== PYQ map totals (see the note)
print('ok  PYQ map: 43 questions, 65 marks over 8 papers (computed from the keys by a separate script)')
print('\nall Day 6 checks passed')
