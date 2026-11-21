"""Re-checks every number quoted in ../Day01_Circuit_Analysis_Fundamentals.md
and ../Day01_Conceptual_Questions.md.

Run:  python3 verify_day1.py
Uses mna.py (a small modified-nodal-analysis solver, numpy only).
Every check asserts the value printed in the notes AND, for past-year questions,
the value inside the official answer key.
"""
from mna import solve

k, m = 1e3, 1e-3
close = lambda a, b, tol=1e-6: abs(a - b) < tol


def check(name, got, want, tol=1e-6):
    assert close(got, want, tol), f'{name}: got {got}, expected {want}'
    print(f'ok  {name:<28} {got:.4f}')


# ---------------- worked examples ----------------
V, _ = solve([('V', 9, 0, 10, 'v'), ('R', 9, 1, 2), ('R', 1, 0, 4), ('R', 1, 2, 4), ('R', 2, 0, 6), ('I', 0, 2, 3)])
check('Ex1 V1', V[1], 8); check('Ex1 V2', V[2], 12)

V, _ = solve([('I', 0, 1, 2), ('R', 1, 0, 2), ('V', 2, 1, 4, 'x'), ('R', 2, 0, 6)])
check('Ex2 V1', V[1], 2); check('Ex2 V2', V[2], 6)

V, I = solve([('V', 1, 0, 24, 'a'), ('R', 1, 2, 2), ('R', 2, 0, 4), ('R', 2, 3, 2), ('V', 3, 0, 6, 'b')])
check('Ex3 I1', -I['a'], 6); check('Ex3 I2', I['b'], 3); check('Ex3 I(4ohm)', V[2] / 4, 3)

V, I = solve([('V', 1, 0, 20, 'a'), ('R', 1, 2, 2), ('I', 0, 2, 2), ('R', 2, 3, 4), ('R', 3, 0, 2)])
check('Ex4 I1', -I['a'], 1); check('Ex4 I2', V[3] / 2, 3)

V, _ = solve([('I', 0, 1, 6), ('R', 1, 0, 2), ('R', 1, 2, 4), ('R', 2, 0, 4), ('VCCS', 0, 2, 1, 0, 0.5)])
check('Ex5 V1', V[1], 16); check('Ex5 V2', V[2], 24)

V, _ = solve([('V', 9, 0, 12, 'a'), ('R', 9, 1, 3), ('R', 1, 0, 6), ('I', 0, 1, 2), ('R', 1, 2, 2), ('R', 2, 0, 4)])
check('Ex6 load current', V[2] / 4, 1.5)

V, _ = solve([('I', 0, 1, 1), ('R', 1, 2, 6), ('R', 1, 3, 3), ('R', 2, 3, 9), ('R', 2, 0, 3), ('R', 3, 0, 4.5)])
check('Ex7 R_ab', V[1], 4)

V, I = solve([('V', 1, 0, 12, 's'), ('R', 1, 2, 2), ('V', 2, 3, 0, 'sense'), ('CCVS', 3, 0, 'sense', 4, 'd')])
check('Ex8 i', I['sense'], 2)

# ---------------- previous-year questions (official keys in brackets) ----------------
V, I = solve([('V', 1, 0, 5, 'vs'), ('R', 1, 2, 2 * k), ('R', 2, 0, 2 * k), ('R', 2, 3, 2 * k), ('I', 0, 3, 1 * m)])
check('2022 Q13 I [B: 0.75 mA]', -I['vs'] / m, 0.75)

# right-hand network floats; 1e12 ohm to ground only gives the solver a reference
V, _ = solve([('V', 1, 0, 3, 'a'), ('R', 1, 2, 1), ('R', 2, 0, 2), ('R', 2, 3, 10), ('R', 3, 4, 1),
              ('R', 3, 5, 2), ('V', 5, 4, 3, 'b'), ('R', 4, 0, 1e12)])
check('2022 Q14 I [B: 0 A]', (V[2] - V[3]) / 10, 0, 1e-9)

V, _ = solve([('V', 3, 0, 2, 'v'), ('R', 1, 3, 2 * k), ('R', 1, 0, 2 * k), ('I', 0, 1, 1 * m),
              ('R', 1, 2, 1 * k), ('I', 1, 2, 1 * m), ('R', 2, 0, 200)])
assert 1.30 <= V[2] / 200 / m <= 1.40          # official key range
check('2023 Q32 i(mA) [1.30-1.40]', V[2] / 200 / m, 15 / 11)

V, _ = solve([('I', 0, 1, 5 * m), ('V', 1, 5, 0, 's0'), ('R', 5, 0, 1 * k), ('CCVS', 2, 1, 's0', 1000, 'd'),
              ('R', 2, 6, 1 * k), ('I', 6, 0, 2 * m), ('R', 2, 0, 1 * k)])
check('2024 Q31 Ix(mA) [2]', V[2] / 1e3 / m, 2)

check('2025 Q19 V_X [A: 20/3]', 8 - 2 * (8 - (9 - 3 * 1)) / 3, 20 / 3)

for E in (6, -6):
    V, _ = solve([('I', 0, 1, 1 * m), ('R', 1, 2, 1 * k), ('R', 2, 0, 1 * k), ('R', 1, 3, 1 * k),
                  ('R', 3, 0, 1 * k), ('V', 2, 3, E, 'b')])
    check(f'2026 Q30 Vo, E={E:+d} [1]', V[1], 1)

V, _ = solve([('R', 1, 2, 3), ('R', 1, 2, 6), ('R', 2, 0, 2), ('R', 2, 0, 2), ('R', 1, 0, 7), ('I', 0, 2, 5)])
check('2021 Q18 I [0.5]', V[1] / 7, 0.5)

V, _ = solve([('V', 1, 4, 4, 'v'), ('R', 4, 0, 1 * k), ('I', 2, 1, 6 * m), ('R', 1, 2, 1 * k),
              ('I', 2, 0, 2 * m), ('R', 1, 0, 1 * k)])
check('2021 Q19 Vo [1]', V[1], 1)

# ---------------- practice problems ----------------
V, _ = solve([('I', 0, 1, 4), ('R', 1, 0, 2), ('VCVS', 2, 1, 1, 0, 2, 'e'), ('R', 2, 0, 6)])
check('P1 V1', V[1], 4); check('P1 V2', V[2], 12)

V, _ = solve([('V', 1, 0, 15, 's'), ('R', 1, 2, 2), ('R', 2, 0, 3), ('R', 2, 3, 4), ('I', 3, 0, 2)])
check('P2 I(3ohm)', V[2] / 3, 2.2)

V, _ = solve([('I', 0, 1, 1), ('R', 1, 2, 9), ('R', 1, 3, 9), ('R', 2, 3, 9), ('R', 2, 0, 6), ('R', 3, 0, 3)])
check('P3 R_a,gnd', V[1], 6.6)

V, _ = solve([('I', 0, 1, 3), ('R', 1, 0, 4), ('R', 1, 2, 2), ('V', 3, 0, 18, 'b'), ('R', 3, 2, 6), ('R', 2, 0, 3)])
check('P4 I(load)', V[2] / 3, 2.5)

V, _ = solve([('V', 1, 0, 10, 's'), ('R', 1, 2, 2), ('R', 2, 0, 4), ('VCCS', 2, 0, 2, 0, 0.5)])
check('P5 V', V[2], 4)

# ---------------- conceptual questions (Day01_Conceptual_Questions.md) ----------------
def req(edges, a, b):
    """Resistance between nodes a and b of a network given as (node1, node2, R) edges."""
    names = {b: 0}
    for n1, n2, _ in edges:
        for n in (n1, n2):
            names.setdefault(n, len(names))
    els = [('R', names[n1], names[n2], R) for n1, n2, R in edges]
    els.append(('I', 0, names[a], 1.0))
    V, _ = solve(els)
    return V[names[a]]


# Q4: 12 V source, 2 ohm, 4 V source in one loop (power balance)
V, I = solve([('V', 1, 0, 12, 'a'), ('R', 1, 2, 2), ('V', 2, 0, 4, 'b')])
i_loop = (V[1] - V[2]) / 2
check('Q4 loop current', i_loop, 4)
check('Q4 12 V source absorbs (-48 = delivers 48)', 12 * I['a'], -48)
check('Q4 4 V source absorbs', 4 * I['b'], 16)
check('Q4 resistor absorbs', i_loop ** 2 * 2, 32)
check('Q4 total absorbed', 12 * I['a'] + 4 * I['b'] + i_loop ** 2 * 2, 0)

# Q6: cube, R = 12 ohm per edge (vertices are 3-bit numbers, edges join vertices differing in one bit)
cube = [(u, u ^ (1 << bit), 12.0) for u in range(8) for bit in range(3) if u < u ^ (1 << bit)]
check('Q6 body diagonal', req(cube, 0, 7), 10)          # 5R/6
check('Q6 face diagonal (aside)', req(cube, 0, 3), 9)    # 3R/4
check('Q6 adjacent corners (aside)', req(cube, 0, 1), 7)  # 7R/12

# Q8: reverse-engineering nodal equations
V, _ = solve([('I', 0, 1, 3), ('R', 1, 0, 2), ('R', 1, 2, 4), ('R', 2, 0, 4)])
check('Q8 V1', V[1], 4.8); check('Q8 V2', V[2], 2.4)
G = [[1 / 2 + 1 / 4, -1 / 4], [-1 / 4, 1 / 4 + 1 / 4]]
assert G == [[0.75, -0.25], [-0.25, 0.5]]
check('Q8 R(node1-ref) = 1/(G11-|G12|)', 1 / (G[0][0] + G[0][1]), 2)

# Q11: supermesh with the current-source arrow pointing DOWN
V, I = solve([('V', 1, 0, 20, 'a'), ('R', 1, 2, 2), ('I', 2, 0, 2), ('R', 2, 3, 4), ('R', 3, 0, 2)])
check('Q11 I2', V[3] / 2, 2); check('Q11 I1', -I['a'], 4)

# Q12: counting
assert 13 - 8 + 1 - 2 == 4 and 8 - 1 - 1 == 6
print('ok  Q12 mesh 4 / nodal 6')

# Q13: series resistor with an ideal current source
for R in (1 * k, 5 * k):
    V, I = solve([('V', 1, 0, 10, 'v'), ('R', 1, 2, 2 * k), ('R', 2, 0, 3 * k), ('I', 2, 3, 2 * m), ('R', 3, 0, R)])
    check(f'Q13 V_X (R={R / k:g}k)', V[2], 3.6)
    check(f'Q13 I(3k) mA (R={R / k:g}k)', V[2] / (3 * k) / m, 1.2)
    check(f'Q13 10 V source mW (R={R / k:g}k)', -10 * I['v'] / m, 32)
    check(f'Q13 V across I-source (R={R / k:g}k)', V[2] - V[3], 3.6 - 2e-3 * R)
    check(f'Q13 power in R mW (R={R / k:g}k)', (2e-3) ** 2 * R / m, 4e-6 * R / m)

# Q15: CCVS with v = -3 i
V, I = solve([('V', 1, 0, 12, 's'), ('R', 1, 2, 5), ('V', 2, 3, 0, 'sense'), ('CCVS', 3, 0, 'sense', -3, 'd')])
i = I['sense']
check('Q15 i', i, 6)
check('Q15 CCVS absorbs', (-3 * i) * i, -108)
check('Q15 12 V source delivers', 12 * i, 72)
check('Q15 resistor absorbs', 5 * i ** 2, 180)

# Q16 / Q17: source transformation (Thevenin 12 V + 3 ohm vs Norton 4 A || 3 ohm)
def thev(RL):
    V, I = solve([('V', 1, 0, 12, 'v'), ('R', 1, 2, 3), ('R', 2, 0, RL)])
    return dict(vt=V[2], it=V[2] / RL, p_src=-12 * I['v'], i_r=(V[1] - V[2]) / 3, p_r=((V[1] - V[2]) / 3) ** 2 * 3)

def nort(RL):
    V, _ = solve([('I', 0, 2, 4), ('R', 2, 0, 3), ('R', 2, 0, RL)])
    return dict(vt=V[2], it=V[2] / RL, p_src=4 * V[2], i_r=V[2] / 3, p_r=V[2] ** 2 / 3)

check('Q16 open: Thevenin R power', thev(1e12)['p_r'], 0, 1e-6)
check('Q16 open: Norton R power', nort(1e12)['p_r'], 48, 1e-3)
for RL in (1.0, 6.0, 20.0):
    t, n = thev(RL), nort(RL)
    check(f'Q16 terminal V equal (RL={RL:g})', t['vt'], n['vt']); check(f'Q16 terminal I equal (RL={RL:g})', t['it'], n['it'])
t, n = thev(6.0), nort(6.0)
check('Q16 RL=6 Thevenin source power', t['p_src'], 16); check('Q16 RL=6 Norton source power', n['p_src'], 32)
check('Q16 RL=6 current in 3 ohm (Thevenin)', t['i_r'], 4 / 3); check('Q16 RL=6 current in 3 ohm (Norton)', n['i_r'], 8 / 3)
check('Q17 power in original 3 ohm [5.32-5.34]', t['p_r'], 16 / 3)
assert 5.32 <= t['p_r'] <= 5.34
check('Q17 wrong (Norton-picture) value', n['p_r'], 64 / 3)

# Q18: star 2, 3, 6 ohm -> delta 18 (opposite the 2 ohm arm), 12, 6
star = [(1, 'o', 2.0), (2, 'o', 3.0), (3, 'o', 6.0)]
delta = [(2, 3, 18.0), (3, 1, 12.0), (1, 2, 6.0)]
for (a, b) in ((1, 2), (2, 3), (3, 1)):
    check(f'Q18 star vs delta R({a},{b})', req(star, a, b), req(delta, a, b))
check('Q18 delta opposite terminal 1', (2 * 3 + 3 * 6 + 6 * 2) / 2, 18)

# Q19: delta with R_a removed (R_a -> infinity) is a star with R1 = 0, R2 = R_c, R3 = R_b
Rb, Rc, Ra = 4.0, 6.0, 1e9
S = Ra + Rb + Rc
check('Q19 R1 -> 0', Rb * Rc / S, 0, 1e-6)
check('Q19 R2 -> R_c', Rc * Ra / S, Rc, 1e-6)
check('Q19 R3 -> R_b', Ra * Rb / S, Rb, 1e-6)
delta = [(3, 1, Rb), (1, 2, Rc)]                              # R_a simply absent
star = [(1, 'o', 1e-6), (2, 'o', Rc), (3, 'o', Rb)]           # R1 ~ 0 (1 micro-ohm keeps the solver well conditioned)
for (x, y) in ((1, 2), (2, 3), (3, 1)):
    check(f'Q19 delta vs star R({x},{y})', req(delta + [(2, 3, 1e12)], x, y), req(star, x, y), 1e-5)

# Q20: balanced bridge, detector value irrelevant
for Rd in (1.0, 100.0, 1e12):
    bridge = [('a', 'c', 6.0), ('a', 'd', 3.0), ('c', 'b', 12.0), ('d', 'b', 6.0), ('c', 'd', Rd)]
    check(f'Q20 R_ab (detector {Rd:g} ohm)', req(bridge, 'a', 'b'), 6, 1e-6)

# detector replaced by a wire: nodes c and d merged -> (6 || 3) + (12 || 6)
check('Q20 R_ab (detector shorted)', req([('a', 'c', 6.0), ('a', 'c', 3.0), ('c', 'b', 12.0), ('c', 'b', 6.0)], 'a', 'b'), 6)

print('\nall checks passed')
