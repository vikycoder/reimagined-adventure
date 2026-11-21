"""Regenerates every Day 7 figure in ../figures (prefix d07_).   Needs: matplotlib numpy"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from fig_helpers import COLORS, Figs

f = Figs(os.path.join(HERE, '..', 'figures'))
C0, C1, C2 = COLORS[0], COLORS[1], COLORS[2]


def style(ax, xlim, ylim, xticks=None, yticks=None, title=None):
    ax.axhline(0, color='k', lw=0.8); ax.axvline(0, color='k', lw=0.8)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    if xticks is not None: ax.set_xticks(xticks)
    if yticks is not None: ax.set_yticks(yticks)
    if title: ax.set_title(title, fontsize=11)


# ------------------------------------------------------------------ standard signals
fig, axs = plt.subplots(1, 5, figsize=(13.5, 2.7))
t = np.linspace(-3, 3, 2000)
ax = axs[0]; ax.plot(t, np.where(t >= 0, 1, 0), color=C0); ax.plot(0, 1, 'o', color=C0, ms=4); style(ax, (-3, 3), (-0.4, 1.5), [-2, 0, 2], [0, 1], 'unit step u(t)')
ax = axs[1]; ax.plot(t, np.maximum(t, 0), color=C0); style(ax, (-3, 3), (-0.5, 3.2), [-2, 0, 2], [0, 1, 2, 3], 'ramp r(t) = t u(t)')
ax = axs[2]; ax.annotate('', (0, 1.0), (0, 0), arrowprops=dict(arrowstyle='-|>', lw=2.4, color=C1)); ax.text(0.15, 0.55, '1', color=C1, fontsize=12)
ax.plot([-3, 3], [0, 0], color=COLORS[0], lw=2); style(ax, (-3, 3), (-0.4, 1.5), [-2, 0, 2], [], 'impulse δ(t): area 1')
ax = axs[3]; ax.plot(t, np.where(np.abs(t) < 0.5, 1, 0), color=C0); style(ax, (-3, 3), (-0.4, 1.5), [-2, -0.5, 0.5, 2], [0, 1], 'rect(t)')
ax = axs[4]; ax.plot(t, np.sinc(t), color=C0); style(ax, (-3, 3), (-0.4, 1.2), [-3, -2, -1, 0, 1, 2, 3], [0, 1], 'sinc(t) = sin(πt)/(πt)')
for a in axs: a.set_xlabel('t')
fig.tight_layout(); f.savefig(fig, 'd07_standard_signals')

# ------------------------------------------------------------------ classification: energy, power, neither
fig, axs = plt.subplots(1, 3, figsize=(11, 2.7))
t = np.linspace(-2, 6, 3000)
ax = axs[0]; ax.plot(t, np.exp(-t) * (t >= 0), color=C0); style(ax, (-2, 6), (-0.3, 1.3), [0, 2, 4, 6], [0, 1], 'energy signal: e⁻ᵗu(t),  E = 1/2')
ax = axs[1]; ax.plot(t, np.cos(2 * np.pi * 0.5 * t), color=C1); style(ax, (-2, 6), (-1.6, 1.6), [0, 2, 4, 6], [-1, 0, 1], 'power signal: cos(πt),  P = 1/2')
ax = axs[2]; ax.plot(t, np.maximum(t, 0), color=C2); style(ax, (-2, 6), (-0.5, 6.5), [0, 2, 4, 6], [0, 2, 4, 6], 'neither: r(t) = t u(t)')
for a in axs: a.set_xlabel('t')
fig.tight_layout(); f.savefig(fig, 'd07_energy_power')

# ------------------------------------------------------------------ even and odd parts of e^{-t} u(t)
fig, axs = plt.subplots(1, 3, figsize=(11, 2.8))
t = np.linspace(-4, 4, 4001)
Hs = np.where(t > 0, 1.0, np.where(t == 0, 0.5, 0.0))        # step with u(0) = 1/2 so the even part has no spike at 0
x = np.exp(-t) * Hs; xr = np.exp(t) * (1 - Hs)
xe = 0.5 * (x + xr); xo = 0.5 * (x - xr)
for ax, y, ttl, col in ((axs[0], x, 'x(t) = e⁻ᵗ u(t)', C0), (axs[1], xe, 'even part  ½e^(−|t|)', C1), (axs[2], xo, 'odd part  ½ sgn(t) e^(−|t|)', C2)):
    ax.plot(t, y, color=col); style(ax, (-4, 4), (-0.7, 1.2), [-4, -2, 0, 2, 4], [-0.5, 0, 0.5, 1], ttl); ax.set_xlabel('t')
fig.tight_layout(); f.savefig(fig, 'd07_even_odd')

# ------------------------------------------------------------------ operations on the time axis
xf = lambda t: np.where((t >= 0) & (t <= 1), t, np.where((t > 1) & (t <= 2), 1.0, 0.0))
fig, axs = plt.subplots(2, 3, figsize=(11.5, 5.0))
t = np.linspace(-4, 5, 9001)
panels = [(xf(t), 'x(t)'), (xf(t - 1), 'x(t − 1)   (delay by 1)'), (xf(-t), 'x(−t)   (reverse)'),
          (xf(2 * t), 'x(2t)   (compress by 2)'), (xf(t / 2), 'x(t/2)   (stretch by 2)'), (xf(-2 * t + 1), 'x(−2t + 1) = x(−2(t − ½))')]
for ax, (y, ttl) in zip(axs.ravel(), panels):
    ax.plot(t, y, color=C0); style(ax, (-4, 5), (-0.3, 1.4), [-4, -2, 0, 2, 4], [0, 1], ttl); ax.set_xlabel('t')
fig.tight_layout(); f.savefig(fig, 'd07_time_ops')

# ------------------------------------------------------------------ discrete-time operations
fig, axs = plt.subplots(1, 5, figsize=(14, 2.7))
n = np.arange(-6, 7)
xd = lambda n: np.select([n == 0, n == 1, n == 2, n == 3], [1.0, 2.0, 3.0, 1.0], 0.0)
sig = [(xd(n), 'x[n]'), (xd(n - 2), 'x[n − 2]'), (xd(-n), 'x[−n]'), (xd(2 * n), 'x[2n]  (loses samples)'), (np.where(n % 2 == 0, xd(n // 2), 0.0), 'x[n/2]  (zeros inserted)')]
for ax, (y, ttl) in zip(axs, sig):
    ax.stem(n, y, linefmt=C0, markerfmt='o', basefmt='k-'); ax.set_ylim(-0.3, 3.6); ax.set_xlim(-6.5, 6.5); ax.set_title(ttl, fontsize=11); ax.set_xlabel('n')
fig.tight_layout(); f.savefig(fig, 'd07_dt_ops')

# ------------------------------------------------------------------ 2019 Q21: periods of a sum of sinusoids
fig, ax = plt.subplots(figsize=(10.5, 3.3))
t = np.linspace(-1, 26, 6000)
ft = 1 + 2 * np.cos(np.pi * t) + 3 * np.sin(2 * np.pi * t / 3) + 4 * np.cos(np.pi * t / 2 + np.pi / 4)
ax.plot(t, ft, color=C0, lw=1.8)
for k in (0, 12, 24):
    ax.axvline(k, color=C1, ls='--', lw=1.2)
ax.annotate('', (12, 10.6), (0, 10.6), arrowprops=dict(arrowstyle='<->', color=C1)); ax.text(6, 10.9, 'T = 12 s', ha='center', color=C1)
ax.text(25.8, 11.4, 'component periods 2 s, 3 s, 4 s  →  LCM = 12 s', ha='right', fontsize=10)
ax.set_xlim(-1, 26); ax.set_ylim(-8, 12.5); ax.axhline(0, color='k', lw=0.6); ax.set_xlabel('t (s)'); ax.set_ylabel('f(t)')
f.savefig(fig, 'd07_pyq_2019q21')

# ------------------------------------------------------------------ 2020 Q5: running maximum of |x[n]|
fig, axs = plt.subplots(1, 4, figsize=(14.5, 2.9))
n = np.arange(-3, 10)
imp = (n == 0).astype(float)
axs[0].stem(n, imp, linefmt=C0, markerfmt='o', basefmt='k-'); axs[0].set_title('input δ[n]', fontsize=11)
rm = lambda v: np.maximum.accumulate(np.abs(v))
axs[1].stem(n, rm(imp), linefmt=C1, markerfmt='o', basefmt='k-'); axs[1].set_title('output = u[n]', fontsize=11)
xx = np.array([0, 0, 0, 1, -2, 1, 0, 3, -1, 0, 1, 0, 0], dtype=float)
axs[2].stem(n, xx, linefmt=C0, markerfmt='o', basefmt='k-'); axs[2].set_title('another input x[n]', fontsize=11)
axs[3].stem(n, rm(xx), linefmt=C1, markerfmt='o', basefmt='k-'); axs[3].set_title('y[n] = max |x[k]|, k ≤ n', fontsize=11)
for a in axs: a.set_xlabel('n'); a.set_xlim(-3.5, 9.5)
for a in (axs[0], axs[1]): a.set_ylim(-0.3, 1.5)
for a in (axs[2], axs[3]): a.set_ylim(-2.5, 3.6)
fig.tight_layout(); f.savefig(fig, 'd07_pyq_2020q5')

# ------------------------------------------------------------------ 2022 Q46: four systems, one sinusoid
fig, ax = plt.subplots(figsize=(8.2, 4.3))
rows = [('S₁', 'sin(−t)', 'same frequency: LTI possible'), ('S₂', 'sin(t + 1)', 'same frequency: LTI possible'),
        ('S₃', 'sin(2t)', 'NEW frequency: not LTI'), ('S₄', 'sin²(t)', 'new frequencies (0 and 2): not LTI')]
for i, (s, out, note) in enumerate(rows):
    y = 3 - i
    ax.add_patch(Rectangle((2.6, y - 0.32), 1.0, 0.64, fill=False, lw=2))
    ax.text(3.1, y, s, ha='center', va='center', fontsize=13)
    ax.annotate('', (2.6, y), (1.4, y), arrowprops=dict(arrowstyle='-|>', lw=1.6)); ax.text(1.35, y, 'sin(t)', ha='right', va='center', fontsize=12)
    ax.annotate('', (5.0, y), (3.6, y), arrowprops=dict(arrowstyle='-|>', lw=1.6)); ax.text(5.05, y, out, ha='left', va='center', fontsize=12)
    ax.text(6.9, y, note, ha='left', va='center', fontsize=10, color=C1 if 'not' in note else C2)
ax.set_xlim(0, 11.5); ax.set_ylim(-0.7, 3.7); ax.axis('off')
f.savefig(fig, 'd07_pyq_2022q46')

# ------------------------------------------------------------------ 2026 Q43: energy under scaling and shifting
fig, axs = plt.subplots(1, 2, figsize=(9, 2.9))
t = np.linspace(-1, 3, 4001)
x0 = lambda t: np.where((t >= 0) & (t < 1), 2.0, 0.0)
axs[0].plot(t, x0(t), color=C0); style(axs[0], (-1, 3), (-0.5, 7), [-1, 0, 1, 2, 3], [0, 2, 6], 'x(t):  E = 2² × 1 = 4')
axs[1].plot(t, 3 * x0(-3 * t + 5), color=C1); style(axs[1], (-1, 3), (-0.5, 7), [-1, 0, 1, 4 / 3, 5 / 3, 2, 3], [0, 2, 6], '3x(−3t + 5):  E = 6² × 1/3 = 12')
axs[1].set_xticklabels(['−1', '0', '1', '4/3', '5/3', '2', '3'])
for a in axs: a.set_xlabel('t')
fig.tight_layout(); f.savefig(fig, 'd07_pyq_2026q43')

f.cleanup()
print('done')
