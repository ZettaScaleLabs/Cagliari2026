# Installing Zenoh

Zenoh is a Rust core ([zenoh](https://github.com/eclipse-zenoh/zenoh)) plus a
family of bindings for other languages. For each language this guide shows two
ways to get it running:

- **From the official distribution** — the package registries and prebuilt
  binaries. These steps were verified in a clean environment by running `z_pub`.
- **From latest source** — building the binding from its GitHub repository.
  These steps follow each project's README (they track the tip of `main`, so
  the exact version may be ahead of the distribution).

`z_pub` is the canonical "hello world" publisher: it opens a session and writes
to the key `demo/example/zenoh-<language>-pub`.

## Versions

- Language bindings published on package registries — **Rust** (crates.io),
  **Python** (PyPI), **Java** / **Kotlin** (Maven Central) and
  **TypeScript** (npm) — are at version **1.9.0**.
- The native libraries (**zenoh-c**, **zenoh-cpp**, **zenoh-pico**), the
  **router** (`zenohd`) and the **remote-api bridge** are distributed as
  prebuilt binaries on the [Eclipse download server](https://download.eclipse.org/zenoh/)
  and on each repository's GitHub releases page, also at **1.9.0**.
- The from-source steps build the current `main` branch of each repository.

## Before you start

- **`z_pub` and the router.** A Zenoh session runs in *peer* mode by default,
  so `z_pub` opens a session and publishes **without** needing a router. Two
  bindings are exceptions and need a running router/bridge first:
  **zenoh-pico** (runs in *client* mode) and **zenoh-ts** (talks to a WebSocket
  bridge). Those sections start the daemon before publishing. See
  [Running a Zenoh router](#running-a-zenoh-router).
- **Platform.** The distribution commands below were verified on Linux and
  download the **x86_64** archives. For other targets pick the matching archive
  on the release page — e.g. `aarch64-unknown-linux-gnu` (or `linux-arm64` for
  zenoh-pico), `apple-darwin`, `pc-windows-msvc`. On macOS the native libraries
  and the router are also available from the Homebrew tap
  [`eclipse-zenoh/homebrew-zenoh`](https://github.com/eclipse-zenoh/homebrew-zenoh).

## Contents

- [Rust](#rust)
- [Python](#python)
- [C — zenoh-c](#c--zenoh-c)
- [C++ — zenoh-cpp](#c--zenoh-cpp)
- [Embedded C — zenoh-pico](#embedded-c--zenoh-pico)
- [Go](#go)
- [Java](#java)
- [Kotlin](#kotlin)
- [TypeScript / JavaScript](#typescript--javascript)
- [Running a Zenoh router](#running-a-zenoh-router)

---

## Rust

Repository: <https://github.com/eclipse-zenoh/zenoh>

The Rust library is the reference implementation, published on
[crates.io](https://crates.io/crates/zenoh).

Create the project and put the publisher in `src/main.rs`:

```sh
cargo new zenoh-pub
cd zenoh-pub
```

```rust
#[tokio::main]
async fn main() {
    let session = zenoh::open(zenoh::Config::default()).await.unwrap();
    let publisher = session.declare_publisher("demo/example/zenoh-rust-pub").await.unwrap();
    publisher.put("Pub from Rust!").await.unwrap();
}
```

### From the official distribution

Add the crates.io dependencies and run:

```sh
cargo add zenoh
cargo add tokio --features rt-multi-thread,macros
cargo run
```

### From latest source

Replace the `zenoh` dependency in `Cargo.toml` with a git dependency on `main`
(the first build compiles Zenoh from source):

```toml
[dependencies]
zenoh = { git = "https://github.com/eclipse-zenoh/zenoh.git", branch = "main" }
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

```sh
cargo run
```

---

## Python

Repository: <https://github.com/eclipse-zenoh/zenoh-python>

The Python package is published on [PyPI](https://pypi.org/project/eclipse-zenoh/)
as `eclipse-zenoh`. Save the publisher as `z_pub.py`:

```python
import zenoh

with zenoh.open(zenoh.Config()) as session:
    pub = session.declare_publisher("demo/example/zenoh-python-pub")
    pub.put("Pub from Python!")
```

### From the official distribution

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install eclipse-zenoh
python z_pub.py
```

### From latest source

Building from source compiles the Rust core, so a [Rust toolchain](https://rustup.rs/)
is required. zenoh-python builds with [maturin](https://www.maturin.rs/):

```sh
git clone https://github.com/eclipse-zenoh/zenoh-python.git
cd zenoh-python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
maturin develop --release
```

`maturin develop` installs the freshly built module into the active virtual
environment; run `python z_pub.py` from there.

---

## C — zenoh-c

Repository: <https://github.com/eclipse-zenoh/zenoh-c>

Save the publisher as `z_pub.c`:

```c
#include "zenoh.h"

int main(void) {
    z_owned_config_t config;
    z_config_default(&config);

    z_owned_session_t s;
    z_open(&s, z_move(config), NULL);

    z_view_keyexpr_t ke;
    z_view_keyexpr_from_str(&ke, "demo/example/zenoh-c-pub");
    z_owned_publisher_t pub;
    z_declare_publisher(z_loan(s), &pub, z_loan(ke), NULL);

    z_owned_bytes_t payload;
    z_bytes_copy_from_str(&payload, "Pub from C!");
    z_publisher_put(z_loan(pub), z_move(payload), NULL);

    z_drop(z_move(pub));
    z_drop(z_move(s));
    return 0;
}
```

### From the official distribution

Download the prebuilt `standalone` archive (headers + library) and build
against it:

```sh
curl -LO https://download.eclipse.org/zenoh/zenoh-c/1.9.0/zenoh-c-1.9.0-x86_64-unknown-linux-gnu-standalone.zip
unzip zenoh-c-1.9.0-x86_64-unknown-linux-gnu-standalone.zip -d zenoh-c
cc z_pub.c -Izenoh-c/include -Lzenoh-c/lib -lzenohc -o z_pub
LD_LIBRARY_PATH=zenoh-c/lib ./z_pub
```

> The release page also offers Debian packages (`libzenohc-*-debian.zip`) if you
> prefer installing the library system-wide with `dpkg -i`.

### From latest source

Build the library from `main` with CMake (needs [Rust](https://rustup.rs/),
`git`, `cmake` and a C compiler), then compile against the install tree:

```sh
git clone https://github.com/eclipse-zenoh/zenoh-c.git
cmake -S zenoh-c -B zenoh-c/build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PWD/zenoh-c/install"
cmake --build zenoh-c/build --target install --config Release
cc z_pub.c -Izenoh-c/install/include -Lzenoh-c/install/lib -lzenohc -o z_pub
LD_LIBRARY_PATH=zenoh-c/install/lib ./z_pub
```

---

## C++ — zenoh-cpp

Repository: <https://github.com/eclipse-zenoh/zenoh-cpp>

zenoh-cpp is a header-only wrapper built on top of **zenoh-c**, so set up
zenoh-c first (the [C section](#c--zenoh-c)) using the matching method below.
Save the publisher as `z_pub.cpp`:

```cpp
#include "zenoh.hxx"
using namespace zenoh;

int main() {
    auto session = Session::open(Config::create_default());
    auto pub = session.declare_publisher(KeyExpr("demo/example/zenoh-cpp-pub"));
    pub.put("Pub from C++!");
}
```

`-DZENOHCXX_ZENOHC=1` selects the zenoh-c backend in both methods below.

### From the official distribution

Download the zenoh-cpp headers and build against the zenoh-c distribution from
the [C section](#c--zenoh-c):

```sh
curl -LO https://download.eclipse.org/zenoh/zenoh-cpp/1.9.0/zenohcpp-1.9.0-standalone.zip
unzip zenohcpp-1.9.0-standalone.zip -d zenoh-cpp
c++ -std=c++17 -DZENOHCXX_ZENOHC=1 z_pub.cpp \
    -Izenoh-cpp/include -Izenoh-c/include \
    -Lzenoh-c/lib -lzenohc -o z_pub
LD_LIBRARY_PATH=zenoh-c/lib ./z_pub
```

### From latest source

Clone the headers from `main` and build against the zenoh-c you built from
source in the [C section](#c--zenoh-c):

```sh
git clone https://github.com/eclipse-zenoh/zenoh-cpp.git
c++ -std=c++17 -DZENOHCXX_ZENOHC=1 z_pub.cpp \
    -Izenoh-cpp/include -Izenoh-c/install/include \
    -Lzenoh-c/install/lib -lzenohc -o z_pub
LD_LIBRARY_PATH=zenoh-c/install/lib ./z_pub
```

---

## Embedded C — zenoh-pico

Repository: <https://github.com/eclipse-zenoh/zenoh-pico>

zenoh-pico is the lightweight implementation for constrained/embedded targets.
Unlike the other bindings it runs in **client** mode, so it needs a running
router. Start one as described in
[Running a Zenoh router](#running-a-zenoh-router) (or, quickly,
`docker run --init -p 7447:7447 eclipse/zenoh`) before publishing.

Save the publisher as `z_pub.c`. It connects to the local router on
`tcp/127.0.0.1:7447`:

```c
#include <zenoh-pico.h>

int main(void) {
    z_owned_config_t config;
    z_config_default(&config);
    zp_config_insert(z_loan_mut(config), Z_CONFIG_CONNECT_KEY, "tcp/127.0.0.1:7447");

    z_owned_session_t s;
    z_open(&s, z_move(config), NULL);
    zp_start_read_task(z_loan_mut(s), NULL);
    zp_start_lease_task(z_loan_mut(s), NULL);

    z_view_keyexpr_t ke;
    z_view_keyexpr_from_str(&ke, "demo/example/zenoh-pico-pub");
    z_owned_publisher_t pub;
    z_declare_publisher(z_loan(s), &pub, z_loan(ke), NULL);

    z_owned_bytes_t payload;
    z_bytes_copy_from_str(&payload, "Pub from Pico!");
    z_publisher_put(z_loan(pub), z_move(payload), NULL);

    z_drop(z_move(pub));
    z_drop(z_move(s));
    return 0;
}
```

`-DZENOH_LINUX=1` selects the platform layer in both methods below.

### From the official distribution

```sh
curl -LO https://download.eclipse.org/zenoh/zenoh-pico/1.9.0/zenoh-pico-1.9.0-linux-x64-standalone.zip
unzip zenoh-pico-1.9.0-linux-x64-standalone.zip -d zenoh-pico
cc z_pub.c -DZENOH_LINUX=1 -Izenoh-pico/include -Lzenoh-pico/lib -lzenohpico -pthread -o z_pub
LD_LIBRARY_PATH=zenoh-pico/lib ./z_pub
```

### From latest source

Build from `main` with CMake (needs `git`, `cmake` and a C compiler):

```sh
git clone https://github.com/eclipse-zenoh/zenoh-pico.git
cmake -S zenoh-pico -B zenoh-pico/build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PWD/zenoh-pico/install"
cmake --build zenoh-pico/build --target install
cc z_pub.c -DZENOH_LINUX=1 -Izenoh-pico/install/include -Lzenoh-pico/install/lib -lzenohpico -pthread -o z_pub
LD_LIBRARY_PATH=zenoh-pico/install/lib ./z_pub
```

---

## Go

Repository: <https://github.com/eclipse-zenoh/zenoh-go>

zenoh-go is a cgo wrapper around zenoh-c. As stated in its README, it requires
zenoh-c built **with unstable features** (`-DZENOHC_BUILD_WITH_UNSTABLE_API=ON`),
which the prebuilt archives do not enable — so build zenoh-c from source once
and point cgo at it (needs [Rust](https://rustup.rs/), `git`, `cmake` and a C
compiler):

```sh
git clone --branch 1.9.0 --depth 1 https://github.com/eclipse-zenoh/zenoh-c.git
cmake -S zenoh-c -B zenoh-c/build \
    -DZENOHC_BUILD_WITH_UNSTABLE_API=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$PWD/zenoh-c/install"
cmake --build zenoh-c/build --target install --config Release
export CGO_CFLAGS="-I$PWD/zenoh-c/install/include"
export CGO_LDFLAGS="-L$PWD/zenoh-c/install/lib"
export LD_LIBRARY_PATH="$PWD/zenoh-c/install/lib"
```

> For the latest zenoh-c, drop `--branch 1.9.0 --depth 1` to clone `main`.

Create the module and save the publisher as `z_pub.go`:

```sh
mkdir zenoh-go-pub && cd zenoh-go-pub
go mod init example.com/zenoh-go-pub
```

```go
package main

import "github.com/eclipse-zenoh/zenoh-go/zenoh"

func main() {
    session, _ := zenoh.Open(zenoh.NewConfigDefault(), nil)
    defer session.Drop()
    ke, _ := zenoh.NewKeyExpr("demo/example/zenoh-go-pub")
    pub, _ := session.DeclarePublisher(ke, nil)
    defer pub.Drop()
    pub.Put(zenoh.NewZBytesFromString("Pub from Go!"), nil)
}
```

### From the official distribution

Pin the published module version (keep the environment variables from above):

```sh
go get github.com/eclipse-zenoh/zenoh-go@v1.9.0
go run .
```

### From latest source

Track the `main` branch of the Go module instead (use the matching zenoh-c
branch):

```sh
go get github.com/eclipse-zenoh/zenoh-go@main
go run .
```

---

## Java

Repository: <https://github.com/eclipse-zenoh/zenoh-java>

The Java library is published on Maven Central as
[`org.eclipse.zenoh:zenoh-java`](https://central.sonatype.com/artifact/org.eclipse.zenoh/zenoh-java);
the artifact bundles the native library for common platforms. The example below
uses Gradle (8+) with JDK 21.

Create the project layout:

```sh
mkdir -p zenoh-java-pub/src/main/java
cd zenoh-java-pub
```

`settings.gradle.kts`:

```kotlin
rootProject.name = "zpub"
```

`src/main/java/ZPub.java`:

```java
import io.zenoh.Config;
import io.zenoh.Session;
import io.zenoh.Zenoh;
import io.zenoh.keyexpr.KeyExpr;
import io.zenoh.pubsub.Publisher;

public class ZPub {
    public static void main(String[] args) throws Exception {
        try (Session session = Zenoh.open(Config.loadDefault())) {
            Publisher publisher = session.declarePublisher(KeyExpr.tryFrom("demo/example/zenoh-java-pub"));
            publisher.put("Pub from Java!");
        }
    }
}
```

### From the official distribution

`build.gradle.kts`:

```kotlin
plugins {
    id("application")
}
repositories { mavenCentral() }
dependencies {
    implementation("org.eclipse.zenoh:zenoh-java:1.9.0")
}
application {
    mainClass.set("ZPub")
}
java {
    toolchain { languageVersion.set(JavaLanguageVersion.of(21)) }
}
```

```sh
gradle run
```

### From latest source

Build the binding from `main` and publish it to your local Maven repository
(needs [Rust](https://rustup.rs/) and a JDK; the repo ships a Gradle wrapper):

```sh
git clone https://github.com/eclipse-zenoh/zenoh-java.git
cd zenoh-java
./gradlew publishJvmPublicationToMavenLocal
```

This compiles the native Zenoh JNI library and publishes the JVM artifact under
`~/.m2/repository/org/eclipse/zenoh/zenoh-java-jvm/`. Check that directory for
the exact version, then point the project at `mavenLocal()`:

```kotlin
repositories {
    mavenCentral()
    mavenLocal()
}
dependencies {
    implementation("org.eclipse.zenoh:zenoh-java-jvm:<version-from-~/.m2>")
}
```

Then run `gradle run` as above.

---

## Kotlin

Repository: <https://github.com/eclipse-zenoh/zenoh-kotlin>

The Kotlin library is published on Maven Central as
[`org.eclipse.zenoh:zenoh-kotlin`](https://central.sonatype.com/artifact/org.eclipse.zenoh/zenoh-kotlin).
The example below uses Gradle (8+) with JDK 21.

Create the project layout:

```sh
mkdir -p zenoh-kotlin-pub/src/main/kotlin
cd zenoh-kotlin-pub
```

`settings.gradle.kts`:

```kotlin
rootProject.name = "zpub"
```

`src/main/kotlin/ZPub.kt`:

```kotlin
import io.zenoh.Config
import io.zenoh.Zenoh
import io.zenoh.bytes.ZBytes
import io.zenoh.keyexpr.intoKeyExpr

fun main() {
    val session = Zenoh.open(Config.default()).getOrThrow()
    val publisher = session.declarePublisher("demo/example/zenoh-kotlin-pub".intoKeyExpr().getOrThrow()).getOrThrow()
    publisher.put(ZBytes.from("Pub from Kotlin!"))
    session.close()
}
```

### From the official distribution

`build.gradle.kts`:

```kotlin
plugins {
    kotlin("jvm") version "2.0.21"
    application
}
repositories { mavenCentral() }
dependencies {
    implementation("org.eclipse.zenoh:zenoh-kotlin:1.9.0")
}
application {
    mainClass.set("ZPubKt")
}
kotlin { jvmToolchain(21) }
```

```sh
gradle run
```

### From latest source

Build the binding from `main` and publish it to your local Maven repository
(needs [Rust](https://rustup.rs/) and a JDK; the repo ships a Gradle wrapper):

```sh
git clone https://github.com/eclipse-zenoh/zenoh-kotlin.git
cd zenoh-kotlin
./gradlew publishJvmPublicationToMavenLocal
```

This publishes the JVM artifact under
`~/.m2/repository/org/eclipse/zenoh/zenoh-kotlin-jvm/`. Check that directory for
the exact version, then point the project at `mavenLocal()`:

```kotlin
repositories {
    mavenCentral()
    mavenLocal()
}
dependencies {
    implementation("org.eclipse.zenoh:zenoh-kotlin-jvm:<version-from-~/.m2>")
}
```

Then run `gradle run` as above.

---

## TypeScript / JavaScript

Repository: <https://github.com/eclipse-zenoh/zenoh-ts>

The library is published on npm as
[`@eclipse-zenoh/zenoh-ts`](https://www.npmjs.com/package/@eclipse-zenoh/zenoh-ts).
It reaches the Zenoh network over a WebSocket connection to the
`zenoh-plugin-remote-api`, so you run the **remote-api bridge** alongside it.
The command-line examples use [Deno](https://deno.com/) (the library targets
browsers and Deno, not Node.js).

Save the publisher as `z_pub.ts`:

```typescript
import { Config, KeyExpr, Session } from "@eclipse-zenoh/zenoh-ts";

const session = await Session.open(new Config("ws/127.0.0.1:10000"));
const publisher = await session.declarePublisher(KeyExpr.autocanonize("demo/example/zenoh-ts-pub"));
await publisher.put("Pub from TypeScript!");
await session.close();
```

### From the official distribution

Download and start the bridge (listens on `ws://localhost:10000` by default):

```sh
curl -LO https://download.eclipse.org/zenoh/zenoh-plugin-remote-api/1.9.0/zenoh-ts-1.9.0-x86_64-unknown-linux-gnu-standalone.zip
unzip zenoh-ts-1.9.0-x86_64-unknown-linux-gnu-standalone.zip -d zenoh-bridge
chmod +x zenoh-bridge/zenoh-bridge-remote-api
./zenoh-bridge/zenoh-bridge-remote-api &
```

Map the npm package for Deno in `deno.json`, then run:

```json
{
  "imports": {
    "@eclipse-zenoh/zenoh-ts": "npm:@eclipse-zenoh/zenoh-ts@1.9.0"
  }
}
```

```sh
deno run -A z_pub.ts
```

### From latest source

The repository contains both the bridge and the library. Run the bridge from
source with Cargo (needs [Rust](https://rustup.rs/)), then build the library
with [yarn](https://classic.yarnpkg.com/):

```sh
git clone https://github.com/eclipse-zenoh/zenoh-ts.git
cd zenoh-ts
cargo run            # starts zenoh-bridge-remote-api on ws://localhost:10000
```

In another shell, build the TypeScript library (output goes to
`zenoh-ts/dist`):

```sh
cd zenoh-ts/zenoh-ts
yarn install
yarn build
```

Point `deno.json` at the local build instead of the npm package (adjust to the
entry in `dist` if needed), then `deno run -A z_pub.ts`:

```json
{
  "imports": {
    "@eclipse-zenoh/zenoh-ts": "./zenoh-ts/dist/index.js"
  }
}
```

---

## Running a Zenoh router

Most bindings publish in peer mode and need no router, but **zenoh-pico** and
**zenoh-ts** do (see their sections). The router `zenohd` is part of the
[zenoh](https://github.com/eclipse-zenoh/zenoh) project. Any of these work:

- **Prebuilt binary** from the official distribution:

  ```sh
  curl -LO https://download.eclipse.org/zenoh/zenoh/1.9.0/zenoh-1.9.0-x86_64-unknown-linux-gnu-standalone.zip
  unzip zenoh-1.9.0-x86_64-unknown-linux-gnu-standalone.zip -d zenohd
  ./zenohd/zenohd
  ```

- **Cargo.** Install the published router from crates.io (needs
  [Rust](https://rustup.rs/)):

  ```sh
  cargo install zenohd
  zenohd
  ```

  To run the latest source instead, build it from a clone:

  ```sh
  git clone https://github.com/eclipse-zenoh/zenoh.git
  cd zenoh
  cargo run --release --bin zenohd
  ```

- **Docker**:

  ```sh
  docker run --init -p 7447:7447 -p 8000:8000 eclipse/zenoh
  ```

- **Homebrew** (macOS): `brew tap eclipse-zenoh/homebrew-zenoh && brew install zenohd`.

By default `zenohd` listens for Zenoh connections on `tcp/[::]:7447`, which is
where the zenoh-pico example connects.
