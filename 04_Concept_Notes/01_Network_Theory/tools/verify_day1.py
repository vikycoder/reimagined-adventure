"""Re-checks every number quoted in ../Day01_Circuit_Analysis_Fundamentals.md.

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

print('\nall checks passed')
