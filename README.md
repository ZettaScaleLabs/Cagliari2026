# Eclipse Zenoh [illustration prompt](readme-prompts/01-eclipse-zenoh.txt)

## Overview [illustration prompt](readme-prompts/02-overview.txt)

[Zenoh](https://zenoh.io/) is a data-oriented publish/subscribe and query/reply network protocol. Data is addressed by slash-separated keys, e.g. `room/sensor/temp`. [illustration prompt](readme-prompts/03-data-oriented-protocol.txt)

Zenoh was developed to provide a universal communication protocol that can work at all infrastructure levels, from microcontrollers to the cloud. [illustration prompt](readme-prompts/04-universal-communication.txt)

A good introduction to Zenoh is the [Zenoh book](https://corsaro.me/fr/zenoh/book/). The [Zenoh Rust documentation](https://docs.rs/zenoh/latest/zenoh/index.html) is also a useful source of information. [illustration prompt](readme-prompts/05-introduction-resources.txt)

The primary characteristics of Zenoh are: [illustration prompt](readme-prompts/06-primary-characteristics-intro.txt)

- **Location transparency:** Data is addressed by keys, not by node addresses. [illustration prompt](readme-prompts/07-location-transparency.txt)
- **Transport/link-protocol agnostic:** Zenoh is not bound to a single network transport; nodes can connect to each other using different protocols such as TCP, TLS, QUIC, UDP, etc. There is also shared memory transport with an enhanced user API. [illustration prompt](readme-prompts/08-transport-link-agnostic.txt)
- **Arbitrary topologies:** Zenoh nodes can establish direct connections or route data. This can be preconfigured or decided at runtime. [illustration prompt](readme-prompts/09-arbitrary-topologies.txt)
- **Wire efficiency:** Protocol overhead is minimal, so users do not pay for features they do not use. [illustration prompt](readme-prompts/10-wire-efficiency.txt)

Zenoh supports two mechanisms of data exchange: [illustration prompt](readme-prompts/11-data-exchange-intro.txt)

- **Publish/Subscribe:** Data is broadcast on a key, and instances subscribed to this key receive it. [illustration prompt](readme-prompts/12-publish-subscribe.txt)
- **Query/Reply:** Data is requested by key, and instances that serve this key send replies. [illustration prompt](readme-prompts/13-query-reply.txt)

Zenoh provides multiple convenient features: [illustration prompt](readme-prompts/14-features-intro.txt)

- **Wildcard support:** Data can be requested using wildcards, e.g. `*/sensor/temp` for all temperature sensors or `room/**` for all data available for `room`. [illustration prompt](readme-prompts/15-wildcard-support.txt)
- **Rich sample metadata:** Despite its maximal wire efficiency, the Zenoh protocol provides multiple optional metadata fields in packets. This includes timestamps, encoding, priority settings, and an area for custom metadata (attachments). [illustration prompt](readme-prompts/16-rich-sample-metadata.txt)
- **Scouting:** A Zenoh node can discover other nodes around it using features of the underlying network protocol (e.g. UDP multicast). It can also discover other nodes in the local network using a gossip mechanism. This allows it to establish a connection to the network without manual configuration. [illustration prompt](readme-prompts/17-scouting.txt)
- **Liveliness:** A node can declare a named token, and other nodes can follow the connection and disconnection of this token from the network. [illustration prompt](readme-prompts/18-liveliness.txt)
- **Matching:** Publishers and queriers can observe whether matching subscribers or queriables exist, which avoids producing or requesting data when no endpoint can consume or answer it. [illustration prompt](readme-prompts/19-matching.txt)

There are also extended features built above the base Zenoh library: [illustration prompt](readme-prompts/20-extended-features-intro.txt)

- **Advanced publisher/subscriber:** A configurable component for guaranteed packet delivery. [illustration prompt](readme-prompts/21-advanced-pub-sub.txt)
- **Serializer/deserializer:** A component for storing primitive types (integers, floats, tuples, arrays) in a compact and platform-independent format. [illustration prompt](readme-prompts/22-serializer-deserializer.txt)

## Zenoh language bindings [illustration prompt](readme-prompts/23-language-bindings.txt)

The primary implementation and source of truth is the Rust implementation of [Zenoh](https://github.com/eclipse-zenoh/zenoh). [illustration prompt](readme-prompts/24-primary-implementation.txt)

There is also a pure-C implementation, [zenoh-pico](https://github.com/eclipse-zenoh/zenoh-pico), dedicated primarily to embedded applications. [illustration prompt](readme-prompts/25-pure-c-implementation.txt)

For more powerful platforms, it is better to use [zenoh-c](https://github.com/eclipse-zenoh/zenoh-c), which wraps Rust Zenoh. [illustration prompt](readme-prompts/26-powerful-platforms.txt)

The C++ Zenoh library, [zenoh-cpp](https://github.com/eclipse-zenoh/zenoh-cpp), is a header-only wrapper over **both** zenoh-pico and zenoh-c. [illustration prompt](readme-prompts/27-cpp-library.txt)

[zenoh-go](https://github.com/eclipse-zenoh/zenoh-go/) is also implemented as a zenoh-c wrapper due to the very good interoperability between Go and C. [illustration prompt](readme-prompts/28-go-binding.txt)

Other language bindings wrap Rust Zenoh directly: [zenoh-python](https://github.com/eclipse-zenoh/zenoh-python), [zenoh-kotlin](https://github.com/eclipse-zenoh/zenoh-kotlin/), and [zenoh-java](https://github.com/eclipse-zenoh/zenoh-java). [illustration prompt](readme-prompts/29-other-language-bindings.txt)

The TypeScript Zenoh library, [zenoh-ts](https://github.com/eclipse-zenoh/zenoh-ts), is different: it connects to a server plugin through WebSocket, and the Zenoh protocol itself is implemented on the server side. [illustration prompt](readme-prompts/30-typescript-library.txt)
