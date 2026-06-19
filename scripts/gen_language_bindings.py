#!/usr/bin/env python3
"""Generate assets/zenoh-language-bindings.svg.

The diagram geometry is derived from a single unit ``P`` (the side of the
square zenoh-pico block) so the size relationships are exact:

    zenoh-pico : square, side P
    zenoh-c    : 2 * P wide   (twice wider than zenoh-pico)
    zenoh      : 4 * P wide   (twice wider than zenoh-c)
    zenoh-cpp  : 2 * P wide   (covers zenoh-pico + half of zenoh-c)

The language logos are sourced from the reusable components in
assets/svg-components/ (rust.svg, c.svg, cpp.svg) and inlined here so the
composite renders standalone in the GitHub README.

Run: python3 scripts/gen_language_bindings.py
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMP = ROOT / "assets" / "svg-components"
OUT = ROOT / "assets" / "zenoh-language-bindings.svg"

LOGO_VB = {"rust": "0 0 256 256", "c": "0 0 256 288", "cpp": "0 0 256 288"}


def load_logo(key):
    txt = (COMP / f"{key}.svg").read_text()
    g = re.search(r'(<g id="' + key + r'-logo">.*?</g>)', txt, re.DOTALL).group(1)
    return "      " + g.strip()


logo_defs = "\n".join(load_logo(k) for k in ("rust", "c", "cpp"))

# ---- geometry: everything is derived from the pico square side P ----
P = 150                      # zenoh-pico is square with side P
H = P                        # each block is one P-high row
PAD = 40

W_pico = P
W_c = 2 * W_pico             # zenoh-c twice wider than zenoh-pico
W_zenoh = 2 * W_c            # zenoh twice wider than zenoh-c  (= 4P)
W_cpp = W_pico + W_c // 2    # covers zenoh-pico + half of zenoh-c (= 2P)

x0 = PAD
y_top = 96                   # zenoh-cpp row
y_mid = y_top + H            # zenoh-pico + zenoh-c row
y_bot = y_mid + H            # zenoh row

VB_W = x0 + W_zenoh + PAD
VB_H = y_bot + H + PAD

RX = 16    # rounded corners on each block
GAP = 7    # inset per side; adjacent blocks end up 2*GAP apart while the
           # P-based grid (and therefore the size ratios) stays exact

STYLE = {
    "rust": dict(grad="grad-rust", stroke="#C44B22", label="#5A2A14", sub="#9C5C3D"),
    "c":    dict(grad="grad-c",    stroke="#5B7CA6", label="#1F3A5F", sub="#5E7CA3"),
    "cpp":  dict(grad="grad-cpp",  stroke="#00599C", label="#013E70", sub="#3C6FA6"),
}

# (x, y, w, h, logo_key, name, sublabel)
BLOCKS = [
    (x0,          y_top, W_cpp,   H, "cpp",  "zenoh-cpp",  "C++ WRAPPER"),
    (x0,          y_mid, W_pico,  H, "c",    "zenoh-pico", "C · EMBEDDED"),
    (x0 + W_pico, y_mid, W_c,     H, "c",    "zenoh-c",    "C BINDING"),
    (x0,          y_bot, W_zenoh, H, "rust", "zenoh",      "RUST · CORE"),
]


def tile(bx, by, bw, bh, key, *_):
    st = STYLE[key]
    ix, iy, iw, ih = bx + GAP, by + GAP, bw - 2 * GAP, bh - 2 * GAP
    return (f'    <rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{RX}" '
            f'fill="url(#{st["grad"]})" stroke="{st["stroke"]}" stroke-width="2" '
            f'filter="url(#softShadow)"/>\n')


def content(bx, by, bw, bh, key, name, sublabel):
    st = STYLE[key]
    bx, by, bw, bh = bx + GAP, by + GAP, bw - 2 * GAP, bh - 2 * GAP
    if bw >= 1.6 * bh:  # wide block: logo left, label to the right
        logo_sz = 62
        lx = bx + 26
        ly = by + (bh - logo_sz) / 2
        tx = lx + logo_sz + 18
        cy = by + bh / 2
        return (
            f'  <svg x="{lx}" y="{ly}" width="{logo_sz}" height="{logo_sz}" '
            f'viewBox="{LOGO_VB[key]}" preserveAspectRatio="xMidYMid meet"><use href="#{key}-logo"/></svg>\n'
            f'  <text x="{tx}" y="{cy - 7}" font-size="27" font-weight="700" '
            f'fill="{st["label"]}" dominant-baseline="middle">{name}</text>\n'
            f'  <text x="{tx}" y="{cy + 18}" font-size="14" font-weight="600" letter-spacing="1.5" '
            f'fill="{st["sub"]}" dominant-baseline="middle">{sublabel}</text>\n'
        )
    # square block: logo on top, label centered below
    logo_sz = 54
    cx = bx + bw / 2
    lx = cx - logo_sz / 2
    ly = by + 26
    ty = ly + logo_sz + 26
    return (
        f'  <svg x="{lx}" y="{ly}" width="{logo_sz}" height="{logo_sz}" '
        f'viewBox="{LOGO_VB[key]}" preserveAspectRatio="xMidYMid meet"><use href="#{key}-logo"/></svg>\n'
        f'  <text x="{cx}" y="{ty}" font-size="21" font-weight="700" text-anchor="middle" '
        f'fill="{st["label"]}" dominant-baseline="middle">{name}</text>\n'
        f'  <text x="{cx}" y="{ty + 20}" font-size="12" font-weight="600" letter-spacing="1.2" '
        f'text-anchor="middle" fill="{st["sub"]}" dominant-baseline="middle">{sublabel}</text>\n'
    )


tiles_svg = "".join(tile(*b) for b in BLOCKS)
content_svg = "".join(content(*b) for b in BLOCKS)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}"
     role="img" aria-labelledby="title desc" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <title id="title">Zenoh language bindings</title>
  <desc id="desc">Size-scaled diagram of Zenoh language bindings: the wide Rust core (zenoh), the zenoh-c C binding (twice the width of the square zenoh-pico), the standalone pure-C zenoh-pico, and the zenoh-cpp C++ wrapper covering zenoh-pico and half of zenoh-c.</desc>
  <defs>
    <linearGradient id="grad-rust" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#FCEFE7"/><stop offset="1" stop-color="#F4CBB3"/>
    </linearGradient>
    <linearGradient id="grad-c" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#F0F5FA"/><stop offset="1" stop-color="#C9DCED"/>
    </linearGradient>
    <linearGradient id="grad-cpp" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#E9F2FC"/><stop offset="1" stop-color="#B8D4EF"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0b2547" flood-opacity=".22"/>
    </filter>

    <!-- Language logos kept inline for GitHub README rendering; reusable copies live in assets/svg-components/. -->
{logo_defs}
  </defs>

  <rect x="14" y="14" width="{VB_W - 28}" height="{VB_H - 28}" rx="22"
        fill="#FBFCFE" stroke="#E7ECF3" stroke-width="1.5"/>

  <text x="{VB_W / 2}" y="58" text-anchor="middle" font-size="30" font-weight="800" fill="#0B2547">Zenoh language bindings</text>

{tiles_svg}{content_svg}</svg>
'''

OUT.write_text(svg)
print(f"wrote {OUT} ({len(svg)} bytes), viewBox 0 0 {VB_W} {VB_H}")
print(f"widths  pico={W_pico} c={W_c} zenoh={W_zenoh} cpp={W_cpp}  (P={P})")
