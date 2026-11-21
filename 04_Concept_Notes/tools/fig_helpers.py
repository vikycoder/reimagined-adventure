"""Shared drawing helpers for the concept-note figures.

    from fig_helpers import Figs
    f = Figs('../figures')          # output folder
    d = f.new(); ...; f.save(d, 'name')          # schemdraw circuit  -> name.png
    fig, ax = f.plot(); ...; f.savefig(fig, 'name')   # matplotlib plot -> name.png

Needs: pip install schemdraw matplotlib numpy
"""
import os
import shutil

import matplotlib
matplotlib.rcParams['figure.max_open_warning'] = 0
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as e

schemdraw.use('matplotlib')

# one consistent look for every plot
plt.rcParams.update({
    'font.size': 12, 'axes.grid': True, 'grid.alpha': 0.3, 'axes.spines.top': False,
    'axes.spines.right': False, 'lines.linewidth': 2, 'figure.facecolor': 'white',
})
COLORS = ['#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9467bd', '#8c564b']


class Figs:
    def __init__(self, out_dir):
        self.out = os.path.abspath(out_dir)
        os.makedirs(self.out, exist_ok=True)

    # ---- circuits (schemdraw) ----
    @staticmethod
    def new(unit=3, fontsize=13):
        d = schemdraw.Drawing(show=False)
        d.config(fontsize=fontsize, unit=unit)
        return d

    def save(self, d, name):
        d.save(os.path.join(self.out, name + '.png'), dpi=110, transparent=False)

    @staticmethod
    def loop(d, x, y, text, cw=True, size=0.9):
        """Mesh-current arrow centred at (x, y)."""
        d.add(e.LoopArrow(direction='cw' if cw else 'ccw', width=size, height=size)
              .at((x, y)).anchor('center').label(text, loc='center', fontsize=12))


    # ---- multi-panel figures: draw each panel with panel(), then stitch with hstack() ----
    def panel(self, d, name):
        """Save a schemdraw panel to a temporary folder (not part of the published figures)."""
        tmp = os.path.join(self.out, '_panels')
        os.makedirs(tmp, exist_ok=True)
        d.save(os.path.join(tmp, name + '.png'), dpi=110, transparent=False)

    def panel_fig(self, fig, name):
        """Save a matplotlib figure as a panel (same temporary folder as panel())."""
        tmp = os.path.join(self.out, '_panels')
        os.makedirs(tmp, exist_ok=True)
        fig.savefig(os.path.join(tmp, name + '.png'), dpi=110, bbox_inches='tight', facecolor='white')
        plt.close(fig)

    def hstack(self, names, out, captions=None, pad=24, line_h=26):
        """Stitch panels side by side; captions may contain newlines; writes <out>.png."""
        from PIL import Image, ImageDraw, ImageFont
        import matplotlib.font_manager as fm
        tmp = os.path.join(self.out, '_panels')
        ims = [Image.open(os.path.join(tmp, n + '.png')).convert('RGB') for n in names]
        H = max(i.height for i in ims)
        n_lines = max((c.count('\n') + 1 for c in captions), default=0) if captions else 0
        W = sum(i.width for i in ims) + pad * (len(ims) + 1)
        canvas = Image.new('RGB', (W, H + n_lines * line_h + 2 * pad), 'white')
        font = ImageFont.truetype(fm.findfont('DejaVu Sans'), 20)
        draw = ImageDraw.Draw(canvas)
        x = pad
        for k, im in enumerate(ims):
            canvas.paste(im, (x, pad + (H - im.height) // 2))
            if captions:
                for j, line in enumerate(captions[k].split('\n')):
                    tw = draw.textlength(line, font=font)
                    draw.text((x + (im.width - tw) / 2, pad + H + 8 + j * line_h), line, fill='black', font=font)
            x += im.width + pad
        canvas.save(os.path.join(self.out, out + '.png'))

    def cleanup(self):
        shutil.rmtree(os.path.join(self.out, '_panels'), ignore_errors=True)

    # ---- plots (matplotlib) ----
    @staticmethod
    def plot(figsize=(6.4, 3.6), **kw):
        return plt.subplots(figsize=figsize, **kw)

    def savefig(self, fig, name):
        fig.savefig(os.path.join(self.out, name + '.png'), dpi=110, bbox_inches='tight', facecolor='white')
        plt.close(fig)
