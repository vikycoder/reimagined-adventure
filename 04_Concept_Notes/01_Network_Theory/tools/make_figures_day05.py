"""Regenerates every Day 5 figure in ../figures (prefix d05_).   Needs: schemdraw matplotlib numpy pillow"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import schemdraw.elements as e
from fig_helpers import COLORS, Figs

f = Figs(os.path.join(HERE, '..', 'figures'))
OHM = 'Ω'


# ------------------------------------------------------------------ small drawing helpers (all coordinates explicit)
def txt(d, xy, s, fs=12):
    d.add(e.Label().at(xy).label(s, fontsize=fs))


def odot(d, *pts):
    for p in pts:
        d.add(e.Dot(open=True).at(p))


def dot(d, *pts):
    for p in pts:
        d.add(e.Dot().at(p))


def wire(d, a, b):
    d.add(e.Line().at(a).to(b))


def box(d, x0, y0, w, h, text='', fs=13):
    wire(d, (x0, y0), (x0 + w, y0)); wire(d, (x0 + w, y0), (x0 + w, y0 + h))
    wire(d, (x0 + w, y0 + h), (x0, y0 + h)); wire(d, (x0, y0 + h), (x0, y0))
    if text:
        txt(d, (x0 + w / 2, y0 + h / 2), text, fs)


def R(d, a, b, label=None, side='top'):
    el = e.Resistor().endpoints(a, b)
    d.add(el.label(label, loc=side) if label else el)


# ------------------------------------------------------------------ the general two-port with its sign conventions
fig, ax = f.plot((6.4, 3.0))
ax.add_patch(Rectangle((1.4, 0.0), 3.2, 2.4, fill=False, lw=2.2, ec='black'))
ax.text(3.0, 1.2, 'linear two-port\n(no independent\nsources inside)', ha='center', va='center', fontsize=11)
for x0, x1 in ((0.0, 1.4), (4.6, 6.0)):
    for y in (2.0, 0.4):
        ax.plot([x0, x1], [y, y], color='black', lw=2)
for x in (0.0, 6.0):
    for y in (2.0, 0.4):
        ax.plot(x, y, 'o', mfc='white', mec='black', ms=7, zorder=3)
ax.annotate('', (1.15, 2.0), (0.45, 2.0), arrowprops=dict(arrowstyle='-|>', lw=2, color=COLORS[1]))
ax.annotate('', (4.85, 2.0), (5.55, 2.0), arrowprops=dict(arrowstyle='-|>', lw=2, color=COLORS[1]))
ax.text(0.8, 2.2, 'I₁', ha='center', color=COLORS[1], fontsize=12); ax.text(5.2, 2.2, 'I₂', ha='center', color=COLORS[1], fontsize=12)
for x, name, ha in ((-0.35, 'V₁', 'right'), (6.35, 'V₂', 'left')):
    ax.annotate('', (x, 0.4), (x, 2.0), arrowprops=dict(arrowstyle='<|-|>', lw=1.5, color=COLORS[0]))
    ax.text(x + (-0.2 if ha == 'right' else 0.2), 1.2, name, ha=ha, va='center', color=COLORS[0], fontsize=12)
    ax.text(x, 2.2, '+', ha='center', fontsize=12, color=COLORS[0]); ax.text(x, 0.0, '−', ha='center', fontsize=13, color=COLORS[0])
ax.text(3.0, -0.6, 'both currents are defined INTO the network (port 1 = left, port 2 = right)', ha='center', fontsize=9.5)
ax.set_xlim(-1.3, 7.3); ax.set_ylim(-0.95, 2.9); ax.axis('off')
f.savefig(fig, 'd05_two_port_box')

# ------------------------------------------------------------------ T and Pi networks
d = f.new()
odot(d, (0, 2.4), (0, 0), (6, 2.4), (6, 0)); dot(d, (3, 2.4), (3, 0))
R(d, (0, 2.4), (3, 2.4), 'Z₁'); R(d, (3, 2.4), (6, 2.4), 'Z₂'); R(d, (3, 2.4), (3, 0), 'Z₃', 'bottom')
wire(d, (0, 0), (6, 0)); txt(d, (-0.35, 1.2), '1', 12); txt(d, (6.35, 1.2), '2', 12)
f.panel(d, 't')
d = f.new()
odot(d, (0, 2.4), (0, 0), (6, 2.4), (6, 0)); dot(d, (1.2, 2.4), (1.2, 0), (4.8, 2.4), (4.8, 0))
wire(d, (0, 2.4), (1.2, 2.4)); R(d, (1.2, 2.4), (4.8, 2.4), 'Y_c'); wire(d, (4.8, 2.4), (6, 2.4))
R(d, (1.2, 2.4), (1.2, 0), 'Y_a', 'bottom'); R(d, (4.8, 2.4), (4.8, 0), 'Y_b', 'bottom')
wire(d, (0, 0), (6, 0)); txt(d, (-0.35, 1.2), '1', 12); txt(d, (6.35, 1.2), '2', 12)
f.panel(d, 'pi')
f.hstack(['t', 'pi'], 'd05_t_pi', ['T network: series arms Z₁, Z₂,\nshunt arm Z₃', 'Π network: shunt arms Y_a, Y_b,\nseries arm Y_c'])

# ------------------------------------------------------------------ interconnections (block diagrams)
fig, axs = plt.subplots(1, 3, figsize=(11.4, 3.3))


def blk(ax, x0, y0, w, h, name):
    ax.add_patch(Rectangle((x0, y0), w, h, fill=False, lw=2, ec='black'))
    ax.text(x0 + w / 2, y0 + h / 2, name, ha='center', va='center', fontsize=12)


def pl(ax, pts, **kw):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color='black', lw=1.8, solid_capstyle='butt', **kw)


def term(ax, *pts):
    for p in pts:
        ax.plot(*p, 'o', mfc='white', mec='black', ms=6, zorder=3)


# (1) series-series: inputs in series, outputs in series -> Z adds
ax = axs[0]
blk(ax, 1.6, 2.4, 1.8, 1.2, 'N_a'); blk(ax, 1.6, 0.4, 1.8, 1.2, 'N_b')
pl(ax, [(0, 3.3), (1.6, 3.3)]); pl(ax, [(1.6, 2.7), (1.0, 2.7), (1.0, 1.3), (1.6, 1.3)]); pl(ax, [(1.6, 0.7), (0.5, 0.7), (0.5, 0.0), (0, 0.0)])
pl(ax, [(5.0, 3.3), (3.4, 3.3)]); pl(ax, [(3.4, 2.7), (4.0, 2.7), (4.0, 1.3), (3.4, 1.3)]); pl(ax, [(3.4, 0.7), (4.5, 0.7), (4.5, 0.0), (5.0, 0.0)])
term(ax, (0, 3.3), (0, 0.0), (5.0, 3.3), (5.0, 0.0)); ax.set_title('series – series:  [Z] = [Z_a] + [Z_b]', fontsize=11)
# (2) parallel-parallel -> Y adds
ax = axs[1]
blk(ax, 1.6, 2.4, 1.8, 1.2, 'N_a'); blk(ax, 1.6, 0.4, 1.8, 1.2, 'N_b')
pl(ax, [(0, 3.3), (0.6, 3.3), (0.6, 1.3), (1.6, 1.3)]); pl(ax, [(0.6, 3.3), (1.6, 3.3)]); dot_pts = [(0.6, 3.3)]
pl(ax, [(0, 0.0), (0.3, 0.0), (0.3, 0.7), (1.6, 0.7)]); pl(ax, [(0.3, 0.7), (0.3, 2.7), (1.6, 2.7)])
pl(ax, [(5.0, 3.3), (4.4, 3.3), (4.4, 1.3), (3.4, 1.3)]); pl(ax, [(4.4, 3.3), (3.4, 3.3)])
pl(ax, [(5.0, 0.0), (4.7, 0.0), (4.7, 0.7), (3.4, 0.7)]); pl(ax, [(4.7, 0.7), (4.7, 2.7), (3.4, 2.7)])
for p in ((0.6, 3.3), (0.6, 1.3), (0.3, 0.7), (0.3, 2.7), (4.4, 3.3), (4.4, 1.3), (4.7, 0.7), (4.7, 2.7)):
    pass
for p in ((0.6, 3.3), (0.3, 0.7), (4.4, 3.3), (4.7, 0.7)):
    ax.plot(*p, 'o', color='black', ms=4)
term(ax, (0, 3.3), (0, 0.0), (5.0, 3.3), (5.0, 0.0)); ax.set_title('parallel – parallel:  [Y] = [Y_a] + [Y_b]', fontsize=11)
# (3) cascade -> ABCD multiplies
ax = axs[2]
blk(ax, 1.0, 1.0, 1.6, 1.6, 'N_a'); blk(ax, 3.4, 1.0, 1.6, 1.6, 'N_b')
pl(ax, [(0, 2.2), (1.0, 2.2)]); pl(ax, [(2.6, 2.2), (3.4, 2.2)]); pl(ax, [(5.0, 2.2), (6.0, 2.2)])
pl(ax, [(0, 1.4), (1.0, 1.4)]); pl(ax, [(2.6, 1.4), (3.4, 1.4)]); pl(ax, [(5.0, 1.4), (6.0, 1.4)])
term(ax, (0, 2.2), (0, 1.4), (6.0, 2.2), (6.0, 1.4)); ax.set_title('cascade:  [T] = [T_a]·[T_b]  (this order)', fontsize=11)
for ax in axs:
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-0.4, 5.4)
axs[2].set_xlim(-0.4, 6.4); axs[0].set_ylim(-0.4, 3.9); axs[1].set_ylim(-0.4, 3.9); axs[2].set_ylim(0.2, 3.2)
fig.tight_layout()
f.savefig(fig, 'd05_interconnect')

# ------------------------------------------------------------------ terminated two-port
d = f.new()
d.add(e.SourceV().at((0, 0)).up(2.8))
txt(d, (-1.0, 1.4), 'V_s', 13)
wire(d, (0, 2.8), (0.5, 2.8)); R(d, (0.5, 2.8), (2.7, 2.8), 'Z_s'); wire(d, (2.7, 2.8), (3.6, 2.8))
box(d, 3.6, -0.4, 2.8, 3.6, 'two-port')
wire(d, (6.4, 2.8), (7.4, 2.8)); wire(d, (6.4, 0), (7.4, 0)); wire(d, (0, 0), (3.6, 0))
R(d, (7.4, 2.8), (7.4, 0)); dot(d, (7.4, 2.8), (7.4, 0)); txt(d, (8.1, 1.4), 'Z_L', 13)
txt(d, (3.15, 3.2), 'I₁ →', 12); txt(d, (6.85, 3.2), '← I₂', 12)
txt(d, (3.7, -1.0), 'Z_in = V₁/I₁ : looking into port 1', 11); txt(d, (3.7, -1.6), 'Z_out : looking into port 2, with V_s off and Z_L removed', 11)
f.save(d, 'd05_terminated')


# ------------------------------------------------------------------ PYQ 2020 Q15 and 2023 Q33: source + 10 ohm, [Z] or [Y], load
def source_box_load(name, label):
    d = f.new()
    d.add(e.SourceV().at((0, 0)).up(2.8)); txt(d, (-1.1, 1.4), '120 V', 12)
    wire(d, (0, 2.8), (0.5, 2.8)); R(d, (0.5, 2.8), (2.5, 2.8), '10 ' + OHM); wire(d, (2.5, 2.8), (3.4, 2.8))
    box(d, 3.4, -0.4, 2.6, 3.6, label, 16)
    wire(d, (6.0, 2.8), (6.9, 2.8)); wire(d, (6.0, 0), (6.9, 0)); wire(d, (0, 0), (3.4, 0))
    R(d, (6.9, 2.8), (6.9, 0)); txt(d, (7.6, 1.4), 'Z_L', 12)
    txt(d, (2.95, 3.2), 'I₁ →', 11); txt(d, (6.4, 3.2), '← I₂', 11)
    f.save(d, name)


source_box_load('d05_pyq_2020q15', '[Z]')
source_box_load('d05_pyq_2023q33', '[Y]')

# ------------------------------------------------------------------ PYQ 2021 Q29: dependent current source 3 V2
d = f.new()
odot(d, (0, 3), (0, 0), (7.2, 3), (7.2, 0)); dot(d, (1.2, 3), (1.2, 0), (3.0, 3), (3.0, 0), (5.8, 3), (5.8, 0))
wire(d, (0, 3), (3.0, 3)); R(d, (3.0, 3), (5.0, 3), '1 ' + OHM); wire(d, (5.0, 3), (7.2, 3)); wire(d, (0, 0), (7.2, 0))
R(d, (1.2, 3), (1.2, 0), '1 ' + OHM, 'bottom'); R(d, (5.8, 3), (5.8, 0), '1 ' + OHM, 'bottom')
d.add(e.SourceControlledI().at((3.0, 0)).up(3)); txt(d, (4.05, 1.5), '3V₂', 12)
txt(d, (0.55, 3.35), 'I₁ →', 12); txt(d, (6.65, 3.35), '← I₂', 12)
txt(d, (-0.45, 3.0), '+', 12); txt(d, (-0.45, 0), '−', 13); txt(d, (7.65, 3.0), '+', 12); txt(d, (7.65, 0), '−', 13)
txt(d, (-0.6, 1.5), 'V₁', 13); txt(d, (7.8, 1.5), 'V₂', 13)
f.save(d, 'd05_pyq_2021q29')

# ------------------------------------------------------------------ PYQ 2024 Q60: 2 ohm, 4 ohm, dependent source 8 V1
d = f.new()
odot(d, (0, 3.2), (0, 0), (5.4, 3.2), (5.4, 0)); dot(d, (3.0, 3.2))
R(d, (0, 3.2), (3.0, 3.2), '2 ' + OHM); wire(d, (3.0, 3.2), (5.4, 3.2)); wire(d, (0, 0), (5.4, 0))
R(d, (3.0, 3.2), (3.0, 1.7)); txt(d, (3.7, 2.45), '4 ' + OHM, 12)
d.add(e.SourceControlledV().at((3.0, 1.7)).down(1.7)); txt(d, (3.8, 0.85), '8V₁', 12)
txt(d, (0.5, 3.55), 'I₁ →', 12); txt(d, (4.9, 3.55), '← I₂', 12)
txt(d, (-0.45, 3.2), '+', 12); txt(d, (-0.45, 0), '−', 13); txt(d, (5.85, 3.2), '+', 12); txt(d, (5.85, 0), '−', 13)
txt(d, (-0.6, 1.6), 'V₁', 13); txt(d, (6.0, 1.6), 'V₂', 13)
f.save(d, 'd05_pyq_2024q60')

# ------------------------------------------------------------------ PYQ 2025 Q40: resistive ladder
d = f.new()
odot(d, (0, 3), (0, 0), (7.2, 3), (7.2, 0)); dot(d, (2.4, 3), (2.4, 0), (4.8, 3), (4.8, 0))
R(d, (0, 3), (2.4, 3), '2 ' + OHM); R(d, (2.4, 3), (4.8, 3), '2 ' + OHM); R(d, (4.8, 3), (7.2, 3), '2 ' + OHM); wire(d, (0, 0), (7.2, 0))
R(d, (2.4, 3), (2.4, 0), '2 ' + OHM, 'bottom'); R(d, (4.8, 3), (4.8, 0), '2 ' + OHM, 'bottom')
txt(d, (0.65, 2.55), 'I₁ →', 12); txt(d, (6.55, 2.55), '← I₂', 12)
txt(d, (-0.45, 3.0), '+', 12); txt(d, (-0.45, 0), '−', 13); txt(d, (7.65, 3.0), '+', 12); txt(d, (7.65, 0), '−', 13)
txt(d, (-0.6, 1.5), 'V₁', 13); txt(d, (7.8, 1.5), 'V₂', 13)
f.save(d, 'd05_pyq_2025q40')

# ------------------------------------------------------------------ PYQ 2026 Q51: T network of 1 kOhm
d = f.new()
odot(d, (0, 3), (0, 0), (4.8, 3), (4.8, 0)); dot(d, (2.4, 3), (2.4, 0))
R(d, (0, 3), (2.4, 3), '1 k' + OHM); R(d, (2.4, 3), (4.8, 3), '1 k' + OHM); wire(d, (0, 0), (4.8, 0)); R(d, (2.4, 3), (2.4, 0), '1 k' + OHM, 'bottom')
txt(d, (-0.45, 1.5), 'P1', 13); txt(d, (5.25, 1.5), 'P2', 13)
f.save(d, 'd05_pyq_2026q51')

# ------------------------------------------------------------------ question figures
# Q6: pi network 1 ohm / 2 ohm / 4 ohm
d = f.new()
odot(d, (0, 3), (0, 0), (5.2, 3), (5.2, 0)); dot(d, (1.2, 3), (1.2, 0), (4.0, 3), (4.0, 0))
wire(d, (0, 3), (1.2, 3)); R(d, (1.2, 3), (4.0, 3), '2 ' + OHM); wire(d, (4.0, 3), (5.2, 3)); wire(d, (0, 0), (5.2, 0))
R(d, (1.2, 3), (1.2, 0), '1 ' + OHM, 'bottom'); R(d, (4.0, 3), (4.0, 0), '4 ' + OHM, 'bottom')
txt(d, (0.45, 3.4), 'I₁ →', 12); txt(d, (4.75, 3.4), '← I₂', 12)
txt(d, (-0.45, 3), '+', 12); txt(d, (-0.45, 0), '−', 13); txt(d, (5.65, 3), '+', 12); txt(d, (5.65, 0), '−', 13)
txt(d, (-0.6, 1.5), 'V₁', 13); txt(d, (5.85, 1.5), 'V₂', 13)
f.save(d, 'd05_q06_pi')
# Q7: series 2 ohm and a VCCS 3 V1 drawn from the port-2 node to the common terminal
d = f.new()
odot(d, (0, 3), (0, 0), (5.2, 3), (5.2, 0)); dot(d, (3.6, 3))
R(d, (0, 3), (3.6, 3), '2 ' + OHM); wire(d, (3.6, 3), (5.2, 3)); wire(d, (0, 0), (5.2, 0))
d.add(e.SourceControlledI().at((3.6, 3)).down(3)); txt(d, (4.35, 1.5), '3V₁', 12)
txt(d, (0.45, 3.4), 'I₁ →', 12); txt(d, (4.7, 3.4), '← I₂', 12)
txt(d, (-0.45, 3), '+', 12); txt(d, (-0.45, 0), '−', 13); txt(d, (5.65, 3), '+', 12); txt(d, (5.65, 0), '−', 13)
txt(d, (-0.6, 1.5), 'V₁', 13); txt(d, (5.85, 1.5), 'V₂', 13)
f.save(d, 'd05_q07_vccs')
# Q8: series 2 ohm then shunt 2 ohm
d = f.new()
odot(d, (0, 3), (0, 0), (4.4, 3), (4.4, 0)); dot(d, (3.2, 3), (3.2, 0))
R(d, (0, 3), (3.2, 3), '2 ' + OHM); wire(d, (3.2, 3), (4.4, 3)); wire(d, (0, 0), (4.4, 0)); R(d, (3.2, 3), (3.2, 0), '2 ' + OHM, 'bottom')
txt(d, (-0.45, 1.5), 'port 1', 12); txt(d, (5.4, 1.5), 'port 2', 12)
f.save(d, 'd05_q08_cascade')

# ------------------------------------------------------------------ coupled inductors and their T equivalent
d = f.new(fontsize=14)
odot(d, (0, 3.2), (0, 0), (4.4, 3.2), (4.4, 0))
wire(d, (0, 3.2), (1.2, 3.2)); wire(d, (0, 0), (1.2, 0)); wire(d, (4.4, 3.2), (3.2, 3.2)); wire(d, (4.4, 0), (3.2, 0))
d.add(e.Inductor().at((1.2, 3.2)).down(3.2)); d.add(e.Inductor().at((3.2, 3.2)).down(3.2))
txt(d, (0.55, 1.6), 'L₁', 15); txt(d, (3.85, 1.6), 'L₂', 15)
txt(d, (1.6, 2.75), '●', 12); txt(d, (2.8, 2.75), '●', 12); txt(d, (2.2, 1.6), 'M', 15)
txt(d, (0.55, 3.6), 'i₁ →', 13); txt(d, (3.85, 3.6), '← i₂', 13)
f.panel(d, 'cl')
d = f.new(fontsize=14)
odot(d, (0, 2.4), (0, 0), (6, 2.4), (6, 0)); dot(d, (3, 2.4), (3, 0))
d.add(e.Inductor().endpoints((0, 2.4), (3, 2.4))); d.add(e.Inductor().endpoints((3, 2.4), (6, 2.4)))
d.add(e.Inductor().endpoints((3, 2.4), (3, 0))); wire(d, (0, 0), (6, 0))
txt(d, (1.5, 3.0), 'L₁ − M', 14); txt(d, (4.5, 3.0), 'L₂ − M', 14); txt(d, (3.65, 1.2), 'M', 14)
f.panel(d, 'cte')
f.hstack(['cl', 'cte'], 'd05_coupled', ['coupled inductors (i₁, i₂ both enter the dotted ends)', 'T equivalent (common terminal tied)'])

f.cleanup()
print('done')
