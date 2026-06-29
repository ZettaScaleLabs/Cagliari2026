#!/usr/bin/env python3
"""Generate the animated Scouting / gossip illustration (assets/zenoh-gossip.svg).

Landscape layout for the "Scouting" slide. A router sits at the top centre with
its locator under it; robot A is at the bottom left with its locator under it;
robot B is at the bottom right. The robot / node artwork is lifted from
assets/zenoh-query.svg so the diagram matches the rest of the deck.

The animation shows connections being established, drawing each link
progressively, and the router gossiping robot A's address to robot B:

    start: robot A is already connected to the router (that link is drawn).
    1. robot B joins  -> the line from robot B to the router is drawn.
    2. the router gossips robot A's address to robot B -> a small packet
       carrying robot A's locator travels from the router to robot B.
    3. robot B now knows robot A's address and connects straight to it ->
       the line from robot B to robot A is drawn.
    final state: the three nodes form a triangle.

The loop then fades the two new links out and restarts (robot A still connected).
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "zenoh-query.svg"
OUT = ROOT / "assets" / "zenoh-gossip.svg"

T = 10.0          # loop length (seconds)
RESET = 8.5       # the two drawn links fade out here, then the loop restarts
FADE = 0.4
W, H = 560, 560

ROUTER = (280, 108)
A = (112, 380)
B = (448, 380)

LINK = "#7aa7e0"
ACCENT = "#147dff"

ROUTER_ADDR = "tls/router.example.com"
ROBOT_A_ADDR = "tcp/10.0.0.5"


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
    """opacity 0 -> 1 at `on`, hold, -> 0 at `off`."""
    return (
        "@keyframes %s {\n"
        "  0%%, %s%% { opacity: 0; }\n"
        "  %s%%, %s%% { opacity: 1; }\n"
        "  %s%%, 100%% { opacity: 0; }\n"
        "}"
    ) % (name, pct(on), pct(on + fin), pct(off), pct(off + fout))


def draw_kf(name, dash, start, end):
    """Draw-in keyframe: fade the stroke in at `start`, sweep stroke-dashoffset
    from `dash` to 0 by `end`, hold drawn until RESET, then fade out (and reset
    the dashoffset so the next loop starts undrawn)."""
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
    """An <animateMotion> that holds at the path start until t0, travels to the
    end by t1, then holds at the end."""
    kt = f"0;{round(t0 / T, 4)};{round(t1 / T, 4)};1"
    return (f'    <animateMotion dur="{T}s" repeatCount="indefinite" calcMode="linear"\n'
            f'      keyTimes="{kt}" keyPoints="0;0;1;1" path="{path}"/>')


def icon(symbol, pos, scale):
    return (f'    <g transform="translate({pos[0]} {pos[1]}) scale({scale})">'
            f'<use href="#{symbol}"/></g>')


def gossip_packet(path, t0, t1):
    """The gossip packet carrying robot A's locator, router -> robot B."""
    return (
        f'  <g class="gossip">\n'
        f'    <rect x="-84" y="-17" width="168" height="34" rx="9" fill="#fff" '
        f'stroke="{ACCENT}" stroke-width="2"/>\n'
        f'    <circle cx="-68" cy="0" r="5" fill="{ACCENT}"/>\n'
        f'    <text x="-56" y="-3" text-anchor="start" class="plabel">robot A</text>\n'
        f'    <text x="-56" y="12" text-anchor="start" class="paddr">{ROBOT_A_ADDR}</text>\n'
        f'{motion(path, t0, t1)}\n'
        f'  </g>'
    )


# ---- timeline (seconds) -----------------------------------------------------
BR_DRAW = (1.0, 2.8)        # robot B -> router
GOSSIP = (3.1, 4.3)         # router gossips robot A's address -> robot B
BA_DRAW = (4.6, 6.4)        # robot B -> robot A (now that it knows the address)

DASH_BR = round(dist(B, ROUTER) + 20)
DASH_BA = round(dist(B, A) + 20)

P_AR = f"M{A[0]} {A[1]} L{ROUTER[0]} {ROUTER[1]}"
P_BR = f"M{B[0]} {B[1]} L{ROUTER[0]} {ROUTER[1]}"
P_BA = f"M{B[0]} {B[1]} L{A[0]} {A[1]}"
P_RB = f"M{ROUTER[0]} {ROUTER[1]} L{B[0]} {B[1]}"

KEYFRAMES = "\n".join([
    draw_kf("kf_br", DASH_BR, *BR_DRAW),
    draw_kf("kf_ba", DASH_BA, *BA_DRAW),
    fade_kf("kf_gossip", GOSSIP[0], GOSSIP[1] + 0.3, fin=0.25, fout=0.35),
])

STYLE = """  <style>
    .bg { fill: #f7f7f7; }
    .link { fill: none; stroke: %s; stroke-width: 3.2; stroke-linecap: round; }
    .endpoint { filter: url(#softShadow); }
    .name { fill: #0b3a82; font: 700 18px Arial, sans-serif; }
    .addr { fill: #5b6b86; font: 600 14px "SFMono-Regular","Menlo","Consolas",monospace; }
    .plabel { fill: #5b6b86; font: 700 11px Arial, sans-serif; }
    .paddr  { fill: #0b3a82; font: 700 13px "SFMono-Regular","Menlo","Consolas",monospace; }

    .lbr { stroke-dasharray: %s; opacity: 0; animation: kf_br %ss linear infinite; }
    .lba { stroke-dasharray: %s; opacity: 0; animation: kf_ba %ss linear infinite; }
    .gossip { opacity: 0; animation: kf_gossip %ss linear infinite; }
%s
  </style>""" % (
    LINK,
    DASH_BR, T,
    DASH_BA, T,
    T,
    "\n".join("    " + line for line in KEYFRAMES.splitlines()),
)


def main():
    body = []

    # links: A<->router is already connected (static); B<->router and B<->A draw in
    body.append('  <g id="links">')
    body.append(f'    <path class="link" d="{P_AR}"/>')
    body.append(f'    <path class="link lbr" d="{P_BR}"/>')
    body.append(f'    <path class="link lba" d="{P_BA}"/>')
    body.append('  </g>')

    # static endpoints: router + the two robots
    body.append('  <g class="endpoint">')
    body.append(icon("node", ROUTER, 1.25))
    body.append(icon("robot", A, 1.3))
    body.append(icon("robot", B, 1.3))
    body.append('  </g>')

    # labels: router locator, robot A name + locator, robot B name
    body.append(f'  <text class="addr" text-anchor="middle" x="{ROUTER[0]}" y="{ROUTER[1]+50}">{ROUTER_ADDR}</text>')
    body.append(f'  <text class="name" text-anchor="middle" x="{A[0]}" y="{A[1]+84}">robot A</text>')
    body.append(f'  <text class="addr" text-anchor="middle" x="{A[0]}" y="{A[1]+103}">{ROBOT_A_ADDR}</text>')
    body.append(f'  <text class="name" text-anchor="middle" x="{B[0]}" y="{B[1]+84}">robot B</text>')

    # gossip packet: robot A's locator travels from the router to robot B
    body.append(gossip_packet(P_RB, *GOSSIP))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Scouting through gossip</title>
  <desc id="desc">Robot A is already connected to a router whose locator is {ROUTER_ADDR}; robot A's
locator is {ROBOT_A_ADDR}. Robot B connects to the router, the router gossips robot A's locator to robot B in a
small packet, and robot B then connects directly to robot A, so the three nodes form a triangle.</desc>
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
