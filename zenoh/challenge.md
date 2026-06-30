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

  Open two browser windows, press **Connect** in both, and watch them talk.

  This prototype was purposely kept as simple as possible to demonstrate Zenoh
  usage without distractions. There are many ways to turn this prototype into a
  genuinely useful application:

  - Chat application with server registration and secure direct connections bypasing server
  - File transfer
  - Android chat application
  - Message encryption
  - Something else?

- **File sharing application.** Share files between peers and let Zenoh choose the
  route automatically — directly over the local network when the peers are close,
  or through the cloud server when they are not — thanks to location transparency.

- **Video / audio streaming.** Live broadcasting, one-to-one calls, or a small
  conference. A nice stress test for Zenoh's throughput and latency.

- **Multiplayer game.** Share game state in real time over Zenoh. The big
  advantage: it can run peer-to-peer on the local network with no central server,
  and fall back to the cloud server when the players are remote.

  Here are a few experiments with it:
  - Game state sharing library and multiplayer Tetris: https://github.com/milyin/zenoh-arena
  - King of bots demo http://demo.zenoh.io/king-of-bots/

- **Collaborative whiteboard or document editor** — every edit is published and
  every participant subscribes, for real-time shared drawing or text.

- **Robot or drone teleoperation** — stream control commands one way and sensor or
  video feedback the other way, locally or over the cloud.

- **Shared clipboard / device sync** — copy on one device and paste on another,
  whether or not they share a network.

See also app examples at https://github.com/eclipse-zenoh/zenoh-demos - some
are obsolete, but they are still useful as inspiration.

## Deliverables

A link to a GitHub repository with the project sources and clear instructions on
how to build and run it.

Links to the results will be published in this repository.

## Evaluation Criteria

| Category | Weight | Description |
|----------|--------|-------------|
| Zenoh functionality usage | 25% | Correct and idiomatic use of Zenoh API and key expression organization. Using advanced Zenoh features when they are useful for the task |
| User interface | 25% | Logical application interface, comprehensive onboarding instructions. It's evaluated how smooth the user experience with the application is. Note: command line interface is not penalized, it's completely ok |
| Application functionality | 25% | How complex and interesting the application is. Does it provide the basic functions which are expected from this kind of application? Does it provide some extended functionality? |
| Code Quality | 10% | Readability, maintainability, clarity of the application logic, clean separation of AI-sloppy parts (it's inavoidable nowadays 😭) behind clean and strict interfaces |
| Idea originality | 15% | Thinking out of the box, making the non-trivial application concept, using zenoh in the original domain |