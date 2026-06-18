# Eclipse Zenoh

## Overview

[Zenoh](https://zenoh.io/) is a data-oriented publish/subscribe and query/reply network protocol. Data is addressed by slash-separated keys, e.g. `room/sensor/temp`.

### Publish/Subscribe Architecture

<svg viewBox="0 0 1000 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto;">
  <defs>
    <style>
      @keyframes fadeInOut { 0%, 100% { opacity: 0; } 50% { opacity: 1; } }
      @keyframes slideRight { 0% { transform: translateX(-300px); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateX(0); opacity: 0; } }
      @keyframes slideLeft { 0% { transform: translateX(300px); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateX(0); opacity: 0; } }
      .publisher { fill: #4A90E2; }
      .subscriber { fill: #7ED321; }
      .router { fill: #F5A623; }
      .key-text { font-size: 12px; font-weight: bold; fill: white; text-anchor: middle; }
      .label { font-size: 14px; font-weight: bold; fill: #333; text-anchor: middle; }
      .message { fill: #FF6B6B; opacity: 0; }
      .msg1 { animation: slideRight 2s ease-in-out infinite; }
      .msg2 { animation: slideRight 2s ease-in-out infinite; animation-delay: 0.3s; }
      .msg3 { animation: slideLeft 2s ease-in-out infinite; animation-delay: 1s; }
      .msg4 { animation: slideLeft 2s ease-in-out infinite; animation-delay: 1.3s; }
    </style>
  </defs>
  
  <!-- Background -->
  <rect width="1000" height="400" fill="#f8f9fa"/>
  
  <!-- Publishers -->
  <circle cx="100" cy="100" r="40" class="publisher"/>
  <text x="100" y="105" class="key-text">Pub</text>
  <text x="100" y="160" class="label">Publisher 1</text>
  
  <circle cx="100" cy="300" r="40" class="publisher"/>
  <text x="100" y="305" class="key-text">Pub</text>
  <text x="100" y="360" class="label">Publisher 2</text>
  
  <!-- Router/Broker -->
  <rect x="350" y="80" width="300" height="240" rx="20" fill="none" stroke="#F5A623" stroke-width="3" stroke-dasharray="10,5"/>
  <text x="500" y="120" class="label" fill="#F5A623">Zenoh Router</text>
  
  <circle cx="500" cy="200" r="50" class="router"/>
  <text x="500" y="205" class="key-text">room/</text>
  <text x="500" y="220" class="key-text">sensor/temp</text>
  
  <!-- Subscribers -->
  <circle cx="900" cy="100" r="40" class="subscriber"/>
  <text x="900" y="105" class="key-text">Sub</text>
  <text x="900" y="160" class="label">Subscriber 1</text>
  
  <circle cx="900" cy="300" r="40" class="subscriber"/>
  <text x="900" y="305" class="key-text">Sub</text>
  <text x="900" y="360" class="label">Subscriber 2</text>
  
  <!-- Messages from Publishers to Router -->
  <circle cx="200" cy="100" r="8" class="message msg1"/>
  <circle cx="200" cy="300" r="8" class="message msg2"/>
  
  <!-- Messages from Router to Subscribers -->
  <circle cx="800" cy="100" r="8" class="message msg3"/>
  <circle cx="800" cy="300" r="8" class="message msg4"/>
  
  <!-- Arrows -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#666"/>
    </marker>
  </defs>
  
  <!-- Flow labels -->
  <text x="250" y="85" font-size="12" fill="#666">publish</text>
  <text x="750" y="85" font-size="12" fill="#666">deliver</text>
  
  <!-- Subscription lines (dashed) -->
  <line x1="140" y1="100" x2="350" y2="170" stroke="#7ED321" stroke-width="2" stroke-dasharray="5,5" opacity="0.5"/>
  <line x1="140" y1="300" x2="350" y2="230" stroke="#7ED321" stroke-width="2" stroke-dasharray="5,5" opacity="0.5"/>
  <line x1="550" y1="170" x2="860" y2="100" stroke="#7ED321" stroke-width="2" stroke-dasharray="5,5" opacity="0.5"/>
  <line x1="550" y1="230" x2="860" y2="300" stroke="#7ED321" stroke-width="2" stroke-dasharray="5,5" opacity="0.5"/>
  
  <!-- Key description -->
  <rect x="350" y="330" width="300" height="50" fill="#fff" stroke="#F5A623" stroke-width="1" rx="5"/>
  <text x="500" y="350" font-size="13" fill="#333" text-anchor="middle" font-weight="bold">Key: room/sensor/temp</text>
  <text x="500" y="370" font-size="11" fill="#666" text-anchor="middle">All publishers write, all subscribers receive</text>
</svg>

Zenoh was developed to provide a universal communication protocol that can work at all infrastructure levels, from microcontrollers to the cloud.

A good introduction to Zenoh is the [Zenoh book](https://corsaro.me/fr/zenoh/book/). The [Zenoh Rust documentation](https://docs.rs/zenoh/latest/zenoh/index.html) is also a useful source of information.

The primary characteristics of Zenoh are:

- **Location transparency:** Data is addressed by keys, not by node addresses.
- **Transport/link-protocol agnostic:** Zenoh is not bound to a single network transport; nodes can connect to each other using different protocols such as TCP, TLS, QUIC, UDP, etc. There is also shared memory transport with an enhanced user API.
- **Arbitrary topologies:** Zenoh nodes can establish direct connections or route data. This can be preconfigured or decided at runtime.
- **Wire efficiency:** Protocol overhead is minimal, so users do not pay for features they do not use.

Zenoh supports two mechanisms of data exchange:

- **Publish/Subscribe:** Data is broadcast on a key, and instances subscribed to this key receive it.
- **Query/Reply:** Data is requested by key, and instances that serve this key send replies.

Zenoh provides multiple convenient features:

- **Wildcard support:** Data can be requested using wildcards, e.g. `*/sensor/temp` for all temperature sensors or `room/**` for all data available for `room`.
- **Rich sample metadata:** Despite its maximal wire efficiency, the Zenoh protocol provides multiple optional metadata fields in packets. This includes timestamps, encoding, priority settings, and an area for custom metadata (attachments).
- **Scouting:** A Zenoh node can discover other nodes around it using features of the underlying network protocol (e.g. UDP multicast). It can also discover other nodes in the local network using a gossip mechanism. This allows it to establish a connection to the network without manual configuration.
- **Liveliness:** A node can declare a named token, and other nodes can follow the connection and disconnection of this token from the network.
- **Matching:** Publishers and queriers can observe whether matching subscribers or queriables exist, which avoids producing or requesting data when no endpoint can consume or answer it.

There are also extended features built above the base Zenoh library:

- **Advanced publisher/subscriber:** A configurable component for guaranteed packet delivery.
- **Serializer/deserializer:** A component for storing primitive types (integers, floats, tuples, arrays) in a compact and platform-independent format.

## Zenoh language bindings

The primary implementation and source of truth is the Rust implementation of [Zenoh](https://github.com/eclipse-zenoh/zenoh).

There is also a pure-C implementation, [zenoh-pico](https://github.com/eclipse-zenoh/zenoh-pico), dedicated primarily to embedded applications.

For more powerful platforms, it is better to use [zenoh-c](https://github.com/eclipse-zenoh/zenoh-c), which wraps Rust Zenoh.

The C++ Zenoh library, [zenoh-cpp](https://github.com/eclipse-zenoh/zenoh-cpp), is a header-only wrapper over **both** zenoh-pico and zenoh-c.

[zenoh-go](https://github.com/eclipse-zenoh/zenoh-go/) is also implemented as a zenoh-c wrapper due to the very good interoperability between Go and C.

Other language bindings wrap Rust Zenoh directly: [zenoh-python](https://github.com/eclipse-zenoh/zenoh-python), [zenoh-kotlin](https://github.com/eclipse-zenoh/zenoh-kotlin/), and [zenoh-java](https://github.com/eclipse-zenoh/zenoh-java).

The TypeScript Zenoh library, [zenoh-ts](https://github.com/eclipse-zenoh/zenoh-ts), is different: it connects to a server plugin through WebSocket, and the Zenoh protocol itself is implemented on the server side.
