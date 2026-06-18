# Eclipse Zenoh [illustration prompt](readme-prompts/01-eclipse-zenoh.txt)

The primary characteristics of Zenoh are: [illustration prompt](readme-prompts/06-primary-characteristics-intro.txt)

Zenoh supports two mechanisms of data exchange: [illustration prompt](readme-prompts/11-data-exchange-intro.txt)

- **Wildcard support:** Data can be requested using wildcards, e.g. `*/sensor/temp` for all temperature sensors or `room/**` for all data available for `room`. [illustration prompt](readme-prompts/15-wildcard-support.txt)
- **Rich sample metadata:** Despite its maximal wire efficiency, the Zenoh protocol provides multiple optional metadata fields in packets. This includes timestamps, encoding, priority settings, and an area for custom metadata (attachments). [illustration prompt](readme-prompts/16-rich-sample-metadata.txt)
- **Scouting:** A Zenoh node can discover other nodes around it using features of the underlying network protocol (e.g. UDP multicast). It can also discover other nodes in the local network using a gossip mechanism. This allows it to establish a connection to the network without manual configuration. [illustration prompt](readme-prompts/17-scouting.txt)
- **Liveliness:** A node can declare a named token, and other nodes can follow the connection and disconnection of this token from the network. [illustration prompt](readme-prompts/18-liveliness.txt)
- **Matching:** Publishers and queriers can observe whether matching subscribers or queriables exist, which avoids producing or requesting data when no endpoint can consume or answer it. [illustration prompt](readme-prompts/19-matching.txt)

- **Advanced publisher/subscriber:** A configurable component for guaranteed packet delivery. [illustration prompt](readme-prompts/21-advanced-pub-sub.txt)
- **Serializer/deserializer:** A component for storing primitive types (integers, floats, tuples, arrays) in a compact and platform-independent format. [illustration prompt](readme-prompts/22-serializer-deserializer.txt)

## Zenoh language bindings [illustration prompt](readme-prompts/23-language-bindings.txt)
