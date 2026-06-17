# Zenoh

Zenoh organizes communication around key expressions: hierarchical resource names that can be matched with wildcards. Applications can publish samples to a key, subscribe to matching keys, issue queries for matching keys, and reply with values. This gives streams and request/reply traffic a shared addressing model instead of separate APIs and discovery schemes.

The runtime can be deployed as clients that attach to the network, peers that exchange data directly, or routers that forward traffic between connected nodes and network segments. Routing is based on declared interests in key expressions, so data is forwarded only where matching publishers, subscribers, queryables, or storage backends exist. Zenoh supports multiple transports and discovery modes, and can bridge DDS systems when interoperability with ROS 2 or other DDS-based software is needed.
