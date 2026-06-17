# Zenoh

Zenoh is a distributed data exchange middleware for connecting application processes through a shared namespace of keys. A key is a slash-separated resource path such as `robot/sensor/temp`; a key expression is a selector over keys, with wildcards such as `robot/sensor/*` for one path segment or `robot/**` for a subtree.

Zenoh supports publish/subscribe for continuous updates and query/reply for request-driven access to values or computations.

- **Transport/link-protocol agnostic:** Zenoh operations are not bound to one network transport; endpoints can use link protocols such as TCP, TLS, QUIC, UDP, WebSocket, serial, Unix sockets, pipes, or vsock.
- **Various topologies:** A Zenoh node is a running Zenoh process; nodes can be arranged as peer-to-peer meshes, brokered client-router deployments, routed router meshes, or hierarchical regions.
- **Scouting:** Zenoh's discovery step finds peer or router endpoints before a transport connection is opened, using mechanisms such as local multicast, configured entry points, or gossip between already discovered nodes.
- **Liveliness:** A node can declare a named token on a key expression, and other nodes can query or subscribe to token appearance and disappearance to track presence.
- **Matching:** Senders and requesters can observe whether a matching receiver or responder exists, which avoids producing or requesting data when no endpoint can consume or answer it.
