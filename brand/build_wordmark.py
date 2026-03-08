"""Render a wordmark to SVG with the text converted to vector PATHS.

Why paths: GitHub (and many SVG <img> contexts) strip @font-face / font-family, so a live
`<text font-family="Figtree">` silently falls back to a system font. Baking the glyphs to
paths makes the wordmark render identically everywhere.

Two variants are written so the wordmark works on both light and dark backgrounds:
    wordmark.svg       dark ink  -> for LIGHT backgrounds (the default)
    wordmark-dark.svg  light ink -> for DARK backgrounds
A README/site picks the right one with a <picture> + prefers-color-scheme block (see SKILL.md).
The MARK (mark/lockup glyph) is a gradient and reads on both, so only the wordmark ink flips.

Usage:
    # 1. get the font (a .ttf next to this script). Example, Figtree (variable):
    #    curl -sL -o Figtree.ttf "https://github.com/google/fonts/raw/main/ofl/figtree/Figtree%5Bwght%5D.ttf"
    # 2. edit CONFIG below, then:
    uv run --with fonttools python build_wordmark.py
    # 3. check BOTH (note the -b background to judge contrast):
    rsvg-convert -w 700 -b white wordmark.svg      -o /tmp/wm-light.png   # then open it
    rsvg-convert -w 700 -b '#14121C' wordmark-dark.svg -o /tmp/wm-dark.png
"""
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

# ---- CONFIG (edit these) ----
TEXT = "monkway"        # the wordmark text
FONT = "Figtree.ttf"    # a .ttf next to this script
WEIGHT = 600            # variable-font weight axis; ignored for static fonts
INK_LIGHT = "#322E45"   # dark ink  -> wordmark.svg, for LIGHT backgrounds
INK_DARK = "#F4F1FB"    # light ink -> wordmark-dark.svg, for DARK backgrounds
HIGHLIGHT = "way"       # a substring of TEXT to tint with ACCENT (e.g. "tensor"); "" = none
ACCENT = "#C96F5A"      # highlight color; stays the same in both modes (only INK flips)
FONT_PX = 120.0         # nominal glyph size; only sets the SVG's internal scale
PAD = 8
OUT = "."               # directory to write the wordmarks + wm.json into
# -----------------------------

# which character indices get the accent (first match of HIGHLIGHT in TEXT)
hl = set()
if HIGHLIGHT:
    i = TEXT.find(HIGHLIGHT)
    if i >= 0:
        hl = set(range(i, i + len(HIGHLIGHT)))

f = TTFont(FONT)
if "fvar" in f:         # only variable fonts can be instanced
    instantiateVariableFont(f, {"wght": WEIGHT}, inplace=True)
upem = f["head"].unitsPerEm
cmap = f.getBestCmap()
gs = f.getGlyphSet()
hmtx = f["hmtx"]
s = FONT_PX / upem

# raw glyph outlines (font units, y-up) + cumulative advance offsets.
# each entry: (x-offset, path-d, accent?)  -- accent flag marks HIGHLIGHT glyphs
glyphs = []
off = 0.0
xmin = ymin = 1e9
xmax = ymax = -1e9
for idx, ch in enumerate(TEXT):
    g = cmap[ord(ch)]
    sp = SVGPathPen(gs)
    gs[g].draw(sp)
    d = sp.getCommands()
    if d:
        glyphs.append((off, d, idx in hl))
        bp = BoundsPen(gs)
        gs[g].draw(bp)
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            xmin = min(xmin, x0 + off); xmax = max(xmax, x1 + off)
            ymin = min(ymin, y0); ymax = max(ymax, y1)
    off += hmtx[g][0]

w_px = (xmax - xmin) * s + 2 * PAD
h_px = (ymax - ymin) * s + 2 * PAD


def render(ink):
    # accent glyphs get their own fill; the rest inherit the group's ink
    return "\n".join(
        f'    <g transform="translate({o:.2f},0)"><path d="{d}"'
        + (f' fill="{ACCENT}"' if acc else "") + "/></g>"
        for o, d, acc in glyphs)


# group maps font space -> pixels, y-flipped: translate(pad,pad) scale(s,-s) translate(-xmin,-ymax)
# one SVG per mode; only the base ink flips (accent stays the same)
for fname, ink in (("wordmark.svg", INK_LIGHT), ("wordmark-dark.svg", INK_DARK)):
    grp = (f'<g transform="translate({PAD},{PAD}) scale({s:.6f},{-s:.6f}) '
           f'translate({-xmin:.2f},{-ymax:.2f})" fill="{ink}">')
    with open(f"{OUT}/{fname}", "w") as fh:
        fh.write(
f'''<svg width="{w_px:.0f}" height="{h_px:.0f}" viewBox="0 0 {w_px:.0f} {h_px:.0f}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{TEXT}">
  <title>{TEXT}</title>
  {grp}
{render(ink)}
  </g>
</svg>
''')

# stash metrics so build_lockup.py can place the wordmark next to the mark
import json
with open(f"{OUT}/wm.json", "w") as fh:
    json.dump({"glyphs": glyphs, "s": s, "xmin": xmin, "xmax": xmax,
               "ymin": ymin, "ymax": ymax, "ink_light": INK_LIGHT, "ink_dark": INK_DARK,
               "accent": ACCENT, "upem": upem}, fh)
print(f"wrote wordmark.svg + wordmark-dark.svg  w={w_px:.0f} h={h_px:.0f}  highlight={HIGHLIGHT!r}")
