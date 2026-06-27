---
marp: true
title: Eclipse Zenoh
description: The next generation network protocol
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

/* extra-tight table slide (Sample) */
section.tight { padding-top: 40px; }
section.tight h2 { font-size: 24px; margin: 8px 0 10px; }
section.tight > p { margin: 0 0 10px; }
section.tight table { font-size: 17px; }
section.tight th, section.tight td { padding: 4px 12px; line-height: 1.3; }

/* two-column bullet lists */
section.cols2 ul { column-count: 2; column-gap: 52px; }
section.cols2 li { break-inside: avoid; }

/* centered media slides — only the media is centered; the title block stays
   left-aligned and identical to every other slide. */
section.media { text-align: center; }
section.media h1 { text-align: left; }
section.media p.cap { color: var(--muted); font-size: 20px; margin: 6px 0 14px; }
section.media img { margin-top: 6px; }

/* side image slide: image pinned to the right, below the logo zone, so the
   top-right logo template stays clear (avoids Marpit split-bg covering it). */
section.side img.side {
  position: absolute;
  right: 48px;
  top: 196px;
  width: 42%;
  height: auto;
}
section.side ul, section.side ol { width: 48%; }

/* grouped-field slide (Sample): several short groups, tighter rhythm */
section.groups { font-size: 19.5px; }
section.groups > p { margin: 0 0 8px; }
section.groups h2 { margin: 10px 0 5px; }
section.groups li { margin: 2px 0; }

/* diagram rows (Matching, Consolidation): three network diagrams side by side */
section .diorow { display: flex; gap: 10px; justify-content: center; align-items: flex-start; margin: 10px 0 0; }
section .diorow figure { margin: 0; text-align: center; }
section .diorow img { width: 368px; height: auto; }
section .diorow figcaption { font-size: 14px; color: var(--muted); margin-top: -2px; }

/* selector breakdown chip */
section .selector { font-size: 26px; margin: 6px 0 14px; }
section .selector .kx { color: var(--zenoh-navy); font-weight: 700; }
section .selector .pm { color: #c47f12; font-weight: 700; }

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
section.title p { margin: 0; }
section.title p:nth-of-type(1) {
  color: var(--zenoh-cyan);
  font-size: 34px;
  letter-spacing: 0.4px;
  margin-top: 26px;
}
section.title p:nth-of-type(2) {
  color: #c7d6ef;
  font-size: 28px;
  margin-top: 40px;
}
section.title p:nth-of-type(3) {
  display: inline-block;
  background: #ffffff;
  border-radius: 16px;
  padding: 18px 34px;
  margin-top: 56px;
  box-shadow: 0 16px 40px rgba(0,0,0,0.35);
}
section.title p:nth-of-type(3) img { vertical-align: middle; margin: 0 26px; }
</style>

<!-- _class: title -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Eclipse Zenoh

The next generation network protocol

Mikhail ILIN&nbsp;&nbsp;·&nbsp;&nbsp;Ivan PAEZ

![h:62](../assets/eclipse-foundation-logo.svg) ![h:84](../assets/zenoh-dragon.png) ![h:54](../assets/svg-components/zetta-scale-logo.svg)

---

<!-- _class: cols2 small -->

# What is Zenoh

**Zenoh** is a location-transparent **publish / subscribe** and **query / reply** network protocol. Built as a **universal communication protocol** that works at every infrastructure level, **from microcontrollers to the cloud**.

- **Location transparency**
  Data is addressed by slash-separated keys — e.g. `room/sensor/temp` — not by node addresses.

- **Transport-agnostic**
  Runs over TCP, TLS, QUIC, UDP, and more — plus shared-memory transport with an enhanced API.

- **Arbitrary topology**
  Nodes connect directly or route through intermediaries; the topology can be preconfigured or decided at runtime.

- **Wire efficiency**
  Minimal overhead — you don't pay for features you don't use. The minimum header is just **5 bytes**.

- **Wildcard support**
  Subscribe to or request data with wildcards — `*/sensor/temp`, or `room/**` for everything under `room`.

---

# Key Expressions

- A **key expression (KE)** is Zenoh's address space: a small, glob-like language describing a **set of keys**.
- Every operation targets a KE, and a KE is **associated with a value — or a stream of values** (each new publication updates it).
- Two wildcards:
  - `*` — matches **a single** chunk: `room/*/temp`
  - `**` — matches **zero or more** chunks: `room/**`
- KEs support set operations such as `intersects` and `includes`, e.g. `robot/**` *includes* `robot/sensor/temp`.

---

<!-- _class: media -->

# Publish / Subscribe

Data is **published** under a key; every instance **subscribed** to a matching key receives it. Subscription declarations are spread across the network, so routers know which subscribers are interested.

![h:404](../assets/zenoh-pub-sub.svg)

---

<!-- _class: media -->

# Get / Reply

Data is **requested by key** via `Session::get` (or a `Querier`); every **queryable** serving a matching key sends back **replies**. Each request returns **zero or more** `Reply` values — each carrying a `Sample` (`Ok`) or a `ReplyError` (`Err`).

![h:356](../assets/zenoh-query.svg)

---

<!-- _class: small groups -->

# Sample

Data delivered to subscribers — and carried inside every reply — arrives as a **`Sample`**. On the user API you never build one when sending: it is assembled internally from the publisher / queryable options and the reply-operation parameters.

## Required

- **`key_expr`** — the key expression on which this `Sample` was published.
- **`payload`** — the data itself, a buffer of bytes (`ZBytes`).
- **`kind`** — whether this is a new value (`Put`) or a removal of the value at the key (`Delete`).

## Metadata

- **`encoding`** *(optional)* — it's up to the application to use it and how to interpret it. A set of predefined encodings are hardcoded into constants to transmit them efficiently, without a string value; others are transmitted as a string.
- **`timestamp`** *(optional)* — the timestamp assigned to the data. If enabled, assigned automatically with the current time and node id (i.e. the timer is identified).
- **`attachment`** *(optional)* — a separate bytes buffer for user-defined metadata.

## Quality of service — how to transmit the message, or how it *was* transmitted

- **`priority`** — the priority it was sent with; **`congestion_control`** — drop it or block when links were congested.
- **`express`** — if set, the message was not batched during transmission, to reduce latency.

---

<!-- _class: small -->

# Selector

A **`Selector`** says **what a query asks for** — a key expression plus optional parameters, written URL-style:

<p class="selector"><span class="kx">room/*/temp</span><span class="pm">?from=sensor;unit=C</span></p>

- **`key_expr()`** — the **set of keys** the query matches: the *what*.
- **`parameters()`** — free-form `key=value;…` arguments handed to every queryable: the *how* — filters, ranges, formatting.
- Parameters are **user-defined**, but there are ones **interpreted by Zenoh itself** — e.g. `_anyke` for **`accept_replies()`**, which lets make **disjoint** replies (on key expressions outside requested keyexpr).
- So one key expression can serve different requests: the same queryable reads the parameters to decide what to compute or return.

---

<!-- _class: small -->

# Matching

Every queryable whose key expression matches can answer. Two things decide **which ones actually do**:

- **Completeness** — a queryable may declare `complete = true`, claiming it holds **all** the data for its key expression; otherwise it is **partial** (it may hold only some).
- **Target** — chosen by the querier, it selects which matching queryables the query reaches:

<div class="diorow">
  <figure><img src="../assets/zenoh-target-bestmatching.svg" alt="BestMatching target reaches only the nearest queryable" /><figcaption><code>BestMatching</code> <em>(default)</em> — nearest match</figcaption></figure>
  <figure><img src="../assets/zenoh-target-all.svg" alt="All target reaches every matching queryable" /><figcaption><code>All</code> — every match</figcaption></figure>
  <figure><img src="../assets/zenoh-target-allcomplete.svg" alt="AllComplete target reaches only complete queryables" /><figcaption><code>AllComplete</code> — complete only</figcaption></figure>
</div>

---

<!-- _class: small -->

# Consolidation

When several queryables answer for the **same key**, consolidation decides what the querier finally sees. Below, three storages reply with values stamped **`t1 < t2 < t3`**, reaching the robot out of order (`t2`, `t1`, `t3`):

<div class="diorow">
  <figure><img src="../assets/zenoh-consolidation-none.svg" alt="None consolidation delivers every reply" /><figcaption><code>None</code> — every reply, in arrival order</figcaption></figure>
  <figure><img src="../assets/zenoh-consolidation-monotonic.svg" alt="Monotonic consolidation drops stale replies" /><figcaption><code>Monotonic</code> — never goes backwards</figcaption></figure>
  <figure><img src="../assets/zenoh-consolidation-latest.svg" alt="Latest consolidation keeps only the newest value per key" /><figcaption><code>Latest</code> — newest per key only</figcaption></figure>
</div>

---

# Reply

Each **`Reply`** is one queryable's answer to the query. `result()` returns one of two variants:

- **`Ok(Sample)`** — a successful answer: a full **`Sample`** (payload, encoding, timestamp…) for a matched key.
- **`Err(ReplyError)`** — the queryable reported a failure; `ReplyError` carries a **`payload()`** and its **`encoding()`** describing what went wrong.
- **`replier_id()`** — identifies which queryable produced this reply.
- A single `get` yields **zero or more** replies, each independently `Ok` or `Err`.

---

<!-- _class: small -->

# Session

The **`Session`** is the main Zenoh object — it holds the runtime and the node's connection state. Opened with `zenoh::open(Config)`.

## Connectivity API

The session provides an API to **get information about its connections to other nodes**.

- **`info()`** → `SessionInfo`: `zid()`, `routers_zid()`, `peers_zid()`, plus `links()` / `transports()`.

## Scouting

The session can **establish connections to other nodes without configuring them explicitly** — peers are discovered automatically over UDP multicast or gossip while the session is opening.

### `zenoh::scout`

A standalone **information API**: it runs the same network browse as the scouting performed internally at session open, but **only to report** the nodes it finds — it establishes no connection.

---

# Liveliness

- A node declares a named **`LivelinessToken`** on a key expression — a lightweight presence signal.
- A token stays **alive** until it is **undeclared**, or its **session is closed / disconnected** from the network.
- Other nodes can observe liveliness on a key expression:
  - **`get()`** — query the tokens that currently exist.
  - **`declare_subscriber()`** — be notified as tokens appear (`Put`) or disappear (`Delete`).
  - The **`history`** option replays already-declared tokens to a new subscriber.
- Ideal for **presence detection** and reacting to nodes joining or failing.

---

# Serialization

- **Not part of the Zenoh wire protocol** — on the wire a payload is just bytes (`ZBytes`).
- It lives in **`zenoh-ext`** as a convenience: `z_serialize` / `z_deserialize` (`ZSerializer` / `ZDeserializer`).
- Produces a **compact, platform-independent** layout, so the **same data looks the same** across languages and platforms — integers, floats, strings, tuples, arrays/vectors, maps…
- Purely optional: users are free to use **Protobuf, JSON / BSON, CBOR**, or any format they like for their payloads.

---

# Advanced Pub/Sub

A **configurable** layer on top of base pub/sub for **guaranteed delivery** — sending data over pub/sub and using query/reply to retransmit what was missed.

- **`AdvancedPublisher`** — **caches** published samples, **numbers** them for miss detection, announces its presence, and can emit periodic **heartbeats**.
- **`AdvancedSubscriber`**:
  - **`history`** — fetch past samples (late joiners catch up).
  - **`recovery`** — request **retransmission of missing** samples (periodic query or heartbeat-driven).
  - **`sample_miss_detection`** — detect gaps and get notified (`Miss`: source + count).
- **Different strategies, all opt-in and tunable** via `CacheConfig`, `HistoryConfig`, `RecoveryConfig`, `MissDetectionConfig`.
