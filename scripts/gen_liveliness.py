#!/usr/bin/env python3
"""Generate the animated Liveliness illustration (assets/zenoh-liveliness.svg).

A server declares a liveliness Subscriber for robot/* with history = true; two
robots (robot/alice, robot/bob) connect and disconnect, and the subscriber
receives Put / Delete liveliness samples routed through the router. The robot /
node / storage artwork is lifted from assets/zenoh-query.svg so the diagram
matches the rest of the deck. Animations are pure CSS keyframes (+ animateMotion
for the moving samples) on a looping timeline, so they play in HTML / browsers.

Timeline (loop = 16 s):
    1  robot/alice connects (declares its liveliness token)
    2  server declares the Subscriber robot/* with history = true
    3  history delivers Put robot/alice
    4  robot/bob connects
    5  subscriber receives Put robot/bob
    6  robot/bob disconnects
    7  subscriber receives Delete robot/bob
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "zenoh-query.svg"
OUT = ROOT / "assets" / "zenoh-liveliness.svg"

T = 16.0          # loop length (seconds)
FADE = 0.5
W, H = 900, 510

SERVER = (155, 310)
ROUTER = (470, 310)
ALICE = (800, 170)
BOB = (800, 415)

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


def packet(cls, label, color, on, off):
    w = 12 + len(label) * 8.3
    kt = f"0;{round(on / T, 4)};{round(off / T, 4)};1"
    return (
        f'  <g class="pkt {cls}">\n'
        f'    <circle class="dot" r="7" fill="{color}"/>\n'
        f'    <g transform="translate(0 -22)">\n'
        f'      <rect x="{-w / 2:.0f}" y="-13" width="{w:.0f}" height="26" rx="13" fill="{color}"/>\n'
        f'      <text x="0" y="5" text-anchor="middle" class="pilltext">{label}</text>\n'
        f'    </g>\n'
        f'    <animateMotion dur="{T}s" repeatCount="indefinite" rotate="0" calcMode="linear"\n'
        f'      keyTimes="{kt}" keyPoints="0;0;1;1" path="M{ROUTER[0]} {ROUTER[1]} L{SERVER[0]} {SERVER[1]}"/>\n'
        f'  </g>'
    )


# timeline (seconds)
ALICE_ON, ALICE_OFF = 0.5, 15.4
SUB_ON, SUB_OFF = 2.5, 15.4
BOB_ON, BOB_OFF = 6.5, 10.5
PUT_A = (4.4, 6.0)
PUT_B = (8.4, 10.0)
DEL_B = (12.4, 14.0)

CAPTIONS = [
    "1 · robot/alice connects — declares its liveliness token",
    "2 · server declares Subscriber  robot/*  ·  history = true",
    "3 · history delivers  Put  robot/alice",
    "4 · robot/bob connects",
    "5 · subscriber receives  Put  robot/bob",
    "6 · robot/bob disconnects",
    "7 · subscriber receives  Delete  robot/bob",
]
CAP_STEP = 2.0
CAP_LAST_END = 15.7

KEYFRAMES = "\n".join([
    fade_keyframes("kf_alice", ALICE_ON, ALICE_OFF),
    fade_keyframes("kf_sub", SUB_ON, SUB_OFF),
    fade_keyframes("kf_bob", BOB_ON, BOB_OFF),
    fade_keyframes("kf_pa", *PUT_A, fade=0.3),
    fade_keyframes("kf_pb", *PUT_B, fade=0.3),
    fade_keyframes("kf_db", *DEL_B, fade=0.3),
] + [
    fade_keyframes(
        f"kf_cap{i + 1}",
        0.3 + i * CAP_STEP,
        (CAP_LAST_END if i == len(CAPTIONS) - 1 else 0.3 + (i + 1) * CAP_STEP),
        fade=0.3,
    )
    for i in range(len(CAPTIONS))
])

STYLE = """  <style>
    .bg { fill: #f7f7f7; }
    .link { fill: none; stroke: #c7c7c7; stroke-width: 2.5; stroke-linecap: round; }
    .endpoint { filter: url(#softShadow); }
    .node-label { fill: #5b6b86; font: 700 16px Arial, sans-serif; }
    .ke { fill: #0b3a82; font: 700 15px Arial, sans-serif; }
    .caption { fill: #16233d; font: 600 18px Arial, sans-serif; }
    .badge { fill: #eef4ff; stroke: #147dff; stroke-width: 1.5; }
    .badge-t { fill: #0b1641; font: 700 14px Arial, sans-serif; }
    .badge-k { fill: #147dff; font: 700 14px Arial, sans-serif; }
    .pilltext { fill: #fff; font: 700 14px Arial, sans-serif; }
    .dot { stroke: #fff; stroke-width: 2; }
    .token { fill: #2f9e44; }

    .alice, .lk-alice { animation: kf_alice %ss linear infinite; }
    .sub { animation: kf_sub %ss linear infinite; }
    .bob, .lk-bob { animation: kf_bob %ss linear infinite; }
    .pkt { opacity: 0; }
    .pa { animation: kf_pa %ss linear infinite; }
    .pb { animation: kf_pb %ss linear infinite; }
    .db { animation: kf_db %ss linear infinite; }
%s
%s
  </style>""" % (
    T, T, T, T, T, T,
    "\n".join(f"    .cap{i + 1} {{ animation: kf_cap{i + 1} {T}s linear infinite; }}"
              for i in range(len(CAPTIONS))),
    "\n".join("    " + line for line in KEYFRAMES.splitlines()),
)


def main():
    body = []

    # links
    body.append('  <g id="links">')
    body.append(f'    <path class="link" d="M{SERVER[0]} {SERVER[1]} L{ROUTER[0]} {ROUTER[1]}"/>')
    body.append(f'    <path class="link lk-alice" d="M{ROUTER[0]} {ROUTER[1]} L{ALICE[0]} {ALICE[1]}"/>')
    body.append(f'    <path class="link lk-bob" d="M{ROUTER[0]} {ROUTER[1]} L{BOB[0]} {BOB[1]}"/>')
    body.append('  </g>')

    # static nodes
    body.append('  <g class="endpoint">')
    body.append(icon("storage", SERVER, 1.25))
    body.append(icon("node", ROUTER, 1.4))
    body.append('  </g>')
    body.append(text(SERVER[0], SERVER[1] + 42, "Server", "node-label"))
    body.append(text(ROUTER[0], ROUTER[1] + 40, "Router", "node-label"))

    # subscriber badge on the server
    body.append('  <g class="sub">')
    body.append(f'    <rect class="badge" x="40" y="186" width="250" height="46" rx="12"/>')
    body.append(text(165, 205, "Liveliness Subscriber", "badge-t"))
    body.append(text(165, 224, "robot/*  ·  history = true", "badge-k"))
    body.append('  </g>')

    # robots (with token + key expression label)
    body.append('  <g class="alice endpoint">')
    body.append(icon("robot", ALICE, 1.5))
    body.append(f'    <circle class="token" cx="{ALICE[0] - 66}" cy="128" r="5"/>')
    body.append(text(ALICE[0] - 54, 133, "robot/alice", "ke", anchor="start"))
    body.append('  </g>')

    body.append('  <g class="bob endpoint">')
    body.append(icon("robot", BOB, 1.5))
    body.append(f'    <circle class="token" cx="{BOB[0] - 60}" cy="463" r="5"/>')
    body.append(text(BOB[0] - 48, 468, "robot/bob", "ke", anchor="start"))
    body.append('  </g>')

    # moving liveliness samples (router -> subscriber)
    body.append(packet("pa", "Put robot/alice", PUT, *PUT_A))
    body.append(packet("pb", "Put robot/bob", PUT, *PUT_B))
    body.append(packet("db", "Delete robot/bob", DEL, *DEL_B))

    # step captions
    for i, cap in enumerate(CAPTIONS):
        body.append(text(450, 492, cap, f"caption cap{i + 1}"))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Zenoh liveliness subscriber</title>
  <desc id="desc">A server declares a liveliness Subscriber for robot/* with history=true. robot/alice
connects and history delivers a Put for robot/alice; robot/bob connects and the subscriber receives a Put for
robot/bob; robot/bob disconnects and the subscriber receives a Delete for robot/bob.</desc>
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
