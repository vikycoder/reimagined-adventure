"""Regenerates every Day 3 figure in ../figures (prefix d03_).   Needs: schemdraw matplotlib numpy pillow"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))

import numpy as np
import schemdraw.elements as e
from fig_helpers import COLORS, Figs

f = Figs(os.path.join(HERE, '..', 'figures'))
OHM, MU = '\u03a9', '\u03bc'

# ------------------------------------------------------------------ first-order response with tau markers
fig, (a1, a2) = f.plot((9.4, 3.7), ncols=2)
t = np.linspace(0, 5.5, 400)
a1.plot(t, 1 - np.exp(-t), color=COLORS[0])
a1.plot([0, 1], [0, 1], '--', color='gray', lw=1.3)                          # tangent at t = 0 reaches the final value at t = tau
for n, lab in ((1, '63.2%'), (2, '86.5%'), (3, '95.0%'), (4, '98.2%'), (5, '99.3%')):
    a1.plot([n], [1 - np.exp(-n)], 'o', color=COLORS[1]); a1.text(n + 0.07, 1 - np.exp(-n) - 0.09, lab, fontsize=8.5)
a1.set_xlabel('t / \u03c4'); a1.set_ylabel('x(t) \u2212 x(0\u207a)  as a fraction of  x(\u221e) \u2212 x(0\u207a)')
a1.set_title('Charging / step response', fontsize=11); a1.set_ylim(0, 1.08)
a1.annotate('tangent at t = 0\nhits the final value at t = \u03c4', (0.5, 0.5), (1.5, 0.22), arrowprops=dict(arrowstyle='->'), fontsize=9)
a2.plot(t, np.exp(-t), color=COLORS[0])
for n, lab in ((1, '36.8%'), (2, '13.5%'), (3, '5.0%'), (4, '1.8%'), (5, '0.7%')):
    a2.plot([n], [np.exp(-n)], 'o', color=COLORS[1]); a2.text(n + 0.07, np.exp(-n) + 0.03, lab, fontsize=8.5)
a2.set_xlabel('t / \u03c4'); a2.set_title('Natural (source-free) response', fontsize=11); a2.set_ylim(0, 1.08)
f.savefig(fig, 'd03_first_order')

# ------------------------------------------------------------------ the 0+ / infinity replacement models
def models(kind):
    # panel 1: the real element, panel 2: model at 0+, panel 3: model at infinity
    d = f.new(); d.add(e.Dot(open=True).label('+', loc='left'))
    d.add(e.Line().right(0.5))
    if kind == 'C':
        d.add(e.Capacitor().down().label('C', loc='right'))
    else:
        d.add(e.Inductor().down().label('L', loc='right'))
    d.add(e.Line().left(0.5)); d.add(e.Dot(open=True).label('\u2212', loc='left'))
    f.panel(d, f'm{kind}1')
    d = f.new(); d.add(e.Dot(open=True).label('+', loc='left'))
    d.add(e.Line().right(0.5))
    if kind == 'C':
        d.add(e.SourceV().down().reverse().label('V\u2080', loc='right'))
    else:
        d.add(e.SourceI().down().label('I\u2080', loc='right'))
    d.add(e.Line().left(0.5)); d.add(e.Dot(open=True).label('\u2212', loc='left'))
    f.panel(d, f'm{kind}2')
    d = f.new(); d.add(e.Dot(open=True).label('+', loc='left'))
    if kind == 'C':
        d.add(e.Line().right(0.5)); d.add(e.Line().down(0.9)); d.add(e.Dot(open=True)); d.add(e.Dot(open=True).at((0.5, -2.1)))
        d.add(e.Line().at((0.5, -2.1)).down(0.9)); d.add(e.Line().left(0.5)); d.add(e.Dot(open=True).label('\u2212', loc='left'))
    else:
        d.add(e.Line().right(0.5)); d.add(e.Line().down(3)); d.add(e.Line().left(0.5)); d.add(e.Dot(open=True).label('\u2212', loc='left'))
    f.panel(d, f'm{kind}3')

models('C'); models('L')
f.hstack(['mC1', 'mC2', 'mC3'], 'd03_models_C',
         ['capacitor with\nv(0\u207b) = V\u2080', 'at t = 0\u207a:\nvoltage source V\u2080', 'at t \u2192 \u221e (DC):\nopen circuit'])
f.hstack(['mL1', 'mL2', 'mL3'], 'd03_models_L',
         ['inductor with\ni(0\u207b) = I\u2080', 'at t = 0\u207a:\ncurrent source I\u2080', 'at t \u2192 \u221e (DC):\nshort circuit'])

# ------------------------------------------------------------------ two capacitors and a switch
d = f.new()
c1 = d.add(e.Capacitor().up())
d.add(e.Label().at((-1.9, 2.0)).label('C\u2081 = 4 ' + MU + 'F', fontsize=12))
d.add(e.Label().at((-1.9, 1.2)).label('V\u2080 = 100 V', fontsize=12))
d.add(e.Switch(action='close').right().label('t = 0', loc='top'))
d.add(e.Resistor().right().label('R', loc='top'))
d.add(e.Capacitor().down())
d.add(e.Label().at((7.6, 1.6)).label('C\u2082 = 6 ' + MU + 'F', fontsize=12))
d.add(e.Label().at((7.6, 0.9)).label('0 V', fontsize=12))
d.add(e.Line().left().tox(c1.start))
f.save(d, 'd03_two_caps')

# ------------------------------------------------------------------ series / parallel RLC schematics (two panels)
d = f.new()
v = d.add(e.SourceV().up().label('V_s'))
d.add(e.Resistor().right().label('R', loc='top'))
d.add(e.Inductor().right().label('L', loc='top'))
d.add(e.Capacitor().down().label('C', loc='right'))
d.add(e.Line().left().tox(v.start))
f.panel(d, 'rlcs')
d = f.new()
i0 = d.add(e.SourceI().up().label('I_s'))
d.add(e.Line().right(1.2)); d.add(e.Dot())
d.push(); d.add(e.Resistor().down().label('R', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.2)); d.add(e.Dot())
d.push(); d.add(e.Inductor().down().label('L', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.2))
d.add(e.Capacitor().down().label('C', loc='right'))
d.add(e.Line().left().tox(i0.start))
f.panel(d, 'rlcp')
f.hstack(['rlcs', 'rlcp'], 'd03_series_parallel',
         ['SERIES RLC\n\u03b1 = R/(2L),   \u03c9\u2080 = 1/\u221a(LC)\nlarger R  \u2192  MORE damping',
          'PARALLEL RLC\n\u03b1 = 1/(2RC),   \u03c9\u2080 = 1/\u221a(LC)\nlarger R  \u2192  LESS damping'])

# ------------------------------------------------------------------ the three damping cases
fig, (a1, a2) = f.plot((9.6, 3.9), ncols=2, gridspec_kw={'width_ratios': [1.5, 1]})
L_, C_ = 1e-3, 1e-6
w0 = 1 / np.sqrt(L_ * C_)
tt = np.linspace(0, 400e-6, 4000)
for Rv, col, lab in ((20.0, COLORS[1], 'underdamped  R = 20 \u03a9  (\u03b6 = 0.32)'),
                     (2 * np.sqrt(L_ / C_), COLORS[2], 'critical  R = 63.2 \u03a9  (\u03b6 = 1)'),
                     (100.0, COLORS[0], 'overdamped  R = 100 \u03a9  (\u03b6 = 1.58)')):
    al = Rv / (2 * L_); z = al / w0
    if z < 1:
        wd = w0 * np.sqrt(1 - z * z); y = 1 - np.exp(-al * tt) * (np.cos(wd * tt) + al / wd * np.sin(wd * tt))
    elif abs(z - 1) < 1e-9:
        y = 1 - np.exp(-al * tt) * (1 + al * tt)
    else:
        r = np.sqrt(al ** 2 - w0 ** 2); s1, s2 = -al + r, -al - r
        y = 1 + (s2 * np.exp(s1 * tt) - s1 * np.exp(s2 * tt)) / (s1 - s2)
    a1.plot(tt / 1e-6, y, color=col, label=lab)
    roots = np.roots([1, 2 * al, w0 ** 2])
    a2.plot(roots.real / 1e3, roots.imag / 1e3, 'x', color=col, ms=9, mew=2.2)
a1.axhline(1, color='gray', lw=0.8); a1.set_xlabel('t (\u03bcs)'); a1.set_ylabel('v_C(t)  for a 1 V step')
a1.set_title('Step response (L = 1 mH, C = 1 \u03bcF)', fontsize=11); a1.legend(fontsize=8.2, frameon=False, loc='lower right')
a2.axhline(0, color='k', lw=0.8); a2.axvline(0, color='k', lw=0.8)
a2.set_xlabel('real part (10\u00b3 rad/s)'); a2.set_ylabel('imaginary part (10\u00b3 rad/s)'); a2.set_title('Poles in the s-plane', fontsize=11)
a2.set_xlim(-100, 10); a2.set_ylim(-40, 40)
f.savefig(fig, 'd03_rlc_cases')

# ------------------------------------------------------------------ s-domain models of C and L
d = f.new(); d.add(e.Dot(open=True).label('a', loc='left'))
d.add(e.Line().right(0.5)); d.add(e.RBox(w=1.0, h=0.55).down().label('1/sC', loc='right'))
d.add(e.SourceV().down().reverse().label('V\u2080/s', loc='right'))
d.add(e.Line().left(0.5)); d.add(e.Dot(open=True).label('b', loc='left'))
f.panel(d, 'sC')
d = f.new(); d.add(e.Dot(open=True).label('a', loc='left'))
d.add(e.Line().right(0.5)); d.add(e.RBox(w=1.0, h=0.55).down().label('sL', loc='right'))
d.add(e.SourceV().down().label('L I\u2080', loc='right'))
d.add(e.Line().left(0.5)); d.add(e.Dot(open=True).label('b', loc='left'))
f.panel(d, 'sL')
f.hstack(['sC', 'sL'], 'd03_s_models',
         ['capacitor with v(0\u207b) = V\u2080\nV = I/(sC) + V\u2080/s', 'inductor with i(0\u207b) = I\u2080\nV = sL\u00b7I \u2212 L I\u2080'])

# ------------------------------------------------------------------ PYQ: 0+ equivalent circuits (2021 Q28, 2023 Q44)
d = f.new()
vs = d.add(e.SourceV().up().label('10 V'))
d.add(e.Line().right(1.2)); d.add(e.Dot().label('v', loc='top'))
d.push(); d.add(e.Resistor().down().label('5 k' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.6))
d.add(e.SourceI().down().label('1 mA', loc='bottom'))
d.add(e.Line().left().tox(vs.start))
f.panel(d, 'z28')
d = f.new()
vs = d.add(e.SourceV().up().label('20 V'))
d.add(e.Line().right(1.2)); d.add(e.Dot().label('T', loc='top'))
d.push(); d.add(e.Resistor().down().label('25 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.6))
d.add(e.SourceI().down().label('0.2 A', loc='bottom'))
d.add(e.Line().left().tox(vs.start))
f.panel(d, 'z44')
f.hstack(['z28', 'z44'], 'd03_pyq_zero_plus',
         ['2021 Q28 at t = 0\u207a\nC \u2192 10 V,  L \u2192 1 mA', '2023 Q44 at t = 0\u207a\nC \u2192 20 V,  L \u2192 0.2 A'])

# ------------------------------------------------------------------ PYQ 2021 Q38
d = f.new()
vs = d.add(e.SourceV().up().label('5 V'))
r = d.add(e.Resistor().right().label(('+', 'V_R', '\u2212'), loc='top').label('250 ' + OHM, loc='bottom'))
d.add(e.Dot().label('N', loc='top'))
d.push(); d.add(e.SourceControlledI().down().label('V_R/500', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.4))
d.push(); d.add(e.Resistor().down().label('250 ' + OHM, loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Switch(action='close').right().label('t = 0', loc='top'))
d.add(e.Line().right(0.6))
d.add(e.Capacitor().down().label('0.6 ' + MU + 'F', loc='right'))
d.add(e.Line().left().tox(vs.start))
f.save(d, 'd03_pyq_2021q38')

# ------------------------------------------------------------------ PYQ 2021 Q47
d = f.new()
src = d.add(e.SourceI().up(3.6).label('1 A'))
d.add(e.Switch(action='close').right().label('t = 0', loc='top'))
d.add(e.Dot())
d.push(); d.add(e.Capacitor().down(3.6)); d.add(e.Dot()); d.pop()
d.add(e.Label().at((4.4, 1.8)).label('100 pF', fontsize=12))
d.add(e.Line().right(0.8))
d.add(e.MeterA().right())
d.add(e.Inductor().down(1.8))
d.add(e.Resistor().down(1.8))
d.add(e.Label().at((5.75, 2.7)).label('10 mH', fontsize=12))
d.add(e.Label().at((5.75, 0.9)).label('5 k' + OHM, fontsize=12))
d.add(e.Line().left().tox(src.start))
f.save(d, 'd03_pyq_2021q47')

# ------------------------------------------------------------------ PYQ 2024 Q49 and 2019 Q52 waveforms
dt = 1e-9
tg = np.arange(0, 16e-6, dt)
ph = tg % 8e-6
Vi = np.where(ph < 4e-6, -2 + 1e6 * ph, 2 - 1e6 * (ph - 4e-6))
V01 = np.empty_like(Vi); st = -10.0
for n, vi in enumerate(Vi):
    st = 10.0 if (vi * 100 + st * 10) / 110 > 0 else -10.0
    V01[n] = st
V02 = np.empty_like(Vi); y = 0.0
for n in range(len(Vi)):
    y = float(np.clip(y - 1e6 * V01[n] * dt, -10, 10)); V02[n] = y
fig, axs = f.plot((7.6, 5.6), nrows=3, sharex=True)
axs[0].plot(tg / 1e-6, Vi, color=COLORS[0]); axs[0].set_ylabel('V_i (V)')
axs[0].axhline(1, color='gray', ls=':', lw=1); axs[0].axhline(-1, color='gray', ls=':', lw=1)
axs[0].text(0.2, 1.15, 'Schmitt thresholds \u00b11 V', fontsize=8.5)
axs[1].plot(tg / 1e-6, V01, color=COLORS[1]); axs[1].set_ylabel('V_01 (V)')
axs[1].annotate('', (3.0, 0), (2.0, 0), arrowprops=dict(arrowstyle='<->')); axs[1].text(2.05, 2.5, 'delay\n1 \u03bcs', fontsize=8.5)
axs[2].plot(tg / 1e-6, V02, color=COLORS[2]); axs[2].set_ylabel('V_02 (V)'); axs[2].set_xlabel('t (\u03bcs)')
axs[2].text(0.2, -7.5, 'clipped at \u00b110 V for 2 \u03bcs per half-cycle:\na trapezoid, not a triangle', fontsize=8.5)
f.savefig(fig, 'd03_pyq_2024q49')

dt = 1e-6
tg = np.arange(0, 12e-3, dt)
Vs = np.where(tg % 4e-3 < 2e-3, 10.0, -10.0)
vc = np.empty_like(tg); v = 0.0; tau = 5e-3
for n, vsn in enumerate(Vs):
    if vsn > v:
        v += (vsn - v) * dt / tau
    vc[n] = v
fig, ax = f.plot((6.6, 3.3))
ax.plot(tg / 1e-3, Vs, color='gray', lw=1.3, label='V_s (square wave, 10 V)')
ax.plot(tg / 1e-3, vc, color=COLORS[0], label='V_c')
ax.plot([3], [vc[3000]], 'o', color=COLORS[1]); ax.annotate('3.3 V at t = 3 ms', (3, vc[3000]), (4.3, 1.2), arrowprops=dict(arrowstyle='->'), fontsize=9)
ax.set_xlabel('t (ms)'); ax.set_ylabel('volts'); ax.legend(fontsize=8.5, frameon=False, loc='upper center', bbox_to_anchor=(0.5, 1.22), ncol=2)
f.savefig(fig, 'd03_pyq_2019q52')

# ------------------------------------------------------------------ practice P2: coil with a resistor switched across it
d = f.new()
c = d.add(e.Inductor().up())
d.add(e.Label().at((1.7, 1.9)).label('L = 50 mH', fontsize=12))
d.add(e.Label().at((1.7, 1.2)).label('i = 2 A', fontsize=12))
d.add(e.Resistor().right().label('10 ' + OHM + ' (coil)', loc='top'))
d.add(e.Resistor().down().label('40 ' + OHM, loc='right'))
d.add(e.Line().left().tox(c.start))
f.save(d, 'd03_p2')

# ------------------------------------------------------------------ Q3: capacitor and battery in a loop
d = f.new()
b = d.add(e.SourceV().up().label('6 V'))
d.add(e.Switch(action='close').right().label('t = 0', loc='top'))
d.add(e.Resistor().right().label('3 ' + OHM, loc='top'))
d.add(e.Capacitor().down())
d.add(e.Label().at((5.55, 2.3)).label('+', fontsize=13))
d.add(e.Label().at((3.7, 1.7)).label('C:  v(0\u207b) = 3 V', fontsize=12))
d.add(e.Line().left().tox(b.start))
f.save(d, 'd03_q03_loop')

# ------------------------------------------------------------------ Q12: capacitor discharging through R and a Zener
d = f.new()
cz = d.add(e.Capacitor().up())
d.add(e.Label().at((3.0, 1.5)).label('10 ' + MU + 'F, v(0) = 10 V', fontsize=12))
d.add(e.Label().at((0.45, 2.4)).label('+', fontsize=13))
d.add(e.Switch(action='close').right().label('t = 0', loc='top'))
d.add(e.Resistor().right().label('10 k' + OHM, loc='top'))
d.add(e.Zener().down().reverse())
d.add(e.Label().at((4.3, 1.0)).label('Zener V_Z = 4 V', fontsize=12))
d.add(e.Line().left().tox(cz.start))
f.save(d, 'd03_q12_zener')

f.cleanup()
print('done')
