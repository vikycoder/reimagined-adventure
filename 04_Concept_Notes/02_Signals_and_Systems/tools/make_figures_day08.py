"""Regenerates every Day 8 figure in ../figures (prefix d08_).   Needs: matplotlib numpy"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle
from fig_helpers import COLORS, Figs

f = Figs(os.path.join(HERE, '..', 'figures'))
C0, C1, C2 = COLORS[0], COLORS[1], COLORS[2]


def axes_style(ax, xlim, ylim, title=None, xt=None, yt=None):
    ax.axhline(0, color='k', lw=0.8); ax.axvline(0, color='k', lw=0.8)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    if xt is not None: ax.set_xticks(xt)
    if yt is not None: ax.set_yticks(yt)
    if title: ax.set_title(title, fontsize=11)


# ------------------------------------------------------------------ graphical convolution of two unit rectangles
fig, axs = plt.subplots(1, 4, figsize=(14, 2.9))
tau = np.linspace(-1, 3, 4001)
rect01 = lambda s: np.where((s >= 0) & (s <= 1), 1.0, 0.0)
ax = axs[0]
ax.plot(tau, rect01(tau), color=C0, label='x(τ)'); ax.plot(tau, rect01(tau), color=C1, ls='--', label='h(τ)')
axes_style(ax, (-1, 3), (-0.3, 1.5), 'x(τ) and h(τ)', [-1, 0, 1, 2, 3], [0, 1]); ax.legend(frameon=False, fontsize=9)
for ax, t0, ttl in ((axs[1], 0.5, 'flip, slide to t = 0.5: overlap 0.5'), (axs[2], 1.0, 'slide to t = 1: overlap 1')):
    ax.plot(tau, rect01(tau), color=C0); ax.plot(tau, rect01(t0 - tau), color=C1, ls='--')
    ax.fill_between(tau, 0, np.minimum(rect01(tau), rect01(t0 - tau)), color=C2, alpha=0.5)
    axes_style(ax, (-1, 3), (-0.3, 1.5), ttl, [-1, 0, 1, 2, 3], [0, 1]); ax.set_xlabel('τ')
ax = axs[3]
tt = np.linspace(-1, 3, 4001)
y = np.where((tt >= 0) & (tt <= 1), tt, np.where((tt > 1) & (tt <= 2), 2 - tt, 0.0))
ax.plot(tt, y, color=C2, lw=2.2)
for t0 in (0.5, 1.0, 1.5): ax.plot(t0, np.interp(t0, tt, y), 'o', color=C1)
axes_style(ax, (-1, 3), (-0.3, 1.5), 'y(t) = overlap area: a triangle on [0, 2]', [-1, 0, 1, 2, 3], [0, 1]); ax.set_xlabel('t')
fig.tight_layout(); f.savefig(fig, 'd08_flip_slide')

# ------------------------------------------------------------------ discrete-time convolution
fig, axs = plt.subplots(1, 3, figsize=(11.5, 2.7))
n = np.arange(-2, 6)
for ax, v, ttl, col in ((axs[0], [1, 2, 3], 'x[n] = {1, 2, 3}', C0), (axs[1], [1, -1], 'h[n] = {1, −1}', C1), (axs[2], np.convolve([1, 2, 3], [1, -1]), 'y[n] = x∗h = {1, 1, 1, −3}', C2)):
    y = np.zeros(len(n)); y[2:2 + len(v)] = v
    ax.stem(n, y, linefmt=col, markerfmt='o', basefmt='k-'); ax.set_title(ttl, fontsize=11); ax.set_xlabel('n'); ax.set_ylim(-3.8, 3.8); ax.set_xlim(-2.5, 5.5)
fig.tight_layout(); f.savefig(fig, 'd08_dt_conv')

# ------------------------------------------------------------------ four standard continuous-time convolutions
fig, axs = plt.subplots(1, 4, figsize=(14, 2.9))
t = np.linspace(-1, 6, 7001)
u = lambda s: np.where(s >= 0, 1.0, 0.0)
axs[0].plot(t, t * u(t), color=C0); axes_style(axs[0], (-1, 6), (-0.5, 6), 'u(t)∗u(t) = r(t)', [0, 2, 4, 6], [0, 2, 4, 6])
axs[1].plot(t, (1 - np.exp(-t)) * u(t), color=C0); axes_style(axs[1], (-1, 6), (-0.2, 1.3), 'e⁻ᵗu(t)∗u(t) = (1 − e⁻ᵗ)u(t)', [0, 2, 4, 6], [0, 1])
axs[2].plot(t, (np.exp(-t) - np.exp(-2 * t)) * u(t), color=C0); axes_style(axs[2], (-1, 6), (-0.05, 0.4), 'e⁻ᵗu ∗ e⁻²ᵗu = (e⁻ᵗ − e⁻²ᵗ)u', [0, 2, 4, 6], [0, 0.25])
tt = np.linspace(-3, 3, 6001)
trap = np.interp(tt, [-1.5, -0.5, 0.5, 1.5], [0, 1, 1, 0], left=0, right=0)
axs[3].plot(tt, trap, color=C0); axes_style(axs[3], (-3, 3), (-0.3, 1.5), 'rect(width 1) ∗ rect(width 2): trapezoid', [-3, -1.5, -0.5, 0.5, 1.5, 3], [0, 1])
for a in axs: a.set_xlabel('t')
fig.tight_layout(); f.savefig(fig, 'd08_ct_examples')

# ------------------------------------------------------------------ 2023 Q58
fig, axs = plt.subplots(1, 3, figsize=(13.5, 3.1))
t = np.linspace(-6, 6, 12001)
x1 = np.where(np.abs(t) < 1.5, 1.0, 0.0)
axs[0].plot(t, x1, color=C0); axes_style(axs[0], (-6, 6), (-0.3, 3.2), 'x₁(t): width 3, area 3', [-6, -3, -1.5, 0, 1.5, 3, 6], [0, 1, 2])
ax = axs[1]
ax.plot(t, np.where(np.abs(t) < 1, 1.0, 0.0), color=C0)
for x0, w in ((-3, 1), (2, 2)):
    ax.annotate('', (x0, w), (x0, 0), arrowprops=dict(arrowstyle='-|>', lw=2.2, color=C1)); ax.text(x0 + 0.15, w * 0.55, str(w), color=C1)
axes_style(ax, (-6, 6), (-0.3, 3.2), 'x₂(t): impulses 1 and 2, pulse of area 2: area 5', [-6, -3, -1, 0, 1, 2, 6], [0, 1, 2])
# y = x1 * x2 = x1(t + 3) + (x1 * rect2) + 2 x1(t - 2)
dt = 0.001
tg = np.arange(-8, 8, dt)
r3 = np.where(np.abs(tg) < 1.5, 1.0, 0.0); r2 = np.where(np.abs(tg) < 1, 1.0, 0.0)
mid = np.convolve(r3, r2) * dt
tc = np.arange(len(mid)) * dt + (tg[0] + tg[0])
ys = np.interp(t, tc, mid, left=0, right=0) + np.where(np.abs(t + 3) < 1.5, 1.0, 0.0) + 2 * np.where(np.abs(t - 2) < 1.5, 1.0, 0.0)
axs[2].plot(t, ys, color=C2, lw=2); axes_style(axs[2], (-6, 6), (-0.3, 4.7), 'y(t) = x₁∗x₂:  ∫y = 3 × 5 = 15', [-6, -3, 0, 3, 6], [0, 1, 2, 3, 4])
for a in axs: a.set_xlabel('t')
fig.tight_layout(); f.savefig(fig, 'd08_pyq_2023q58')
print('area of y by integration:', round(float(np.trapezoid(ys, t)), 3))

# ------------------------------------------------------------------ 2022 Q33
fig, ax = plt.subplots(figsize=(7.6, 3.0))
t = np.linspace(-1, 12, 13001)
y = np.where(t < 0, 0.0, np.where(t < 2, 1 - np.exp(-t), np.exp(-t) * (np.exp(2) - 1)))
ax.plot(t, y, color=C2, lw=2.2); ax.plot(2, 1 - np.exp(-2), 'o', color=C1)
ax.text(2.2, 0.93, 'peak 1 − e⁻² = 0.865 at t = 2', color=C1, fontsize=10)
axes_style(ax, (-1, 12), (-0.1, 1.1), 'y(t) = e⁻ᵗu(t) ∗ [u(t) − u(t − 2)]:  y → 0 as t → ∞', [0, 2, 4, 6, 8, 10, 12], [0, 0.5, 1]); ax.set_xlabel('t')
f.savefig(fig, 'd08_pyq_2022q33')

# ------------------------------------------------------------------ 2021 Q40
fig, axs = plt.subplots(1, 4, figsize=(14.5, 2.8))
n = np.arange(-4, 8)
s = np.zeros(len(n)); s[n == -1] = 2; s[n == 0] = 1; s[n == 1] = 1
h = np.zeros(len(n)); h[n == -1] = 2; h[n == 0] = -1; h[n == 2] = -1
x = np.where(n >= 0, 0.5 ** np.maximum(n, 0), 0.0)
y = np.convolve(h, x)[: len(n)]                                 # offset handled below
# full convolution index bookkeeping
yfull = np.convolve(h, x)
nfull = np.arange(len(yfull)) + (n[0] + n[0])
yy = np.interp(n, nfull, yfull, left=0, right=0)
for ax, v, ttl, col in ((axs[0], s, 'step response s[n] = 2δ[n+1] + δ[n] + δ[n−1]', C0), (axs[1], h, 'h[n] = s[n] − s[n−1]', C1), (axs[2], x, 'input (1/2)ⁿu[n]', C0), (axs[3], yy, 'y[n] = x∗h:  y[0] = 0', C2)):
    ax.stem(n, v, linefmt=col, markerfmt='o', basefmt='k-'); ax.set_title(ttl, fontsize=10); ax.set_xlabel('n'); ax.set_xlim(-4.5, 7.5); ax.set_ylim(-2.2, 2.6)
fig.tight_layout(); f.savefig(fig, 'd08_pyq_2021q40')


# ------------------------------------------------------------------ block diagrams (2025 Q17 and 2026 Q47)
def box(ax, x, y, w, h, text, fs=12):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, lw=1.8)); ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs)


def adder(ax, x, y, r=0.28, signs=None):
    ax.add_patch(Circle((x, y), r, fill=False, lw=1.8)); ax.plot([x - r * 0.6, x + r * 0.6], [y, y], 'k', lw=1.4); ax.plot([x, x], [y - r * 0.6, y + r * 0.6], 'k', lw=1.4)


def arrow(ax, p, q, **kw):
    ax.annotate('', q, p, arrowprops=dict(arrowstyle='-|>', lw=1.5, **kw))


def seg(ax, *pts):
    xs, ys = zip(*pts); ax.plot(xs, ys, 'k', lw=1.5)


fig, ax = plt.subplots(figsize=(11.5, 3.2))
ax.add_patch(Rectangle((0.9, 0.1), 9.4, 2.7, fill=False, lw=1.2, ls='--'))
ax.text(0, 1.7, 'x[n]', ha='right', va='center', fontsize=13); arrow(ax, (0.05, 1.7), (1.4, 1.7))
box(ax, 1.4, 1.35, 1.5, 0.7, 'h₁[n]'); arrow(ax, (2.9, 1.7), (4.62, 1.7)); adder(ax, 4.9, 1.7)
ax.text(4.9, 0.55, 'b δ[n]', ha='center', fontsize=12); arrow(ax, (4.9, 0.8), (4.9, 1.42))
arrow(ax, (5.18, 1.7), (6.2, 1.7)); box(ax, 6.2, 1.35, 1.5, 0.7, 'h₂[n]'); arrow(ax, (7.7, 1.7), (8.82, 1.7)); adder(ax, 9.1, 1.7)
ax.text(9.1, 0.55, '−b δ[n]', ha='center', fontsize=12); arrow(ax, (9.1, 0.8), (9.1, 1.42)); arrow(ax, (9.38, 1.7), (10.8, 1.7)); ax.text(10.9, 1.7, 'y[n]', va='center', fontsize=13)
ax.text(2.1, 2.55, 'subsystem 1', fontsize=10, ha='left'); ax.text(6.4, 2.55, 'subsystem 2', fontsize=10, ha='left')
ax.text(5.6, -0.25, 'y = h₂∗(h₁∗x + bδ) − bδ = (h₁∗h₂)∗x + b(h₂ − δ):  an LTI part plus a FIXED signal that does not move when the input moves', ha='center', fontsize=10, color=C1)
ax.set_xlim(-1, 11.6); ax.set_ylim(-0.5, 3.0); ax.axis('off')
f.savefig(fig, 'd08_pyq_2025q17')

fig, ax = plt.subplots(figsize=(11.5, 4.0))
ax.text(0, 1.9, 'x[n]', ha='right', va='center', fontsize=13); seg(ax, (0.05, 1.9), (1.2, 1.9)); ax.plot(1.2, 1.9, 'ko', ms=4)
seg(ax, (1.2, 1.9), (1.2, 3.4)); arrow(ax, (1.2, 3.4), (2.0, 3.4)); box(ax, 2.0, 3.05, 1.5, 0.7, 'h₁[n]'); seg(ax, (3.5, 3.4), (4.6, 3.4)); ax.plot(4.6, 3.4, 'ko', ms=4)
arrow(ax, (4.6, 3.4), (7.32, 3.4)); adder(ax, 7.6, 3.4); ax.text(7.2, 3.75, '+', fontsize=12); arrow(ax, (7.88, 3.4), (9.3, 3.4)); ax.text(9.4, 3.4, 'y[n]', va='center', fontsize=13)
seg(ax, (4.6, 3.4), (4.6, 2.95)); box(ax, 4.2, 2.3, 0.8, 0.65, 'z⁻¹', 11); arrow(ax, (4.6, 2.3), (4.6, 1.12)); ax.text(4.75, 1.55, '−', fontsize=13)
seg(ax, (1.2, 1.9), (1.2, 0.8)); arrow(ax, (1.2, 0.8), (4.32, 0.8)); adder(ax, 4.6, 0.8); ax.text(3.9, 1.0, '+', fontsize=12)
arrow(ax, (4.88, 0.8), (5.6, 0.8)); box(ax, 5.6, 0.45, 1.5, 0.7, 'h₂[n]'); seg(ax, (7.1, 0.8), (7.6, 0.8)); arrow(ax, (7.6, 0.8), (7.6, 1.5)); box(ax, 7.2, 1.5, 0.8, 0.65, 'z⁻¹', 11); arrow(ax, (7.6, 2.15), (7.6, 3.12)); ax.text(7.75, 2.65, '−', fontsize=13)
ax.text(5.5, -0.25, 'no feedback loop: every block is LTI, so the whole system is LTI (but causal only if h₁ and h₂ are)', ha='center', fontsize=10, color=C1)
ax.set_xlim(-1, 10.6); ax.set_ylim(-0.6, 4.2); ax.axis('off')
f.savefig(fig, 'd08_pyq_2026q47')

f.cleanup()
print('done')
