#!/usr/bin/env python3
"""Generate the static "location transparency" infographic.

The reusable node artwork (computer / router node / robot / storage) and the
ZettaScale wordmark are lifted verbatim from assets/zenoh-query.svg so this
diagram stays visually identical to the animated query/reply demo. The result
is a self-contained, animation-free SVG suitable for the README.

Layout: storages sit on top, routers below them, and the robot shares the
routers' row. Positions are deliberately a little irregular (no perfect grid)
to match the loose, hand-placed feel of the other diagrams.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "zenoh-query.svg"
OUT = ROOT / "assets" / "zenoh-location-transparency.svg"

W, H = 600, 372

# use point = anchor passed to <use>; for storages it is the bottom of the stack.
ROBOT = (96, 290)
ROUTER1 = (252, 298)
ROUTER2 = (450, 286)
STORAGE1 = (190, 182)   # complete = true  (best match -> data path)
STORAGE3 = (336, 166)   # complete = false (also on router1, not chosen)
STORAGE2 = (470, 196)   # complete = true  (on router2, farther away)

# A storage stack reaches ~62px above its use point; labels sit above that.
STORAGE_TOP = 62
LABEL_GAP = 20          # gap between the bottom label line and the storage top
LINE = 18               # label line height


def slice_between(text, start_marker, end_open_marker, close_marker="</g>"):
    start = text.index(start_marker)
    anchor = text.index(end_open_marker, start)
    end = text.index(close_marker, anchor) + len(close_marker)
    return text[start:end]


def link(a, b):
    return f"M{a[0]} {a[1]} L{b[0]} {b[1]}"


def storage_labels(pos, complete):
    x = pos[0]
    flag_y = pos[1] - STORAGE_TOP - LABEL_GAP
    key_y = flag_y - LINE
    title_y = key_y - LINE
    value = "true" if complete else "false"
    cls = "flag-true" if complete else "flag-false"
    return (
        f'    <text class="storageLabel" text-anchor="middle" x="{x}" y="{title_y}">Storage</text>\n'
        f'    <text class="key" text-anchor="middle" x="{x}" y="{key_y}">warehouse/**</text>\n'
        f'    <text class="flag" text-anchor="middle" x="{x}" y="{flag_y}">complete = '
        f'<tspan class="{cls}">{value}</tspan></text>'
    )


def main():
    src = SRC.read_text()

    # computer + router node + robot + storage symbols (consecutive in defs).
    symbols = slice_between(src, "<g id=\"computer\">", "<g id=\"storage\">")

    links = " ".join([
        link(ROBOT, ROUTER1),
        link(ROUTER1, ROUTER2),
        link(ROUTER1, STORAGE1),
        link(ROUTER1, STORAGE3),
        link(ROUTER2, STORAGE2),
    ])
    flow = f"M{ROBOT[0]} {ROBOT[1]} L{ROUTER1[0]} {ROUTER1[1]} L{STORAGE1[0]} {STORAGE1[1]}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Zenoh location transparency</title>
  <desc id="desc">A robot issues a Get for the key warehouse/robot1/order with target BestMatching. Three storages serve warehouse/**: two are complete and one is incomplete. Zenoh routes the request to the nearest complete storage. Gray lines show the network links; the yellow line shows the path the data actually travels from the robot through the nearest router up to that storage.</desc>
  <defs>
    <linearGradient id="node-fill" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#62bfff"/>
      <stop offset="1" stop-color="#247fbd"/>
    </linearGradient>
    <linearGradient id="storage-fill" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#62bfff"/>
      <stop offset="1" stop-color="#247fbd"/>
    </linearGradient>
    <linearGradient id="robot-fill" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#5bbcff"/>
      <stop offset="1" stop-color="#1f78c9"/>
    </linearGradient>
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.5" flood-color="#0b2547" flood-opacity=".25"/>
    </filter>

    <!-- Kept inline for portable README rendering; reusable copies live in assets/svg-components/. -->
    {symbols}
  </defs>

  <style>
    .bg {{ fill: #f7f7f7; }}
    .link {{ fill: none; stroke: #c7c7c7; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
    .flow {{ fill: none; stroke: #f5aa00; stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; }}
    .endpoint {{ filter: url(#softShadow); }}
    .getLabel, .storageLabel {{ fill: #f5aa00; font: 700 15px Arial, sans-serif; }}
    .key {{ fill: #85888f; font: 15px Arial, sans-serif; }}
    .flag {{ fill: #85888f; font: 13px Arial, sans-serif; }}
    .flag-true {{ fill: #3a9b4e; font-weight: 700; }}
    .flag-false {{ fill: #c0392b; font-weight: 700; }}
  </style>

  <rect class="bg" width="{W}" height="{H}"/>

  <g id="base-links">
    <path class="link" d="{links}"/>
  </g>

  <path class="flow" d="{flow}"/>

  <g id="routers" class="endpoint">
    <use href="#node" x="{ROUTER1[0]}" y="{ROUTER1[1]}"/>
    <use href="#node" x="{ROUTER2[0]}" y="{ROUTER2[1]}"/>
  </g>

  <g id="endpoints" class="endpoint">
    <use href="#robot" x="{ROBOT[0]}" y="{ROBOT[1]}"/>
    <use href="#storage" x="{STORAGE1[0]}" y="{STORAGE1[1]}"/>
    <use href="#storage" x="{STORAGE3[0]}" y="{STORAGE3[1]}"/>
    <use href="#storage" x="{STORAGE2[0]}" y="{STORAGE2[1]}"/>
  </g>

  <g id="labels">
    <text class="getLabel" x="28" y="332">Get (target = BestMatching)</text>
    <text class="key" x="28" y="351">warehouse/robot1/order</text>

{storage_labels(STORAGE1, True)}

{storage_labels(STORAGE3, False)}

{storage_labels(STORAGE2, True)}
  </g>
</svg>
"""

    OUT.write_text(svg)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
