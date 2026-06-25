# <img src="../assets/zenoh-dragon.png" alt="Eclipse Zenoh logo" height="64" align="middle">&nbsp; Zenoh Challenge

## Introduction

The challenge invites you to explore the Eclipse Zenoh network protocol in your
favourite programming language and to build a prototype distributed application
with it. Zenoh is a location-transparent, transport-agnostic pub/sub and
query/reply protocol that connects everything from microcontrollers to the
cloud — see the [introduction](intro.md) for the concepts and the
[installation guide](install.md) to get it running.

You can use any of the supported languages — Rust, C, C++, Python, TypeScript,
Kotlin, Java, or Go — on Linux, macOS, or Windows. The core idea of the
challenge is to make instances of your application **discover their counterparts
and connect to each other**, both over the local network and through a cloud
server.

The challenge is split into three levels:

- **Level 1 — Basics.** Install Zenoh, then build and run the basic examples
  (publish/subscribe and query/reply).
- **Level 2 — Local network.** Implement an application whose instances discover
  each other and interact over the local network, with no central server.
- **Level 3 — Cloud.** Connect to a Zenoh node running in the cloud so your
  instances can reach their peers from anywhere. The configuration and access
  keys — including the key for the TLS connection to the remote server — will be
  provided.

## Ideas

Pick one of the ideas below or invent your own. A good application can start
small on the local network (Level 2) and then grow into a cloud-connected one
(Level 3) without changing its logic — Zenoh takes care of where the data flows.

- **Chat application.** Start from the zenoh-ts browser chat example and grow it
  into something richer. Build the library as shown in the
  [installation guide](install.md#typescript--javascript); the `DAEMON` argument
  then starts the Zenoh bridge for you, so a single command from the `zenoh-ts`
  directory is enough:

  ```sh
  yarn start DAEMON example browser chat
  ```

  Open two browser windows, press **Connect** in both, and watch them talk. From
  there, extend both the functionality and the protocol: direct (private) chats,
  file transfer, presence / online status, a dedicated server component, message
  history, or a client written for another platform or language that interoperates
  over the same key expressions.

- **File sharing application.** Share files between peers and let Zenoh choose the
  route automatically — directly over the local network when the peers are close,
  or through the cloud server when they are not — thanks to location transparency.

- **Video / audio streaming.** Live broadcasting, one-to-one calls, or a small
  conference. A nice stress test for Zenoh's throughput and latency.

- **Multiplayer game.** Share game state in real time over Zenoh. The big
  advantage: it can run peer-to-peer on the local network with no central server,
  and fall back to the cloud server when the players are remote.

A few more ideas to spark your imagination:

- **Collaborative whiteboard or document editor** — every edit is published and
  every participant subscribes, for real-time shared drawing or text.
- **Distributed sensor dashboard (IoT)** — publish telemetry from sensors (or from
  zenoh-pico on a microcontroller) and visualise it live; use query/reply and
  storages to fetch history. This plays directly to Zenoh's "microcontrollers to
  the cloud" strength.
- **Robot or drone teleoperation** — stream control commands one way and sensor or
  video feedback the other way, locally or over the cloud.
- **Shared clipboard / device sync** — copy on one device and paste on another,
  whether or not they share a network.
- **Presence and service directory** — use liveliness tokens to track which nodes
  and services are online across the whole network.

## Deliverables

A link to a GitHub repository with the project sources and clear instructions on
how to build and run it.

## Evaluation criteria

| Category | Weight | Description |
| --- | --- | --- |
| Zenoh functionality usage | 25% | Correct and idiomatic use of the Zenoh API and key-expression design, including advanced Zenoh features where they help the task. |
| User interface | 25% | A logical interface and clear onboarding instructions, and how smooth the overall experience is. A command-line interface is perfectly fine and is **not** penalised. |
| Application functionality | 25% | How complex and interesting the application is: does it provide the functions expected of such an app, and does it add something extra? |
| Code quality | 10% | Readability, maintainability, and a clean separation of generated / "AI" parts behind clear, strict interfaces. |
| Idea originality | 15% | Thinking outside the box — a non-trivial concept, or using Zenoh in an original domain. |
