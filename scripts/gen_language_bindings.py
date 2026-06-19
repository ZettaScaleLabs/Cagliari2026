#!/usr/bin/env python3
"""Generate assets/zenoh-language-bindings.svg.

The diagram geometry is derived from a single unit ``P`` (the width of the
zenoh-pico pillar) so the size relationships are exact:

    zenoh-pico : P wide, 2 * P tall  (a standalone pillar that stands on the
                 ground, independent of the Rust core)
    zenoh-c    : 2 * P wide
    zenoh      : the Rust core, fills the rest of the bottom row (3 * P wide)
    zenoh-cpp  : 2 * P wide   (covers zenoh-pico + half of zenoh-c)

The language logos are sourced from the reusable components in
assets/svg-components/ (rust.svg, c.svg, cpp.svg, go.svg) and inlined here so
the composite renders standalone in the GitHub README.

Run: python3 scripts/gen_language_bindings.py
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMP = ROOT / "assets" / "svg-components"
OUT = ROOT / "assets" / "zenoh-language-bindings.svg"

LOGO_VB = {
    "rust": "0 0 256 256", "c": "0 0 256 288", "cpp": "0 0 256 288", "go": "0 0 512 192",
    "python": "0 0 256 255", "java": "0 0 256 346", "kotlin": "0 0 106 113",
    "ts": "0 0 256 256", "server": "-31 -20 62 44",
}


def load_logo(key):
    txt = (COMP / f"{key}.svg").read_text()
    g = re.search(r'(<g id="' + key + r'-logo">.*?</g>)', txt, re.DOTALL).group(1)
    return "      " + g.strip()


logo_defs = "\n".join(load_logo(k) for k in ("rust", "c", "cpp", "go", "python", "java", "kotlin", "ts", "server"))

# ---- geometry: everything is derived from the pico square side P ----
P = 150                      # zenoh-pico is square with side P
H = P                        # each block is one P-high row
H_pico = 2 * H               # zenoh-pico pillar spans the mid row to the ground
PAD = 40

W_pico = P
W_c = 2 * W_pico             # zenoh-c twice wider than zenoh-pico
W_zenoh = 2 * W_c            # zenoh twice wider than zenoh-c  (= 4P)
W_cpp = W_pico + W_c // 2    # covers zenoh-pico + half of zenoh-c (= 2P)

x0 = PAD
y_top = PAD                  # zenoh-cpp row (top of the diagram; no title above)
y_mid = y_top + H            # zenoh-pico + zenoh-c row
y_bot = y_mid + H            # zenoh row

# Right-side bindings (python, java, kotlin) are tall pillars that stand ON the
# Rust core: each is W_pico wide and H_pico tall, resting on top of the zenoh
# block to the right of zenoh-c.
right_x0 = x0 + W_pico + W_c          # first right pillar starts after zenoh-c
RIGHT = ["python", "java", "kotlin"]
pillars_end = right_x0 + len(RIGHT) * W_pico

# zenoh-ts does not sit directly on Rust: it reaches the core through a
# WebSocket bridge. The bridge is a square box resting on the Rust core, and
# zenoh-ts is a square box resting on the bridge (so the column is two stacked
# squares, the same total height as the language pillars beside it).
x_ts = pillars_end
right_end = x_ts + W_pico
W_rust = right_end - (x0 + W_pico)    # rust spans from zenoh-pico under the TS column

VB_W = right_end + PAD
VB_H = y_bot + H + PAD

RX = 16    # rounded corners on each block
GAP = 7    # inset per side; adjacent blocks end up 2*GAP apart while the
           # P-based grid (and therefore the size ratios) stays exact

STYLE = {
    "rust":   dict(grad="grad-rust",   stroke="#C44B22", label="#5A2A14", sub="#9C5C3D"),
    "c":      dict(grad="grad-c",      stroke="#5B7CA6", label="#1F3A5F", sub="#5E7CA3"),
    "cpp":    dict(grad="grad-cpp",    stroke="#00599C", label="#013E70", sub="#3C6FA6"),
    "go":     dict(grad="grad-go",     stroke="#0095BD", label="#0A4A5A", sub="#2E8AA8"),
    "python": dict(grad="grad-python", stroke="#3776AB", label="#244E7A", sub="#4B79A8"),
    "java":   dict(grad="grad-java",   stroke="#E76F00", label="#9C4E00", sub="#C06A1E"),
    "kotlin": dict(grad="grad-kotlin", stroke="#7F52FF", label="#5B2ECC", sub="#7E5AD6"),
    "ts":     dict(grad="grad-ts",     stroke="#2D6CB5", label="#1C4477", sub="#3D6CA6"),
    "server": dict(grad="grad-server", stroke="#7287A0", label="#33414F", sub="#5B6B7D"),
}

# (x, y, w, h, logo_key, name)
BLOCKS = [
    (x0,            y_top, W_cpp,   H,      "cpp",  "zenoh-cpp"),
    (x0 + W_cpp,    y_top, W_pico,  H,      "go",   "zenoh-go"),
    (x0,            y_mid, W_pico,  H_pico, "c",    "zenoh-pico"),
    (x0 + W_pico,   y_mid, W_c,     H,      "c",    "zenoh-c"),
    (x0 + W_pico,   y_bot, W_rust,  H,      "rust", "zenoh"),
    # zenoh-ts reaches the Rust core through a WebSocket bridge, not directly.
    (x_ts,          y_top, W_pico,  H,      "ts",     "zenoh-ts"),
    (x_ts,          y_mid, W_pico,  H,      "server", "websocket bridge"),
]
# python / java / kotlin: tall pillars standing on the Rust core, to the right.
for i, key in enumerate(RIGHT):
    BLOCKS.append((right_x0 + i * W_pico, y_top, W_pico, H_pico, key, f"zenoh-{key}"))


def tile(bx, by, bw, bh, key, *_):
    st = STYLE[key]
    ix, iy, iw, ih = bx + GAP, by + GAP, bw - 2 * GAP, bh - 2 * GAP
    return (f'    <rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{RX}" '
            f'fill="url(#{st["grad"]})" stroke="{st["stroke"]}" stroke-width="2" '
            f'filter="url(#softShadow)"/>\n')


def content(bx, by, bw, bh, key, name):
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
            f'  <text x="{tx}" y="{cy}" font-size="27" font-weight="700" '
            f'fill="{st["label"]}" dominant-baseline="middle">{name}</text>\n'
        )
    if bh >= 1.6 * bw:  # tall block: logo on top, label rotated vertically
        logo_sz = 56
        cx = bx + bw / 2
        lx = cx - logo_sz / 2
        ly = by + 22
        tcy = (ly + logo_sz + by + bh) / 2
        return (
            f'  <svg x="{lx}" y="{ly}" width="{logo_sz}" height="{logo_sz}" '
            f'viewBox="{LOGO_VB[key]}" preserveAspectRatio="xMidYMid meet"><use href="#{key}-logo"/></svg>\n'
            f'  <text x="{cx}" y="{tcy}" font-size="27" font-weight="700" text-anchor="middle" '
            f'fill="{st["label"]}" dominant-baseline="middle" transform="rotate(-90 {cx} {tcy})">{name}</text>\n'
        )
    # square block: logo on top, label centered below (wrap a 2-word label)
    logo_sz = 54
    text_h = 21
    gap_between = 16
    line_gap = 22
    lines = name.split(" ") if " " in name else [name]
    group_h = logo_sz + gap_between + text_h + (line_gap if len(lines) > 1 else 0)
    cx = bx + bw / 2
    lx = cx - logo_sz / 2
    ly = by + (bh - group_h) / 2
    ty = ly + logo_sz + gap_between + text_h / 2
    label = "".join(
        f'  <text x="{cx}" y="{ty + i * line_gap}" font-size="21" font-weight="700" '
        f'text-anchor="middle" fill="{st["label"]}" dominant-baseline="middle">{ln}</text>\n'
        for i, ln in enumerate(lines)
    )
    return (
        f'  <svg x="{lx}" y="{ly}" width="{logo_sz}" height="{logo_sz}" '
        f'viewBox="{LOGO_VB[key]}" preserveAspectRatio="xMidYMid meet"><use href="#{key}-logo"/></svg>\n'
        + label
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
    <linearGradient id="grad-go" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#E6F7FB"/><stop offset="1" stop-color="#ABE4F1"/>
    </linearGradient>
    <linearGradient id="grad-python" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#EAF2FB"/><stop offset="1" stop-color="#CADEF2"/>
    </linearGradient>
    <linearGradient id="grad-java" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#FBF0E6"/><stop offset="1" stop-color="#F3D9BE"/>
    </linearGradient>
    <linearGradient id="grad-kotlin" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#F3ECFC"/><stop offset="1" stop-color="#DBC9F5"/>
    </linearGradient>
    <linearGradient id="grad-ts" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#E7F0FA"/><stop offset="1" stop-color="#C2DAF1"/>
    </linearGradient>
    <linearGradient id="grad-server" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#EEF2F6"/><stop offset="1" stop-color="#D3DDE7"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0b2547" flood-opacity=".22"/>
    </filter>

    <!-- Language logos kept inline for GitHub README rendering; reusable copies live in assets/svg-components/. -->
{logo_defs}
  </defs>

  <rect x="14" y="14" width="{VB_W - 28}" height="{VB_H - 28}" rx="22"
        fill="#FBFCFE" stroke="#E7ECF3" stroke-width="1.5"/>

{tiles_svg}{content_svg}</svg>
'''

OUT.write_text(svg)
print(f"wrote {OUT} ({len(svg)} bytes), viewBox 0 0 {VB_W} {VB_H}")
print(f"widths  pico={W_pico} c={W_c} zenoh={W_zenoh} cpp={W_cpp}  (P={P})")
