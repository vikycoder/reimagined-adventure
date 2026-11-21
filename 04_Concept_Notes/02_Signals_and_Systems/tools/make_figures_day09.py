"""Regenerates every Day 9 figure in ../figures (prefix d09_).   Needs: matplotlib numpy scipy"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))

import matplotlib.pyplot as plt
import numpy as np
from fig_helpers import COLORS, Figs

f = Figs(os.path.join(HERE, '..', 'figures'))
C0, C1, C2, C3 = COLORS[0], COLORS[1], COLORS[2], COLORS[3]
pi = np.pi


def coeffs(x, T0, K, N=1 << 16):
    t = (np.arange(N) + 0.5) * T0 / N
    F = np.fft.fft(x(t)) / N
    k = np.arange(-K, K + 1)
    return k, F[k % N] * np.exp(-1j * pi * k / N)


def sq_pm(t, T0=2.0):
    return np.where((t % T0) < T0 / 2, 1.0, -1.0)


def stems(ax, k, v, color=C0, ms=5):
    ml, sl, bl = ax.stem(k, v, linefmt=color, markerfmt='o', basefmt='k-')
    plt.setp(ml, color=color, markersize=ms); plt.setp(sl, color=color, lw=1.6); plt.setp(bl, lw=0.8)


# ------------------------------------------------------------------ synthesis: partial sums of the +-1 square wave
fig, axs = plt.subplots(1, 4, figsize=(15, 2.9), sharey=True)
t = np.linspace(-1, 2, 6001)
for ax, Nh in zip(axs, (1, 3, 9, 49)):
    s = sum(4 / (pi * m) * np.sin(m * pi * t) for m in range(1, Nh + 1, 2))
    ax.plot(t, sq_pm(t), color='0.65', lw=1.4)
    ax.plot(t, s, color=C0, lw=1.6)
    ax.set_title(f'harmonics up to k = {Nh}', fontsize=11); ax.set_xlabel('t (period T0 = 2)'); ax.set_ylim(-1.6, 1.6); ax.set_xlim(-1, 2)
    ax.axhline(0, color='k', lw=0.6)
axs[0].set_ylabel('x(t) and partial sum')
fig.tight_layout(); f.savefig(fig, 'd09_synthesis')

# ------------------------------------------------------------------ line spectra of three waveforms
fig, axs = plt.subplots(1, 3, figsize=(14.5, 3.1))
kk = np.arange(-12, 13)
ck_sq = np.where(kk == 0, 0.5, np.sin(kk * pi / 2) / (np.where(kk == 0, 1, kk) * pi))
stems(axs[0], kk, ck_sq); axs[0].set_title('even 0/1 square wave: c_k = sin(kπ/2)/(kπ)', fontsize=10.5)
ck_p = np.where(kk == 0, 0.25, 0.25 * np.sinc(kk / 4))
stems(axs[1], kk, ck_p, C1)
kx = np.linspace(-12, 12, 2001)
axs[1].plot(kx, 0.25 * np.sinc(kx / 4), color='0.6', ls='--', lw=1.2)
axs[1].set_title('pulse train, duty ¼: c_k = ¼ sinc(k/4), zeros at k = ±4, ±8', fontsize=10.5)
ck_t = np.where(kk == 0, 0.5, np.where(kk % 2 != 0, 2 / (pi ** 2 * np.where(kk == 0, 1, kk) ** 2), 0.0))
stems(axs[2], kk, ck_t, C2); axs[2].set_title('even triangle 0…1: c_k = 2/(π²k²), odd k', fontsize=10.5)
for ax in axs:
    ax.set_xlabel('harmonic number k'); ax.axhline(0, color='k', lw=0.6); ax.set_xticks(range(-12, 13, 4))
axs[0].set_ylabel('c_k')
fig.tight_layout(); f.savefig(fig, 'd09_spectra')

# ------------------------------------------------------------------ symmetry
fig, axs = plt.subplots(1, 3, figsize=(14.5, 3.0))
t = np.linspace(-2, 4, 6001)
tri1 = lambda s: 1 - 2 * np.abs(((s + 1) % 2) - 1)
axs[0].plot(t, tri1(t), color=C0); axs[0].set_title('even: x(−t) = x(t)\nc_k real and even · cosines only', fontsize=10.5)
saw = lambda s: (((s + 1) % 2) - 1)
axs[1].plot(t, saw(t), color=C1); axs[1].set_title('odd: x(−t) = −x(t)\nc0 = 0, c_k imaginary · sines only', fontsize=10.5)
T = 2 * pi; w = 1.0
tt = np.linspace(-pi, 3 * pi, 8001)
xh = lambda s: np.cos(w * s) + 0.5 * np.sin(3 * w * s)
axs[2].plot(tt, xh(tt), color=C2, label='x(t)')
axs[2].plot(tt, -xh(tt - T / 2), color=C3, ls='--', lw=1.6, label='−x(t − T/2)  (same curve)')
axs[2].set_title('half-wave: x(t − T/2) = −x(t)\nonly odd harmonics (c_k = 0 for even k)', fontsize=10.5); axs[2].legend(frameon=False, fontsize=8.5, loc='upper center', bbox_to_anchor=(0.5, -0.33), ncol=2)
for ax in axs: ax.axhline(0, color='k', lw=0.6); ax.set_xlabel('t')
axs[2].set_xticks([-pi, 0, pi, 2 * pi, 3 * pi]); axs[2].set_xticklabels(['−T/2', '0', 'T/2', 'T', '3T/2']); axs[2].set_xlabel('')
fig.tight_layout(); f.savefig(fig, 'd09_symmetry')

# ------------------------------------------------------------------ Gibbs phenomenon
fig, axs = plt.subplots(1, 2, figsize=(12, 3.4))
tz = np.linspace(0, 0.5, 5001)
ax = axs[0]
for Nh, col in ((5, C0), (21, C1), (101, C2)):
    s = sum(4 / (pi * m) * np.sin(m * pi * tz) for m in range(1, Nh + 1, 2))
    ax.plot(tz, s, color=col, lw=1.4, label=f'k ≤ {Nh}')
ax.axhline(1, color='0.5', lw=1, ls=':'); ax.axhline(1.179, color=C3, lw=1, ls='--')
ax.text(0.27, 1.19, 'limit of the peaks: 1.179\n(overshoot ≈ 8.95 % of the jump of 2)', color=C3, fontsize=9, va='bottom')
ax.set_xlabel('t, just after the jump at t = 0'); ax.set_ylabel('partial sum'); ax.set_ylim(0.8, 1.42); ax.legend(frameon=False, fontsize=9, loc='lower right')
ax.set_title('the overshoot narrows but does not shrink', fontsize=11)
ax = axs[1]
Ns = np.array([1, 3, 5, 9, 15, 25, 51, 101, 201, 401])
tf = np.linspace(1e-4, 0.5, 100001)
pk = []
for Nh in Ns:
    s = sum(4 / (pi * m) * np.sin(m * pi * tf) for m in range(1, Nh + 1, 2))
    pk.append(s.max())
ax.semilogx(Ns, pk, 'o-', color=C0)
ax.axhline(2 / pi * 1.8519370519824, color=C3, ls='--', lw=1)
ax.text(3, 1.162, 'limit (2/π)·Si(π) = 1.17898', color=C3, fontsize=9)
ax.set_xlabel('highest harmonic included'); ax.set_ylabel('peak of the partial sum'); ax.set_ylim(1.15, 1.30); ax.set_title('peak value, ±1 square wave', fontsize=11)
fig.tight_layout(); f.savefig(fig, 'd09_gibbs')

# ------------------------------------------------------------------ 2021 Q39
fig, axs = plt.subplots(1, 3, figsize=(14.5, 3.1))
w0 = pi / 3
x39 = lambda s: 2 + sum(2 * k * np.cos(k * w0 * s) for k in (1, 2, 3))
t = np.linspace(-6, 6, 6001)
axs[0].plot(t, x39(t), color=C0); axs[0].set_title('x(t) = 2 + 2cos(πt/3) + 4cos(2πt/3) + 6cos(πt)\nreal, even, period 6 (dotted line: average 2)', fontsize=10)
axs[0].set_xlabel('t'); axs[0].axhline(0, color='k', lw=0.6); axs[0].axhline(2, color='0.6', ls=':', lw=1)
kk = np.arange(-5, 6)
a39 = np.array([2 if k == 0 else (abs(k) if 1 <= abs(k) <= 3 else 0) for k in kk], dtype=float)
stems(axs[1], kk, a39, C1); axs[1].set_title('coefficients a_k: real and even (a₋ₖ = aₖ)', fontsize=10.5); axs[1].set_xlabel('k')
axs[1].set_ylim(0, 4)
pw = a39 ** 2
cols = [C2 if v else '0.8' for v in pw]
axs[2].bar(kk, pw, color=cols, width=0.7)
for k, v in zip(kk, pw):
    if v: axs[2].text(k, v + 0.3, f'{int(v)}', ha='center', fontsize=9)
axs[2].set_title('power per coefficient |a_k|²: total 4 + 2(1 + 4 + 9) = 32', fontsize=10.5); axs[2].set_xlabel('k'); axs[2].set_ylim(0, 11)
fig.tight_layout(); f.savefig(fig, 'd09_pyq_2021q39')

# ------------------------------------------------------------------ 2026 Q37
fig, axs = plt.subplots(1, 2, figsize=(12, 3.1), gridspec_kw={'width_ratios': [1.6, 1]})
tt = np.linspace(-pi, 3 * pi, 8001)
axs[0].plot(tt, xh(tt), color=C0, label='x(t)')
axs[0].plot(tt, xh(tt - T / 2), color=C1, ls='--', label='x(t − T/2)')
axs[0].set_title('x(t − T/2) = −x(t): shifting by half a period flips the sign', fontsize=10.5); axs[0].legend(frameon=False, fontsize=9, loc='upper center', bbox_to_anchor=(0.5, -0.33), ncol=2)
axs[0].set_xticks([-pi, 0, pi, 2 * pi, 3 * pi]); axs[0].set_xticklabels(['−T/2', '0', 'T/2', 'T', '3T/2']); axs[0].axhline(0, color='k', lw=0.6); axs[0].set_xlabel('t')
kk = np.arange(-6, 7)
k_, cc = coeffs(lambda s: xh(s), T, 6)
stems(axs[1], kk, np.abs(cc), C2)
for k in (-6, -4, -2, 0, 2, 4, 6):
    axs[1].plot(k, 0, 'o', color=C1, ms=8, mfc='none', mew=1.6)
axs[1].set_title('|a_k|: zero for every even k (red circles)', fontsize=10.5); axs[1].set_xlabel('k')
fig.tight_layout(); f.savefig(fig, 'd09_pyq_2026q37')

# ------------------------------------------------------------------ 2025 Q55
fig, axs = plt.subplots(1, 2, figsize=(12.5, 3.2), gridspec_kw={'width_ratios': [1.25, 1]})
T0 = 4.0
fq = lambda s: 1 - 2 * np.abs(((s + T0 / 2) % T0) - T0 / 2) / T0
t = np.linspace(0, 2 * T0, 4001)
axs[0].plot(t, fq(t), color=C0, label='f(t): period T0')
axs[0].plot(t, fq(2 * t), color=C1, lw=1.5, label='y(t) = f(2t): period T0/2')
axs[0].set_xticks([0, T0 / 2, T0, 1.5 * T0, 2 * T0]); axs[0].set_xticklabels(['0', 'T0/2', 'T0', '3T0/2', '2T0']); axs[0].legend(frameon=False, fontsize=9, loc='upper right', bbox_to_anchor=(1.0, 1.28), ncol=2)
axs[0].set_xlabel('t')
k_, cf = coeffs(fq, T0, 9)
kk = np.arange(0, 10)
w0 = 2 * pi / T0
ax = axs[1]
ax.stem(kk * w0, np.abs(cf[9:]), linefmt=C0, markerfmt='o', basefmt='k-', label='f: |c_k| at kω0')
ml, sl, bl = ax.stem(2 * kk * w0 + 0.12, np.abs(cf[9:]) * 0.97, linefmt=C1, markerfmt='s', basefmt='k-', label='y: d_k = c_k at 2kω0')
plt.setp(ml, color=C1); plt.setp(sl, color=C1)
ax.set_xlabel('frequency (rad/s)'); ax.set_title('same coefficients, harmonics twice as far apart', fontsize=10.5); ax.legend(frameon=False, fontsize=9)
fig.tight_layout(); f.savefig(fig, 'd09_pyq_2025q55')

# ------------------------------------------------------------------ 2026 Q58
fig, axs = plt.subplots(1, 2, figsize=(12.5, 3.2))
ta = np.linspace(0, 1, 4001)
prod = lambda s: np.cos(2 * pi * s) * 2 * np.sin(4 * pi * s)
axs[0].plot(ta, prod(ta), color='k', lw=1.2)
axs[0].fill_between(ta, 0, prod(ta), where=prod(ta) > 0, color=C2, alpha=0.55); axs[0].fill_between(ta, 0, prod(ta), where=prod(ta) < 0, color=C1, alpha=0.55)
axs[0].set_title('over one period [0, 1): x₁x₂ has equal + and − areas: ∫ = 0', fontsize=10.5); axs[0].axhline(0, color='k', lw=0.6); axs[0].set_xlabel('t   (n = 1)')
tb = np.linspace(0, 0.5, 2001)
axs[1].plot(ta, prod(ta), color='0.8', lw=1)
axs[1].plot(tb, prod(tb), color='k', lw=1.2); axs[1].fill_between(tb, 0, prod(tb), color=C2, alpha=0.55)
axs[1].set_title('over [0, 1/2): the area is positive: ∫ = 4/(3π) = 0.424 ≠ 0', fontsize=10.5); axs[1].axhline(0, color='k', lw=0.6); axs[1].set_xlabel('t   (n = 1)')
fig.tight_layout(); f.savefig(fig, 'd09_pyq_2026q58')

# ------------------------------------------------------------------ periodic input through a low-pass filter
fig, axs = plt.subplots(1, 2, figsize=(12.5, 3.2), gridspec_kw={'width_ratios': [1.5, 1]})
T0 = 2 * pi
t = np.linspace(0, 2 * T0, 6001)
xin = np.where((t % T0) < T0 / 2, 1.0, -1.0)
yout = sum(4 / (pi * m) / np.sqrt(1 + m * m) * np.sin(m * t - np.arctan(m)) for m in range(1, 400, 2))
axs[0].plot(t, xin, color='0.65', lw=1.4, label='x(t): ±1 square wave'); axs[0].plot(t, yout, color=C0, label='y(t): output of H(jω) = 1/(1 + jω)')
axs[0].set_xticks([0, pi, 2 * pi, 3 * pi, 4 * pi]); axs[0].set_xticklabels(['0', 'T/2', 'T', '3T/2', '2T']); axs[0].legend(frameon=False, fontsize=9, loc='upper right', bbox_to_anchor=(1.0, 1.26), ncol=2); axs[0].axhline(0, color='k', lw=0.6)
ks = np.array([1, 3, 5, 7])
w_ = 0.38
axs[1].bar(np.arange(4) - w_ / 2, 4 / (pi * ks), w_, color='0.7', label='input')
axs[1].bar(np.arange(4) + w_ / 2, 4 / (pi * ks) / np.sqrt(1 + ks ** 2), w_, color=C0, label='output: × |H(jk)|')
axs[1].set_xticks(range(4)); axs[1].set_xticklabels([f'k = {k}' for k in ks]); axs[1].set_ylabel('harmonic amplitude'); axs[1].legend(frameon=False, fontsize=9)
axs[1].set_title('each harmonic is scaled by |H(jkω0)|', fontsize=10.5)
fig.tight_layout(); f.savefig(fig, 'd09_lti_periodic')

# ------------------------------------------------------------------ 2019 Q44
fig, axs = plt.subplots(1, 2, figsize=(11.5, 3.0))
n = np.arange(-3, 4)
hv = np.array([-1, -2, -3, 4, 3, 2, 1])
keep = np.abs(n) <= 1
ax = axs[0]
ml, sl, bl = ax.stem(n[keep], hv[keep], linefmt=C2, markerfmt='o', basefmt='k-'); plt.setp(ml, color=C2); plt.setp(sl, color=C2)
ml, sl, bl = ax.stem(n[~keep], hv[~keep], linefmt=C1, markerfmt='o', basefmt='k-'); plt.setp(ml, color=C1); plt.setp(sl, color=C1)
ax.set_title('h[n]: kept taps (green) and dropped taps (red)', fontsize=10.5); ax.set_xlabel('n'); ax.set_ylim(-4.5, 5)
gv = np.where(keep, hv, 0)
ml, sl, bl = axs[1].stem(n, gv, linefmt=C0, markerfmt='o', basefmt='k-'); plt.setp(ml, color=C0)
axs[1].set_title('best 3-tap g[n]: 10g[−1] + g[1] = −30 + 3 = −27\nerror E = 2π(1 + 4 + 4 + 1) = 20π', fontsize=10.5); axs[1].set_xlabel('n'); axs[1].set_ylim(-4.5, 5)
fig.tight_layout(); f.savefig(fig, 'd09_pyq_2019q44')

f.cleanup()
print('figures written to', f.out)
