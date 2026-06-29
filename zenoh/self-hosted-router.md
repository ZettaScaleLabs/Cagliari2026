# Running a self-hosted Zenoh router

This guide shows how to run `zenohd` router with
**mutual TLS** and connect nodes to it. It also demonstrates a useful property of
Zenoh: nodes that meet through the router then talk **directly** to each other —
the router is used only for *discovery*, never for relaying their data.

Everything below is plain configuration plus the **bundled Rust examples**
(`z_pub`, `z_sub`, `z_info`) — no code is written. The steps were verified
end-to-end against a real `zenohd 1.9.0`.

## Contents

- [How it works](#how-it-works)
- [Prerequisites](#prerequisites)
- [1. Generate the certificates](#1-generate-the-certificates)
- [2. Run zenohd on your server](#2-run-zenohd-on-your-server)
- [3. Configure a node](#3-configure-a-node)
- [4. Test it with the Rust examples](#4-test-it-with-the-rust-examples)
- [Troubleshooting](#troubleshooting)

---

## How it works

**Mutual TLS.** One self-signed Certificate Authority (CA) signs two
certificates: a **server** certificate for the router and a **node** certificate
shared by the clients. Each side verifies the other against the shared CA — that
is what makes the TLS *mutual*. Keys are ECDSA P-384, stored as PKCS#8 PEM.

```text
              Self-signed CA  (ca.key.pem + ca.cert.pem)
              (the CA private key stays on your machine)
                           |
         +-----------------+--------------+
         |                                |
   server.cert.pem                   client.cert.pem
   SAN = your-server.example.com     used by every node
   (used by zenohd)
```

**Gossip discovery.** A node in `peer` mode that connects to the router learns,
through the router's *gossip*, the locators of the other peers connected to it.
It then **autoconnects** straight to them and routes over that direct link
instead of through the router. We deliberately turn **multicast scouting off**, so
gossip through the router is the *only* way two nodes can discover each other — if
they still exchange data, gossip did the job. Because each node also *listens* on
a `tls/` endpoint, the direct link it forms is itself mTLS-encrypted.

## Prerequisites

- `openssl` on your machine (to generate the certificates).
- A server reachable by DNS (`your-server.example.com` below) with **TCP and UDP
  port 7447** open to the nodes.
- `zenohd` on the server. Download a prebuilt binary from the
  [releases](https://github.com/eclipse-zenoh/zenoh/releases) (a `1.9.x` tag
  matches the examples) and unzip it, or `cargo install zenohd`. No root or
  container is required.
- A [Rust toolchain](https://rustup.rs/) and a clone of
  [`eclipse-zenoh/zenoh`](https://github.com/eclipse-zenoh/zenoh) on the machine(s)
  running the nodes — that is where the `z_pub` / `z_sub` / `z_info` examples live.

Set your server's hostname once so the snippets below can be pasted as-is:

```sh
ROUTER_HOST=your-server.example.com
```

## 1. Generate the certificates

Run this **locally** in a fresh `tls/` directory. `openssl genpkey` emits PKCS#8
keys (`-----BEGIN PRIVATE KEY-----`), which is the format Zenoh expects.

```sh
mkdir -p tls && cd tls

# CA — signs everything; its private key never leaves this machine
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -out ca.key.pem
openssl req -x509 -new -key ca.key.pem -sha384 -days 3650 \
  -subj "/CN=Zenoh Self-Signed CA" -out ca.cert.pem

# Server certificate — SAN must equal the hostname nodes dial
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -out server.key.pem
openssl req -new -key server.key.pem -sha384 -subj "/CN=$ROUTER_HOST" -out server.csr.pem
cat > server.ext <<EOF
subjectAltName   = DNS:$ROUTER_HOST
keyUsage         = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
EOF
openssl x509 -req -in server.csr.pem -CA ca.cert.pem -CAkey ca.key.pem -CAcreateserial \
  -sha384 -days 825 -extfile server.ext -out server.cert.pem

# Node certificate — shared by every node; serverAuth + clientAuth so the same
# cert works for both the connect side and the listen side of a peer link
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -out client.key.pem
openssl req -new -key client.key.pem -sha384 -subj "/CN=zenoh-node" -out client.csr.pem
cat > client.ext <<'EOF'
subjectAltName   = DNS:zenoh-node
keyUsage         = critical, digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth, serverAuth
EOF
openssl x509 -req -in client.csr.pem -CA ca.cert.pem -CAkey ca.key.pem -CAcreateserial \
  -sha384 -days 825 -extfile client.ext -out client.cert.pem

openssl verify -CAfile ca.cert.pem server.cert.pem client.cert.pem   # expect: OK, OK
```

> Keep `ca.key.pem` private — anyone holding it can mint certificates your router
> will trust. The server SAN must match the name nodes dial; if you connect by IP
> instead, add `IP:<addr>` to the `subjectAltName` line and re-issue.

## 2. Run zenohd on your server

Copy the CA certificate and the **server** certificate and key to the server (the
CA key and the node key stay off it):

```sh
ssh "$ROUTER_HOST" 'mkdir -p ~/zenoh-tls'
scp tls/ca.cert.pem tls/server.cert.pem tls/server.key.pem "$ROUTER_HOST:~/zenoh-tls/"
```

Create `~/zenohd-config.json5` on the server (replace `<user>` with the output of
`echo $HOME` there):

```json5
{
  mode: "router",
  listen: { endpoints: ["tls/0.0.0.0:7447", "quic/0.0.0.0:7447"] },
  transport: {
    link: {
      tls: {
        root_ca_certificate: "/home/<user>/zenoh-tls/ca.cert.pem",
        listen_certificate:  "/home/<user>/zenoh-tls/server.cert.pem",
        listen_private_key:  "/home/<user>/zenoh-tls/server.key.pem",
        enable_mtls: true
      }
    }
  }
}
```

Start it in the foreground (Ctrl-C to stop):

```sh
RUST_LOG=info zenohd -c ~/zenohd-config.json5
```

The log should report it is reachable on both transports:

```text
Zenoh can be reached at: tls/<server-ip>:7447
Zenoh can be reached at: quic/<server-ip>:7447
```

To keep it running after you log out, start it detached instead:

```sh
RUST_LOG=info nohup zenohd -c ~/zenohd-config.json5 > ~/zenohd.log 2>&1 &
```

Notes:

- The single `tls` block serves **both** the `tls/` and `quic/` listeners.
- `enable_mtls: true` together with `root_ca_certificate` make the router reject
  any client whose certificate is not signed by your CA.
- `0.0.0.0` listens on all IPv4 interfaces; use `[::]` for IPv6 / dual-stack.

## 3. Configure a node

Each node needs the CA certificate and the **node** certificate/key. Put them in a
`tls/` directory and create `peer.json5` next to it (replace
`your-server.example.com`):

```json5
{
  mode: "peer",
  connect: { endpoints: ["tls/your-server.example.com:7447", "quic/your-server.example.com:7447"] },
  listen:  { endpoints: ["tls/0.0.0.0:0"] },
  scouting: {
    multicast: { enabled: false },
    gossip:    { enabled: true, autoconnect: { peer: ["router", "peer"] } }
  },
  transport: {
    link: {
      protocols: ["tls", "quic"],
      tls: {
        root_ca_certificate: "tls/ca.cert.pem",
        connect_certificate: "tls/client.cert.pem",
        connect_private_key: "tls/client.key.pem",
        listen_certificate:  "tls/client.cert.pem",
        listen_private_key:  "tls/client.key.pem",
        enable_mtls: true,
        verify_name_on_connect: false
      }
    }
  }
}
```

The settings that matter (Zenoh 1.9.0):

| Setting | Why |
| --- | --- |
| `mode: "peer"` | Only peers form direct links; a `client` relays everything through the router. |
| `scouting.multicast.enabled: false` | Forces discovery through the router's gossip, so a working link proves gossip did it. |
| `scouting.gossip` (on, `autoconnect.peer`) | Lets a peer auto-dial the peers the router gossips about. |
| `listen: ["tls/0.0.0.0:0"]` | Each node listens on an ephemeral **TLS** port, so the locator it gossips is a `tls/` locator → the direct link is encrypted. |
| `protocols: ["tls", "quic"]` | Allows only encrypted links — no plain TCP is ever attempted. |
| `verify_name_on_connect: false` | Required: a peer dials the *other peer's IP*, which won't match the cert SAN. Full mTLS chain validation still applies; only the hostname↔cert check is dropped. The setting is global, so it also relaxes that one check on the router link. |

> The same `client.cert.pem` / `client.key.pem` is used for both the `connect_*`
> and `listen_*` sides because the node certificate carries both `clientAuth` and
> `serverAuth`.

## 4. Test it with the Rust examples

Clone Zenoh and put `peer.json5` together with its `tls/` directory inside
`zenoh/examples`, so the relative paths resolve when you run from there:

```sh
git clone https://github.com/eclipse-zenoh/zenoh.git
cd zenoh/examples
# copy peer.json5 and tls/ into this directory
```

Start two nodes — a subscriber and a publisher (the first build compiles Zenoh):

```sh
cargo run --example z_sub -- -c peer.json5   # terminal 1 (node A)
cargo run --example z_pub -- -c peer.json5   # terminal 2 (node B)
```

The subscriber receives the publisher's samples:

```text
>> [Subscriber] Received PUT ('demo/example/zenoh-rs-pub': '[   0] Pub from Rust!')
>> [Subscriber] Received PUT ('demo/example/zenoh-rs-pub': '[   1] Pub from Rust!')
...
```

Multicast is off and neither node was given the other's address, so the **only**
way node A could have found node B is the router gossiping B's locator to it.

To *see* the direct link, run `z_info` as a third node while the subscriber is
still up. Build it with `--features unstable` so it keeps printing live
transport/link details:

```sh
cargo run --example z_info --features unstable -- -c peer.json5   # terminal 3
```

```text
routers zid: [405c097f9d81187c7a98eba42e4eb659]
peers zid:   [baeb0eb1f35b7047a0f73baef1b7867b]

links:
Link { zid: baeb…, src: tls/192.168.1.104:49567, dst: tls/192.168.1.104:49561, …
       auth_identifier: Some("zenoh-node") … }                          # ← direct peer link (mTLS)
Link { zid: 405c…, src: quic/0.0.0.0:62427, dst: quic/your-server.example.com:7447, …
       auth_identifier: Some("your-server.example.com") … }             # ← link to the router
```

`peers zid` is **non-empty** — the node found another peer through gossip — and
the link to it is a direct `tls/` connection authenticated by the node
certificate (`auth_identifier: Some("zenoh-node")`). The link to the router is a
separate `quic/` connection, used only for discovery. (If the peer list is briefly
empty at start-up, watch the live `[Link Event] Added` lines: the `tls/` peer link
appears once autoconnect completes.)

For contrast, add `-m client` to the same command: `peers zid` stays `[]`, because
a client never forms peer-to-peer links — all of its traffic goes through the
router.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| TLS/mTLS handshake fails | CA mismatch between the two sides, or `enable_mtls` set on only one of them. |
| `certificate not valid for name` on the router link | Server cert SAN ≠ `$ROUTER_HOST`; re-issue with the correct SAN. |
| Connection refused / timeout | Port 7447 not open for **both** TCP and UDP, DNS not resolving, or `zenohd` not running. |
| Private key parse error | Key is not PKCS#8 — it must begin with `-----BEGIN PRIVATE KEY-----`. |
| `peers zid` stays empty | Check `mode: "peer"`, `multicast.enabled: false`, and `gossip.enabled: true` with `autoconnect.peer` including `"peer"`; confirm the router is reachable (it provides the gossip). |
