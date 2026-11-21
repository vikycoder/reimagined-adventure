"""Regenerates the Day 6 figures in ../figures (prefix d06_).   Needs: schemdraw matplotlib pillow"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))

import schemdraw.elements as e
from fig_helpers import Figs

f = Figs(os.path.join(HERE, '..', 'figures'))
OHM = 'Ω'


def txt(d, xy, s, fs=12):
    d.add(e.Label().at(xy).label(s, fontsize=fs))


def dot(d, *pts):
    for p in pts:
        d.add(e.Dot().at(p))


def odot(d, *pts):
    for p in pts:
        d.add(e.Dot(open=True).at(p))


def wire(d, a, b):
    d.add(e.Line().at(a).to(b))


def R(d, a, b, label=None, side='top'):
    el = e.Resistor().endpoints(a, b)
    d.add(el.label(label, loc=side) if label else el)


# ------------------------------------------------------------------ mock test Q16: dependent current source 0.25 V_x
d = f.new()
d.add(e.SourceV().at((0, 0)).up(3)); txt(d, (-1.0, 1.5), '12 V', 12)
wire(d, (0, 3), (0.5, 3)); R(d, (0.5, 3), (3.0, 3), '2 ' + OHM); wire(d, (3.0, 3), (3.6, 3)); wire(d, (3.6, 3), (6.0, 3))
R(d, (3.6, 3), (3.6, 0), '4 ' + OHM, 'bottom'); wire(d, (0, 0), (6.0, 0))
d.add(e.SourceControlledI().at((6.0, 3)).down(3)); txt(d, (7.35, 1.5), '0.25 V_x', 12)
dot(d, (3.6, 3), (3.6, 0), (6.0, 3), (6.0, 0))
txt(d, (3.0, 1.5), '+', 12); txt(d, (3.0, 0.45), '−', 13); txt(d, (2.5, 1.0), 'V_x', 12)
f.save(d, 'd06_q16_dependent')

# ------------------------------------------------------------------ mock test Q17: Thevenin with a CCCS
d = f.new()
d.add(e.SourceV().at((0, 0)).up(3)); txt(d, (-1.0, 1.5), '20 V', 12)
wire(d, (0, 3), (0.5, 3)); R(d, (0.5, 3), (3.0, 3), '4 ' + OHM); wire(d, (3.0, 3), (3.6, 3)); wire(d, (3.6, 3), (7.0, 3))
R(d, (3.6, 3), (3.6, 0), '2 ' + OHM, 'bottom'); wire(d, (0, 0), (7.0, 0))
d.add(e.SourceControlledI().at((5.2, 0)).up(3)); txt(d, (6.35, 1.5), '1·i₁', 12)
dot(d, (3.6, 3), (3.6, 0), (5.2, 3), (5.2, 0)); odot(d, (7.0, 3), (7.0, 0))
txt(d, (1.75, 2.55), 'i₁ →', 12); txt(d, (7.45, 3.0), 'a', 13); txt(d, (7.45, 0), 'b', 13)
f.save(d, 'd06_q17_thevenin')

# ------------------------------------------------------------------ mixed question 2: a floating source between two nodes
d = f.new()
d.add(e.SourceI().at((0, 0)).up(3)); txt(d, (-0.9, 1.5), '6 A', 12)
wire(d, (0, 3), (1.6, 3)); dot(d, (1.6, 3), (1.6, 0), (4.8, 3), (4.8, 0))
R(d, (1.6, 3), (1.6, 0), '2 ' + OHM, 'bottom')
d.add(e.SourceV().endpoints((4.8, 3), (1.6, 3))); txt(d, (3.2, 4.05), '6 V', 12)
R(d, (4.8, 3), (4.8, 0), '4 ' + OHM, 'bottom'); wire(d, (0, 0), (4.8, 0))
txt(d, (1.15, 3.4), '1', 13); txt(d, (5.25, 3.4), '2', 13)
f.save(d, 'd06_m02_supernode')

f.cleanup()
print('done')
