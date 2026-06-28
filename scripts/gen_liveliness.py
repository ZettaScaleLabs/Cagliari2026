#!/usr/bin/env python3
"""Generate the animated Liveliness illustration (assets/zenoh-liveliness.svg).

Vertical layout for the right-hand side of the Liveliness slide: a server (a
workstation running a liveliness Subscriber for robot/*, history = true) sits on
top with the samples it collects stacked underneath it; the router is in the
middle; the robots robot/alice and robot/bob are at the bottom. robot/alice is
already connected at the start and later disconnects; robot/bob connects in the
middle and stays. The robot / node / workstation artwork is lifted from
assets/zenoh-query.svg so the diagram matches the rest of the deck.

Each liveliness sample is drawn like the Sample cards elsewhere in the deck — a
block with a dot and the key expression — with a green dot for Put and a red dot
for Delete. Samples travel up from the router and stay in the subscriber's list,
so by the end three samples are collected.

Timeline (loop = 14 s), starting with robot/alice already connected:
    server declares the Subscriber (code shown over the server)
    history delivers Put robot/alice       -> green, list slot 1
    robot/bob connects
    subscriber receives Put robot/bob       -> green, list slot 2
    robot/alice disconnects
    subscriber receives Delete robot/alice  -> red,   list slot 3
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "zenoh-query.svg"
OUT = ROOT / "assets" / "zenoh-liveliness.svg"

T = 14.0          # loop length (seconds)
FADE = 0.5
W, H = 430, 560

SERVER = (215, 100)
ROUTER = (215, 352)
ALICE = (110, 478)
BOB = (320, 478)
SLOTS = [(215, 182), (215, 218), (215, 254)]   # collected-sample list (top -> bottom)

PUT = "#2f9e44"
DEL = "#e03131"


def slice_between(text, start_marker, end_open_marker, close_marker="</g>"):
    start = text.index(start_marker)
    anchor = text.index(end_open_marker, start)
    end = text.index(close_marker, anchor) + len(close_marker)
    return text[start:end]


# computer, node, robot, storage, workstation (consecutive in the source defs)
SYMBOLS = slice_between(SRC.read_text(), '<g id="computer">', '<g id="workstation">')


def pct(t):
    return round(max(0.0, min(t, T)) / T * 100, 2)


def fade_keyframes(name, on, off, fade=FADE):
    return (
        "@keyframes %s {\n"
        "  0%%, %s%% { opacity: 0; }\n"
        "  %s%%, %s%% { opacity: 1; }\n"
        "  %s%%, 100%% { opacity: 0; }\n"
        "}"
    ) % (name, pct(on), pct(on + fade), pct(off), pct(off + fade))


def icon(symbol, pos, scale):
    return (f'  <g><g transform="translate({pos[0]} {pos[1]}) scale({scale})">'
            f'<use href="#{symbol}"/></g></g>')


def text(x, y, s, cls, anchor="middle"):
    return f'    <text class="{cls}" text-anchor="{anchor}" x="{x}" y="{y}">{s}</text>'


def card(cls, label, dot, slot, on, off_travel):
    kt = f"0;{round(on / T, 4)};{round(off_travel / T, 4)};1"
    return (
        f'  <g class="card {cls}">\n'
        f'    <rect x="-66" y="-15" width="132" height="30" rx="8" fill="#fff" stroke="#0b3a82" stroke-width="2"/>\n'
        f'    <circle cx="-50" cy="0" r="6" fill="{dot}"/>\n'
        f'    <text x="-36" y="5" text-anchor="start" class="samp">{label}</text>\n'
        f'    <animateMotion dur="{T}s" repeatCount="indefinite" rotate="0" calcMode="linear"\n'
        f'      keyTimes="{kt}" keyPoints="0;0;1;1" path="M{ROUTER[0]} {ROUTER[1]} L{slot[0]} {slot[1]}"/>\n'
        f'  </g>'
    )


def robot(pos, name, cls):
    return (
        f'  <g class="{cls}">\n'
        f'    <g transform="translate({pos[0]} {pos[1]}) scale(1.3)"><use href="#robot"/></g>\n'
        + text(pos[0], pos[1] + 42, f"token = {name}", "ke") + "\n"
        f'  </g>'
    )


# timeline (seconds)
SUB_ON, RESET = 0.4, 12.5
C1 = (1.4, 2.9)      # Put robot/alice (history)
BOB_ON = 3.4
C2 = (4.6, 6.1)      # Put robot/bob
ALICE_OFF = 7.0      # robot/alice disconnects
C3 = (8.2, 9.7)      # Delete robot/alice

# robot/alice: connected from the start, disconnects at ALICE_OFF, fades back in
# at the end so the loop restarts already-connected.
KF_ALICE = (
    "@keyframes kf_alice {\n"
    "  0%%, %s%% { opacity: 1; }\n"
    "  %s%%, %s%% { opacity: 0; }\n"
    "  %s%%, 100%% { opacity: 1; }\n"
    "}"
) % (pct(ALICE_OFF), pct(ALICE_OFF + FADE), pct(RESET + 0.5), pct(RESET + 1.0))

KEYFRAMES = "\n".join([
    KF_ALICE,
    fade_keyframes("kf_sub", SUB_ON, RESET),
    fade_keyframes("kf_bob", BOB_ON, RESET),
    fade_keyframes("kf_c1", C1[0], RESET, fade=0.3),
    fade_keyframes("kf_c2", C2[0], RESET, fade=0.3),
    fade_keyframes("kf_c3", C3[0], RESET, fade=0.3),
])

STYLE = """  <style>
    .bg { fill: #f7f7f7; }
    .link { fill: none; stroke: #c7c7c7; stroke-width: 2.5; stroke-linecap: round; }
    .endpoint { filter: url(#softShadow); }
    .ke { fill: #0b3a82; font: 700 14px Arial, sans-serif; }
    .codebox { fill: #eef4ff; stroke: #bcd0f2; stroke-width: 1.5; }
    .code { fill: #0b3a82; font: 600 13px "SFMono-Regular", "Menlo", "Consolas", monospace; }
    .samp { fill: #0b3a82; font: 700 14px Arial, sans-serif; }

    .alice, .lk-alice { animation: kf_alice %ss linear infinite; }
    .sub { animation: kf_sub %ss linear infinite; }
    .bob, .lk-bob { animation: kf_bob %ss linear infinite; }
    .card { opacity: 0; }
    .c1 { animation: kf_c1 %ss linear infinite; }
    .c2 { animation: kf_c2 %ss linear infinite; }
    .c3 { animation: kf_c3 %ss linear infinite; }
%s
  </style>""" % (
    T, T, T, T, T, T,
    "\n".join("    " + line for line in KEYFRAMES.splitlines()),
)


def code_over_server():
    x = 100   # left padding for code text
    return (
        '  <g class="sub">\n'
        '    <rect class="codebox" x="91" y="46" width="250" height="82" rx="10"/>\n'
        f'    <text class="code" text-anchor="start" x="{x}" y="64">session</text>\n'
        f'    <text class="code" text-anchor="start" x="{x}" y="84">.liveliness()</text>\n'
        f'    <text class="code" text-anchor="start" x="{x}" y="104">.declare_subscriber('
        '<tspan fill="#2f9e44">"robot/*"</tspan>)</text>\n'
        f'    <text class="code" text-anchor="start" x="{x}" y="124">.history()</text>\n'
        '  </g>'
    )


def main():
    body = []

    # links: spine router->server (static); alice toggles; bob toggles
    body.append('  <g id="links">')
    body.append(f'    <path class="link" d="M{ROUTER[0]} {ROUTER[1]} L{SERVER[0]} {SERVER[1]}"/>')
    body.append(f'    <path class="link lk-alice" d="M{ROUTER[0]} {ROUTER[1]} L{ALICE[0]} {ALICE[1]}"/>')
    body.append(f'    <path class="link lk-bob" d="M{ROUTER[0]} {ROUTER[1]} L{BOB[0]} {BOB[1]}"/>')
    body.append('  </g>')

    # static nodes (workstation server + router)
    body.append('  <g class="endpoint">')
    body.append(icon("workstation", SERVER, 1.3))
    body.append(icon("node", ROUTER, 1.2))
    body.append('  </g>')

    # subscriber declaration drawn over the server
    body.append(code_over_server())

    # robots
    body.append(robot(ALICE, "robot/alice", "alice"))
    body.append(robot(BOB, "robot/bob", "bob"))

    # collected liveliness samples (travel up from the router, then stay)
    body.append(card("c1", "robot/alice", PUT, SLOTS[0], *C1))
    body.append(card("c2", "robot/bob", PUT, SLOTS[1], *C2))
    body.append(card("c3", "robot/alice", DEL, SLOTS[2], *C3))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Zenoh liveliness subscriber</title>
  <desc id="desc">A server runs session.liveliness().declare_subscriber("robot/*").history() while robot/alice is
already connected. History delivers a Put for robot/alice; robot/bob connects and the subscriber receives a Put
for robot/bob; robot/alice disconnects and the subscriber receives a Delete for robot/alice. The three samples
stay in the subscriber's list (green dot = Put, red dot = Delete).</desc>
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
