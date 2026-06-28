#!/usr/bin/env python3
"""Generate the animated Liveliness illustration (assets/zenoh-liveliness.svg).

Vertical layout for the right-hand side of the Liveliness slide: the server (a
liveliness Subscriber for robot/* with history = true) sits on top with the
samples it collects stacked underneath it; the router is in the middle; the
robots robot/alice and robot/bob are at the bottom. robot/alice is already
connected at the start. The robot / node / storage artwork is lifted from
assets/zenoh-query.svg so the diagram matches the rest of the deck.

Each liveliness sample is drawn like the Sample cards elsewhere in the deck — a
block with a dot and the key expression — with a green dot for Put and a red dot
for Delete. Samples travel up from the router and stay in the subscriber's list,
so by the end three samples are collected. Animations are pure CSS keyframes
(+ animateMotion for the moving samples) on a looping timeline.

Timeline (loop = 14 s), starting with robot/alice already connected:
    server declares Subscriber robot/* (history = true)
    history delivers Put robot/alice      -> green, list slot 1
    robot/bob connects
    subscriber receives Put robot/bob      -> green, list slot 2
    robot/bob disconnects
    subscriber receives Delete robot/bob   -> red,   list slot 3
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "zenoh-query.svg"
OUT = ROOT / "assets" / "zenoh-liveliness.svg"

T = 14.0          # loop length (seconds)
FADE = 0.5
W, H = 430, 560

SERVER = (215, 84)
ROUTER = (215, 355)
ALICE = (110, 475)
BOB = (320, 475)
SLOTS = [(215, 186), (215, 222), (215, 258)]   # collected-sample list (top -> bottom)

PUT = "#2f9e44"
DEL = "#e03131"


def slice_between(text, start_marker, end_open_marker, close_marker="</g>"):
    start = text.index(start_marker)
    anchor = text.index(end_open_marker, start)
    end = text.index(close_marker, anchor) + len(close_marker)
    return text[start:end]


SYMBOLS = slice_between(SRC.read_text(), '<g id="computer">', '<g id="storage">')


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


def icon(symbol, pos, scale, cls=None):
    c = f' class="{cls}"' if cls else ""
    return (f'  <g{c}><g transform="translate({pos[0]} {pos[1]}) scale({scale})">'
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
    extra = f" {cls}" if cls else ""
    return (
        f'  <g class="robot{extra}">\n'
        f'    <g transform="translate({pos[0]} {pos[1]}) scale(1.3)"><use href="#robot"/></g>\n'
        f'    <circle class="token" cx="{pos[0] - 52}" cy="{pos[1] + 38}" r="5"/>\n'
        + text(pos[0] - 40, pos[1] + 42, name, "ke", anchor="start") + "\n"
        f'  </g>'
    )


# timeline (seconds)
SUB_ON, RESET = 0.4, 13.0
C1 = (1.4, 2.9)     # Put robot/alice (history)
BOB_ON, BOB_OFF = 3.4, 7.0
C2 = (4.6, 6.1)     # Put robot/bob
C3 = (8.2, 9.7)     # Delete robot/bob

KEYFRAMES = "\n".join([
    fade_keyframes("kf_sub", SUB_ON, RESET),
    fade_keyframes("kf_bob", BOB_ON, BOB_OFF),
    fade_keyframes("kf_c1", C1[0], RESET, fade=0.3),
    fade_keyframes("kf_c2", C2[0], RESET, fade=0.3),
    fade_keyframes("kf_c3", C3[0], RESET, fade=0.3),
])

STYLE = """  <style>
    .bg { fill: #f7f7f7; }
    .link { fill: none; stroke: #c7c7c7; stroke-width: 2.5; stroke-linecap: round; }
    .endpoint { filter: url(#softShadow); }
    .node-label { fill: #5b6b86; font: 700 15px Arial, sans-serif; }
    .ke { fill: #0b3a82; font: 700 14px Arial, sans-serif; }
    .badge { fill: #eef4ff; stroke: #147dff; stroke-width: 1.5; }
    .badge-t { fill: #0b1641; font: 700 14px Arial, sans-serif; }
    .badge-k { fill: #147dff; font: 700 14px Arial, sans-serif; }
    .samp { fill: #0b3a82; font: 700 14px Arial, sans-serif; }
    .token { fill: #2f9e44; }

    .sub { animation: kf_sub %ss linear infinite; }
    .bob, .lk-bob { animation: kf_bob %ss linear infinite; }
    .card { opacity: 0; }
    .c1 { animation: kf_c1 %ss linear infinite; }
    .c2 { animation: kf_c2 %ss linear infinite; }
    .c3 { animation: kf_c3 %ss linear infinite; }
%s
  </style>""" % (
    T, T, T, T, T,
    "\n".join("    " + line for line in KEYFRAMES.splitlines()),
)


def main():
    body = []

    # links (alice is always connected; bob's link toggles; spine router->server)
    body.append('  <g id="links">')
    body.append(f'    <path class="link" d="M{ROUTER[0]} {ROUTER[1]} L{SERVER[0]} {SERVER[1]}"/>')
    body.append(f'    <path class="link" d="M{ROUTER[0]} {ROUTER[1]} L{ALICE[0]} {ALICE[1]}"/>')
    body.append(f'    <path class="link lk-bob" d="M{ROUTER[0]} {ROUTER[1]} L{BOB[0]} {BOB[1]}"/>')
    body.append('  </g>')

    # static nodes
    body.append('  <g class="endpoint">')
    body.append(icon("storage", SERVER, 1.0))
    body.append(icon("node", ROUTER, 1.2))
    body.append('  </g>')
    body.append(text(ROUTER[0] + 48, ROUTER[1] + 5, "Router", "node-label", anchor="start"))

    # subscriber badge under the server
    body.append('  <g class="sub">')
    body.append('    <rect class="badge" x="95" y="112" width="240" height="42" rx="11"/>')
    body.append(text(215, 128, "Liveliness Subscriber", "badge-t"))
    body.append(text(215, 146, "robot/*  ·  history = true", "badge-k"))
    body.append('  </g>')

    # robots
    body.append(robot(ALICE, "robot/alice", None))
    body.append(robot(BOB, "robot/bob", "bob"))

    # collected liveliness samples (travel up from the router, then stay)
    body.append(card("c1", "robot/alice", PUT, SLOTS[0], *C1))
    body.append(card("c2", "robot/bob", PUT, SLOTS[1], *C2))
    body.append(card("c3", "robot/bob", DEL, SLOTS[2], *C3))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Zenoh liveliness subscriber</title>
  <desc id="desc">A server declares a liveliness Subscriber for robot/* with history=true while robot/alice is
already connected. History delivers a Put for robot/alice; robot/bob connects and the subscriber receives a Put
for robot/bob; robot/bob disconnects and the subscriber receives a Delete for robot/bob. The three samples stay
in the subscriber's list (green dot = Put, red dot = Delete).</desc>
  <defs>
    <linearGradient id="node-fill" x1="0" x2="0" y1="0" y2="1">
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

  <rect class="bg" width="{W}" height="{H}"/>

{chr(10).join(body)}
</svg>
"""
    OUT.write_text(svg)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
