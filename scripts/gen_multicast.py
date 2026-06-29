#!/usr/bin/env python3
"""Generate the animated UDP-multicast scouting illustration (assets/zenoh-multicast.svg).

Square companion to assets/zenoh-gossip.svg, drawn with the same notation (robot
artwork from assets/zenoh-query.svg, tcp/... locators, links drawn progressively,
small packet cards carrying addresses).

Three robots (A, B, C) are already connected to each other. A fourth robot, D,
joins and discovers them by UDP multicast:

    1. robot D broadcasts a scout message on the local network -> an expanding
       ring radiates out from robot D.
    2. each of the three robots replies with its address -> a small packet
       carrying that robot's locator travels back from it to robot D.
    3. robot D now knows the three addresses and connects to each robot ->
       the lines from robot D to A, B and C are drawn.

The loop then fades robot D's links out and restarts.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "zenoh-query.svg"
OUT = ROOT / "assets" / "zenoh-multicast.svg"

T = 12.0          # loop length (seconds)
RESET = 10.0      # robot D's links fade out here, then the loop restarts
FADE = 0.4
W, H = 560, 560

A = (280, 95)
B = (112, 300)
C = (448, 300)
D = (280, 452)

LINK = "#7aa7e0"
ACCENT = "#147dff"

ADDR = {"A": "tcp/10.0.0.1", "B": "tcp/10.0.0.2", "C": "tcp/10.0.0.3"}


def dist(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5


def slice_between(text, start_marker, end_open_marker, close_marker="</g>"):
    start = text.index(start_marker)
    anchor = text.index(end_open_marker, start)
    end = text.index(close_marker, anchor) + len(close_marker)
    return text[start:end]


# computer, node, robot (+ parts), storage, workstation (consecutive in source defs)
SYMBOLS = slice_between(SRC.read_text(), '<g id="computer">', '<g id="workstation">')


def pct(t):
    return round(max(0.0, min(t, T)) / T * 100, 2)


def fade_kf(name, on, off, fin=FADE, fout=FADE):
    return (
        "@keyframes %s {\n"
        "  0%%, %s%% { opacity: 0; }\n"
        "  %s%%, %s%% { opacity: 1; }\n"
        "  %s%%, 100%% { opacity: 0; }\n"
        "}"
    ) % (name, pct(on), pct(on + fin), pct(off), pct(off + fout))


def draw_kf(name, dash, start, end):
    return (
        "@keyframes %s {\n"
        "  0%%, %s%% { opacity: 0; stroke-dashoffset: %s; }\n"
        "  %s%% { opacity: 1; stroke-dashoffset: %s; }\n"
        "  %s%% { opacity: 1; stroke-dashoffset: 0; }\n"
        "  %s%% { opacity: 1; stroke-dashoffset: 0; }\n"
        "  %s%%, 100%% { opacity: 0; stroke-dashoffset: 0; }\n"
        "}"
    ) % (
        name, pct(start), dash,
        pct(start + 0.15), dash,
        pct(end), pct(RESET), pct(RESET + FADE),
    )


def motion(path, t0, t1):
    kt = f"0;{round(t0 / T, 4)};{round(t1 / T, 4)};1"
    return (f'    <animateMotion dur="{T}s" repeatCount="indefinite" calcMode="linear"\n'
            f'      keyTimes="{kt}" keyPoints="0;0;1;1" path="{path}"/>')


def icon(symbol, pos, scale):
    return (f'    <g transform="translate({pos[0]} {pos[1]}) scale({scale})">'
            f'<use href="#{symbol}"/></g>')


def ring(t0, t1):
    """An expanding broadcast ring radiating from robot D during [t0, t1]."""
    s, s2, e = round(t0 / T, 4), round((t0 + 0.12) / T, 4), round(t1 / T, 4)
    return (
        f'  <circle cx="{D[0]}" cy="{D[1]}" r="16" fill="none" stroke="{ACCENT}" '
        f'stroke-width="2.5" opacity="0">\n'
        f'    <animate attributeName="r" dur="{T}s" repeatCount="indefinite" calcMode="linear"\n'
        f'      keyTimes="0;{s};{e};1" values="16;16;232;232"/>\n'
        f'    <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="linear"\n'
        f'      keyTimes="0;{s};{s2};{e};1" values="0;0;0.55;0;0"/>\n'
        f'  </circle>'
    )


def reply(cls, addr, path, t0, t1):
    """A reply packet carrying a robot's locator back to robot D."""
    return (
        f'  <g class="{cls}">\n'
        f'    <rect x="-62" y="-14" width="124" height="28" rx="7" fill="#fff" '
        f'stroke="{ACCENT}" stroke-width="2"/>\n'
        f'    <circle cx="-48" cy="0" r="4.5" fill="{ACCENT}"/>\n'
        f'    <text x="-38" y="4" text-anchor="start" class="paddr">{addr}</text>\n'
        f'{motion(path, t0, t1)}\n'
        f'  </g>'
    )


# ---- timeline (seconds) -----------------------------------------------------
RING1 = (1.0, 2.6)
RING2 = (1.7, 3.3)
REPLY = {"A": (3.6, 5.0), "B": (3.9, 5.3), "C": (4.2, 5.6)}
CONN = {"B": (6.0, 7.2), "C": (6.5, 7.7), "A": (7.0, 8.4)}

NODE = {"A": A, "B": B, "C": C}
DASH = {k: round(dist(D, p) + 20) for k, p in NODE.items()}

# robot -> D (reply) and D -> robot (connect) paths
P_REPLY = {k: f"M{p[0]} {p[1]} L{D[0]} {D[1]}" for k, p in NODE.items()}
P_CONN = {k: f"M{D[0]} {D[1]} L{p[0]} {p[1]}" for k, p in NODE.items()}

KEYFRAMES = "\n".join(
    [fade_kf(f"kf_r{k.lower()}", *REPLY[k], fin=0.2, fout=0.3) for k in "ABC"]
    + [draw_kf(f"kf_c{k.lower()}", DASH[k], *CONN[k]) for k in "ABC"]
)

STYLE = """  <style>
    .bg { fill: #f7f7f7; }
    .link { fill: none; stroke: %s; stroke-width: 3.2; stroke-linecap: round; }
    .endpoint { filter: url(#softShadow); }
    .name { fill: #0b3a82; font: 700 18px Arial, sans-serif; }
    .addr { fill: #5b6b86; font: 600 14px "SFMono-Regular","Menlo","Consolas",monospace; }
    .paddr { fill: #0b3a82; font: 700 12px "SFMono-Regular","Menlo","Consolas",monospace; }

    .lca { stroke-dasharray: %s; opacity: 0; animation: kf_ca %ss linear infinite; }
    .lcb { stroke-dasharray: %s; opacity: 0; animation: kf_cb %ss linear infinite; }
    .lcc { stroke-dasharray: %s; opacity: 0; animation: kf_cc %ss linear infinite; }
    .ra { opacity: 0; animation: kf_ra %ss linear infinite; }
    .rb { opacity: 0; animation: kf_rb %ss linear infinite; }
    .rc { opacity: 0; animation: kf_rc %ss linear infinite; }
%s
  </style>""" % (
    LINK,
    DASH["A"], T, DASH["B"], T, DASH["C"], T,
    T, T, T,
    "\n".join("    " + line for line in KEYFRAMES.splitlines()),
)


def main():
    body = []

    # links: A<->B<->C<->A already connected (static); D<->A/B/C draw in
    body.append('  <g id="links">')
    body.append(f'    <path class="link" d="M{A[0]} {A[1]} L{B[0]} {B[1]}"/>')
    body.append(f'    <path class="link" d="M{A[0]} {A[1]} L{C[0]} {C[1]}"/>')
    body.append(f'    <path class="link" d="M{B[0]} {B[1]} L{C[0]} {C[1]}"/>')
    body.append(f'    <path class="link lca" d="{P_CONN["A"]}"/>')
    body.append(f'    <path class="link lcb" d="{P_CONN["B"]}"/>')
    body.append(f'    <path class="link lcc" d="{P_CONN["C"]}"/>')
    body.append('  </g>')

    # broadcast rings from robot D (drawn under the robots)
    body.append(ring(*RING1))
    body.append(ring(*RING2))

    # static endpoints: the four robots
    body.append('  <g class="endpoint">')
    for p in (A, B, C, D):
        body.append(icon("robot", p, 1.2))
    body.append('  </g>')

    # labels: A/B/C name + locator (A's above-interior like the router label), D name
    body.append(f'  <text class="name" text-anchor="middle" x="{A[0]}" y="{A[1]+62}">robot A</text>')
    body.append(f'  <text class="addr" text-anchor="middle" x="{A[0]}" y="{A[1]+80}">{ADDR["A"]}</text>')
    body.append(f'  <text class="name" text-anchor="middle" x="{B[0]}" y="{B[1]+82}">robot B</text>')
    body.append(f'  <text class="addr" text-anchor="middle" x="{B[0]}" y="{B[1]+100}">{ADDR["B"]}</text>')
    body.append(f'  <text class="name" text-anchor="middle" x="{C[0]}" y="{C[1]+82}">robot C</text>')
    body.append(f'  <text class="addr" text-anchor="middle" x="{C[0]}" y="{C[1]+100}">{ADDR["C"]}</text>')
    body.append(f'  <text class="name" text-anchor="middle" x="{D[0]}" y="{D[1]+84}">robot D</text>')

    # reply packets: each robot's locator travels back to robot D
    for k in "ABC":
        body.append(reply(f"r{k.lower()}", ADDR[k], P_REPLY[k], *REPLY[k]))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">UDP multicast scouting</title>
  <desc id="desc">Robots A, B and C are already connected to each other. Robot D broadcasts a UDP scout
message (an expanding ring); each of the three robots replies with its locator (tcp/10.0.0.1, .2, .3) in a small
packet, and robot D then connects to all three.</desc>
  <defs>
    <linearGradient id="node-fill" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#62bfff"/>
      <stop offset="1" stop-color="#247fbd"/>
    </linearGradient>
    <linearGradient id="robot-fill" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#5bbcff"/>
      <stop offset="1" stop-color="#1f78c9"/>
    </linearGradient>
    <linearGradient id="workstation-screen-fill" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#f7fdff"/>
      <stop offset="1" stop-color="#caeef9"/>
    </linearGradient>
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.5" flood-color="#0b2547" flood-opacity=".25"/>
    </filter>

    <!-- Kept inline for portable rendering; reusable copies live in assets/svg-components/. -->
    {SYMBOLS}
  </defs>

{STYLE}

  <rect class="bg" width="{W}" height="{H}"/>

{chr(10).join(body)}
</svg>
"""
    OUT.write_text(svg)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
