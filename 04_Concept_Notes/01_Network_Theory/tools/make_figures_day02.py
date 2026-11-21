"""Regenerates every Day 2 figure in ../figures (prefix d02_).   Needs: schemdraw matplotlib numpy pillow"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))

import numpy as np
import schemdraw.elements as e
from fig_helpers import COLORS, Figs

f = Figs(os.path.join(HERE, '..', 'figures'))
OHM = 'Ω'

# ---------------------------------------------------------------- V-I line and the maximum-power rectangle
fig, ax = f.plot((5.6, 3.8))
Voc, Isc = 10.0, 5.0                      # V_th = 10 V, R_th = 2 ohm
i = np.linspace(0, Isc, 50)
ax.plot(i, Voc - (Voc / Isc) * i, color=COLORS[0], label='linear one-port:  v = V_th − R_th·i')
ax.add_patch(__import__('matplotlib.patches', fromlist=['Rectangle']).Rectangle((0, 0), Isc / 2, Voc / 2, fill=True, alpha=0.15, color=COLORS[1]))
ax.plot([Isc / 2], [Voc / 2], 'o', color=COLORS[1])
ax.annotate('max power point\nv = V_th/2,  i = I_N/2', (Isc / 2, Voc / 2), (2.9, 7.3), arrowprops=dict(arrowstyle='->'), fontsize=10)
ax.plot([0], [Voc], 'o', color='black'); ax.text(0.1, Voc + 0.3, 'open circuit  (i = 0, v = V_th)', fontsize=10)
ax.plot([Isc], [0], 'o', color='black'); ax.text(Isc - 0.1, 0.5, 'short circuit\n(v = 0, i = I_N)', fontsize=10, ha='right')
ax.set_xlim(0, Isc * 1.08); ax.set_ylim(0, Voc * 1.15)
ax.set_xlabel('terminal current i (A)'); ax.set_ylabel('terminal voltage v (V)')
f.savefig(fig, 'd02_vi_line')

# ---------------------------------------------------------------- power curves
fig, (a1, a2) = f.plot((9.2, 3.6), ncols=2)
x = np.logspace(-1.3, 1.3, 400)
a1.plot(x, 4 * x / (1 + x) ** 2, color=COLORS[0], label='load power  P/P_max')
a1.plot(x, x / (1 + x), color=COLORS[2], ls='--', label='efficiency  η')
a1.axvline(1, color='gray', lw=1)
a1.set_xscale('log'); a1.set_xlabel('R_L / R_th  (R_th fixed, R_L varied)'); a1.set_ylim(0, 1.05)
a1.legend(fontsize=9, frameon=False, loc='upper left')
a1.set_title('Vary the load', fontsize=11)
y = np.linspace(0, 4, 400)                  # R_th / R_L
a2.plot(y, 1 / (1 + y) ** 2, color=COLORS[1])
a2.set_xlabel('R_th / R_L  (R_L fixed, source resistance varied)'); a2.set_ylabel('P / P(R_th = 0)')
a2.set_ylim(0, 1.05); a2.set_title('Vary the source resistance', fontsize=11)
a2.annotate('largest at R_th = 0,\nnot at R_th = R_L', (0, 1), (1.4, 0.75), arrowprops=dict(arrowstyle='->'), fontsize=10)
f.savefig(fig, 'd02_power_curves')

# ---------------------------------------------------------------- Thevenin / Norton equivalents (three panels)
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(3.3, 2.7)); ax.axis('off'); ax.set_xlim(0, 4.4); ax.set_ylim(0, 3.2)
ax.add_patch(Rectangle((0.2, 0.2), 2.6, 2.8, fill=False, lw=2.2))
ax.text(1.5, 1.6, 'linear\nnetwork\n(R, dependent\nand independent\nsources)', ha='center', va='center', fontsize=10.5)
for y, t in ((2.6, 'a'), (0.6, 'b')):
    ax.plot([2.8, 3.8], [y, y], 'k', lw=2.2); ax.plot([3.8], [y], 'o', mfc='white', mec='k', ms=7); ax.text(4.0, y, t, va='center', fontsize=13)
f.panel_fig(fig, 'eq_box')

d = f.new()
v = d.add(e.SourceV().up().label('V_th'))
d.add(e.Resistor().right().label('R_th', loc='top'))
d.add(e.Dot(open=True).label('a', loc='right'))
xr = d.here[0]
d.add(e.Line().at(v.start).to((xr, v.start[1])))
d.add(e.Dot(open=True).at((xr, v.start[1])).label('b', loc='right'))
f.panel(d, 'eq_thev')

d = f.new()
i0 = d.add(e.SourceI().up().label('I_N'))
d.add(e.Line().right(1.5))
d.add(e.Dot())
d.push(); d.add(e.Resistor().down().label('R_N', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(1.5))
d.add(e.Dot(open=True).label('a', loc='right'))
xr = d.here[0]
d.add(e.Line().at(i0.start).to((xr, i0.start[1])))
d.add(e.Dot(open=True).at((xr, i0.start[1])).label('b', loc='right'))
f.panel(d, 'eq_nort')
f.hstack(['eq_box', 'eq_thev', 'eq_nort'], 'd02_equivalents',
         ['any linear one-port', 'Thevenin form\nV_th = V_oc,  R_th = V_oc / I_sc', 'Norton form\nI_N = I_sc,  R_N = R_th'])

# ---------------------------------------------------------------- Ex 1: superposition (three panels)
def ex1(v_on, i_on):
    d = f.new()
    if v_on:
        d.add(e.SourceV().up().label('12 V'))
    else:
        d.add(e.Line().up())
    d.add(e.Resistor().right().label('2 ' + OHM))
    d.add(e.Dot().label('X', loc='top'))
    d.push(); d.add(e.Resistor().down().label('6 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
    d.add(e.Line().right(2))
    if i_on:
        d.add(e.SourceI().down().reverse().label('3 A', loc='bottom'))
    else:
        y0 = d.here[1]; xr = d.here[0]
        d.add(e.Line().down(1.1)); d.add(e.Dot(open=True))
        d.add(e.Dot(open=True).at((xr, y0 - 1.9))); d.add(e.Line().at((xr, y0 - 1.9)).down(1.1))
    d.add(e.Line().left().tox(0))
    return d

f.panel(ex1(True, True), 'ex1a'); f.panel(ex1(True, False), 'ex1b'); f.panel(ex1(False, True), 'ex1c')
f.hstack(['ex1a', 'ex1b', 'ex1c'], 'd02_ex1_super',
         ['(a) both sources', "(b) 12 V alone (3 A opened)\nV_X' = 9 V", '(c) 3 A alone (12 V shorted)\nV_X" = 4.5 V'])

# ---------------------------------------------------------------- Ex 2: superposition with a CCVS
d = f.new()
v = d.add(e.SourceV().up().label('10 V'))
r = d.add(e.Resistor().right().label('2 ' + OHM))
d.add(e.CurrentLabelInline(direction='in').at(r).label('i'))
d.add(e.SourceControlledV().right().label('3 i', loc='top'))
d.add(e.Dot().label('X', loc='top'))
d.push(); d.add(e.Resistor().down().label('4 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2))
d.add(e.SourceI().down().reverse().label('2 A', loc='bottom'))
d.add(e.Line().left().tox(v.start))
f.save(d, 'd02_ex2_dep')

# ---------------------------------------------------------------- Ex 3: two sources, find the equivalent at a-b
d = f.new()
v = d.add(e.SourceV().up().label('24 V'))
d.add(e.Resistor().right().label('6 ' + OHM))
d.add(e.Dot())
d.push(); d.add(e.Resistor().down().label('12 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2))
d.push(); d.add(e.SourceI().down().reverse().label('2 A', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2))
d.add(e.Dot(open=True).label('a', loc='right'))
d.add(e.Line().at((v.start[0], v.start[1])).to((7.0, v.start[1])))
d.add(e.Dot(open=True).at((7.0, v.start[1])).label('b', loc='right'))
f.save(d, 'd02_ex3_circuit')

# ---------------------------------------------------------------- Ex 4: 6 ohm in parallel with a CCCS
d = f.new()
d.add(e.Dot(open=True).label('a', loc='left'))
d.add(e.Line().right(1.5))
d.add(e.Dot())
d.push()
r = d.add(e.Resistor().down().label('6 ' + OHM, loc='bottom'))
d.add(e.CurrentLabelInline(direction='in').at(r).label('i'))
d.add(e.Dot())
d.pop()
d.add(e.Line().right(2.2))
d.add(e.SourceControlledI().down().label('β i', loc='bottom'))
d.add(e.Line().left().tox(0.0))
d.add(e.Dot(open=True).label('b', loc='left'))
f.save(d, 'd02_ex4_oneport')

# ---------------------------------------------------------------- Ex 5: ladder for the unit-output method
d = f.new()
v = d.add(e.SourceV().up().label('V_s'))
d.add(e.Resistor().right().label('1 ' + OHM))
d.add(e.Dot().label('A', loc='top'))
d.push(); d.add(e.Resistor().down().label('3 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Resistor().right().label('1 ' + OHM))
d.add(e.Dot().label('B', loc='top'))
d.push(); d.add(e.Resistor().down().label('4 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Resistor().right().label('1 ' + OHM))
d.add(e.Dot().label('C', loc='top'))
d.add(e.Resistor().down().label('R_L = 3 ' + OHM, loc='bottom'))
d.add(e.Line().left().tox(v.start))
f.save(d, 'd02_ex5_ladder')

# ---------------------------------------------------------------- PYQ 2020 Q9
d = f.new()
d.add(e.SourceI().up().label('1 A'))
d.add(e.Line().right(1.5))
d.add(e.Dot().label('A', loc='top'))
d.push(); d.add(e.Resistor().down().label('1 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.SourceV().right().label('2 V', loc='top'))
d.add(e.Resistor().right().label('2 ' + OHM))
d.add(e.Dot().label('B', loc='top'))
d.push(); d.add(e.SourceI().down().reverse().label('2 A', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.6))
d.push(); d.add(e.Resistor().down().label('2 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Resistor().right().label('4 ' + OHM))
d.add(e.Dot(open=True).label('+', loc='top'))
xr = d.here[0]
d.add(e.Line().at((0, 0)).to((xr, 0)))
d.add(e.Dot(open=True).at((xr, 0)).label('−', loc='bottom'))
d.add(e.Label().at((xr + 0.6, 1.5)).label('V_TH', fontsize=13))
f.save(d, 'd02_pyq_2020q9')

# ---------------------------------------------------------------- PYQ 2024 Q62
d = f.new()
v = d.add(e.SourceV().up().label('50 V'))
d.add(e.Dot())
d.push()
d.add(e.Line().up(1.6))
d.add(e.Resistor().right().label('2 ' + OHM))
d.add(e.Resistor().right().label(('−', 'V_x', '+'), loc='top').label('3 ' + OHM, loc='bottom'))
top_right = d.here
d.pop()
d.add(e.SourceControlledV().right().label('V_x', loc='bottom'))
d.add(e.Resistor().right().label('2 ' + OHM, loc='bottom'))
d.add(e.Dot().label('N', loc='right'))
nx, ny = d.here
d.add(e.Line().at(top_right).to((nx, top_right[1])))
d.add(e.Line().at((nx, top_right[1])).to((nx, ny)))
d.add(e.Resistor().down().at((nx, ny)).label('R_L', loc='bottom'))
d.add(e.Line().at((nx, 0)).to((0, 0)))
f.save(d, 'd02_pyq_2024q62')

# ---------------------------------------------------------------- PYQ 2022 Q54: the measured line and the load line
fig, ax = f.plot((5.6, 3.9))
xs = np.linspace(-8, 22, 100)
ax.plot(xs, 5 - 0.25 * xs, color=COLORS[0], label='network at port 2:  V₂ = 5 − 250·(−I₂)')
xl = np.linspace(-8, 3, 50)
ax.plot(xl, 10 + 1.0 * xl, color=COLORS[1], label='load (c):  V₂ = 10 + 1000·(−I₂)')
ax.plot([0, 4], [5, 4], 'ko'); ax.text(0.3, 5.35, '(0 mA, 5 V)', fontsize=9); ax.text(4.5, 4.45, '(4 mA, 4 V)', fontsize=9)
ax.plot([-4], [6], 'o', ms=9, color='#2ca02c')
ax.annotate('operating point\n−I₂ = −4 mA  →  I₂ = +4 mA', (-4, 6), (3, 8.6), arrowprops=dict(arrowstyle='->'), fontsize=10)
ax.axhline(0, color='k', lw=0.8); ax.axvline(0, color='k', lw=0.8)
ax.set_xlim(-8, 22); ax.set_ylim(-0.5, 12)
ax.set_xlabel('−I₂ (mA)  (current leaving port 2)'); ax.set_ylabel('V₂ (V)')
ax.legend(fontsize=8.5, frameon=False, loc='upper right')
f.savefig(fig, 'd02_pyq_2022q54')

# ---------------------------------------------------------------- PYQ 2019 Q4: reciprocity
def tnet(left_src, right_src, lab):
    d = f.new()
    if left_src:
        d.add(e.SourceV().up().label('5 V'))
    else:
        d.add(e.MeterA().up().label(lab))
    d.add(e.Resistor().right().label('1 ' + OHM))
    d.add(e.Dot())
    d.push(); d.add(e.Resistor().down().label('R', loc='bottom')); d.add(e.Dot()); d.pop()
    d.add(e.Resistor().right().label('2 ' + OHM))
    if right_src:
        d.add(e.SourceV().down().reverse().label('5 V', loc='bottom'))
    else:
        d.add(e.MeterA().down().label(lab, loc='bottom'))
    d.add(e.Line().left().tox(0))
    return d

f.panel(tnet(True, False, '1 A'), 't19a'); f.panel(tnet(False, True, '?'), 't19b')
f.hstack(['t19a', 't19b'], 'd02_pyq_2019q4',
         ['(a) 5 V at port 1, port 2 shorted\nthrough an ammeter: 1 A', '(b) 5 V at port 2, port 1 shorted\nthrough an ammeter: ?'])

# ---------------------------------------------------------------- Practice P1: three sources at one node
d = f.new()
v = d.add(e.SourceV().up().label('24 V'))
d.add(e.Resistor().right().label('4 ' + OHM))
d.add(e.Dot().label('X', loc='top'))
d.push(); d.add(e.Resistor().down().label('12 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.6))
d.add(e.Dot())
d.push(); d.add(e.SourceI().down().reverse().label('6 A', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Resistor().right().label('6 ' + OHM))
d.add(e.SourceV().down().reverse().label('12 V', loc='bottom'))
d.add(e.Line().left().tox(v.start))
f.save(d, 'd02_p1')

# ---------------------------------------------------------------- Practice P2: one-port with a CCCS
d = f.new()
v = d.add(e.SourceV().up().label('12 V'))
r = d.add(e.Resistor().right().label('2 ' + OHM))
d.add(e.CurrentLabelInline(direction='in').at(r).label('i'))
d.add(e.Dot())
d.push(); d.add(e.Resistor().down().label('4 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.4))
d.push(); d.add(e.SourceControlledI().down().label('0.5 i', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(1.5))
d.add(e.Dot(open=True).label('a', loc='right'))
xr = d.here[0]
d.add(e.Line().at(v.start).to((xr, v.start[1])))
d.add(e.Dot(open=True).at((xr, v.start[1])).label('b', loc='right'))
f.save(d, 'd02_p2')

# ---------------------------------------------------------------- Q9: one-port with a VCCS that injects current
d = f.new()
d.add(e.Dot(open=True).label('a', loc='left'))
d.add(e.Line().right(1.5))
d.add(e.Dot())
d.push(); d.add(e.Resistor().down().label('4 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2))
d.push(); d.add(e.SourceControlledI().down().reverse().label('0.5 v', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().left().tox(0.0).at((d.here[0], d.here[1] - 3)))
d.add(e.Dot(open=True).at((0.0, -3.0)).label('b', loc='left'))
d.add(e.Label().at((-0.55, -0.5)).label('+', fontsize=13))
d.add(e.Label().at((-0.55, -2.5)).label('−', fontsize=13))
d.add(e.Label().at((-0.9, -1.5)).label('v', fontsize=13))
f.save(d, 'd02_q09_negres')

# ---------------------------------------------------------------- Q10: Thevenin source feeding a nonlinear resistor
d = f.new()
v = d.add(e.SourceV().up().label('6 V'))
d.add(e.Resistor().right().label('1 k' + OHM))
d.add(e.ResistorVar().down().label('nonlinear\ni = 10⁻³ v²', loc='bottom'))
d.add(e.Line().left().tox(v.start))
f.save(d, 'd02_q10_nonlinear')

# ---------------------------------------------------------------- Q11: unbalanced bridge with a detector
d = f.new()
a, c, dd, b = (3, 6), (0, 3), (6, 3), (3, 0)
d.add(e.Dot().at(a).label('a', loc='top'))
d.add(e.Dot().at(b).label('b', loc='bottom'))
d.add(e.Dot().at(c).label('c', loc='left'))
d.add(e.Dot().at(dd).label('d', loc='right'))
d.add(e.Resistor().endpoints(a, c).label('6 ' + OHM, loc='top'))
d.add(e.Resistor().endpoints(a, dd).label('3 ' + OHM, loc='bottom'))
d.add(e.Resistor().endpoints(c, dd).label('detector', loc='top'))
d.add(e.Resistor().endpoints(c, b).label('12 ' + OHM, loc='bottom'))
d.add(e.Resistor().endpoints(dd, b).label('9 ' + OHM, loc='top'))
d.add(e.Line().at(a).to((9.5, 6)))
d.add(e.SourceV().at((9.5, 6)).down(3).reverse().label('18 V', loc='bottom'))
d.add(e.Line().at((9.5, 3)).to((9.5, 0)))
d.add(e.Line().at((9.5, 0)).to(b))
f.save(d, 'd02_q11_bridge')

f.cleanup()
print('done')
