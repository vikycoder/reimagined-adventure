"""Re-checks every number quoted in Day05_Two_Port_Networks.md and Day05_Conceptual_Questions.md.

Run:  python3 verify_day05.py          (needs numpy; uses mna.py)

Two-port parameters are *measured on circuits* by exciting the ports (as the definitions say), so the
conversion tables and the terminated-two-port formulas in the note are tested against real circuit solutions,
not just against each other.  Past-year answers are checked against the official keys quoted in the comments.
"""
import numpy as np

from mna import solve

rng = np.random.default_rng(5)


def check(name, got, want, tol=1e-6):
    assert abs(got - want) < tol, f'{name}: got {got}, expected {want}'
    print(f'ok  {name:<66} {got:.6g}' if np.isrealobj(got) else f'ok  {name:<66} {got:.6g}')


def checkm(name, got, want, tol=1e-9):
    assert np.allclose(got, want, atol=tol, rtol=0), f'{name}: got\n{got}\nexpected\n{want}'
    print(f'ok  {name}')


# ============================================================ measuring a two-port on a circuit
def measure(elems, n1, n2):
    """Return dict of 2x2 matrices Z, Y, h, g, T (ABCD) obtained from the definitions (port excitations).
    Ports: (n1, 0) and (n2, 0).  I1, I2 are the currents INTO the ports.  Entries that do not exist are None."""
    out = {}
    # --- Y: V at one port, other port shorted
    Y = np.zeros((2, 2), dtype=complex)
    for k in (0, 1):
        V, I = solve(elems + [('V', n1, 0, 1.0 if k == 0 else 0.0, 'p1'), ('V', n2, 0, 1.0 if k == 1 else 0.0, 'p2')])
        Y[0, k], Y[1, k] = -I['p1'], -I['p2']
    out['Y'] = Y
    # --- Z: I at one port, other port open
    Z = np.zeros((2, 2), dtype=complex)
    try:
        for k in (0, 1):
            extra = [('I', 0, n1 if k == 0 else n2, 1.0)]
            V, _ = solve(elems + extra)
            Z[0, k], Z[1, k] = V[n1], V[n2]
        out['Z'] = Z
    except np.linalg.LinAlgError:
        out['Z'] = None
    # --- h: (I1, V2) are the independent variables
    try:
        h = np.zeros((2, 2), dtype=complex)
        V, I = solve(elems + [('I', 0, n1, 1.0), ('V', n2, 0, 0.0, 'p2')])               # I1 = 1, V2 = 0
        h[0, 0], h[1, 0] = V[n1], -I['p2']
        V, I = solve(elems + [('V', n2, 0, 1.0, 'p2')])                                    # I1 = 0, V2 = 1
        h[0, 1], h[1, 1] = V[n1], -I['p2']
        out['h'] = h
    except np.linalg.LinAlgError:
        out['h'] = None
    # --- g: (V1, I2) are the independent variables
    try:
        g = np.zeros((2, 2), dtype=complex)
        V, I = solve(elems + [('V', n1, 0, 1.0, 'p1')])                                    # V1 = 1, I2 = 0
        g[0, 0], g[1, 0] = -I['p1'], V[n2]
        V, I = solve(elems + [('V', n1, 0, 0.0, 'p1'), ('I', 0, n2, 1.0)])                 # V1 = 0, I2 = 1
        g[0, 1], g[1, 1] = -I['p1'], V[n2]
        out['g'] = g
    except np.linalg.LinAlgError:
        out['g'] = None
    # --- ABCD: V1 = A V2 + B (-I2) ; I1 = C V2 + D (-I2)
    try:
        V, I = solve(elems + [('V', n1, 0, 1.0, 'p1')])                                    # port 2 open: I2 = 0
        A, C = 1.0 / V[n2], (-I['p1']) / V[n2]
        V, I = solve(elems + [('V', n1, 0, 1.0, 'p1'), ('V', n2, 0, 0.0, 'p2')])           # port 2 shorted
        B, D = -1.0 / (-I['p2']), (-I['p1']) / I['p2']
        out['T'] = np.array([[A, B], [C, D]], dtype=complex)
    except np.linalg.LinAlgError:
        out['T'] = None
    return out


def det(M):
    return M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]


# ---- conversion formulas exactly as written in the note ------------------------------------------------------
def Z_from_Y(Y):
    d = det(Y); return np.array([[Y[1, 1], -Y[0, 1]], [-Y[1, 0], Y[0, 0]]]) / d


def Y_from_Z(Z):
    return Z_from_Y(Z)                                    # same formula: the matrices are inverses of each other


def T_from_Z(Z):
    return np.array([[Z[0, 0], det(Z)], [1, Z[1, 1]]]) / Z[1, 0]


def T_from_Y(Y):
    return np.array([[-Y[1, 1], -1], [-det(Y), -Y[0, 0]]]) / Y[1, 0]


def Z_from_T(T):
    A, B, C, D = T.ravel()
    return np.array([[A, A * D - B * C], [1, D]]) / C


def Y_from_T(T):
    A, B, C, D = T.ravel()
    return np.array([[D, -(A * D - B * C)], [-1, A]]) / B


def h_from_Z(Z):
    return np.array([[det(Z), Z[0, 1]], [-Z[1, 0], 1]]) / Z[1, 1]


def h_from_Y(Y):
    return np.array([[1, -Y[0, 1]], [Y[1, 0], det(Y)]]) / Y[0, 0]


def Z_from_h(h):
    return np.array([[det(h), h[0, 1]], [-h[1, 0], 1]]) / h[1, 1]


def Y_from_h(h):
    return np.array([[1, -h[0, 1]], [h[1, 0], det(h)]]) / h[0, 0]


def T_from_h(h):
    return np.array([[-det(h), -h[0, 0]], [-h[1, 1], -1]]) / h[1, 0]


def h_from_T(T):
    A, B, C, D = T.ravel()
    return np.array([[B, A * D - B * C], [-1, C]]) / D


def g_from_Y(Y):
    return np.array([[det(Y), Y[0, 1]], [-Y[1, 0], 1]]) / Y[1, 1]


# ============================================================ 1. conversion tables on real circuits
# a reciprocal network: bridged-T style resistor network, ports at nodes 1 and 2
net_rec = [('R', 1, 3, 2.0), ('R', 3, 2, 3.0), ('R', 3, 0, 4.0), ('R', 1, 2, 12.0), ('R', 1, 0, 20.0)]
# a NON-reciprocal network: same plus a VCCS and a CCVS-free amplifier action
net_non = net_rec + [('VCCS', 2, 0, 1, 0, 0.1)]
for label, net in (('reciprocal', net_rec), ('non-reciprocal (VCCS)', net_non)):
    P = measure(net, 1, 2)
    Z, Y, h, g, T = P['Z'], P['Y'], P['h'], P['g'], P['T']
    checkm(f'[{label}] Z Y = I', Z @ Y, np.eye(2))
    checkm(f'[{label}] Z from Y formula', Z_from_Y(Y), Z); checkm(f'[{label}] Y from Z formula', Y_from_Z(Z), Y)
    checkm(f'[{label}] ABCD from Z', T_from_Z(Z), T); checkm(f'[{label}] ABCD from Y', T_from_Y(Y), T)
    checkm(f'[{label}] Z from ABCD', Z_from_T(T), Z); checkm(f'[{label}] Y from ABCD', Y_from_T(T), Y)
    checkm(f'[{label}] h from Z', h_from_Z(Z), h); checkm(f'[{label}] h from Y', h_from_Y(Y), h)
    checkm(f'[{label}] Z from h', Z_from_h(h), Z); checkm(f'[{label}] Y from h', Y_from_h(h), Y)
    checkm(f'[{label}] ABCD from h', T_from_h(h), T); checkm(f'[{label}] h from ABCD', h_from_T(T), h)
    checkm(f'[{label}] g = inverse of h', np.linalg.inv(h), g); checkm(f'[{label}] g from Y', g_from_Y(Y), g)
    recip = {'reciprocal': True, 'non-reciprocal (VCCS)': False}[label]
    print(f'      [{label}]  z12 = {Z[0, 1].real:.4f}, z21 = {Z[1, 0].real:.4f},  y12 = {Y[0, 1].real:.4f}, y21 = {Y[1, 0].real:.4f},  AD - BC = {det(T).real:.4f},  h12 = {h[0, 1].real:.4f}, h21 = {h[1, 0].real:.4f}')
    if recip:
        check('reciprocal: z12 = z21', Z[0, 1].real, Z[1, 0].real, 1e-12)
        check('reciprocal: y12 = y21', Y[0, 1].real, Y[1, 0].real, 1e-12)
        check('reciprocal: h12 = -h21', h[0, 1].real, -h[1, 0].real, 1e-12)
        check('reciprocal: g12 = -g21', g[0, 1].real, -g[1, 0].real, 1e-12)
        check('reciprocal: AD - BC = 1', det(T).real, 1.0, 1e-12)
    else:
        assert abs(Z[0, 1] - Z[1, 0]) > 1e-3 and abs(det(T) - 1) > 1e-3
        print('ok  non-reciprocal network breaks all the reciprocity conditions')

# ============================================================ 2. T and Pi networks, elementary blocks
Z1, Z2, Z3 = 4.0, 6.0, 12.0                                           # Ex 1: T network
tnet = [('R', 1, 3, Z1), ('R', 3, 2, Z2), ('R', 3, 0, Z3)]
P = measure(tnet, 1, 2)
checkm('Ex1 T-network Z', P['Z'].real, [[Z1 + Z3, Z3], [Z3, Z2 + Z3]])
checkm('Ex1 T-network Z = [[16,12],[12,18]]', P['Z'].real, [[16, 12], [12, 18]])
checkm('Ex1 T-network ABCD formulas', P['T'].real, [[1 + Z1 / Z3, Z1 + Z2 + Z1 * Z2 / Z3], [1 / Z3, 1 + Z2 / Z3]])
checkm('Ex1 T-network ABCD numbers', P['T'].real, [[4 / 3, 12], [1 / 12, 1.5]])
check('Ex1 AD - BC = 1', det(P['T']).real, 1.0, 1e-12)
checkm('Ex1 T-network Y from Z (inverse)', P['Y'].real, np.linalg.inv([[16, 12], [12, 18]]))
check('Ex1 y11 = z22/det Z (S)', P['Y'][0, 0].real, 18 / 144, 1e-12); check('Ex1 det Z', det(P['Z']).real, 144.0, 1e-12)
check('Ex1 y11 is NOT 1/z11 (difference)', abs(P['Y'][0, 0].real - 1 / 16), 0.0625, 1e-12)

Ya, Yb, Yc = 1.0, 1 / 4, 1 / 2                                          # Pi network: 1 ohm shunt, 4 ohm shunt, 2 ohm series
pnet = [('R', 1, 0, 1 / Ya), ('R', 2, 0, 1 / Yb), ('R', 1, 2, 1 / Yc)]
P = measure(pnet, 1, 2)
checkm('Pi-network Y', P['Y'].real, [[Ya + Yc, -Yc], [-Yc, Yb + Yc]])
checkm('Pi-network ABCD formulas', P['T'].real, [[1 + Yb / Yc, 1 / Yc], [Ya + Yb + Ya * Yb / Yc, 1 + Ya / Yc]])
check('Q6 y21 of the pi network (S)', P['Y'][1, 0].real, -0.5, 1e-12)
check('Q6 wrong: +0.5 (sign) / y22 = 0.75', P['Y'][1, 1].real, 0.75, 1e-12)

# series impedance only: Z does not exist, Y singular
snet = [('R', 1, 2, 5.0)]
P = measure(snet, 1, 2)
check('Q2 series resistor: det Y = 0 (Z does not exist)', abs(det(P['Y'])), 0.0, 1e-12)
checkm('Q2 series resistor: h = [[R, 1],[-1, 0]]', P['h'].real, [[5, 1], [-1, 0]])
checkm('Q2 series resistor: ABCD = [[1, R],[0, 1]]', P['T'].real, [[1, 5], [0, 1]])
print('      (Z for a lone series resistor:', 'None' if P['Z'] is None else 'solver returned values, but the matrix is singular', ')')

# shunt resistor only (both ports across the same element): Y does not exist, Z = [[R,R],[R,R]] singular
shnet = [('R', 1, 2, 1e-9), ('R', 1, 0, 5.0)]                            # ports tied together by a wire (1e-9 ohm), one shunt
Zs_ = np.array([[5, 5], [5, 5.0]])
check('shunt resistor: det Z = 0 (Y does not exist)', det(Zs_), 0.0, 1e-12)

# ============================================================ 3. cascade: order matters (Q8, Q14)
Tser = lambda Z: np.array([[1, Z], [0, 1.0]]); Tsh = lambda Y: np.array([[1, 0], [Y, 1.0]])
T_ab = Tser(2.0) @ Tsh(0.5)                                              # series 2 ohm first (port-1 side), then shunt 0.5 S
T_ba = Tsh(0.5) @ Tser(2.0)
checkm('Q8 series then shunt = [[2,2],[0.5,1]]', T_ab, [[2, 2], [0.5, 1]])
checkm('Q8 shunt then series = [[1,2],[0.5,2]] (reverse order)', T_ba, [[1, 2], [0.5, 2]])
cnet = [('R', 1, 3, 2.0), ('R', 3, 0, 2.0)]                              # port 1 -> series 2 ohm -> shunt 2 ohm (0.5 S) -> port 2 at node 3
cnet = [('R', 1, 2, 2.0), ('R', 2, 0, 2.0)]
P = measure(cnet, 1, 2)
checkm('Q8 measured on the circuit', P['T'].real, [[2, 2], [0.5, 1]])
Tid = np.array([[2, 3], [1, 2.0]])
check('Q14 identical section reciprocal: AD - BC', det(Tid), 1.0, 1e-12)
checkm('Q14 cascade of two identical sections', Tid @ Tid, [[7, 12], [4, 7]])
check('Q14 B of the cascade (ohm)', (Tid @ Tid)[0, 1], 12.0, 1e-12)
check('Q14 wrong: adding the matrices gives B', (Tid + Tid)[0, 1], 6.0, 1e-12)
# physical cascade check with two T networks measured on a circuit
t1 = [('R', 1, 3, 4.0), ('R', 3, 2, 6.0), ('R', 3, 0, 12.0)]
t2 = [('R', 2, 5, 3.0), ('R', 5, 4, 2.0), ('R', 5, 0, 6.0)]              # second T from node 2 to node 4
Pa, Pb, Pab = measure(t1, 1, 2), measure(t2, 2, 4), measure(t1 + t2, 1, 4)
checkm('cascade of two T networks: T_total = T_a T_b', Pab['T'], Pa['T'] @ Pb['T'])
assert not np.allclose(Pab['T'], Pb['T'] @ Pa['T']); print('ok  ... and the reverse order is different')

# ============================================================ 4. interconnections
# parallel (common ground): Y adds.  Both networks are 3-terminal so the port condition holds automatically
na = [('R', 1, 3, 4.0), ('R', 3, 2, 6.0), ('R', 3, 0, 12.0)]
nb = [('R', 1, 7, 2.0), ('R', 7, 2, 5.0), ('R', 7, 0, 9.0), ('R', 1, 0, 30.0)]
Ya_, Yb_, Yab = measure(na, 1, 2)['Y'], measure(nb, 1, 2)['Y'], measure(na + nb, 1, 2)['Y']
checkm('parallel connection: Y_total = Y_a + Y_b', Yab, Ya_ + Yb_)

# series-series of two THREE-terminal networks fails the port condition (the common terminals force a short).
# Network A has ports (1, ref_a) and (2, ref_a); network B has ports (b1, ref_b) and (b2, ref_b).
# Series connection: port 1 = (1, ref_b), port 2 = (2, ref_b);  ref_a is joined to b1 (for port 1) AND to b2 (for port 2),
# so b1 and b2 end up on the SAME node (node 4): network B is not the network we thought it was.
seriesA = [('R', 1, 3, 4.0), ('R', 3, 2, 6.0), ('R', 3, 4, 12.0)]          # A: T network with reference node 4
seriesB = [('R', 4, 7, 3.0), ('R', 7, 4, 5.0), ('R', 7, 0, 9.0)]           # B: T network, its two top terminals are both node 4
Pser = measure(seriesA + seriesB, 1, 2)
Zsum = measure([('R', 1, 3, 4.0), ('R', 3, 2, 6.0), ('R', 3, 0, 12.0)], 1, 2)['Z'] + measure([('R', 1, 3, 3.0), ('R', 3, 2, 5.0), ('R', 3, 0, 9.0)], 1, 2)['Z']
print('      series-series of two 3-terminal networks: measured Z =', np.round(Pser['Z'].real, 4).tolist(), '   Z_a + Z_b =', np.round(Zsum.real, 4).tolist())
assert not np.allclose(Pser['Z'], Zsum, atol=1e-3)
print('ok  Z_a + Z_b is WRONG for this series connection (port condition violated)')


# valid series connection: isolated (4-terminal) boxes.  A box with matrix Z is built from a resistor + CCVS per port
def isolated_box(base, Zm, p1, p2):
    """4-terminal realisation of an arbitrary Z matrix.  p1=(top,bottom) of port 1, p2=(top,bottom) of port 2 (integer nodes).
    Port 1 branch: top -> 0 V meter -> R z11 -> CCVS(z12*I2) -> bottom;  port 2 branch likewise with z22 and z21*I1."""
    t1, b1 = p1
    t2, b2 = p2
    a, b, c, d = base + 1, base + 2, base + 3, base + 4
    return [
        ('V', t1, a, 0.0, f'm1_{base}'),                                    # measures I1 (flows t1 -> a)
        ('R', a, b, Zm[0, 0]),
        ('CCVS', b, b1, f'm2_{base}', Zm[0, 1], f'e1_{base}'),              # V(b) - V(b1) = z12 * I2
        ('V', t2, c, 0.0, f'm2_{base}'),                                    # measures I2 (flows t2 -> c)
        ('R', c, d, Zm[1, 1]),
        ('CCVS', d, b2, f'm1_{base}', Zm[1, 0], f'e2_{base}'),              # V(d) - V(b2) = z21 * I1
    ]


Za_m = np.array([[16.0, 12.0], [12.0, 18.0]])
Zb_m = np.array([[10.0, 3.0], [5.0, 9.0]])                                  # non-reciprocal on purpose
box = isolated_box(100, Za_m, (11, 12), (13, 14)) + isolated_box(200, Zb_m, (12, 0), (14, 0))     # A.bottoms == B.tops, B.bottoms = ground
checkm('isolated box A alone reproduces its Z', measure(isolated_box(100, Za_m, (11, 0), (13, 0)), 11, 13)['Z'].real, Za_m)
Pser2 = measure(box, 11, 13)
checkm('valid series-series (isolated boxes): Z_total = Z_a + Z_b', Pser2['Z'].real, Za_m + Zb_m, 1e-9)

# h adds for series-parallel and g adds for parallel-series: algebra on random matrices
ha, hb = rng.normal(size=(2, 2)), rng.normal(size=(2, 2))
# series-parallel: I1 common, V1 adds, V2 common, I2 adds
def sp_combine(ha, hb):
    return ha + hb
vA = rng.normal(size=2)                         # arbitrary (I1, V2)
V1a, I2a = ha @ vA; V1b, I2b = hb @ vA
check('series-parallel: V1 adds -> h11 row adds', V1a + V1b, (ha + hb)[0] @ vA, 1e-12)
check('series-parallel: I2 adds -> h21 row adds', I2a + I2b, (ha + hb)[1] @ vA, 1e-12)
print('ok  series-parallel: h matrices add (and parallel-series: g matrices add, by the same argument)')

# ============================================================ 5. terminated two-port formulas (checked on circuits)
P = measure(tnet, 1, 2)          # Ex 1 T network: Z1 = 4, Z2 = 6, Z3 = 12
Z, Y, h, T = P['Z'].real, P['Y'].real, P['h'].real, P['T'].real
Rs, RL, Vs = 4.0, 6.0, 24.0
circ = [('V', 9, 0, Vs, 'vs'), ('R', 9, 1, Rs)] + tnet + [('R', 2, 0, RL)]
V, I = solve(circ)
I1 = -I['vs']; V1, V2 = V[1], V[2]
Zin_ckt = V1 / I1
check('Ex3 circuit: Z_in measured', Zin_ckt, 16 - 12 * 12 / (18 + RL), 1e-9)                  # z11 - z12 z21/(z22 + RL)
check('Ex3 Z_in (Z form) = 10', Z[0, 0] - Z[0, 1] * Z[1, 0] / (Z[1, 1] + RL), 10.0, 1e-9)
check('Ex3 Z_in (Y form)', 1 / (Y[0, 0] - Y[0, 1] * Y[1, 0] / (Y[1, 1] + 1 / RL)), Zin_ckt, 1e-9)
check('Ex3 Z_in (ABCD form)', (T[0, 0] * RL + T[0, 1]) / (T[1, 0] * RL + T[1, 1]), Zin_ckt, 1e-9)
dh = det(h)
check('Ex3 Z_in (h form)', h[0, 0] - h[0, 1] * h[1, 0] * RL / (1 + h[1, 1] * RL), Zin_ckt, 1e-9)
Av = V2 / V1; Ai = (V2 / RL) / I1
check('Ex3 voltage gain V2/V1 (Z form)', Z[1, 0] * RL / (Z[0, 0] * RL + det(Z)), Av, 1e-9)
check('Ex3 voltage gain (Y form)', -Y[1, 0] / (Y[1, 1] + 1 / RL), Av, 1e-9)
check('Ex3 voltage gain (ABCD form)', RL / (T[0, 0] * RL + T[0, 1]), Av, 1e-9)
check('Ex3 voltage gain (h form)', -h[1, 0] * RL / (h[0, 0] + dh * RL), Av, 1e-9)
check('Ex3 current gain I_L/I1 (Z form)', Z[1, 0] / (Z[1, 1] + RL), Ai, 1e-9)
check('Ex3 current gain (ABCD form)', 1 / (T[1, 0] * RL + T[1, 1]), Ai, 1e-9)
check('Ex3 current gain I_L/I1 = -I2/I1 (h form: -h21/(1 + h22 RL))', -h[1, 0] / (1 + h[1, 1] * RL), Ai, 1e-9)
check('Ex3 current gain (Y form: -y21 Y_L/(y11(y22+Y_L) - y12 y21))', -Y[1, 0] * (1 / RL) / (Y[0, 0] * (Y[1, 1] + 1 / RL) - Y[0, 1] * Y[1, 0]), Ai, 1e-9)
# output impedance (source off) seen at port 2
Zout_ckt = None
V_, I_ = solve([('R', 0, 1, Rs)] + tnet + [('V', 2, 0, 1.0, 'tst')])          # source turned off = short: R_s goes to ground
Zout_ckt = 1 / (-I_['tst'])
check('Ex3 Z_out measured (source off)', Zout_ckt, Z[1, 1] - Z[0, 1] * Z[1, 0] / (Z[0, 0] + Rs), 1e-9)
check('Ex3 Z_out (Y form)', 1 / (Y[1, 1] - Y[0, 1] * Y[1, 0] / (Y[0, 0] + 1 / Rs)), Zout_ckt, 1e-9)
check('Ex3 Z_out (ABCD form)', (T[1, 1] * Rs + T[0, 1]) / (T[1, 0] * Rs + T[0, 0]), Zout_ckt, 1e-9)
check('Ex3 Z_out (h form)', (h[0, 0] + Rs) / (dh + h[1, 1] * Rs), Zout_ckt, 1e-9)
print(f'      Ex3 numbers: Z_in = {Zin_ckt:.4f}, Z_out = {Zout_ckt:.4f}, V2/V1 = {Av:.4f}, I_L/I1 = {Ai:.4f}, V2/Vs = {V2 / Vs:.4f}')
check('Ex3 V2/V_s with source resistance (Z form)', Z[1, 0] * RL / ((Z[0, 0] + Rs) * (Z[1, 1] + RL) - Z[0, 1] * Z[1, 0]), V2 / Vs, 1e-9)
# Thevenin at port 2 and maximum power
Voc = Z[1, 0] * Vs / (Z[0, 0] + Rs)
check('Ex3 Thevenin voltage at port 2 (V)', Voc, 24 * 12 / 20, 1e-9)

# ============================================================ 6. Q16, Q17 (z = [[20,10],[10,15]])
Zq = np.array([[20.0, 10.0], [10.0, 15.0]])
check('Q16 Z_in with R_L = 5', Zq[0, 0] - Zq[0, 1] * Zq[1, 0] / (Zq[1, 1] + 5), 15.0, 1e-12)
check('Q16 wrong: z11 itself', Zq[0, 0], 20.0, 1e-12)
Zo = Zq[1, 1] - Zq[0, 1] * Zq[1, 0] / (Zq[0, 0] + 5)
Vth = Zq[1, 0] * 50 / (Zq[0, 0] + 5)
check('Q17 Z_out (R_s = 5)', Zo, 11.0, 1e-12); check('Q17 V_th at port 2 (V)', Vth, 20.0, 1e-12)
check('Q17 P_max = V_th^2/(4 Z_out) (W)', Vth ** 2 / (4 * Zo), 9.0909, 1e-4)
RLs = np.linspace(0.1, 60, 600001)
Vlo = Zq[1, 0] * 50 / ((Zq[0, 0] + 5) * (Zq[1, 1] + RLs) - Zq[0, 1] * Zq[1, 0]) * RLs
Plo = Vlo ** 2 / RLs
check('Q17 brute-force best R_L (ohm)', RLs[np.argmax(Plo)], 11.0, 1e-3); check('Q17 brute-force P_max (W)', Plo.max(), 9.0909, 1e-4)
check('Q17 wrong: R_L = z22 = 15 gives only (W)', (Zq[1, 0] * 50 / ((25) * (30) - 100) * 15) ** 2 / 15, 8.8757, 1e-3)
# Q18: V2/V1 = Z_L / (A Z_L + B)
check('Q18 sample: A = 2, B = 10, Z_L = 10 -> V2/V1', 10 / (2 * 10 + 10), 1 / 3, 1e-12)
# Q19: h parameters h11 = 1 k, h12 = 0, h21 = 50, h22 = 20 uS, R_L = 5 k
hq = np.array([[1000.0, 0.0], [50.0, 20e-6]]); RLq = 5000.0
check('Q19 delta h', det(hq), 0.02, 1e-12)
check('Q19 voltage gain V2/V1', -hq[1, 0] * RLq / (hq[0, 0] + det(hq) * RLq), -227.2727, 1e-3)
check('Q19 I2/I1 = h21/(1 + h22 R_L)', hq[1, 0] / (1 + hq[1, 1] * RLq), 45.4545, 1e-3)
check('Q19 load current gain I_L/I1 = -I2/I1', -hq[1, 0] / (1 + hq[1, 1] * RLq), -45.4545, 1e-3)
# solve the h equations directly:  V1 = h11 I1 + h12 V2 ; I2 = h21 I1 + h22 V2 ; V2 = -RL I2
I1q = 1.0
V2q = -RLq * hq[1, 0] * I1q / (1 + hq[1, 1] * RLq)
V1q = hq[0, 0] * I1q + hq[0, 1] * V2q
check('Q19 V2/V1 from solving the equations', V2q / V1q, -227.2727, 1e-3)
check('Q19 wrong: ignoring h22 (h21 R_L / h11)', -hq[1, 0] * RLq / hq[0, 0], -250.0, 1e-9)

# ============================================================ 7. other numbers in the questions
check('Q5 D for a reciprocal two-port: (1 + B C)/A', (1 + 5 * 1.5) / 2, 4.25, 1e-12)
check('Q5 AD - BC check', 2 * 4.25 - 5 * 1.5, 1.0, 1e-12)
# Q7: series 2 ohm between top terminals + VCCS (3*V1) from node 2 to ground
q7 = [('R', 1, 2, 2.0), ('VCCS', 2, 0, 1, 0, 3.0)]
P = measure(q7, 1, 2)
checkm('Q7 Y = [[0.5, -0.5],[2.5, 0.5]]', P['Y'].real, [[0.5, -0.5], [2.5, 0.5]])
check('Q7 y21 (S)', P['Y'][1, 0].real, 2.5, 1e-12); check('Q7 y12 != y21 (non-reciprocal): y12', P['Y'][0, 1].real, -0.5, 1e-12)
# Q9
Tq9 = np.array([[3, 5], [1, 2.0]])
check('Q9 reciprocal: AD - BC', det(Tq9), 1.0, 1e-12)
Yq9 = Y_from_T(Tq9)
checkm('Q9 Y from ABCD = [[0.4, -0.2],[-0.2, 0.6]]', Yq9, [[0.4, -0.2], [-0.2, 0.6]])
check('Q9 y22 = A/B (S)', Yq9[1, 1], 0.6, 1e-12); check('Q9 wrong: B/A', 5 / 3, 1.6667, 1e-4)
Zq9 = Z_from_T(Tq9)
checkm('Q9 Z from ABCD = [[3, 1],[1, 2]]', Zq9, [[3, 1], [1, 2]])
# Q10: z11 = 10 (open), short-circuit input resistance = 1/y11 = det(Z)/z22 = 6, z22 = 9 -> |z12| = 6
Zq10 = np.array([[10.0, 6.0], [6.0, 9.0]])
check('Q10 Rin(port 2 open) = z11', Zq10[0, 0], 10.0, 1e-12)
check('Q10 Rin(port 2 shorted) = det Z / z22', det(Zq10) / Zq10[1, 1], 6.0, 1e-12)
check('Q10 |z12| from z11 - Rin_sc = z12^2/z22', np.sqrt((10 - 6) * 9), 6.0, 1e-12)
# Q11: symmetrical reciprocal two-port (T network with equal arms)
tsym = [('R', 1, 3, 3.0), ('R', 3, 2, 3.0), ('R', 3, 0, 5.0)]
P = measure(tsym, 1, 2)
check('Q11 z11 = z22', P['Z'][0, 0].real - P['Z'][1, 1].real, 0.0, 1e-12)
check('Q11 A = D', P['T'][0, 0].real - P['T'][1, 1].real, 0.0, 1e-12)
check('Q11 h11 h22 - h12 h21 = 1', det(P['h']).real, 1.0, 1e-12)
check('Q11 y11 = y22', P['Y'][0, 0].real - P['Y'][1, 1].real, 0.0, 1e-12)
print(f'      Q11: B = {P["T"][0, 1].real:.4f} and C = {P["T"][1, 0].real:.4f} (not equal, so "B = C" is false)')
assert abs(P['T'][0, 1].real - P['T'][1, 0].real) > 1e-3
# Q12: Z -> Y
Zq12 = np.array([[4.0, 2.0], [2.0, 3.0]])
check('Q12 y11 = z22/det Z (S)', Z_from_Y(Zq12)[0, 0], 0.375, 1e-12); check('Q12 wrong: 1/z11', 1 / 4, 0.25, 1e-12)
checkm('Q12 full Y', Z_from_Y(Zq12), [[0.375, -0.25], [-0.25, 0.5]])
# Q3 (B), (D): y12 = y21 (not -y21), h12 = -h21 (not h21)  -> covered in the reciprocal block above

# ============================================================ 8. PYQs
# 2020 Q15 (key 48): Z = [[40,60],[60,120]], 120 V with 10 ohm
Z20 = np.array([[40.0, 60.0], [60.0, 120.0]]); Rs20 = 10.0
check('2020 Q15 Z_out = z22 - z12 z21/(z11 + R_s)  [key 48]', Z20[1, 1] - Z20[0, 1] * Z20[1, 0] / (Z20[0, 0] + Rs20), 48.0, 1e-12)
RLs = np.linspace(1, 200, 199001)
V2 = Z20[1, 0] * 120 / ((Z20[0, 0] + Rs20) * (Z20[1, 1] + RLs) - Z20[0, 1] * Z20[1, 0]) * RLs
check('2020 Q15 brute-force best Z_L (ohm)', RLs[np.argmax(V2 ** 2 / RLs)], 48.0, 2e-3)
# 2023 Q33 (key 80): Y = (1/100)[[2,-1],[-1,4/3]], 120 V with 10 ohm
Y23 = np.array([[2.0, -1.0], [-1.0, 4 / 3]]) / 100; Rs23 = 10.0
Yout = Y23[1, 1] - Y23[0, 1] * Y23[1, 0] / (Y23[0, 0] + 1 / Rs23)
check('2023 Q33 Y_out (S)', Yout, 0.0125, 1e-12); check('2023 Q33 R_L = 1/Y_out (ohm)  [key 80]', 1 / Yout, 80.0, 1e-9)
Z23 = np.linalg.inv(Y23)
check('2023 Q33 via Z: z22 - z12 z21/(z11 + R_s)', Z23[1, 1] - Z23[0, 1] * Z23[1, 0] / (Z23[0, 0] + Rs23), 80.0, 1e-9)
# 2021 Q29 (key C): series 1 ohm, shunt 1 ohm at port 1, shunt 1 ohm at port 2, VCCS 3*V2 injecting into node 1 (arrow up)
q29 = [('R', 1, 0, 1.0), ('R', 1, 2, 1.0), ('R', 2, 0, 1.0), ('VCCS', 0, 1, 2, 0, 3.0)]        # 3*V2 flows ground -> node 1
P = measure(q29, 1, 2)
checkm('2021 Q29 Y = [[2, -4],[-1, 2]]  [key C]', P['Y'].real, [[2, -4], [-1, 2]])
# 2024 Q60 (key 1.5): 2 ohm in series from port 1 to node X (= port 2 top), 4 ohm from X to the CCVS-like source 8 V1 (+ at bottom)
q60 = [('R', 1, 2, 2.0), ('R', 2, 3, 4.0), ('VCVS', 0, 3, 1, 0, 8.0, 'dep')]       # V(0) - V(3) = 8 V1  -> '+' terminal at the bottom (ground side)
P = measure(q60, 1, 2)
print('      2024 Q60 measured Y =', np.round(P['Y'].real, 4).tolist())
check('2024 Q60 y21 (S)  [key 1.5]', P['Y'][1, 0].real, 1.5, 1e-12)
check('2024 Q60 y12 (S)', P['Y'][0, 1].real, -0.5, 1e-12)
# 2025 Q40 (key A): ladder 2,(2 shunt),2,(2 shunt),2
q40 = [('R', 1, 3, 2.0), ('R', 3, 0, 2.0), ('R', 3, 4, 2.0), ('R', 4, 0, 2.0), ('R', 4, 2, 2.0)]
P = measure(q40, 1, 2)
checkm('2025 Q40 Z = [[10/3, 2/3],[2/3, 10/3]]  [key A]', P['Z'].real, [[10 / 3, 2 / 3], [2 / 3, 10 / 3]])
checkm('2025 Q40 same by cascading ABCD blocks', Tser(2) @ Tsh(0.5) @ Tser(2) @ Tsh(0.5) @ Tser(2), P['T'].real)
# 2026 Q51 (key D): T network 1k, 1k shunt, 1k
q51 = [('R', 1, 3, 1e3), ('R', 3, 2, 1e3), ('R', 3, 0, 1e3)]
P = measure(q51, 1, 2)
checkm('2026 Q51 ABCD = [[2, 3e3],[1e-3, 2]]  [key D]', P['T'].real, [[2, 3e3], [1e-3, 2]], 1e-6)
# 2020 Q46 (key 0.8): ideal 2:1 transformer, Z0 = 10 ohm -> S21 = 2 V2/Vs with both ports terminated in Z0
n_ = 2.0
Z0 = 10.0
V2_ = 1.0; I2L = V2_ / Z0; I1_ = I2L / n_; V1_ = n_ * V2_
Vs_ = V1_ + Z0 * I1_
check('2020 Q46 S21 = 2 V2/Vs  [key 0.8]', 2 * V2_ / Vs_, 0.8, 1e-12)
check('2020 Q46 S21 = 2n/(n^2+1)', 2 * n_ / (n_ ** 2 + 1), 0.8, 1e-12)
Tid_ = np.array([[n_, 0], [0, 1 / n_]])
check('2020 Q46 S21 = 2/(A + B/Z0 + C Z0 + D)', 2 / (Tid_[0, 0] + Tid_[0, 1] / Z0 + Tid_[1, 0] * Z0 + Tid_[1, 1]), 0.8, 1e-12)
check('2020 Q46 S11 = 0 only if n = 1; here S11 =', ((n_ ** 2 - 1) / (n_ ** 2 + 1)), 0.6, 1e-12)
# 2019 Q4 (key B = 1 A): reciprocity y12 = y21  (cross-reference to Day 2)
print('ok  2019 Q4 / 2022 Q54: cross-references to Day 2 (reciprocity, Thevenin from a measured V-I line)')

# ============================================================ 9. transformer and coupled inductors
n = 3.0                                                  # ideal transformer V1 = n V2, I1 = -I2/n (both currents into the dotted terminals)
check('ideal transformer: Z_in = n^2 Z_L (n = 3, Z_L = 10)', n ** 2 * 10, 90.0, 1e-12)
check('Q20 reflected impedance n = N1/N2 = 1/2, Z_L = 100 -> Z_in', (1 / 2) ** 2 * 100, 25.0, 1e-12)
# coupled inductors
L1, L2, k = 4.0, 9.0, 0.5
M = k * np.sqrt(L1 * L2)
check('coupled inductors: M = k sqrt(L1 L2)', M, 3.0, 1e-12)
check('series aiding L1 + L2 + 2M', L1 + L2 + 2 * M, 19.0, 1e-12); check('series opposing L1 + L2 - 2M', L1 + L2 - 2 * M, 7.0, 1e-12)
# T-equivalent: (L1 - M), (L2 - M), M ;  Z = jw [[L1, M],[M, L2]]
w = 2.0
tco = [('Z', 1, 3, 1j * w * (L1 - M)), ('Z', 3, 2, 1j * w * (L2 - M)), ('Z', 3, 0, 1j * w * M)]
Pt = measure(tco, 1, 2)
checkm('T-equivalent of coupled inductors: Z = jw[[L1, M],[M, L2]]', Pt['Z'], 1j * w * np.array([[L1, M], [M, L2]]))
check('energy: k <= 1 means M^2 <= L1 L2 (k = 0.5)', float(M ** 2 <= L1 * L2), 1.0, 0.5)
# series connection via the T-equivalent: apply the same current through both coils  v = jw(L1 + L2 + 2M) i
Zc = 1j * w * np.array([[L1, M], [M, L2]])
i = 1.0
v_total = (Zc[0, 0] + Zc[0, 1]) * i + (Zc[1, 0] + Zc[1, 1]) * i
check('series aiding via Z matrix: L_eq', (v_total / (1j * w * i)).real, 19.0, 1e-12)
# parallel connection of coupled inductors (aiding): L = (L1 L2 - M^2)/(L1 + L2 - 2M)
Zpar = 1 / np.sum(np.linalg.inv(Zc))                    # same voltage across both: i1 + i2 = v * sum(inv(Z)) entries
check('parallel aiding L = (L1 L2 - M^2)/(L1 + L2 - 2M)', ((1 / np.sum(np.linalg.inv(Zc))) / (1j * w)).real, (L1 * L2 - M ** 2) / (L1 + L2 - 2 * M), 1e-12)


# ============================================================ 10. extra numbers used in the note (examples, practice, remarks)
# AD - BC = z12/z21 = y12/y21 = -h12/h21 in general (the reciprocity test is "this ratio is 1")
Pn = measure(net_non, 1, 2)
Zn, Yn, hn, Tn = Pn['Z'], Pn['Y'], Pn['h'], Pn['T']
check('AD - BC = z12/z21 (non-reciprocal network)', det(Tn).real, (Zn[0, 1] / Zn[1, 0]).real, 1e-12)
check('AD - BC = y12/y21', det(Tn).real, (Yn[0, 1] / Yn[1, 0]).real, 1e-12)
check('AD - BC = -h12/h21', det(Tn).real, (-hn[0, 1] / hn[1, 0]).real, 1e-12)
check('delta h = z11/z22  (so "symmetric" <=> delta h = 1)', det(hn).real, (Zn[0, 0] / Zn[1, 1]).real, 1e-12)

# Ex 2: unilateral amplifier  R_i = 1 k, VCCS g_m V1 drawn out of node 2, R_o = 5 k
gm, Ri, Ro, RLa = 0.04, 1e3, 5e3, 5e3
amp = [('R', 1, 0, Ri), ('R', 2, 0, Ro), ('VCCS', 2, 0, 1, 0, gm)]
P = measure(amp, 1, 2)
checkm('Ex2 Y = [[1 mS, 0],[40 mS, 0.2 mS]]', P['Y'].real, [[1e-3, 0], [0.04, 2e-4]], 1e-12)
checkm('Ex2 Z = [[1000, 0],[-200000, 5000]]', P['Z'].real, [[1000, 0], [-2e5, 5000]], 1e-6)
checkm('Ex2 h = [[1000, 0],[40, 200 uS]]', P['h'].real, [[1000, 0], [40, 2e-4]], 1e-12)
checkm('Ex2 ABCD = [[-0.005, -25],[-5e-6, -0.025]]', P['T'].real, [[-0.005, -25], [-5e-6, -0.025]], 1e-12)
check('Ex2 AD - BC = y12/y21 = 0 (non-reciprocal)', det(P['T']).real, 0.0, 1e-12)
check('Ex2 voltage gain from Y: -y21/(y22 + 1/RL)', -P['Y'][1, 0].real / (P['Y'][1, 1].real + 1 / RLa), -100.0, 1e-9)
check('Ex2 voltage gain from h: -h21 RL/(h11 + dh RL)', -40 * RLa / (1000 + det(P['h']).real * RLa), -100.0, 1e-9)
Vamp, _ = solve([('V', 1, 0, 1.0, 'v1'), ('R', 1, 0, Ri), ('R', 2, 0, Ro), ('R', 2, 0, RLa), ('VCCS', 2, 0, 1, 0, gm)])
check('Ex2 V2 for V1 = 1 V with the load connected', Vamp[2], -100.0, 1e-9)

# Ex 1 extras: Y of the T network
check('Ex1 Y = (1/144)[[18,-12],[-12,16]]: y22', measure(tnet, 1, 2)['Y'][1, 1].real, 16 / 144, 1e-12)

# 2025 Q40 by cascading: T = Ts(2) Tsh(0.5) Ts(2) Tsh(0.5) Ts(2) = [[5, 16],[1.5, 5]]
Tl = Tser(2) @ Tsh(0.5) @ Tser(2) @ Tsh(0.5) @ Tser(2)
checkm('2025 Q40 cascade product = [[5, 16],[1.5, 5]]', Tl, [[5, 16], [1.5, 5]])
checkm('2025 Q40 Z from that T = [[A/C, 1/C],[1/C, D/C]]', Z_from_T(Tl), [[10 / 3, 2 / 3], [2 / 3, 10 / 3]])

# Practice problems
# P1: T network Z1 = 3, Z2 = 5, Z3 = 2
P = measure([('R', 1, 3, 3.0), ('R', 3, 2, 5.0), ('R', 3, 0, 2.0)], 1, 2)
checkm('P1 Z = [[5, 2],[2, 7]]', P['Z'].real, [[5, 2], [2, 7]]); checkm('P1 ABCD = [[2.5, 15.5],[0.5, 3.5]]', P['T'].real, [[2.5, 15.5], [0.5, 3.5]])
check('P1 AD - BC', det(P['T']).real, 1.0, 1e-12)
# P2: Pi network Ya = 1 S, Yb = 2 S, Yc = 3 S
P = measure([('R', 1, 0, 1.0), ('R', 2, 0, 0.5), ('R', 1, 2, 1 / 3)], 1, 2)
checkm('P2 Y = [[4, -3],[-3, 5]]', P['Y'].real, [[4, -3], [-3, 5]]); checkm('P2 ABCD = [[5/3, 1/3],[11/3, 4/3]]', P['T'].real, [[5 / 3, 1 / 3], [11 / 3, 4 / 3]])
# P3: ABCD = [[2,3],[1,2]], V_s = 12 V, R_s = 3, R_L = 4
T3 = np.array([[2.0, 3.0], [1.0, 2.0]]); Rs3, RL3, Vs3 = 3.0, 4.0, 12.0
Zin3 = (T3[0, 0] * RL3 + T3[0, 1]) / (T3[1, 0] * RL3 + T3[1, 1])
Zout3 = (T3[1, 1] * Rs3 + T3[0, 1]) / (T3[1, 0] * Rs3 + T3[0, 0])
V1_3 = Vs3 * Zin3 / (Rs3 + Zin3); V2_3 = V1_3 * RL3 / (T3[0, 0] * RL3 + T3[0, 1])
check('P3 Z_in (ohm)', Zin3, 11 / 6, 1e-12); check('P3 V1 (V)', V1_3, 4.5517, 1e-3); check('P3 V2 (V)', V2_3, 1.6552, 1e-3)
check('P3 Z_out (ohm)', Zout3, 1.8, 1e-12)
Voc3 = Vs3 / (T3[0, 0] + T3[1, 0] * Rs3)
check('P3 open-circuit voltage at port 2 (V) = V_s/(A + C R_s)', Voc3, 12 / 5, 1e-12)
check('P3 max power into the load (W) = Voc^2/(4 Z_out)', Voc3 ** 2 / (4 * Zout3), 0.8, 1e-12)
# P3 cross-check on a circuit: build the ABCD from series/shunt blocks?  Use Z form instead
Z3 = Z_from_T(T3)
a_ = np.array([[Z3[0, 0] + Rs3, Z3[0, 1]], [Z3[1, 0], Z3[1, 1] + RL3]])
sol = np.linalg.solve(a_, [Vs3, 0.0])
check('P3 V2 from solving the Z equations (V)', -RL3 * sol[1], 1.6552, 1e-3)
# P4: cascade of two Ex1 T networks
T4 = measure(tnet, 1, 2)['T'].real
checkm('P4 cascade = [[25/9, 34],[17/72, 13/4]]', T4 @ T4, [[25 / 9, 34], [17 / 72, 3.25]]); check('P4 AD - BC', det(T4 @ T4), 1.0, 1e-12)
# P5: coupled inductors L1 = 0.4, L2 = 0.9, k = 0.5
L1p, L2p, kp = 0.4, 0.9, 0.5
Mp = kp * np.sqrt(L1p * L2p)
check('P5 M (H)', Mp, 0.3, 1e-12); check('P5 series aiding (H)', L1p + L2p + 2 * Mp, 1.9, 1e-12); check('P5 series opposing (H)', L1p + L2p - 2 * Mp, 0.7, 1e-12)
check('P5 energy for i1 = 2, i2 = 1 into the dots (J)', 0.5 * L1p * 4 + 0.5 * L2p * 1 + Mp * 2 * 1, 1.85, 1e-12)
check('P5 energy with i2 reversed (J)', 0.5 * L1p * 4 + 0.5 * L2p * 1 - Mp * 2 * 1, 0.65, 1e-12)

# ============================================================ 11. last numbers quoted in the PYQ solutions
V20 = Z20[1, 0] * 120 / (Z20[0, 0] + Rs20)
check('2020 Q15 Thevenin voltage at port 2 (V)', V20, 144.0, 1e-12); check('2020 Q15 P_max (W)', V20 ** 2 / (4 * 48), 108.0, 1e-12)
check('2020 Q15 wrong: z22 alone / ignoring R_s', Z20[1, 1] - Z20[0, 1] * Z20[1, 0] / Z20[0, 0], 30.0, 1e-12)
V23 = Z23[1, 0] * 120 / (Z23[0, 0] + Rs23)
check('2023 Q33 Thevenin voltage at port 2 (V)', V23, 80.0, 1e-9); check('2023 Q33 P_max (W)', V23 ** 2 / (4 * 80), 20.0, 1e-9)
# S21 = 2 V2/Vs (both ports terminated in Z0) versus the ABCD formula, on a real circuit (Ex 1 T network)
Z0c = 10.0
Vs_c, _ = solve([('V', 9, 0, 1.0, 'vs'), ('R', 9, 1, Z0c)] + tnet + [('R', 2, 0, Z0c)])
Tt = measure(tnet, 1, 2)['T'].real
check('S21 measured on a circuit = 2/(A + B/Z0 + C Z0 + D)', 2 * Vs_c[2], 2 / (Tt[0, 0] + Tt[0, 1] / Z0c + Tt[1, 0] * Z0c + Tt[1, 1]), 1e-12)
# ideal transformer in the h form: V1 = n V2, I1 = -I2/n  ->  h = [[0, n],[-n, 0]]; no Z or Y
nn = 2.0
hT = np.array([[0, nn], [-nn, 0.0]])
checkm('ideal transformer h = [[0, n],[-n, 0]] gives ABCD [[n,0],[0,1/n]]', T_from_h(hT), [[nn, 0], [0, 1 / nn]])

# ============================================================ 12. distractors quoted in the question solutions
checkm('Q8 wrong (C): shunt 2 ohm treated as 2 S', Tser(2.0) @ Tsh(2.0), [[5, 2], [2, 1]])
checkm('Q8 wrong (D): matrices added instead of multiplied', Tser(2.0) + Tsh(0.5), [[2, 2], [0.5, 2]])
check('Q14 wrong: squaring every element gives B', 3.0 ** 2, 9.0, 1e-12)
check('Q12 wrong: y11 = z11/det Z', Zq12[0, 0] / det(Zq12), 0.5, 1e-12); check('Q12 wrong: sign error in the determinant', Zq12[1, 1] / (Zq12[0, 0] * Zq12[1, 1] + Zq12[0, 1] * Zq12[1, 0]), 0.1875, 1e-12)
Zo_wrong = Zq[1, 1] - Zq[0, 1] * Zq[1, 0] / Zq[0, 0]; Vth_wrong = Zq[1, 0] * 50 / Zq[0, 0]
check('Q17 wrong: dropping R_s gives Z_out', Zo_wrong, 10.0, 1e-12); check('Q17 wrong: ... and V_th', Vth_wrong, 25.0, 1e-12)
check('Q17 wrong: ... and P_max (W)', Vth_wrong ** 2 / (4 * Zo_wrong), 15.625, 1e-9)
tsym2 = [('R', 1, 3, 3.0), ('R', 3, 2, 3.0), ('R', 3, 0, 5.0)]
Ps = measure(tsym2, 1, 2)
check('Q11 symmetric T network: A = D = 1.6', Ps['T'][0, 0].real, 1.6, 1e-12); check('Q11 ... B (ohm)', Ps['T'][0, 1].real, 7.8, 1e-12); check('Q11 ... C (S)', Ps['T'][1, 0].real, 0.2, 1e-12)

print('\nall Day 5 checks passed')
