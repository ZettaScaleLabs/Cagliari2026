# Eclipse Zenoh

## Overview

[Zenoh](https://zenoh.io/) is a data-oriented publish/subscribe and query/reply network protocol. Data is addressed by slash-separated keys, e.g. `room/sensor/temp`.

Zenoh was developed to provide a universal communication protocol that can work at all infrastructure levels, from microcontrollers to the cloud.

A good introduction to Zenoh is the [Zenoh book](https://corsaro.me/fr/zenoh/book/). The [Zenoh Rust documentation](https://docs.rs/zenoh/latest/zenoh/index.html) is also a useful source of information.

The primary advantages of Zenoh are:

- **Transport agnostic**

  Zenoh is not bound to a single network transport; it can work above multiple protocols such as TCP, TLS, QUIC, UDP, etc. There is also shared memory transport with an enhanced user API.

- **Arbitrary topology**

  Zenoh nodes can establish direct connections to each otehr or route data through intermedate notes. The network topolgy can be preconfigured or decided at runtime.

- **Wire efficiency**

  Protocol overhead is minimal, so users do not pay for features they do not use. The minimal header size is just 5 bytes.

- **Wildcard support**

  Data can be requested / subscribed using wildcard key expressions, e.g. `*/sensor/temp` for all temperature sensors or `room/**` for all data available for `room`.

## Zenoh concepts

The primary mechanisms of zenoh are data-centric: publish / subscribe and query / reply. There is also and set of supporting APIs and functtionalities.

### Publish / Subscribe

Data is published under a key, and instances subscribed to that key receive it. Subscription declarations are distributed throughout the network, so routers know which subscribers are interested in the data.

<p align="center">
  <img src="assets/zenoh-pub-sub.svg" alt="Animated Zenoh publish/subscribe data flow" width="860">
</p>

### Query / Reply

Data is requested by key, and instances that can serve that key send replies. As with publish/subscribe, key-availability declarations are distributed so routers know where to forward requests.

<p align="center">
  <img src="assets/zenoh-query.svg" alt="Animated Zenoh query/reply data flow" width="860">
</p>

### Other functionalities

- **Rich data sample**

  Despite of the minial network overhead, the multiple optional metadata fields are provided. It's timestamp, encoding, priority settings, and custom metadata buffer (attachment).

- **Liveliness:**

  A node can declare a named token, and other nodes can follow the connection and disconnection of this token from the network. 

- **Matching**

  Publishers and queriers can observe whether matching subscribers or queriables exist, which avoids producing or requesting data when no endpoint can consume or answer it.

- **Advanced publisher / subscriber** 

  A configurable component for guaranteed packet delivery. It's composed over base publish/subscribe for sending data and query/reply for retransmission requests

- **Serializer / deserializer**
  
  A component for buffering primitive types (integers, floats, tuples, arrays) into compact platform-independent format to send them in the unified way.

- **Scouting**

  A Zenoh node can discover other nodes around it using features of the underlying network protocol (e.g. UDP multicast). It can also discover other nodes in the local network using a gossip mechanism. This allows it to establish a connection to the network without manual configuration.


## Location transparency

Zenoh is data-centric protocol. The data is addressed by keys, not by node addresses. Example is on the diagram: all storages provides the same data, the request is served by the closest one. If necessary, it's possbie to make request to all storages by setting `target` option of the request.

<p align="center">
  <img src="assets/zenoh-location-transparency.svg" alt="Diagram of Zenoh location transparency: a robot issues a Get for warehouse/robot1/order with target BestMatching; three storages serve warehouse/** (two with complete = true, one with complete = false), and Zenoh routes the request along the yellow path through the nearest router up to the nearest complete storage" width="560">
</p>

## Programming languages support

<p align="center">
  <img src="assets/zenoh-language-bindings.svg" alt="Diagram of Zenoh language bindings: the Rust core (zenoh) with zenoh-pico, zenoh-c, zenoh-cpp, zenoh-go, zenoh-python, zenoh-java, zenoh-kotlin, and zenoh-ts connected through a WebSocket bridge" width="860">
</p>

The primary implementation and source of truth is the Rust implementation of [Zenoh](https://github.com/eclipse-zenoh/zenoh).

There is also a pure-C implementation, [zenoh-pico](https://github.com/eclipse-zenoh/zenoh-pico), dedicated primarily to embedded applications.

For more powerful platforms, it is better to use [zenoh-c](https://github.com/eclipse-zenoh/zenoh-c), which wraps Rust Zenoh.

The C++ Zenoh library, [zenoh-cpp](https://github.com/eclipse-zenoh/zenoh-cpp), is a header-only wrapper over **both** zenoh-pico and zenoh-c.

[zenoh-go](https://github.com/eclipse-zenoh/zenoh-go/) is also implemented as a zenoh-c wrapper due to the very good interoperability between Go and C.

Other language bindings wrap Rust Zenoh directly: [zenoh-python](https://github.com/eclipse-zenoh/zenoh-python), [zenoh-kotlin](https://github.com/eclipse-zenoh/zenoh-kotlin/), and [zenoh-java](https://github.com/eclipse-zenoh/zenoh-java).

The TypeScript Zenoh library, [zenoh-ts](https://github.com/eclipse-zenoh/zenoh-ts), is different: it connects to a server plugin through WebSocket, and the Zenoh protocol itself is implemented on the server side.
