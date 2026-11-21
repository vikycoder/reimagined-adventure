"""Regenerates every Day 4 figure in ../figures (prefix d04_).   Needs: schemdraw matplotlib numpy pillow"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))

import matplotlib.pyplot as plt
import numpy as np
import schemdraw.elements as e
from fig_helpers import COLORS, Figs

f = Figs(os.path.join(HERE, '..', 'figures'))
OHM, MU = 'Ω', 'μ'

# ------------------------------------------------------------------ phasor diagram of the series RLC example
fig, ax = f.plot((5.2, 4.2))
VR, VL, VC = 8.0, 14.0, 8.0
ax.annotate('', (VR, 0), (0, 0), arrowprops=dict(arrowstyle='-|>', color=COLORS[0], lw=2.2))
ax.annotate('', (VR, VL), (VR, 0), arrowprops=dict(arrowstyle='-|>', color=COLORS[1], lw=2.2))
ax.annotate('', (VR + 0.7, VL - VC), (VR + 0.7, VL), arrowprops=dict(arrowstyle='-|>', color=COLORS[2], lw=2.2))
ax.plot([VR, VR + 0.7], [VL, VL], color='gray', lw=0.8, ls=':')
ax.annotate('', (VR, VL - VC), (0, 0), arrowprops=dict(arrowstyle='-|>', color='black', lw=2.6))
ax.text(VR / 2, -0.9, 'V_R = 8 V  (in phase with I)', ha='center', fontsize=9.5, color=COLORS[0])
ax.text(VR - 0.5, 11.6, 'V_L = 14 V\n(leads I by 90°)', fontsize=9.5, color=COLORS[1], va='center', ha='right')
ax.text(VR + 1.3, 10.5, 'V_C = 8 V\n(lags I by 90°)', fontsize=9.5, color=COLORS[2], va='center')
ax.text(2.0, 4.4, 'V_s = 10 V', fontsize=10.5, rotation=36.87, ha='center')
ax.text(3.2, 0.5, 'φ = 36.9°', fontsize=10)
ax.set_xlim(-1, 14); ax.set_ylim(-2, 16); ax.set_aspect('equal'); ax.grid(False)
ax.set_xlabel('real axis  (reference = current I)'); ax.set_ylabel('imaginary axis')
ax.set_title('R = 4 Ω, X_L = 7 Ω, X_C = 4 Ω, I = 2 A', fontsize=10.5)
f.savefig(fig, 'd04_phasor_rlc')

# ------------------------------------------------------------------ power triangle and power-factor correction
fig, (a1, a2) = f.plot((9.4, 3.8), ncols=2)
P, Q1, Q2 = 10.0, 7.5, 3.287
a1.annotate('', (P, 0), (0, 0), arrowprops=dict(arrowstyle='-|>', lw=2.2, color=COLORS[0]))
a1.annotate('', (P, Q1), (P, 0), arrowprops=dict(arrowstyle='-|>', lw=2.2, color=COLORS[1]))
a1.annotate('', (P, Q1), (0, 0), arrowprops=dict(arrowstyle='-|>', lw=2.6, color='black'))
a1.text(P / 2, -0.9, 'P = 10 kW (real power)', ha='center', fontsize=9.5)
a1.text(P + 0.2, Q1 / 2, 'Q = 7.5 kvar\n(inductive, Q > 0)', fontsize=9.5, va='center')
a1.text(4.6, 3.6, 'S = 12.5 kVA', rotation=36.9, fontsize=10, ha='center', va='bottom', rotation_mode='anchor')
a1.text(2.6, 0.5, 'φ', fontsize=11)
a1.set_xlim(-1, 17); a1.set_ylim(-2, 10.5); a1.set_aspect('equal'); a1.grid(False); a1.set_title('Power triangle (0.8 lagging)', fontsize=11)
a1.set_xticks([]); a1.set_yticks([])
a2.annotate('', (P, 0), (0, 0), arrowprops=dict(arrowstyle='-|>', lw=2.0, color=COLORS[0]))
a2.annotate('', (P, Q1), (0, 0), arrowprops=dict(arrowstyle='-|>', lw=2.2, color='gray'))
a2.annotate('', (P, Q2), (0, 0), arrowprops=dict(arrowstyle='-|>', lw=2.6, color='black'))
a2.annotate('', (P, Q2), (P, Q1), arrowprops=dict(arrowstyle='-|>', lw=2.2, color=COLORS[2]))
a2.text(P + 0.2, (Q1 + Q2) / 2, 'capacitor supplies\nQ_C = 4.21 kvar', fontsize=9.5, va='center', color=COLORS[2])
a2.text(4.6, 3.6, 'S₁ (before)', rotation=36.9, fontsize=9, color='gray', ha='center', va='bottom', rotation_mode='anchor')
a2.text(5.4, 1.55, 'S₂ (0.95 lagging)', rotation=18.2, fontsize=9, ha='center', va='top', rotation_mode='anchor')
a2.set_xlim(-1, 17); a2.set_ylim(-2, 10.5); a2.set_aspect('equal'); a2.grid(False); a2.set_xticks([]); a2.set_yticks([])
a2.set_title('Correction: P unchanged, Q reduced', fontsize=11)
f.savefig(fig, 'd04_power_triangle')

# ------------------------------------------------------------------ series resonance curves
fig, (a1, a2) = f.plot((9.6, 3.8), ncols=2)
x = np.linspace(0.5, 1.6, 2000)
for Q, col in ((2, COLORS[0]), (5, COLORS[2]), (10, COLORS[1])):
    Zr = 1 + 1j * Q * (x - 1 / x)                                  # Z / R for a series RLC
    a1.plot(x, 1 / abs(Zr), color=col, label=f'Q = {Q}')
    a2.plot(x, -np.degrees(np.angle(Zr)), color=col)
a1.axhline(1 / np.sqrt(2), color='gray', ls='--', lw=1); a1.text(0.52, 0.73, '0.707 (half power)', fontsize=8.5)
a1.set_xlabel('ω / ω₀'); a1.set_ylabel('|I| / I_max'); a1.legend(frameon=False, fontsize=9)
a1.set_title('Current in a series RLC (voltage source)', fontsize=10.5)
a2.axhline(0, color='k', lw=0.8); a2.axhline(45, color='gray', ls='--', lw=0.8); a2.axhline(-45, color='gray', ls='--', lw=0.8)
a2.set_xlabel('ω / ω₀'); a2.set_ylabel('phase of I relative to V (deg)'); a2.set_ylim(-95, 95)
a2.set_title('Below ω₀ the circuit is capacitive (I leads)', fontsize=10.5)
f.savefig(fig, 'd04_resonance_curves')

# ------------------------------------------------------------------ series, parallel and practical-tank schematics
d = f.new()
v = d.add(e.SourceV().up().label('V_s'))
d.add(e.Resistor().right().label('R', loc='top'))
d.add(e.Inductor().right().label('L', loc='top'))
d.add(e.Capacitor().down().label('C', loc='bottom'))
d.add(e.Line().left().tox(v.start))
f.panel(d, 'rs')
d = f.new()
i0 = d.add(e.SourceI().up().label('I_s'))
d.add(e.Line().right(1.2)); d.add(e.Dot())
d.push(); d.add(e.Resistor().down().label('R', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.2)); d.add(e.Dot())
d.push(); d.add(e.Inductor().down().label('L', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.2))
d.add(e.Capacitor().down().label('C', loc='bottom'))
d.add(e.Line().left().tox(i0.start))
f.panel(d, 'rp')
d = f.new()
i0 = d.add(e.SourceI().up().label('I_s'))
d.add(e.Line().right(1.2)); d.add(e.Dot())
d.push(); d.add(e.Inductor().down(1.8)); d.add(e.Resistor().down(1.8)); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.6))
d.add(e.Capacitor().down(3.6).label('C', loc='bottom'))
d.add(e.Label().at((1.9, 3.0)).label('L', fontsize=12)); d.add(e.Label().at((1.9, 1.2)).label('R_L', fontsize=12))
d.add(e.Line().left().tox(i0.start))
f.panel(d, 'rt')
f.hstack(['rs', 'rp', 'rt'], 'd04_series_parallel_res',
         ['series: Z = R + j(ωL − 1/ωC)\nZ is MINIMUM at resonance', 'parallel (ideal): Y = G + j(ωC − 1/ωL)\nZ is MAXIMUM at resonance',
          'practical tank (coil with R_L)\nZ_d = L/(C R_L) at unity pf'])

# ------------------------------------------------------------------ impedance loci
fig, axs = f.plot((11.2, 3.7), ncols=3)
w = np.logspace(-3, 3, 4000)
a = axs[0]
a.plot([2, 2], [0, 4], color=COLORS[0], label='R + jωL  (series RL)'); a.plot([2, 2], [0, -4], color=COLORS[1], label='R − j/ωC  (series RC)')
a.annotate('', (2, 3.4), (2, 2.8), arrowprops=dict(arrowstyle='-|>', color=COLORS[0])); a.annotate('', (2, -2.8), (2, -3.4), arrowprops=dict(arrowstyle='-|>', color=COLORS[1]))
a.text(2.15, 2.0, 'ω ↑', color=COLORS[0], fontsize=9); a.text(2.15, -2.3, 'ω ↓', color=COLORS[1], fontsize=9)
a.axhline(0, color='k', lw=0.8); a.axvline(0, color='k', lw=0.8); a.set_xlim(-0.5, 5); a.set_ylim(-4.5, 4.5)
a.set_xlabel('Re Z'); a.set_ylabel('Im Z'); a.set_title('Series: a vertical line', fontsize=10.5); a.legend(frameon=False, fontsize=8, loc='center right')
a = axs[1]
Rr = 4.0
zc = Rr / (1 + 1j * w * Rr * 1.0); zl = Rr / (1 + 1 / (1j * w * Rr * 1.0))
a.plot(zc.real, zc.imag, color=COLORS[1], label='R ∥ C'); a.plot(zl.real, zl.imag, color=COLORS[0], label='R ∥ L')
a.axhline(0, color='k', lw=0.8); a.axvline(0, color='k', lw=0.8); a.set_aspect('equal'); a.set_xlim(-0.5, 4.8); a.set_ylim(-2.6, 2.6)
a.text(0.3, -1.9, 'ω = ∞', fontsize=8.5); a.text(3.3, -0.4, 'ω = 0', fontsize=8.5); a.legend(frameon=False, fontsize=8.5, loc='lower center', bbox_to_anchor=(0.5, -0.42), ncol=2)
a.set_xlabel('Re Z'); a.set_title('Parallel: a semicircle of diameter R', fontsize=10.5)
a = axs[2]
z = 2 + 3 / (1 + 1j * w * 3)
a.plot(z.real, -z.imag, color=COLORS[0])
a.plot([5, 2], [0, 0], 'o', color=COLORS[1])
a.annotate('ω = 0:  R₁ + R₂ = 5', (5, 0), (3.2, 0.5), arrowprops=dict(arrowstyle='->'), fontsize=8.5)
a.annotate('ω → ∞:  R₁ = 2', (2, 0), (0.1, 0.9), arrowprops=dict(arrowstyle='->'), fontsize=8.5)
a.text(1.9, 1.85, 'peak: −Im Z = R₂/2 = 1.5', fontsize=8.5)
a.axhline(0, color='k', lw=0.8); a.set_xlim(0, 5.6); a.set_ylim(-0.2, 2.1); a.set_xlabel('Re Z (kΩ)'); a.set_ylabel('−Im Z (kΩ)')
a.set_title('2022 Q38:  R₁ + (R₂ ∥ C)', fontsize=10.5)
f.savefig(fig, 'd04_locus')

# ------------------------------------------------------------------ PYQ 2019 Q30: outer R triangle, inner C star
d = f.new()
T, BL, BR, O = (4, 5.4), (0, 0), (8, 0), (4, 1.9)
src = d.add(e.SourceV().at((-2.5, 0)).up(5.4).label('v(t)'))
d.add(e.Line().at((-2.5, 5.4)).to(T)); d.add(e.Line().at((-2.5, 0)).to(BL))
for p in (T, BL, BR, O):
    d.add(e.Dot().at(p))
d.add(e.Resistor().endpoints(BL, T))
d.add(e.Resistor().endpoints(T, BR))
d.add(e.Resistor().endpoints(BL, BR))
d.add(e.Capacitor().endpoints(T, O))
d.add(e.Capacitor().endpoints(BL, O))
d.add(e.Capacitor().endpoints(BR, O))
for xy, t in (((1.5, 3.0), 'R'), ((6.5, 3.0), 'R'), ((4.0, -0.55), 'R'), ((4.55, 3.7), 'C'), ((2.2, 1.65), 'C'), ((5.8, 1.65), 'C'), ((-1.0, 5.75), 'i(t) \u2192')):
    d.add(e.Label().at(xy).label(t, fontsize=12))
f.save(d, 'd04_pyq_2019q30')

# ------------------------------------------------------------------ PYQ 2020 Q28
d = f.new()
s1 = d.add(e.SourceV().at((0, 3)).up(3))
d.add(e.Line().at((0, 6)).to((8, 6)))
s2 = d.add(e.SourceV().at((0, 3)).down(3))
d.add(e.Line().at((0, 0)).to((8, 0)))
d.add(e.Resistor().at((4, 6)).down(3))
d.add(e.Resistor().at((4, 3)).down(3))
d.add(e.Resistor().at((8, 6)).down(6))
d.add(e.Line().at((0, 3)).to((4, 3)))
for p in ((0, 3), (0, 6), (0, 0), (4, 3), (4, 6), (4, 0), (8, 6), (8, 0)):
    d.add(e.Dot().at(p))
for xy, t, fs in (((-1.95, 4.5), '120\u2220\u221290\u00b0 V', 11), ((-1.95, 1.5), '120\u2220\u221230\u00b0 V', 11), ((4.7, 4.5), 'Z', 12), ((4.7, 1.5), 'Z', 12),
                  ((9.6, 3.0), 'Z = 80 \u2212 j35 ' + OHM, 11), ((2.0, 3.45), 'I \u2192', 12), ((0.0, 6.4), 'T', 11), ((0.0, -0.45), 'B', 11), ((-0.4, 3.35), 'M', 11), ((4.35, 3.35), 'm', 11)):
    d.add(e.Label().at(xy).label(t, fontsize=fs))
f.save(d, 'd04_pyq_2020q28')

# ------------------------------------------------------------------ PYQ 2022 Q39: lag or lead?
fig, ax = f.plot((6.2, 3.3))
t = np.linspace(0, 4 * np.pi, 2000)
ax.plot(t, np.sin(t - np.pi / 4) / np.sqrt(2), color=COLORS[0], label='inductor: I = sin(t − π/4)/√2   (lags V)')
ax.plot(t, np.sin(t + np.pi / 4) / np.sqrt(2), color=COLORS[1], ls='--', label='capacitor: I = sin(t + π/4)/√2   (leads V)')
ax.axvline(np.pi / 4, color='gray', ls=':'); ax.text(np.pi / 4 + 0.08, -0.62, 't = π/4', fontsize=9)
ax.axhline(0, color='k', lw=0.8); ax.set_xlim(0, 4 * np.pi); ax.set_ylim(-0.95, 0.95)
ax.set_xlabel('t (s)'); ax.set_ylabel('I(t) (A)'); ax.legend(frameon=False, fontsize=8, loc='upper right', bbox_to_anchor=(1.0, 1.28))
f.savefig(fig, 'd04_pyq_2022q39')

# ------------------------------------------------------------------ PYQ 2026 Q31: source across an LC-R parallel circuit
d = f.new()
vs = d.add(e.SourceV().up().label('v_i(t)', loc='left'))
d.add(e.Line().right(1.5)); d.add(e.Dot())
d.push(); d.add(e.Capacitor().down().label('1 ' + MU + 'F', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.4)); d.add(e.Dot())
d.push(); d.add(e.Inductor().down().label('2.2 mH', loc='bottom')); d.add(e.Dot()); d.pop()
d.add(e.Line().right(2.4))
d.add(e.Resistor().down().label('1 k' + OHM, loc='bottom'))
d.add(e.Line().left().tox(vs.start))
f.save(d, 'd04_pyq_2026q31')

# ------------------------------------------------------------------ PYQ 2026 Q39: circuit and phasor diagram
d = f.new()
d.add(e.Dot(open=True).at((-0.8, 0)).label('+', loc='left'))
d.add(e.Line().at((-0.8, 0)).to((4.0, 0)))
d.add(e.Resistor().at((1.2, 0)).down(1.8))
d.add(e.Capacitor().at((1.2, -1.8)).down(1.8))
d.add(e.Resistor().at((4.0, 0)).down(1.8))
d.add(e.Inductor().at((4.0, -1.8)).down(1.8))
d.add(e.Line().at((-0.8, -3.6)).to((4.0, -3.6)))
d.add(e.Dot(open=True).at((-0.8, -3.6)).label('\u2212', loc='left'))
for p in ((1.2, 0), (4.0, 0), (1.2, -3.6), (4.0, -3.6)):
    d.add(e.Dot().at(p))
for xy, t in (((2.0, -0.9), 'R_C'), ((1.9, -2.7), 'C'), ((4.8, -0.9), 'R_L'), ((4.7, -2.7), 'L')):
    d.add(e.Label().at(xy).label(t, fontsize=12))
f.panel(d, 'c39')
fig, ax = f.plot((3.4, 2.6)); ax.axis('off')
ax.annotate('', (1.0, 0.75), (0, 0), arrowprops=dict(arrowstyle='-|>', lw=2)); ax.text(1.03, 0.78, 'I_C')
ax.annotate('', (1.0, -0.75), (0, 0), arrowprops=dict(arrowstyle='-|>', lw=2)); ax.text(1.03, -0.88, 'I_L')
ax.annotate('', (1.25, 0), (0, 0), arrowprops=dict(arrowstyle='-', lw=1.5, ls='--')); ax.text(1.28, -0.05, 'V')
ax.text(0.45, 0.2, '\u03b8\u2081', fontsize=12); ax.text(0.45, -0.32, '\u03b8\u2082', fontsize=12)
ax.set_xlim(-0.1, 1.6); ax.set_ylim(-1.1, 1.1)
f.panel_fig(fig, 'p39')
f.hstack(['c39', 'p39'], 'd04_pyq_2026q39', ['parallel branches: (R_C, C) and (R_L, L)', '\u03b8\u2081 + \u03b8\u2082 = 90\u00b0  at 159.15 kHz'])

# ------------------------------------------------------------------ Q17: practical tank circuit
d = f.new()
i0 = d.add(e.SourceI().up(3.6).label('I_s'))
d.add(e.Line().right(1.2)); d.add(e.Dot())
d.push(); d.add(e.Inductor().down(1.8)); d.add(e.Resistor().down(1.8)); d.add(e.Dot()); d.pop()
d.add(e.Line().right(3.4))
d.add(e.Capacitor().down(3.6))
d.add(e.Label().at((5.7, 1.8)).label('C = 2 ' + MU + 'F', fontsize=11))
d.add(e.Label().at((2.7, 2.7)).label('L = 5 mH', fontsize=11)); d.add(e.Label().at((2.7, 0.9)).label('R_L = 40 ' + OHM, fontsize=11))
d.add(e.Line().left().tox(i0.start))
f.save(d, 'd04_q17_tank')

f.cleanup()
print('done')
