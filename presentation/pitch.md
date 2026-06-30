---
marp: true
title: Zenoh Challenge — Pitch
description: The hackathon track in two slides
author: Mikhail ILIN, Ivan PAEZ
paginate: true
size: 16:9
footer: 'Eclipse Zenoh · Cagliari 2026'
---

<style>
:root {
  --zenoh-blue: #147dff;
  --zenoh-cyan: #62bfff;
  --zenoh-navy: #0b1641;
  --ink: #16233d;
  --muted: #5b6b86;
}

section {
  font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
  font-size: 25px;
  color: var(--ink);
  background-color: #ffffff;
  /* Logo template: fixed top-right on every content slide, independent of
     content flow and split backgrounds. */
  background-image: url(../assets/svg-components/zetta-scale-logo.svg);
  background-repeat: no-repeat;
  background-position: right 64px top 28px;
  background-size: 132px auto;
  padding: 54px 64px 60px;
  line-height: 1.45;
}

section h1 {
  color: var(--zenoh-navy);
  font-size: 46px;
  margin: 0 0 2px;
  text-align: left;
}
section h1::after {
  content: "";
  display: block;
  width: 84px;
  height: 5px;
  margin: 10px 0 0;
  background: linear-gradient(90deg, var(--zenoh-blue), var(--zenoh-cyan));
  border-radius: 3px;
}
section h2 {
  color: var(--zenoh-blue);
  font-size: 29px;
  font-weight: 600;
  margin: 16px 0 18px;
}
section h3 {
  color: var(--zenoh-navy);
  font-size: 20px;
  font-weight: 700;
  margin: 10px 0 4px;
}

section a { color: var(--zenoh-blue); text-decoration: none; }
strong { color: var(--zenoh-navy); }
code {
  background: #eef4ff;
  color: #0b3a82;
  padding: 1px 6px;
  border-radius: 5px;
  font-size: 0.9em;
}
ul, ol { margin-top: 4px; }
li { margin: 7px 0; }
li::marker { color: var(--zenoh-blue); }

table { font-size: 22px; border-collapse: collapse; width: 100%; }
th { background: var(--zenoh-navy); color: #fff; text-align: left; padding: 7px 12px; }
td { border-bottom: 1px solid #dde6f3; padding: 6px 12px; vertical-align: top; }
td code { white-space: nowrap; }

footer { color: var(--muted); font-size: 15px; }
section::after { color: var(--muted); font-size: 15px; }

/* dense slides */
section.small { font-size: 21px; }
section.small h2 { margin: 10px 0 12px; }
section.small table { font-size: 18.5px; }
section.small li { margin: 4px 0; }

/* two-column bullet lists */
section.cols2 ul { column-count: 2; column-gap: 52px; }
section.cols2 li { break-inside: avoid; }

/* callout box for the Day-2 demo / definition of done */
section .callout {
  background: #eef4ff;
  border-left: 5px solid var(--zenoh-blue);
  border-radius: 0 10px 10px 0;
  padding: 12px 18px;
  margin: 14px 0 0;
}
section .callout p { margin: 4px 0; }

/* idea chips row */
section .chips { margin: 6px 0 2px; line-height: 2.1; }
section .chips span {
  background: #eef4ff;
  color: #0b3a82;
  border: 1px solid #d4e3ff;
  border-radius: 14px;
  padding: 4px 12px;
  margin: 0 6px 6px 0;
  white-space: nowrap;
  font-size: 0.92em;
}

/* architecture-evolution opener: three columns (text over diagram) + arrows */
section.prob { font-size: 16px; padding-top: 32px; padding-bottom: 26px; }
section.prob h1 { font-size: 30px; }
section.prob h1::after { margin-top: 6px; }
section.prob .cols {
  display: grid;
  grid-template-columns: 1fr 76px 1fr 76px 1fr;
  align-items: stretch;
  margin: 16px 0 0;
}
section.prob .col { display: flex; flex-direction: column; padding: 8px 12px; }
section.prob .col h3 { margin: 0 0 4px; font-size: 18px; }
section.prob .col p { margin: 0; }
/* diagrams sit at the bottom of every column so all three line up */
section.prob .col img { width: 100%; height: auto; margin-top: auto; padding-top: 10px; }
section.prob .col.sol { background: #eef4ff; border-radius: 12px; }
section.prob .col.sol h3 { color: var(--zenoh-blue); }
section.prob .arrow { align-self: center; display: flex; justify-content: center; padding: 0 8px; }
section.prob .arrow img { width: 100%; height: auto; }
section.prob .adopt { margin: 16px 0 0; }
section.prob .adopt h2 { color: var(--zenoh-blue); font-size: 21px; margin: 0 0 5px; }
section.prob .adopt h2::after {
  content: ""; display: block; width: 64px; height: 4px; margin: 6px 0 0;
  background: linear-gradient(90deg, var(--zenoh-blue), var(--zenoh-cyan)); border-radius: 3px;
}
section.prob .logos { display: flex; align-items: stretch; gap: 14px; margin-top: 12px; }
section.prob .logos .item { flex: 1; display: flex; flex-direction: column; align-items: center; text-align: center; }
section.prob .logos .lg { height: 46px; display: flex; align-items: center; justify-content: center; }
section.prob .logos .lg img { max-height: 42px; max-width: 100%; width: auto; height: auto; }
section.prob .logos .ds { margin-top: 8px; font-size: 12.5px; color: var(--muted); line-height: 1.25; }
section.prob .logos .item.partner { background: #eef4ff; border-radius: 10px; padding: 6px 8px; }
section.prob .logos .item.partner .ds { color: var(--zenoh-navy); font-weight: 600; }
section.prob .logos .item.partner .tag {
  display: inline-block; font-size: 10.5px; font-weight: 700; letter-spacing: .4px;
  color: #fff; background: var(--zenoh-blue); border-radius: 6px; padding: 1px 7px; margin-bottom: 5px;
}

/* title slide */
section.title {
  background: radial-gradient(1200px 620px at 72% -12%, #16345f 0%, var(--zenoh-navy) 56%, #060d22 100%);
  color: #eaf2ff;
  text-align: left;
  justify-content: center;
  padding: 72px 90px;
}
section.title h1 {
  color: #ffffff;
  font-size: 86px;
  margin: 0 0 6px;
}
section.title h1::after {
  display: block;
  width: 140px;
  height: 6px;
  margin: 14px 0 0;
}
</style>

<!-- _class: prob -->

# Zenoh — the next step in cloud · edge · IoT architecture evolution

<div class="cols">

<div class="col">

### Pure cloud

Every device talks straight to the cloud. Simple, but high latency, low bandwidth, and nothing works when the link drops.

<img src="../assets/pitch-cloud.svg" alt="Two robots each connect over a long link straight to the cloud" />

</div>

<div class="arrow"><img src="../assets/arrow-right.svg" alt="evolves into" /></div>

<div class="col">

### Edge architecture

An edge router adds fast, local processing — at the cost of complexity and a different protocol on every hop (HTTPS, MQTT…).

<img src="../assets/pitch-edge.svg" alt="Cloud connects to an edge router over HTTPS; robots connect to the router over MQTT" />

</div>

<div class="arrow"><img src="../assets/arrow-right.svg" alt="evolves into" /></div>

<div class="col sol">

### Zenoh

One protocol across cloud, router and devices, with direct peer-to-peer links — transport-agnostic, any topology, minimal overhead, even *inside* a single robot.

<img src="../assets/pitch-zenoh.svg" alt="Cloud, router and robots all speak Zenoh; the two robots also peer directly with each other" />

</div>

</div>

<div class="adopt">

## Zenoh adoption

<div class="logos"><div class="item"><div class="lg"><img src="../assets/logo-ros.png" alt="ROS 2" /></div><div class="ds">ROS 2 middleware<br><code>rmw_zenoh</code></div></div><div class="item"><div class="lg"><img src="../assets/logo-woven.png" alt="Woven by Toyota" /></div><div class="ds">Software-defined<br>vehicles</div></div><div class="item"><div class="lg"><img src="../assets/logo-gm.png" alt="General Motors" /></div><div class="ds">Automotive<br>connectivity</div></div><div class="item"><div class="lg"><img src="../assets/logo-nxp.png" alt="NXP Semiconductors" /></div><div class="ds">Automotive<br>silicon</div></div><div class="item"><div class="lg"><img src="../assets/logo-eclipse-sdv.png" alt="Eclipse SDV" /></div><div class="ds">Open in-vehicle<br>stack</div></div><div class="item partner"><span class="tag">PARTNER</span><div class="lg"><img src="../assets/logo-o-cei.png" alt="O-CEI" /></div><div class="ds">Cloud·Edge·IoT continuum — Zenoh is its connectivity layer</div></div></div>

</div>

---

<!-- _class: small -->

# The Challenge — what you'll build

Pick a language you like and build a **prototype distributed app** whose instances **discover their counterparts and connect to each other** — over the local network *and* through the cloud. The work grows in **three levels**:

- **Level 1 — Basics.** Install Zenoh; run the publish/subscribe and query/reply examples.
- **Level 2 — Local network.** Instances discover each other and interact over the LAN, **with no central server**.
- **Level 3 — Cloud.** Connect through a Zenoh node in the cloud (config + access keys provided) so peers reach each other **from anywhere** — same code, Zenoh decides where the data flows.

## Pick a scenario — or invent your own

<p class="chips"><span>Chat</span><span>File sharing</span><span>Video / audio streaming</span><span>Multiplayer game</span><span>Collaborative whiteboard</span><span>Robot / drone teleop</span><span>Shared clipboard</span></p>

<div class="callout">

**Definition of Done** — a **GitHub repo** with the sources and clear build/run instructions; the **same app** runs peer-to-peer on the LAN (L2) and over the cloud (L3) without changing its logic.

**A good Day-2 demo** — two laptops running your app find each other on the local network with no server, then a **remote peer joins through the cloud router** and it just works.

</div>

---

<!-- _class: small -->

# Who it's for · what we provide

This track suits anyone curious about **distributed systems, networking and real-time apps** — and **no prior Zenoh experience is required**.

## Profiles that will enjoy it

- **Any language, any OS** — Rust, C, C++, Python, TypeScript, Kotlin, Java or Go, on Linux, macOS or Windows.
- From **embedded / microcontroller** hackers to **web / cloud** developers and **game · IoT · robotics** builders.
- People who like to **think out of the box** — originality is part of the score.

## What we provide

- **Repos & starting points** — the challenge guide, the `zenoh-ts` browser-chat example, the [zenoh-arena](https://github.com/milyin/zenoh-arena) game-state library, and the [zenoh-demos](https://github.com/eclipse-zenoh/zenoh-demos) gallery.
- **Docs** — the Zenoh introduction, a verified installation guide, and the self-hosted-router setup.
- **A cloud Zenoh router** with the access and **TLS keys** handed to you for Level 3.
- **On-site mentoring / office hours** from the Zenoh team, with the **evaluation criteria shared up front** so you know what *good* looks like.
