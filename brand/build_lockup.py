"""Compose a logo lockup: your hand-drawn MARK next to the generated wordmark.

Run build_wordmark.py first (it writes wm.json). This places the wordmark beside the mark,
vertically centered, and writes logo-wordmark.svg.

This file is necessarily mark-specific. The default below is monktensor's gradient lemniscate
as a WORKING EXAMPLE. To use it for your project, replace the two blocks marked `### REPLACE`:
the MARK bbox (MK) and the MARK markup (defs + paths). Everything else is generic layout math.

Like the wordmark, two variants are written (the mark is identical, only the wordmark ink flips):
    logo-wordmark.svg       dark ink  -> for LIGHT backgrounds (default)
    logo-wordmark-dark.svg  light ink -> for DARK backgrounds

    uv run --with fonttools python build_lockup.py
    rsvg-convert -w 760 -b white       logo-wordmark.svg      -o /tmp/lockup-light.png
    rsvg-convert -w 760 -b '#14121C'   logo-wordmark-dark.svg -o /tmp/lockup-dark.png
"""
import json

TITLE = "monkway"   # used for the SVG title / aria-label
OUT = "."
wm = json.load(open("wm.json"))
glyphs, s120, xmin, xmax, ymin, ymax = (
    wm["glyphs"], wm["s"], wm["xmin"], wm["xmax"], wm["ymin"], wm["ymax"])
ink_light, ink_dark, accent = wm["ink_light"], wm["ink_dark"], wm["accent"]
upem = 120.0 / s120

PAD = 16

### REPLACE 1 — the mark's visual bounding box, in the mark SVG's own coordinates
MK = dict(x0=23, y0=23, x1=137, y1=137)
###

mk_w0, mk_h0 = MK["x1"] - MK["x0"], MK["y1"] - MK["y0"]
MARK_H = 84.0                  # how tall to render the mark in the lockup
sm = MARK_H / mk_h0
mk_w = mk_w0 * sm

WM_PX = 92.0                   # wordmark cap size; tune so it balances the mark
sw = WM_PX / upem
wm_h = (ymax - ymin) * sw
wm_w = (xmax - xmin) * sw

GAP = 34
H = MARK_H + 2 * PAD
wm_x = PAD + mk_w + GAP
W = wm_x + wm_w + PAD
mark_tx = PAD - MK["x0"] * sm
mark_ty = PAD - MK["y0"] * sm
wm_top = PAD + (MARK_H - wm_h) / 2
# accent glyphs (3rd tuple element) carry their own fill; the rest inherit the group ink
inner = "\n".join(
    f'      <g transform="translate({o:.2f},0)"><path d="{d}"'
    + (f' fill="{accent}"' if acc else "") + "/></g>"
    for o, d, acc in glyphs)

### REPLACE 2 — the mark markup (defs + paths), in its own coordinate space (matching MK)
MARK_DEFS = '''
    <linearGradient id="mwmark" x1="40" y1="130" x2="120" y2="46" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#E9A294"/><stop offset="0.4" stop-color="#C2A4CD"/>
      <stop offset="0.7" stop-color="#A2ABDE"/><stop offset="1" stop-color="#88B2EC"/>
    </linearGradient>'''
MARK_BODY = '''
    <path d="M118,48 A50,50 0 1 0 118,112" stroke="url(#mwmark)" stroke-width="13" stroke-linecap="round" fill="none"/>
    <circle cx="120" cy="80" r="9" fill="#C96F5A"/>'''
###

for fname, ink in (("logo-wordmark.svg", ink_light), ("logo-wordmark-dark.svg", ink_dark)):
    svg = f'''<svg width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{TITLE}">
  <title>{TITLE}</title>
  <defs>{MARK_DEFS}
  </defs>
  <g transform="translate({mark_tx:.2f},{mark_ty:.2f}) scale({sm:.5f})">{MARK_BODY}
  </g>
  <g transform="translate({wm_x:.2f},{wm_top:.2f}) scale({sw:.6f},{-sw:.6f}) translate({-xmin:.2f},{-ymax:.2f})" fill="{ink}">
{inner}
  </g>
</svg>
'''
    open(f"{OUT}/{fname}", "w").write(svg)
print(f"logo-wordmark.svg + logo-wordmark-dark.svg  W={W:.0f} H={H:.0f}  mark_w={mk_w:.0f} wm_w={wm_w:.0f}")
