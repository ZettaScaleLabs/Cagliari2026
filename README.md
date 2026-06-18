# Eclipse Zenoh

## Overview

[Zenoh](https://zenoh.io/) is a data-oriented publish/subscribe and query/reply network protocol. The data is addessed by slash-separated keys, e.g. `room/sensor/temp`.

The Zenoh was developed to provide universal communication protocol which can work on all infrastructure levels from microcontroller to the cloud.

The primary characteristics of Zenoh are:

- **Location transparency**: Data is addressed by keys, not by node addresses
- **Transport/link-protocol agnostic:** Zenoh is not bound to single network transport; nodes can connecte each other by different protocols such as TCP, TLS, QUIC, UDP, etc. There is also shared memory transport with enhanced user API.
- **Arbitrary topologies:** A Zenoh nodes can establish direct connections or route data. This can be preconfigured or decided at runtime.
- **Wire efficiency** The protocol overhead is minimal, the user is not paying for features he doesn't use

Zenoh support two mechanisms of data exchange:

- **Publish/Subscribe**: The data is broadcasted on key, the instances subcribed to this key receives it
- **Query/Reply**: The data is requested by the key, the instances which serves this key send the replies

There are multiple convenient features provided by zenoh:

- **Wildcard support**: The data can be requested using wildcards, e.g. `*/sensor/temp` for all temperature sensors or `room/**` for all data availabe for `room`.
- **Rich sample metadata**: Despite of maximal wire efficiency, the Zenoh protocol provides multiplle optional metadata field in the packet. This includes timestamp, encoding, priority settings, area for custom metadata (attachment).
- **Scouting**: Zenoh node can discover other nodes around it using features of underlying network protocol (e.g. UDP multicast). It can also discover other nodes in the local network using gossip mechanism. This allows to establish connection to the network without manual configuration.
- **Liveliness**: A node can declare a named token and other nodes can follow the connection and disconnection of this token from the network.
- **Matching**: Publishers and queriers can observe whether a matching subscribers or queriables exists, which avoids producing or requesting data when no endpoint can consume or answer it.

There are also extended features built above the base Zenoh library:

- **Advanced publisher/subscriber**: The configurable component for guaranteed packet delivery
- **Serializer/deserializer**: The component for storing primitive types (integers, floats, tuples, arrays) in compact and platform-independent format

## Zenoh language bindings

The primary implementation and the source of truth is the Rust implementation of [Zenoh](https://github.com/eclipse-zenoh/zenoh)

There is also pure-C implementation [zenoh-pico](https://github.com/eclipse-zenoh/zenoh-pico) dedicated primarily to embedded applications.

For the more powerful platforms it's better to use [zenoh-c](https://github.com/eclipse-zenoh/zenoh-c) which wraps the Rust zenoh.

The C++ zenoh library https://github.com/eclipse-zenoh/zenoh-cpp is a header-only wrapper over **both** zenoh-pico and zenoh-c.

The [zenoh-go](https://github.com/eclipse-zenoh/zenoh-go/) is also implemented as zenoh-c wrapper due to very good interoperability between Go and C.

Other language bindings wraps the Rust zenoh directly: [zenoh-python](https://github.com/eclipse-zenoh/zenoh-python), [zenoh-kotlin](https://github.com/eclipse-zenoh/zenoh-kotlin/), [zenoh-java](https://github.com/eclipse-zenoh/zenoh-java)

The Typescript zenoh lirary [zenoh-ts](https://github.com/eclipse-zenoh/zenoh-ts) is different: it connects to server plugin through websocket, the zenoh protocol itself is implemented on the server side.
