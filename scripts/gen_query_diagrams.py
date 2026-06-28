#!/usr/bin/env python3
"""Generate the Matching (QueryTarget) and Consolidation diagrams.

Both are single combined pictures that reuse the robot / router / storage artwork
and the loose network layout of assets/zenoh-location-transparency.svg (itself
lifted from assets/zenoh-query.svg), so the two slides stay visually consistent
with it and with each other.

Shared template: three storages on top, two routers in the middle, three robots
at the bottom — each robot runs the same Get but with a different parameter, so
the three behave differently on one identical network.

Matching (assets/zenoh-matching.svg): each robot uses a different QueryTarget.
Its request path is drawn in its own colour (red / green / blue), and overlapping
paths are drawn as parallel lanes so all three stay visible. Each
storage holds one Sample (A / B / C) and is marked complete or partial; the tray
under a robot shows the Samples that target collects:
    BestMatching -> nearest complete storage           -> A
    All          -> every matching storage             -> A, B, C
    AllComplete  -> only the complete storages          -> A, B

Consolidation (assets/zenoh-consolidation.svg): each robot uses a different
consolidation. The storages reply with Samples for the same key tagged t1<t2<t3,
reaching the robots in the order t2, t1, t3; the tray shows what survives:
    None       -> every reply, in arrival order      t2, t1, t3
    Monotonic  -> drop any value older than the last  t2, (t1 dropped), t3
    Latest     -> only the newest value               t3
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "zenoh-query.svg"
ASSETS = ROOT / "assets"

W, H = 980, 500


def slice_between(text, start_marker, end_open_marker, close_marker="</g>"):
    start = text.index(start_marker)
    anchor = text.index(end_open_marker, start)
    end = text.index(close_marker, anchor) + len(close_marker)
    return text[start:end]


SYMBOLS = slice_between(SRC.read_text(), '<g id="computer">', '<g id="storage">')

STYLE = """  <style>
    .bg { fill: #f7f7f7; }
    .flow { fill: none; stroke: #f5aa00; stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; }
    .req { fill: none; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }
    .endpoint { filter: url(#softShadow); }
    .getLabel { fill: #f5aa00; font: 700 15px Arial, sans-serif; }
    .flag { fill: #85888f; font: 700 13px Arial, sans-serif; }
    .flag-true { fill: #3a9b4e; font-weight: 700; }
    .flag-false { fill: #c0392b; font-weight: 700; }
    .samp { fill: #0b3a82; font: 700 15px Arial, sans-serif; }
    .legend { fill: #85888f; font: 12px Arial, sans-serif; }
  </style>"""


def document(name, title, desc, body, w=W, h=H):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
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


# --- shared building blocks ---------------------------------------------------

def storage_use(pos, opacity=1.0):
    op = "" if opacity == 1.0 else f' opacity="{opacity}"'
    return f'    <use href="#storage" x="{pos[0]}" y="{pos[1]}"{op}/>'


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


def get_label(cx, y, text):
    return (f'    <text class="getLabel" text-anchor="middle" x="{cx}" y="{y}">{text}</text>')


# A second router carries the right-hand storage and robot, so the topology is
# deliberately a little irregular rather than a symmetric star. Both diagrams use
# the same coordinates so the slides line up.
S1, S2, S3 = (200, 160), (470, 145), (805, 165)
R1, R2 = (430, 275), (715, 335)
ROBOT_L, ROBOT_C, ROBOT_R = (175, 395), (455, 407), (810, 401)


def routers():
    return ('  <g id="routers" class="endpoint">\n'
            f'    <use href="#node" x="{R1[0]}" y="{R1[1]}"/>\n'
            f'    <use href="#node" x="{R2[0]}" y="{R2[1]}"/>\n'
            '  </g>')


# --- Matching -----------------------------------------------------------------

MATCH_NODES = {"S1": S1, "S2": S2, "S3": S3, "R1": R1, "R2": R2,
               "BM": ROBOT_L, "ALL": ROBOT_C, "AC": ROBOT_R}
LANE_GAP = 8

# lane: a stable offset rank so each request keeps the same side on every shared
# link; All sits in the centre lane and keeps the default flow colour.
REQUESTS = [
    ("BestMatching", dict(lane=-1, color="#e03131",
                          routes=[["BM", "R1", "S1"]],
                          tray=[("A", False)])),
    ("All", dict(lane=0, color="#2f9e44",
                 routes=[["ALL", "R1", "S1"], ["ALL", "R1", "S2"], ["ALL", "R1", "R2", "S3"]],
                 tray=[("A", False), ("B", False), ("C", False)])),
    ("AllComplete", dict(lane=1, color="#1c7ed6",
                         routes=[["AC", "R2", "R1", "S1"], ["AC", "R2", "R1", "S2"]],
                         tray=[("A", False), ("B", False)])),
]
MATCH_ROBOT = {"BestMatching": "BM", "All": "ALL", "AllComplete": "AC"}


def _perp(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = (dx * dx + dy * dy) ** 0.5
    return (-dy / length, dx / length)


def _offset_segment(n1, n2, lane):
    # canonical node order keeps the perpendicular (hence the lane side) stable
    a, b = sorted((n1, n2))
    pa, pb = MATCH_NODES[a], MATCH_NODES[b]
    nx, ny = _perp(pa, pb)
    o = lane * LANE_GAP
    return (f"M{pa[0] + nx * o:.1f} {pa[1] + ny * o:.1f} "
            f"L{pb[0] + nx * o:.1f} {pb[1] + ny * o:.1f}")


def request_path_segments():
    segments, seen = [], set()
    for _, req in REQUESTS:
        for route in req["routes"]:
            for n1, n2 in zip(route, route[1:]):
                key = (tuple(sorted((n1, n2))), req["lane"])
                if key in seen:
                    continue
                seen.add(key)
                segments.append((_offset_segment(n1, n2, req["lane"]), req["color"]))
    return segments


def completeness_flag(pos, complete):
    word, cls = ("complete", "flag-true") if complete else ("partial", "flag-false")
    return (f'    <text class="flag" text-anchor="middle" x="{pos[0]}" y="{pos[1] - 112}">'
            f'<tspan class="{cls}">{word}</tspan></text>')


def color_legend(y):
    items = [(req["color"], name) for name, req in REQUESTS]
    xs = [205, 435, 605]
    parts = ['    <text class="legend" x="70" y="{}">query paths:</text>'.format(y + 4)]
    for (color, label), x in zip(items, xs):
        parts.append(f'    <line x1="{x}" y1="{y}" x2="{x + 28}" y2="{y}" '
                     f'stroke="{color}" stroke-width="5" stroke-linecap="round"/>')
        parts.append(f'    <text class="legend" x="{x + 36}" y="{y + 4}">{label}</text>')
    return "\n".join(parts)


def matching_combined(name="zenoh-matching.svg"):
    body = ['  <g id="requests">']
    body += [f'    <path class="req" d="{d}" stroke="{c}"/>' for d, c in request_path_segments()]
    body += ['  </g>', '  <g id="nodes" class="endpoint">',
             f'    <use href="#node" x="{R1[0]}" y="{R1[1]}"/>',
             f'    <use href="#node" x="{R2[0]}" y="{R2[1]}"/>',
             storage_use(S1), storage_use(S2), storage_use(S3),
             f'    <use href="#robot" x="{ROBOT_L[0]}" y="{ROBOT_L[1]}"/>',
             f'    <use href="#robot" x="{ROBOT_C[0]}" y="{ROBOT_C[1]}"/>',
             f'    <use href="#robot" x="{ROBOT_R[0]}" y="{ROBOT_R[1]}"/>',
             '  </g>', '  <g id="labels">',
             completeness_flag(S1, True), storage_sample(S1, "A"),
             completeness_flag(S2, True), storage_sample(S2, "B"),
             completeness_flag(S3, False), storage_sample(S3, "C")]
    for target, req in REQUESTS:
        pos = MATCH_NODES[MATCH_ROBOT[target]]
        body.append(get_label(pos[0], pos[1] + 27, f"Get (target = {target})"))
        body.append(centered_tray(pos[0], pos[1] + 56, req["tray"]))
    body.append(color_legend(490))
    body.append("  </g>")

    desc = ("Three storages serve the same key (two complete, one partial), each holding a Sample "
            "A, B or C. Three robots run the same Get with a different target; each request path is "
            "drawn in its own colour. BestMatching reaches the nearest complete storage "
            "(A); All reaches every storage (A, B, C); AllComplete reaches only the complete "
            "storages (A, B). The tray under each robot shows the Samples it collects.")
    document(name, "QueryTarget matching", desc, "\n".join(body))


# --- Consolidation ------------------------------------------------------------

CONS_ROBOTS = {"None": ROBOT_L, "Monotonic": ROBOT_C, "Latest": ROBOT_R}


def consolidation_combined(name="zenoh-consolidation.svg"):
    robots = CONS_ROBOTS

    def seg(a, b):
        return f"M{a[0]} {a[1]} L{b[0]} {b[1]}"

    flow_paths = [
        seg(S1, R1), seg(S2, R1), seg(S3, R2), seg(R1, R2),
        seg(R1, robots["None"]), seg(R1, robots["Monotonic"]), seg(R2, robots["Latest"]),
    ]

    keeps = {
        "None": [("t2", False), ("t1", False), ("t3", False)],
        "Monotonic": [("t2", False), ("t1", True), ("t3", False)],
        "Latest": [("t3", False)],
    }
    body = ['  <g id="flows">']
    body += [f'    <path class="flow" d="{p}"/>' for p in flow_paths]
    body += ['  </g>', '  <g id="nodes" class="endpoint">',
             f'    <use href="#node" x="{R1[0]}" y="{R1[1]}"/>',
             f'    <use href="#node" x="{R2[0]}" y="{R2[1]}"/>',
             storage_use(S1), storage_use(S2), storage_use(S3)]
    body += [f'    <use href="#robot" x="{p[0]}" y="{p[1]}"/>' for p in robots.values()]
    body += ['  </g>', '  <g id="labels">',
             storage_sample(S1, "t2"), storage_sample(S2, "t1"), storage_sample(S3, "t3")]
    for mode, pos in robots.items():
        body.append(get_label(pos[0], pos[1] + 27, f"Get (consolidation = {mode})"))
        body.append(centered_tray(pos[0], pos[1] + 56, keeps[mode]))
    body.append('    <text class="legend" text-anchor="middle" x="490" y="486">'
                'each storage replies with one Sample &#183; t1 &lt; t2 &lt; t3 (newer) &#183; '
                'they reach the robots in the order t2, t1, t3</text>')
    body.append("  </g>")

    desc = ("Three storages reply with Samples for the same key (t1&lt;t2&lt;t3), reaching the "
            "robots in the order t2, t1, t3. Three robots run the same Get with different "
            "consolidation: None keeps t2, t1, t3; Monotonic drops the stale t1 and keeps t2, t3; "
            "Latest keeps only t3.")
    document(name, "Reply consolidation", desc, "\n".join(body))


def main():
    matching_combined("zenoh-matching.svg")
    consolidation_combined("zenoh-consolidation.svg")


if __name__ == "__main__":
    main()
