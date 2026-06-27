#!/usr/bin/env python3
"""Generate the Matching (QueryTarget) and Consolidation diagram family.

Every diagram reuses the robot / router / storage artwork and the loose network
layout of assets/zenoh-location-transparency.svg (itself lifted from
assets/zenoh-query.svg), so the Matching and Consolidation slides stay visually
consistent with it.

Topology (shared by all six diagrams):
    robot ── router1 ──┬── storage1   complete=true,  value t2   (nearest)
                       └── storage3   complete=false, value t1
              router1 ── router2 ──── storage2   complete=true,  value t3 (far)

Matching: the yellow flow(s) show which storages the Get reaches.
    BestMatching -> nearest complete (storage1)            -> 1 reply
    All          -> every matching storage                 -> 3 replies
    AllComplete  -> only complete storages (1 and 2)       -> 2 replies

Consolidation: all three storages reply; each carries a Sample (the card glyph,
assets/svg-components/sample.svg) tagged with its value timestamp t1<t2<t3. The
small number on each card is the order in which that reply reaches the robot
(t2 first, then t1, then t3). The "robot keeps" tray shows what survives:
    None       -> every reply, in arrival order      t2, t1, t3
    Monotonic  -> drop any value older than the last  t2, (t1 dropped), t3
    Latest     -> only the newest value               t3
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "zenoh-query.svg"
ASSETS = ROOT / "assets"

W, H = 600, 372

ROBOT = (96, 290)
ROUTER1 = (252, 298)
ROUTER2 = (450, 286)
STORAGE1 = (190, 182)   # complete=true,  t2, nearest (via router1)
STORAGE3 = (336, 166)   # complete=false, t1          (via router1)
STORAGE2 = (470, 196)   # complete=true,  t3, far      (via router2)

STORAGE_TOP = 62
LABEL_GAP = 20
LINE = 18


def slice_between(text, start_marker, end_open_marker, close_marker="</g>"):
    start = text.index(start_marker)
    anchor = text.index(end_open_marker, start)
    end = text.index(close_marker, anchor) + len(close_marker)
    return text[start:end]


def link(a, b):
    return f"M{a[0]} {a[1]} L{b[0]} {b[1]}"


BASE_LINKS = " ".join([
    link(ROBOT, ROUTER1),
    link(ROUTER1, ROUTER2),
    link(ROUTER1, STORAGE1),
    link(ROUTER1, STORAGE3),
    link(ROUTER2, STORAGE2),
])

FLOW1 = f"M{ROBOT[0]} {ROBOT[1]} L{ROUTER1[0]} {ROUTER1[1]} L{STORAGE1[0]} {STORAGE1[1]}"
FLOW3 = f"M{ROBOT[0]} {ROBOT[1]} L{ROUTER1[0]} {ROUTER1[1]} L{STORAGE3[0]} {STORAGE3[1]}"
FLOW2 = (f"M{ROBOT[0]} {ROBOT[1]} L{ROUTER1[0]} {ROUTER1[1]} "
         f"L{ROUTER2[0]} {ROUTER2[1]} L{STORAGE2[0]} {STORAGE2[1]}")

SYMBOLS = slice_between(SRC.read_text(), '<g id="computer">', '<g id="storage">')

STYLE = """  <style>
    .bg { fill: #f7f7f7; }
    .link { fill: none; stroke: #c7c7c7; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
    .flow { fill: none; stroke: #f5aa00; stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; }
    .endpoint { filter: url(#softShadow); }
    .getLabel, .storageLabel { fill: #f5aa00; font: 700 15px Arial, sans-serif; }
    .key { fill: #85888f; font: 15px Arial, sans-serif; }
    .flag { fill: #85888f; font: 13px Arial, sans-serif; }
    .flag-true { fill: #3a9b4e; font-weight: 700; }
    .flag-false { fill: #c0392b; font-weight: 700; }
    .samp { fill: #0b3a82; font: 700 15px Arial, sans-serif; }
    .order { fill: #fff; font: 700 11px Arial, sans-serif; }
    .trayLabel { fill: #f5aa00; font: 700 13px Arial, sans-serif; }
    .legend { fill: #85888f; font: 12px Arial, sans-serif; }
    .count { fill: #c47f12; font: 700 14px Arial, sans-serif; }
  </style>"""


def document(name, title, desc, body, w=W, h=H):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
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

    <!-- Kept inline for portable rendering; reusable copies live in assets/svg-components/. -->
    {SYMBOLS}
  </defs>

{STYLE}

  <rect class="bg" width="{w}" height="{h}"/>

{body}
</svg>
"""
    (ASSETS / name).write_text(svg)
    print(f"Wrote assets/{name}")


def flows(paths):
    return "\n  ".join(f'<path class="flow" d="{p}"/>' for p in paths)


def storage_use(pos, opacity=1.0):
    op = "" if opacity == 1.0 else f' opacity="{opacity}"'
    return f'    <use href="#storage" x="{pos[0]}" y="{pos[1]}"{op}/>'


def routers_and_robot():
    return (
        '  <g id="routers" class="endpoint">\n'
        f'    <use href="#node" x="{ROUTER1[0]}" y="{ROUTER1[1]}"/>\n'
        f'    <use href="#node" x="{ROUTER2[0]}" y="{ROUTER2[1]}"/>\n'
        '  </g>'
    )


def robot_use():
    return f'    <use href="#robot" x="{ROBOT[0]}" y="{ROBOT[1]}"/>'


# --- Matching (target) labels -------------------------------------------------

def storage_flag_labels(pos, complete, opacity=1.0):
    x = pos[0]
    flag_y = pos[1] - STORAGE_TOP - LABEL_GAP
    key_y = flag_y - LINE
    title_y = key_y - LINE
    value = "true" if complete else "false"
    cls = "flag-true" if complete else "flag-false"
    op = "" if opacity == 1.0 else f' opacity="{opacity}"'
    return (
        f'    <g{op}>\n'
        f'      <text class="storageLabel" text-anchor="middle" x="{x}" y="{title_y}">Storage</text>\n'
        f'      <text class="key" text-anchor="middle" x="{x}" y="{key_y}">warehouse/**</text>\n'
        f'      <text class="flag" text-anchor="middle" x="{x}" y="{flag_y}">complete = '
        f'<tspan class="{cls}">{value}</tspan></text>\n'
        f'    </g>'
    )


def count_badge(n):
    word = "reply" if n == 1 else "replies"
    return (
        '    <g transform="translate(96 228)">\n'
        '      <rect x="-52" y="-14" width="104" height="28" rx="14" fill="#fff7e6" stroke="#f5aa00" stroke-width="1.5"/>\n'
        f'      <text x="0" y="5" text-anchor="middle" class="count">{n} {word}</text>\n'
        '    </g>'
    )


def target_diagram(name, target, paths, n, complete3_opacity=1.0):
    body = "\n".join([
        f'  <g id="base-links"><path class="link" d="{BASE_LINKS}"/></g>',
        "  " + flows(paths),
        routers_and_robot(),
        '  <g id="endpoints" class="endpoint">',
        robot_use(),
        storage_use(STORAGE1),
        storage_use(STORAGE3, complete3_opacity),
        storage_use(STORAGE2),
        "  </g>",
        '  <g id="labels">',
        f'    <text class="getLabel" x="28" y="332">Get (target = {target})</text>',
        '    <text class="key" x="28" y="351">warehouse/robot1/order</text>',
        storage_flag_labels(STORAGE1, True),
        storage_flag_labels(STORAGE3, False, complete3_opacity),
        storage_flag_labels(STORAGE2, True),
        count_badge(n),
        "  </g>",
    ])
    desc = (f"A robot issues a Get for warehouse/robot1/order with target {target}. "
            "Three storages serve warehouse/** (two complete, one incomplete); the "
            f"yellow paths show the {n} storage(s) the request reaches.")
    document(name, f"QueryTarget {target}", desc, body)


# --- Consolidation labels -----------------------------------------------------

def storage_sample(pos, label, dy=86):
    cx, cy = pos[0], pos[1] - dy
    return (
        f'    <g transform="translate({cx} {cy})">\n'
        '      <rect x="-23" y="-15" width="46" height="30" rx="7" fill="#ffffff" stroke="#0b3a82" stroke-width="2"/>\n'
        '      <circle cx="-12" cy="0" r="5.5" fill="#f5aa00"/>\n'
        f'      <text x="7" y="5" text-anchor="middle" class="samp">{label}</text>\n'
        '    </g>'
    )


def tray_card(cx, cy, label, dropped=False):
    op = ' opacity="0.4"' if dropped else ""
    strike = ('\n      <line x1="-21" y1="-13" x2="21" y2="13" stroke="#c0392b" stroke-width="2.5"/>'
              if dropped else "")
    return (
        f'    <g transform="translate({cx} {cy})"{op}>\n'
        '      <rect x="-23" y="-15" width="46" height="30" rx="7" fill="#ffffff" stroke="#0b3a82" stroke-width="2"/>\n'
        '      <circle cx="-12" cy="0" r="5.5" fill="#f5aa00"/>\n'
        f'      <text x="7" y="5" text-anchor="middle" class="samp">{label}</text>{strike}\n'
        '    </g>'
    )


def centered_tray(cx, y, cards, step=46):
    start = cx - (len(cards) - 1) * step / 2
    return "\n".join(
        tray_card(start + i * step, y, label, dropped)
        for i, (label, dropped) in enumerate(cards)
    )


# One combined picture: three storages reply through the routers to three
# robots, each running the same Get for the same key but with a different
# consolidation, so each robot keeps a different set of the same samples. A
# second router carries the right-hand storage and robot, so the topology is
# deliberately a little irregular rather than a symmetric star.
CW, CH = 980, 500
C_S1, C_S2, C_S3 = (200, 160), (470, 145), (805, 165)   # t2, t1, t3
C_ROUTER1 = (430, 275)
C_ROUTER2 = (715, 335)
C_ROBOTS = {"None": (175, 395), "Monotonic": (455, 407), "Latest": (810, 402)}


def consolidation_combined(name="zenoh-consolidation.svg"):
    robots = C_ROBOTS

    def seg(a, b):
        return f"M{a[0]} {a[1]} L{b[0]} {b[1]}"

    flow_paths = [
        seg(C_S1, C_ROUTER1), seg(C_S2, C_ROUTER1), seg(C_S3, C_ROUTER2),
        seg(C_ROUTER1, C_ROUTER2),
        seg(C_ROUTER1, robots["None"]),
        seg(C_ROUTER1, robots["Monotonic"]),
        seg(C_ROUTER2, robots["Latest"]),
    ]

    keeps = {
        "None": [("t2", False), ("t1", False), ("t3", False)],
        "Monotonic": [("t2", False), ("t1", True), ("t3", False)],
        "Latest": [("t3", False)],
    }
    body_lines = ['  <g id="flows">']
    body_lines += [f'    <path class="flow" d="{p}"/>' for p in flow_paths]
    body_lines += ['  </g>', '  <g id="nodes" class="endpoint">',
                   f'    <use href="#node" x="{C_ROUTER1[0]}" y="{C_ROUTER1[1]}"/>',
                   f'    <use href="#node" x="{C_ROUTER2[0]}" y="{C_ROUTER2[1]}"/>',
                   storage_use(C_S1), storage_use(C_S2), storage_use(C_S3)]
    body_lines += [f'    <use href="#robot" x="{p[0]}" y="{p[1]}"/>' for p in robots.values()]
    body_lines += ['  </g>', '  <g id="labels">',
                   storage_sample(C_S1, "t2"),
                   storage_sample(C_S2, "t1"),
                   storage_sample(C_S3, "t3")]
    for mode, pos in robots.items():
        body_lines.append(
            f'    <text class="getLabel" text-anchor="middle" x="{pos[0]}" y="{pos[1] + 27}">'
            f'Get (consolidation = {mode})</text>')
        body_lines.append(centered_tray(pos[0], pos[1] + 56, keeps[mode]))
    body_lines.append('    <text class="legend" text-anchor="middle" x="490" y="486">'
                      'each storage replies with one Sample &#183; t1 &lt; t2 &lt; t3 (newer) &#183; '
                      'they reach the robots in the order t2, t1, t3</text>')
    body_lines.append("  </g>")

    desc = ("Three storages reply with Samples for the same key (t1&lt;t2&lt;t3), reaching the "
            "robots in the order t2, t1, t3. Three robots run the same Get with different "
            "consolidation: None keeps t2, t1, t3; Monotonic drops the stale t1 and keeps t2, t3; "
            "Latest keeps only t3.")
    document(name, "Reply consolidation", desc, "\n".join(body_lines), w=CW, h=CH)


def main():
    # Matching / QueryTarget
    target_diagram("zenoh-target-bestmatching.svg", "BestMatching", [FLOW1], 1)
    target_diagram("zenoh-target-all.svg", "All", [FLOW1, FLOW3, FLOW2], 3)
    target_diagram("zenoh-target-allcomplete.svg", "AllComplete", [FLOW1, FLOW2], 2,
                   complete3_opacity=0.3)

    # Consolidation — one combined picture, three robots (one per mode)
    consolidation_combined("zenoh-consolidation.svg")


if __name__ == "__main__":
    main()
