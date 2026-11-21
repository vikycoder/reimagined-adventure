"""Regenerates every circuit figure in ../figures (needs: pip install schemdraw matplotlib)."""
import schemdraw
import schemdraw.elements as e
schemdraw.use('matplotlib')
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures') + os.sep


def new():
    d = schemdraw.Drawing(show=False)
    d.config(fontsize=13, unit=3)
    return d


def save(d, name):
    d.save(OUT + name + '.png', dpi=110, transparent=False)


def loop(d, x, y, text, cw=True):
    d.add(e.LoopArrow(direction='cw' if cw else 'ccw', width=0.9, height=0.9)
          .at((x, y)).anchor('center').label(text, loc='center', fontsize=12))


# ---------- passive sign convention
d = new()
d.add(e.Line().right(1))
d.add(e.Resistor().right().label(('+', 'v', '−'), loc='bottom').label('element', loc='top'))
d.add(e.Line().right(1))
d.add(e.CurrentLabelInline(direction='in').at(d.elements[0]).label('i'))
save(d, 'passive_sign')

# ---------- Ex1: basic nodal
d = new()
vs = d.add(e.SourceV().up().label('10 V'))
d.add(e.Resistor().right().label('2 Ω'))
d.add(e.Dot().label('V₁', loc='top'))
d.push(); d.add(e.Resistor().down().label('4 Ω', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Resistor().right().label('4 Ω'))
d.add(e.Dot().label('V₂', loc='top'))
d.push(); d.add(e.Resistor().down().label('6 Ω', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right())
d.add(e.SourceI().down().reverse().label('3 A', loc='bottom'))
d.add(e.Line().left().tox(vs.start))
d.add(e.Ground().at((vs.start[0] + 6, vs.start[1])))
save(d, 'ex1_nodal')

# ---------- Ex2: supernode
d = new()
isrc = d.add(e.SourceI().up().label('2 A'))
d.add(e.Line().right())
n1 = d.add(e.Dot().label('V₁', loc='top'))
d.push(); d.add(e.Resistor().down().label('2 Ω', loc='bottom')); d.add(e.Dot()); d.pop()
vx = d.add(e.SourceV().right().label('4 V', loc='top', ofst=0.6))
n2 = d.add(e.Dot().label('V₂', loc='top'))
d.add(e.Resistor().down().label('6 Ω', loc='bottom'))
d.add(e.Line().left().tox(isrc.start))
d.add(e.Ground().at((isrc.start[0] + 3, isrc.start[1])))
d.add(e.EncircleBox([n1, vx, n2], padx=0.45, pady=0.35).linestyle('--').color('#d62728')
      .label('supernode', loc='top', color='#d62728', fontsize=11))
save(d, 'ex2_supernode')

# ---------- Ex3: mesh
d = new()
v1 = d.add(e.SourceV().up().label('24 V'))
d.add(e.Resistor().right().label('2 Ω'))
d.push(); d.add(e.Resistor().down().label('4 Ω', loc='top')); d.pop()
d.add(e.Resistor().right().label('2 Ω'))
d.add(e.SourceV().down().reverse().label('6 V', loc='bottom'))
d.add(e.Line().left().tox(v1.start))
loop(d, 1.45, 1.5, 'I₁'); loop(d, 4.55, 1.5, 'I₂')
save(d, 'ex3_mesh')

# ---------- Ex4: supermesh
d = new()
v1 = d.add(e.SourceV().up().label('20 V'))
d.add(e.Resistor().right().label('2 Ω'))
d.push(); d.add(e.SourceI().down().reverse().label('2 A', loc='bottom')); d.pop()
d.add(e.Resistor().right().label('4 Ω'))
d.add(e.Resistor().down().label('2 Ω', loc='bottom'))
d.add(e.Line().left().tox(v1.start))
loop(d, 1.4, 1.5, 'I₁'); loop(d, 4.95, 1.5, 'I₂')
save(d, 'ex4_supermesh')

# ---------- Ex5: VCCS (nodal with dependent source)
d = new()
isrc = d.add(e.SourceI().up().label('6 A'))
d.add(e.Line().right())
d.add(e.Dot().label('V₁', loc='top'))
d.push(); d.add(e.Resistor().down().label(('+', 'vₓ', '−'), loc='bottom').label('2 Ω', loc='top')); d.pop()
d.add(e.Resistor().right().label('4 Ω'))
d.add(e.Dot().label('V₂', loc='top'))
d.push(); d.add(e.Resistor().down().label('4 Ω', loc='bottom')); d.pop()
d.add(e.Line().right())
d.add(e.SourceControlledI().down().reverse().label('0.5 vₓ', loc='bottom'))
d.add(e.Line().left().tox(isrc.start))
d.add(e.Ground().at((isrc.start[0] + 3, isrc.start[1])))
save(d, 'ex5_vccs')

# ---------- Ex6: source transformation (original circuit)
d = new()
vs = d.add(e.SourceV().up().label('12 V'))
d.add(e.Resistor().right().label('3 Ω'))
d.add(e.Dot().label('A', loc='top'))
d.push(); d.add(e.Resistor().down().label('6 Ω', loc='bottom')); d.pop()
d.add(e.Line().right())
d.push(); d.add(e.SourceI().down().reverse().label('2 A', loc='bottom')); d.pop()
d.add(e.Resistor().right().label('2 Ω'))
d.add(e.Dot().label('B', loc='top'))
d.add(e.Resistor().down().label('4 Ω  (load)', loc='bottom'))
d.add(e.Line().left().tox(vs.start))
save(d, 'ex6_source_transform')

# ---------- Ex7: bridge needing delta-wye
d = new()
a, c, dd, b = (3, 6), (0, 3), (6, 3), (3, 0)
d.add(e.Dot().at(a).label('a', loc='top'))
d.add(e.Dot().at(b).label('b', loc='bottom'))
d.add(e.Dot().at(c).label('c', loc='left'))
d.add(e.Dot().at(dd).label('d', loc='right'))
d.add(e.Resistor().endpoints(a, c).label('6 Ω', loc='top'))
d.add(e.Resistor().endpoints(a, dd).label('3 Ω', loc='bottom'))
d.add(e.Resistor().endpoints(c, dd).label('9 Ω', loc='top'))
d.add(e.Resistor().endpoints(c, b).label('3 Ω', loc='bottom'))
d.add(e.Resistor().endpoints(dd, b).label('4.5 Ω', loc='top'))
save(d, 'ex7_bridge')

# ---------- Delta and Wye generic
d = new()
p1, p2, p3 = (0, 0), (5, 0), (2.5, 4.33)
for p, t, loc in ((p1, '1', 'left'), (p2, '2', 'right'), (p3, '3', 'top')):
    d.add(e.Dot().at(p).label(t, loc=loc))
d.add(e.Resistor().endpoints(p1, p2).label('$R_c$', loc='bottom'))
d.add(e.Resistor().endpoints(p2, p3).label('$R_a$', loc='bottom'))
d.add(e.Resistor().endpoints(p3, p1).label('$R_b$', loc='bottom'))
d.add(e.Label().at((2.5, -1.4)).label('Δ (delta): $R_a$ is opposite terminal 1, etc.'))
q1, q2, q3, o = (8, 0), (13, 0), (10.5, 4.33), (10.5, 1.44)
for p, t, loc in ((q1, '1', 'left'), (q2, '2', 'right'), (q3, '3', 'top')):
    d.add(e.Dot().at(p).label(t, loc=loc))
d.add(e.Resistor().endpoints(q1, o).label('$R_1$', loc='bottom'))
d.add(e.Resistor().endpoints(q2, o).label('$R_2$', loc='top'))
d.add(e.Resistor().endpoints(q3, o).label('$R_3$', loc='bottom'))
d.add(e.Dot().at(o))
d.add(e.Label().at((10.5, -1.4)).label('Y (star): $R_1$ touches terminal 1, etc.'))
save(d, 'delta_wye')

# ---------- Ex8: CCVS in a single loop
d = new()
v1 = d.add(e.SourceV().up().label('12 V'))
d.add(e.Resistor().right().label('2 Ω'))
r = d.elements[-1]
d.add(e.CurrentLabelInline(direction='in').at(r).label('i'))
d.add(e.SourceControlledV().down().reverse().label('4 i', loc='bottom'))
d.add(e.Line().left().tox(v1.start))
save(d, 'ex8_ccvs')


# ================= practice problems =================
# P1: dependent voltage source forming a supernode
d = new()
isrc = d.add(e.SourceI().up().label('4 A'))
d.add(e.Line().right())
n1 = d.add(e.Dot().label('V₁', loc='top'))
d.push(); d.add(e.Resistor().down().label('2 Ω', loc='bottom')); d.add(e.Dot()); d.pop()
dv = d.add(e.SourceControlledV().right().label('2V₁', loc='top', ofst=0.6))
n2 = d.add(e.Dot().label('V₂', loc='top'))
d.add(e.Resistor().down().label('6 Ω', loc='bottom'))
d.add(e.Line().left().tox(isrc.start))
d.add(e.Ground().at((isrc.start[0] + 3, isrc.start[1])))
save(d, 'p1_dep_supernode')

# P2: mesh with a current source in an outer branch
d = new()
v1 = d.add(e.SourceV().up().label('15 V'))
d.add(e.Resistor().right().label('2 Ω'))
d.push(); d.add(e.Resistor().down().label('3 Ω', loc='top')); d.pop()
d.add(e.Resistor().right().label('4 Ω'))
d.add(e.SourceI().down().label('2 A', loc='bottom'))
d.add(e.Line().left().tox(v1.start))
save(d, 'p2_mesh_cs')

# P3: balanced delta feeding a ladder
d = new()
A, C, D = (0, 0), (4, 2.2), (4, -2.2)
d.add(e.Line().endpoints((-1.5, 0), A))
d.add(e.Dot().at((-1.5, 0)).label('a', loc='left'))
d.add(e.Dot().at(A))
d.add(e.Resistor().endpoints(A, C).label('9 Ω', loc='top'))
d.add(e.Resistor().endpoints(A, D).label('9 Ω', loc='bottom'))
d.add(e.Resistor().endpoints(C, D).label('9 Ω', loc='bottom'))
d.add(e.Dot().at(C)); d.add(e.Dot().at(D))
d.add(e.Resistor().endpoints(C, (7.5, 2.2)).label('6 Ω', loc='top'))
d.add(e.Resistor().endpoints(D, (7.5, -2.2)).label('3 Ω', loc='bottom'))
d.add(e.Line().endpoints((7.5, 2.2), (7.5, -2.2)))
d.add(e.Ground().at((7.5, 0)))
save(d, 'p3_delta')

# P4: sources on both ends, load in the middle
d = new()
i1 = d.add(e.SourceI().up().label('3 A'))
d.add(e.Line().right())
d.add(e.Dot())
d.push(); d.add(e.Resistor().down().label('4 Ω', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Resistor().right().label('2 Ω'))
d.add(e.Dot().label('V₂', loc='top'))
d.push(); d.add(e.Resistor().down().label('3 Ω (load)', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Resistor().right().label('6 Ω'))
d.add(e.SourceV().down().reverse().label('18 V', loc='bottom'))
d.add(e.Line().left().tox(i1.start))
save(d, 'p4_mixed')

# P5: self-controlled dependent source
d = new()
vs = d.add(e.SourceV().up().label('10 V'))
d.add(e.Resistor().right().label('2 Ω'))
d.add(e.Dot().label('V', loc='top'))
d.push(); d.add(e.Resistor().down().label('4 Ω', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right())
d.add(e.SourceControlledI().down().label('0.5 V', loc='bottom'))
d.add(e.Line().left().tox(vs.start))
save(d, 'p5_selfctrl')
print('done')
