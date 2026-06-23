# Installing Zenoh

Zenoh is a Rust core ([zenoh](https://github.com/eclipse-zenoh/zenoh)) plus a
family of bindings for other languages. This guide installs each binding from
its **official distribution** and verifies the result by running `z_pub`, the
canonical "hello world" publisher that opens a session and writes to the key
`demo/example/zenoh-<language>-pub`.

For deeper documentation, each section links to the binding's GitHub repository.

## Versions

- Language bindings published on package registries — **Rust** (crates.io),
  **Python** (PyPI), **Java** / **Kotlin** (Maven Central) and
  **TypeScript** (npm) — are at version **1.9.0**.
- The native libraries (**zenoh-c**, **zenoh-cpp**, **zenoh-pico**), the
  **router** (`zenohd`) and the **remote-api bridge** are distributed as
  prebuilt binaries on the [Eclipse download server](https://download.eclipse.org/zenoh/)
  and on each repository's GitHub releases page, also at **1.9.0**.

## Before you start

- **`z_pub` and the router.** A Zenoh session runs in *peer* mode by default,
  so `z_pub` opens a session and publishes **without** needing a router. Two
  bindings are exceptions and need a running router/bridge first:
  **zenoh-pico** (runs in *client* mode) and **zenoh-ts** (talks to a WebSocket
  bridge). Those sections start the daemon before publishing. See
  [Running a Zenoh router](#running-a-zenoh-router).
- **Platform.** The commands below were verified on Linux and download the
  **x86_64** archives. For other targets pick the matching archive on the
  release page — e.g. `aarch64-unknown-linux-gnu` (or `linux-arm64` for
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

The Rust library is published on [crates.io](https://crates.io/crates/zenoh) and
is the reference implementation.

1. Install the Rust toolchain with [rustup](https://rustup.rs/).

2. Create a project and add the dependencies:

   ```sh
   cargo new zenoh-pub
   cd zenoh-pub
   cargo add zenoh
   cargo add tokio --features rt-multi-thread,macros,time
   ```

3. Put the publisher in `src/main.rs`:

   ```rust
   use std::time::Duration;

   #[tokio::main]
   async fn main() {
       let key = "demo/example/zenoh-rust-pub";
       println!("Opening session...");
       let session = zenoh::open(zenoh::Config::default()).await.unwrap();
       println!("Declaring Publisher on '{key}'...");
       let publisher = session.declare_publisher(key).await.unwrap();
       for idx in 0..3u32 {
           let buf = format!("[{idx:4}] Pub from Rust!");
           println!("Putting Data ('{key}': '{buf}')...");
           publisher.put(buf).await.unwrap();
           tokio::time::sleep(Duration::from_secs(1)).await;
       }
       println!("Done.");
   }
   ```

4. Run it:

   ```sh
   cargo run
   ```

   ```text
   Opening session...
   Declaring Publisher on 'demo/example/zenoh-rust-pub'...
   Putting Data ('demo/example/zenoh-rust-pub': '[   0] Pub from Rust!')...
   ...
   ```

---

## Python

Repository: <https://github.com/eclipse-zenoh/zenoh-python>

The Python package is published on [PyPI](https://pypi.org/project/eclipse-zenoh/)
as `eclipse-zenoh`.

1. Install it (a virtual environment is recommended):

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install eclipse-zenoh
   ```

2. Save the publisher as `z_pub.py`:

   ```python
   import time
   import zenoh

   KEY = "demo/example/zenoh-python-pub"
   print("Opening session...")
   with zenoh.open(zenoh.Config()) as session:
       print(f"Declaring Publisher on '{KEY}'...")
       pub = session.declare_publisher(KEY)
       for idx in range(3):
           buf = f"[{idx:4d}] Pub from Python!"
           print(f"Putting Data ('{KEY}': '{buf}')...")
           pub.put(buf)
           time.sleep(1)
   print("Done.")
   ```

3. Run it:

   ```sh
   python z_pub.py
   ```

---

## C — zenoh-c

Repository: <https://github.com/eclipse-zenoh/zenoh-c>

Download the prebuilt `standalone` archive (headers + library) from the official
distribution and build against it.

1. Download and unpack the library:

   ```sh
   curl -LO https://download.eclipse.org/zenoh/zenoh-c/1.9.0/zenoh-c-1.9.0-x86_64-unknown-linux-gnu-standalone.zip
   unzip zenoh-c-1.9.0-x86_64-unknown-linux-gnu-standalone.zip -d zenoh-c
   ```

   The `zenoh-c` directory now contains `include/` and `lib/`.

2. Save the publisher as `z_pub.c`:

   ```c
   #include <stdio.h>
   #include "zenoh.h"

   int main(void) {
       const char *keyexpr = "demo/example/zenoh-c-pub";
       z_owned_config_t config;
       z_config_default(&config);

       printf("Opening session...\n");
       z_owned_session_t s;
       if (z_open(&s, z_move(config), NULL) < 0) {
           printf("Unable to open session!\n");
           return -1;
       }

       printf("Declaring Publisher on '%s'...\n", keyexpr);
       z_view_keyexpr_t ke;
       z_view_keyexpr_from_str(&ke, keyexpr);
       z_owned_publisher_t pub;
       if (z_declare_publisher(z_loan(s), &pub, z_loan(ke), NULL) < 0) {
           printf("Unable to declare Publisher!\n");
           return -1;
       }

       char buf[256];
       for (int idx = 0; idx < 3; idx++) {
           sprintf(buf, "[%4d] Pub from C!", idx);
           printf("Putting Data ('%s': '%s')...\n", keyexpr, buf);
           z_owned_bytes_t payload;
           z_bytes_copy_from_str(&payload, buf);
           z_publisher_put(z_loan(pub), z_move(payload), NULL);
           z_sleep_s(1);
       }
       z_drop(z_move(pub));
       z_drop(z_move(s));
       printf("Done.\n");
       return 0;
   }
   ```

3. Compile and run:

   ```sh
   cc z_pub.c -Izenoh-c/include -Lzenoh-c/lib -lzenohc -o z_pub
   LD_LIBRARY_PATH=zenoh-c/lib ./z_pub
   ```

> The same release page also offers Debian packages (`libzenohc-*-debian.zip`)
> if you prefer installing the library system-wide with `dpkg -i`.

---

## C++ — zenoh-cpp

Repository: <https://github.com/eclipse-zenoh/zenoh-cpp>

zenoh-cpp is a header-only wrapper. This guide builds it on top of **zenoh-c**,
so install zenoh-c first (the [C section](#c--zenoh-c), step 1), then add the
zenoh-cpp headers.

1. Download and unpack the zenoh-cpp headers:

   ```sh
   curl -LO https://download.eclipse.org/zenoh/zenoh-cpp/1.9.0/zenohcpp-1.9.0-standalone.zip
   unzip zenohcpp-1.9.0-standalone.zip -d zenoh-cpp
   ```

2. Save the publisher as `z_pub.cpp`:

   ```cpp
   #include <chrono>
   #include <iostream>
   #include <sstream>
   #include <thread>

   #include "zenoh.hxx"

   using namespace zenoh;
   using namespace std::chrono_literals;

   int main() {
       init_log_from_env_or("error");
       const char *keyexpr = "demo/example/zenoh-cpp-pub";

       auto config = Config::create_default();
       std::cout << "Opening session..." << std::endl;
       auto session = Session::open(std::move(config));

       std::cout << "Declaring Publisher on '" << keyexpr << "'..." << std::endl;
       auto pub = session.declare_publisher(KeyExpr(keyexpr));

       for (int idx = 0; idx < 3; ++idx) {
           std::this_thread::sleep_for(1s);
           std::ostringstream ss;
           ss << "[" << idx << "] Pub from C++!";
           auto s = ss.str();
           std::cout << "Putting Data ('" << keyexpr << "': '" << s << "')...\n";
           pub.put(s);
       }
       std::cout << "Done." << std::endl;
       return 0;
   }
   ```

3. Compile and run. `-DZENOHCXX_ZENOHC=1` selects the zenoh-c backend:

   ```sh
   c++ -std=c++17 -DZENOHCXX_ZENOHC=1 z_pub.cpp \
       -Izenoh-cpp/include -Izenoh-c/include \
       -Lzenoh-c/lib -lzenohc -o z_pub
   LD_LIBRARY_PATH=zenoh-c/lib ./z_pub
   ```

---

## Embedded C — zenoh-pico

Repository: <https://github.com/eclipse-zenoh/zenoh-pico>

zenoh-pico is the lightweight implementation for constrained/embedded targets.
Unlike the other bindings it runs in **client** mode, so it needs a running
router. Start one as described in
[Running a Zenoh router](#running-a-zenoh-router) (or, quickly,
`docker run --init -p 7447:7447 eclipse/zenoh`) before publishing.

1. Download and unpack the library:

   ```sh
   curl -LO https://download.eclipse.org/zenoh/zenoh-pico/1.9.0/zenoh-pico-1.9.0-linux-x64-standalone.zip
   unzip zenoh-pico-1.9.0-linux-x64-standalone.zip -d zenoh-pico
   ```

2. Save the publisher as `z_pub.c`. It connects to the local router on
   `tcp/127.0.0.1:7447`:

   ```c
   #include <stdio.h>
   #include <zenoh-pico.h>

   int main(void) {
       const char *keyexpr = "demo/example/zenoh-pico-pub";

       z_owned_config_t config;
       z_config_default(&config);
       zp_config_insert(z_loan_mut(config), Z_CONFIG_CONNECT_KEY, "tcp/127.0.0.1:7447");

       printf("Opening session...\n");
       z_owned_session_t s;
       if (z_open(&s, z_move(config), NULL) < 0) {
           printf("Unable to open session!\n");
           return -1;
       }
       if (zp_start_read_task(z_loan_mut(s), NULL) < 0 ||
           zp_start_lease_task(z_loan_mut(s), NULL) < 0) {
           printf("Unable to start read and lease tasks\n");
           z_drop(z_move(s));
           return -1;
       }

       printf("Declaring publisher for '%s'...\n", keyexpr);
       z_view_keyexpr_t ke;
       z_view_keyexpr_from_str(&ke, keyexpr);
       z_owned_publisher_t pub;
       if (z_declare_publisher(z_loan(s), &pub, z_loan(ke), NULL) < 0) {
           printf("Unable to declare publisher!\n");
           return -1;
       }

       char buf[256];
       for (int idx = 0; idx < 3; ++idx) {
           z_sleep_s(1);
           sprintf(buf, "[%4d] Pub from Pico!", idx);
           printf("Putting Data ('%s': '%s')...\n", keyexpr, buf);
           z_owned_bytes_t payload;
           z_bytes_copy_from_str(&payload, buf);
           z_publisher_put(z_loan(pub), z_move(payload), NULL);
       }
       z_drop(z_move(pub));
       z_drop(z_move(s));
       printf("Done.\n");
       return 0;
   }
   ```

3. Compile and run. `-DZENOH_LINUX=1` selects the platform layer:

   ```sh
   cc z_pub.c -DZENOH_LINUX=1 -Izenoh-pico/include -Lzenoh-pico/lib -lzenohpico -pthread -o z_pub
   LD_LIBRARY_PATH=zenoh-pico/lib ./z_pub
   ```

---

## Go

Repository: <https://github.com/eclipse-zenoh/zenoh-go>

zenoh-go is a cgo wrapper around zenoh-c. As stated in its README, it requires
zenoh-c built **with unstable features**
(`-DZENOHC_BUILD_WITH_UNSTABLE_API=ON`), which the prebuilt archives do not
enable — so build zenoh-c from source once and point cgo at it.

1. Build and install zenoh-c with the unstable API (needs
   [Rust](https://rustup.rs/), `git`, `cmake` and a C compiler):

   ```sh
   git clone --branch 1.9.0 --depth 1 https://github.com/eclipse-zenoh/zenoh-c.git
   cmake -S zenoh-c -B zenoh-c/build \
       -DZENOHC_BUILD_WITH_UNSTABLE_API=ON \
       -DCMAKE_BUILD_TYPE=Release \
       -DCMAKE_INSTALL_PREFIX="$PWD/zenoh-c/install"
   cmake --build zenoh-c/build --target install --config Release
   ```

2. Point cgo and the loader at the freshly built library:

   ```sh
   export CGO_CFLAGS="-I$PWD/zenoh-c/install/include"
   export CGO_LDFLAGS="-L$PWD/zenoh-c/install/lib"
   export LD_LIBRARY_PATH="$PWD/zenoh-c/install/lib"
   ```

3. Create the module and add the dependency:

   ```sh
   mkdir zenoh-go-pub && cd zenoh-go-pub
   go mod init example.com/zenoh-go-pub
   go get github.com/eclipse-zenoh/zenoh-go@v1.9.0
   ```

4. Save the publisher as `z_pub.go`:

   ```go
   package main

   import (
       "fmt"
       "time"

       "github.com/eclipse-zenoh/zenoh-go/zenoh"
   )

   func main() {
       key := "demo/example/zenoh-go-pub"
       fmt.Println("Opening session...")
       config := zenoh.NewConfigDefault()
       session, err := zenoh.Open(config, nil)
       if err != nil {
           fmt.Printf("Unable to open session: %v\n", err)
           return
       }
       defer session.Drop()

       ke, err := zenoh.NewKeyExpr(key)
       if err != nil {
           fmt.Printf("Invalid key expression: %v\n", err)
           return
       }
       fmt.Printf("Declaring Publisher on '%s'...\n", key)
       pub, err := session.DeclarePublisher(ke, nil)
       if err != nil {
           fmt.Printf("Unable to declare publisher: %v\n", err)
           return
       }
       defer pub.Drop()

       for idx := 0; idx < 3; idx++ {
           msg := fmt.Sprintf("[%4d] Pub from Go!", idx)
           fmt.Printf("Putting Data ('%s': '%s')...\n", key, msg)
           if err := pub.Put(zenoh.NewZBytesFromString(msg), nil); err != nil {
               fmt.Printf("put error: %v\n", err)
           }
           time.Sleep(time.Second)
       }
       fmt.Println("Done.")
   }
   ```

5. Run it (keep the environment variables from step 2):

   ```sh
   go run .
   ```

---

## Java

Repository: <https://github.com/eclipse-zenoh/zenoh-java>

The Java library is published on Maven Central as
[`org.eclipse.zenoh:zenoh-java`](https://central.sonatype.com/artifact/org.eclipse.zenoh/zenoh-java);
the artifact bundles the native library for common platforms. The example below
uses Gradle (8+) with JDK 21.

1. Create the project layout:

   ```sh
   mkdir -p zenoh-java-pub/src/main/java
   cd zenoh-java-pub
   ```

2. `settings.gradle.kts`:

   ```kotlin
   rootProject.name = "zpub"
   ```

3. `build.gradle.kts`:

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

4. `src/main/java/ZPub.java`:

   ```java
   import io.zenoh.Config;
   import io.zenoh.Session;
   import io.zenoh.Zenoh;
   import io.zenoh.keyexpr.KeyExpr;
   import io.zenoh.pubsub.Publisher;

   public class ZPub {
       public static void main(String[] args) throws Exception {
           Zenoh.initLogFromEnvOr("error");
           Config config = Config.loadDefault();
           System.out.println("Opening session...");
           try (Session session = Zenoh.open(config)) {
               KeyExpr keyExpr = KeyExpr.tryFrom("demo/example/zenoh-java-pub");
               System.out.println("Declaring publisher on '" + keyExpr + "'...");
               Publisher publisher = session.declarePublisher(keyExpr);
               for (int idx = 0; idx < 3; idx++) {
                   Thread.sleep(1000);
                   String payload = String.format("[%4d] Pub from Java!", idx);
                   System.out.println("Putting Data ('" + keyExpr + "': '" + payload + "')...");
                   publisher.put(payload);
               }
           }
           System.out.println("Done.");
       }
   }
   ```

5. Run it:

   ```sh
   gradle run
   ```

---

## Kotlin

Repository: <https://github.com/eclipse-zenoh/zenoh-kotlin>

The Kotlin library is published on Maven Central as
[`org.eclipse.zenoh:zenoh-kotlin`](https://central.sonatype.com/artifact/org.eclipse.zenoh/zenoh-kotlin).
The example below uses Gradle (8+) with JDK 21.

1. Create the project layout:

   ```sh
   mkdir -p zenoh-kotlin-pub/src/main/kotlin
   cd zenoh-kotlin-pub
   ```

2. `settings.gradle.kts`:

   ```kotlin
   rootProject.name = "zpub"
   ```

3. `build.gradle.kts`:

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

4. `src/main/kotlin/ZPub.kt`:

   ```kotlin
   import io.zenoh.Config
   import io.zenoh.Zenoh
   import io.zenoh.bytes.ZBytes
   import io.zenoh.keyexpr.intoKeyExpr

   fun main() {
       Zenoh.initLogFromEnvOr("error")
       val config = Config.default()
       println("Opening session...")
       val session = Zenoh.open(config).getOrThrow()
       val keyExpr = "demo/example/zenoh-kotlin-pub".intoKeyExpr().getOrThrow()
       println("Declaring publisher on '$keyExpr'...")
       val publisher = session.declarePublisher(keyExpr).getOrThrow()
       for (idx in 0 until 3) {
           Thread.sleep(1000)
           val payload = "[${idx.toString().padStart(4, ' ')}] Pub from Kotlin!"
           println("Putting Data ('$keyExpr': '$payload')...")
           publisher.put(ZBytes.from(payload))
       }
       session.close()
       println("Done.")
   }
   ```

5. Run it:

   ```sh
   gradle run
   ```

---

## TypeScript / JavaScript

Repository: <https://github.com/eclipse-zenoh/zenoh-ts>

The library is published on npm as
[`@eclipse-zenoh/zenoh-ts`](https://www.npmjs.com/package/@eclipse-zenoh/zenoh-ts).
It reaches the Zenoh network over a WebSocket connection to the
`zenoh-plugin-remote-api`, so you run the **remote-api bridge** alongside it.
The command-line examples use [Deno](https://deno.com/) (the library targets
browsers and Deno, not Node.js).

1. Download and start the bridge (listens on `ws://localhost:10000` by default):

   ```sh
   curl -LO https://download.eclipse.org/zenoh/zenoh-plugin-remote-api/1.9.0/zenoh-ts-1.9.0-x86_64-unknown-linux-gnu-standalone.zip
   unzip zenoh-ts-1.9.0-x86_64-unknown-linux-gnu-standalone.zip -d zenoh-bridge
   chmod +x zenoh-bridge/zenoh-bridge-remote-api
   ./zenoh-bridge/zenoh-bridge-remote-api &
   ```

2. Map the package for Deno in `deno.json`:

   ```json
   {
     "imports": {
       "@eclipse-zenoh/zenoh-ts": "npm:@eclipse-zenoh/zenoh-ts@1.9.0"
     }
   }
   ```

3. Save the publisher as `z_pub.ts`:

   ```typescript
   import { Config, KeyExpr, Session, Encoding, CongestionControl, Priority } from "@eclipse-zenoh/zenoh-ts";

   async function main() {
     console.log("Opening session...");
     const session = await Session.open(new Config("ws/127.0.0.1:10000"));
     const keyExpr = KeyExpr.autocanonize("demo/example/zenoh-ts-pub");
     console.log(`Declaring publisher on '${keyExpr}'...`);
     const publisher = await session.declarePublisher(keyExpr, {
       encoding: Encoding.default(),
       congestionControl: CongestionControl.BLOCK,
       priority: Priority.DATA,
       express: true,
     });
     for (let idx = 0; idx < 3; idx++) {
       const buf = `[${idx}] Pub from TypeScript!`;
       console.log(`Putting Data ('${keyExpr}': '${buf}')...`);
       await publisher.put(buf, { encoding: Encoding.TEXT_PLAIN });
       await new Promise((r) => setTimeout(r, 1000));
     }
     await session.close();
     console.log("Done.");
   }
   main();
   ```

4. Run it:

   ```sh
   deno run -A z_pub.ts
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

- **Docker**:

  ```sh
  docker run --init -p 7447:7447 -p 8000:8000 eclipse/zenoh
  ```

- **Homebrew** (macOS): `brew tap eclipse-zenoh/homebrew-zenoh && brew install zenohd`.

By default `zenohd` listens for Zenoh connections on `tcp/[::]:7447`, which is
where the zenoh-pico example connects.
