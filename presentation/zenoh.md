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
  background: #ffffff;
  padding: 54px 64px 60px;
  line-height: 1.45;
}

section h1 {
  color: var(--zenoh-navy);
  font-size: 46px;
  margin: 0 0 2px;
}
section h1::after {
  content: "";
  display: block;
  width: 84px;
  height: 5px;
  margin-top: 10px;
  background: linear-gradient(90deg, var(--zenoh-blue), var(--zenoh-cyan));
  border-radius: 3px;
}
section h2 {
  color: var(--zenoh-blue);
  font-size: 29px;
  font-weight: 600;
  margin: 16px 0 18px;
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
section.tight h1 { font-size: 38px; }
section.tight h1::after { margin-top: 6px; height: 4px; }
section.tight h2 { font-size: 24px; margin: 8px 0 10px; }
section.tight > p { margin: 0 0 10px; }
section.tight table { font-size: 17px; }
section.tight th, section.tight td { padding: 4px 12px; line-height: 1.3; }

/* two-column bullet lists */
section.cols2 ul { column-count: 2; column-gap: 52px; }
section.cols2 li { break-inside: avoid; }

/* centered media slides */
section.media { text-align: center; }
section.media h1::after { margin-left: auto; margin-right: auto; }
section.media p.cap { color: var(--muted); font-size: 20px; margin: 6px 0 14px; }
section.media img { margin-top: 6px; }

/* title slide */
section.title {
  background: radial-gradient(1200px 620px at 72% -12%, #16345f 0%, var(--zenoh-navy) 56%, #060d22 100%);
  color: #eaf2ff;
  text-align: center;
  justify-content: center;
  padding: 64px;
}
section.title h1 {
  color: #ffffff;
  font-size: 78px;
  margin: 0 0 10px;
}
section.title h1::after { display: none; }
section.title p { margin: 0; }
section.title p:nth-of-type(1) {
  color: var(--zenoh-cyan);
  font-size: 30px;
  letter-spacing: 0.4px;
}
section.title p:nth-of-type(2) {
  color: #c7d6ef;
  font-size: 26px;
  margin-top: 30px;
}
section.title p:nth-of-type(3) {
  display: inline-block;
  background: #ffffff;
  border-radius: 16px;
  padding: 16px 30px;
  margin-top: 46px;
  box-shadow: 0 16px 40px rgba(0,0,0,0.35);
}
section.title p:nth-of-type(3) img { vertical-align: middle; margin: 0 22px; }
</style>

<!-- _class: title -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Eclipse Zenoh

The next generation network protocol

Mikhail ILIN&nbsp;&nbsp;·&nbsp;&nbsp;Ivan PAEZ

![h:62](../assets/eclipse-foundation-logo.svg) ![h:84](../assets/zenoh-dragon.png) ![h:54](../assets/svg-components/zetta-scale-logo.svg)

---

# What is Zenoh

**Zenoh** is a data-oriented **publish / subscribe** and **query / reply** network protocol.

- Data is addressed by **slash-separated keys** — e.g. `room/sensor/temp` — not by node addresses.
- Built as a **universal communication protocol** that works at every infrastructure level, **from microcontrollers to the cloud**.
- It unifies data **in motion**, data **at rest**, and **computations** in a single, efficient stack.

Learn more: [zenoh.io](https://zenoh.io/) · the [Zenoh book](https://corsaro.me/fr/zenoh/book/) · [Zenoh Rust](https://docs.rs/zenoh/latest/zenoh/index.html) & [Zenoh-Python](https://zenoh-python.readthedocs.io/en/latest/) API docs.

---

<!-- _class: cols2 -->

# Zenoh's advantages

- **Transport-agnostic**
  Runs over TCP, TLS, QUIC, UDP, and more — plus shared-memory transport with an enhanced API.

- **Arbitrary topology**
  Nodes connect directly or route through intermediaries; the topology can be preconfigured or decided at runtime.

- **Wire efficiency**
  Minimal overhead — you don't pay for features you don't use. The minimum header is just **5 bytes**.

- **Wildcard support**
  Subscribe to or request data with wildcards — `*/sensor/temp`, or `room/**` for everything under `room`.

---

# Concepts
## Key Expressions

- A **key expression (KE)** is Zenoh's address space: a small, glob-like language describing a **set of keys**.
- Every operation targets a KE, and a KE is **associated with a value — or a stream of values** (each new publication updates it).
- Two wildcards:
  - `*` — matches **a single** chunk: `room/*/temp`
  - `**` — matches **zero or more** chunks: `room/**`
- KEs support set operations such as `intersects` and `includes`, e.g. `robot/**` *includes* `robot/sensor/temp`.

---

<!-- _class: media -->

# Concepts
## Publish / Subscribe

Data is **published** under a key; every instance **subscribed** to a matching key receives it. Subscription declarations are spread across the network, so routers know which subscribers are interested.

![h:404](../assets/zenoh-pub-sub.svg)

---

<!-- _class: small tight -->

# Concepts
## Sample

A **`Sample`** is the unit of data delivered to subscribers and carried inside replies.

| Field | Meaning |
|---|---|
| `key_expr` | The key the data is associated with |
| `payload` | The data bytes (`ZBytes`) |
| `kind` | `Put` (new value) or `Delete` (value removed) |
| `encoding` | Hint describing how to interpret the payload |
| `timestamp` | Optional network timestamp (ordering / dedup) |
| `priority` | Transmission priority of the message |
| `congestion_control` | Behaviour under congestion: `Drop` or `Block` |
| `express` | If `true`, the message is **not batched** → lower latency |
| `reliability` | `Reliable` or `BestEffort` delivery |
| `attachment` | Optional user-defined metadata buffer |
| `source_info` | Source id and sequence number of the message |

---

<!-- _class: media -->

# Concepts
## Get / Reply

Data is **requested by key** via `Session::get` (or a `Querier`); every **queryable** serving a matching key sends back **replies**. Each request returns **zero or more** `Reply` values — each carrying a `Sample` (`Ok`) or a `ReplyError` (`Err`).

![h:356](../assets/zenoh-query.svg)

---

<!-- _class: small -->
<!-- _backgroundColor: #ffffff -->

# Concepts
## Selector, Reply

![bg right:45% fit](../assets/zenoh-location-transparency.svg)

- A **`Selector`** = a key expression **+ parameters**, URL-like: `room/temp?day=2023-03-15;unit=C`
  - `key_expr()` · `parameters()` · `accept_replies()`
- A **`Reply`** carries `result()` → `Ok(Sample)` or `Err(ReplyError)`, plus the `replier_id()`.
- **Completeness** — a queryable may declare `complete = true`, claiming it holds **all** data for its keyexpr; otherwise it is partial.
- **Target** selects which queryables answer: `BestMatching` (nearest), `All`, or `AllComplete`.
- Replies can be **best-effort** and **consolidated** so the querier sees only the latest value per key.

---

# Concepts
## Session

- The **`Session`** is the main Zenoh object — it holds the runtime and the node's connection state. Opened with `zenoh::open(Config)`.
- **`config()`** — the runtime configuration (connect/listen endpoints, scouting, transports…).
- **`info()`** → `SessionInfo`: `zid()`, `routers_zid()`, `peers_zid()`, plus `links()` / `transports()` — the **connectivity API**.
- **`zid()`** → the **`ZenohId`**, this node's unique network identity.
- **Scouting** — discover peers automatically via UDP multicast or gossip (`zenoh::scout`), no manual config.
- Roughly **1 session = 1 Zenoh node** *(plugins are the exception: they share one `zenohd` runtime, hence one `zid`)*.

---

# Concepts
## Liveliness

- A node declares a named **`LivelinessToken`** on a key expression — a lightweight presence signal.
- A token stays **alive** until it is **undeclared**, or its **session is closed / disconnected** from the network.
- Other nodes can observe liveliness on a key expression:
  - **`get()`** — query the tokens that currently exist.
  - **`declare_subscriber()`** — be notified as tokens appear (`Put`) or disappear (`Delete`).
  - The **`history`** option replays already-declared tokens to a new subscriber.
- Ideal for **presence detection** and reacting to nodes joining or failing.

---

# Concepts
## Serialization

- **Not part of the Zenoh wire protocol** — on the wire a payload is just bytes (`ZBytes`).
- It lives in **`zenoh-ext`** as a convenience: `z_serialize` / `z_deserialize` (`ZSerializer` / `ZDeserializer`).
- Produces a **compact, platform-independent** layout, so the **same data looks the same** across languages and platforms — integers, floats, strings, tuples, arrays/vectors, maps…
- Purely optional: users are free to use **Protobuf, JSON / BSON, CBOR**, or any format they like for their payloads.

---

# Concepts
## Advanced Pub/Sub

A **configurable** layer on top of base pub/sub for **guaranteed delivery** — sending data over pub/sub and using query/reply to retransmit what was missed.

- **`AdvancedPublisher`** — **caches** published samples, **numbers** them for miss detection, announces its presence, and can emit periodic **heartbeats**.
- **`AdvancedSubscriber`**:
  - **`history`** — fetch past samples (late joiners catch up).
  - **`recovery`** — request **retransmission of missing** samples (periodic query or heartbeat-driven).
  - **`sample_miss_detection`** — detect gaps and get notified (`Miss`: source + count).
- **Different strategies, all opt-in and tunable** via `CacheConfig`, `HistoryConfig`, `RecoveryConfig`, `MissDetectionConfig`.
