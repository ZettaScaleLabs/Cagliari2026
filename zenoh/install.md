# Installing Zenoh

Zenoh is a Rust core ([zenoh](https://github.com/eclipse-zenoh/zenoh)) plus a
family of bindings for other languages, together with
[zenoh-pico](https://github.com/eclipse-zenoh/zenoh-pico), an independent
lightweight C implementation for constrained and embedded targets. For each
language this guide shows two ways to get it running:

- **From the official distribution** — install the prebuilt binding from its
  package registry (or a prebuilt archive), then write a tiny **publisher** and
  **subscriber** and run them together to watch data flow. These steps were
  verified in a clean environment.
- **From latest source** — clone the binding's GitHub repository, build it and
  run the **bundled `z_pub` / `z_sub` examples** (no code to write). These steps
  follow each project's README and track the tip of `main`, so the exact version
  may be ahead of the distribution.

## Platform

The distribution commands below were verified on Linux and download the
**x86_64** archives. For other targets pick the matching archive on the release
page — e.g. `aarch64-unknown-linux-gnu` (or `linux-arm64` for zenoh-pico),
`apple-darwin`, `pc-windows-msvc`. On macOS the native libraries and the router
are also available from the Homebrew tap
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

### From the official distribution

Create a project and add the dependencies:

```sh
cargo new zenoh-demo
cd zenoh-demo
rm src/main.rs
cargo add zenoh
cargo add tokio --features rt-multi-thread,time,macros
```

Put the publisher in `src/bin/pub.rs`:

```rust
use std::time::Duration;

#[tokio::main]
async fn main() {
    let session = zenoh::open(zenoh::Config::default()).await.unwrap();
    let publisher = session.declare_publisher("demo/example/hello").await.unwrap();
    for i in 0..10 {
        println!("Sent Hello #{i}");
        publisher.put(format!("Hello #{i}")).await.unwrap();
        tokio::time::sleep(Duration::from_secs(1)).await;
    }
}
```

and the subscriber in `src/bin/sub.rs`:

```rust
#[tokio::main]
async fn main() {
    let session = zenoh::open(zenoh::Config::default()).await.unwrap();
    let subscriber = session.declare_subscriber("demo/example/hello").await.unwrap();
    println!("Listening on 'demo/example/hello'...");
    while let Ok(sample) = subscriber.recv_async().await {
        println!("{}: {}", sample.key_expr().as_str(), sample.payload().try_to_string().unwrap());
    }
}
```

Run them together (the first build compiles Zenoh):

```sh
cargo run --bin sub   # terminal 1
cargo run --bin pub   # terminal 2
```

### From latest source

Clone the repository and run the bundled examples (the first build compiles
Zenoh from source):

```sh
git clone https://github.com/eclipse-zenoh/zenoh.git
cd zenoh/examples
cargo run --example z_sub   # terminal 1
cargo run --example z_pub   # terminal 2
```

---

## Python

Repository: <https://github.com/eclipse-zenoh/zenoh-python>

The Python package is published on [PyPI](https://pypi.org/project/eclipse-zenoh/)
as `eclipse-zenoh`.

### From the official distribution

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install eclipse-zenoh
```

Save the publisher as `pub.py`:

```python
import time
import zenoh

with zenoh.open(zenoh.Config()) as session:
    pub = session.declare_publisher("demo/example/hello")
    for i in range(10):
        print(f"Sent Hello #{i}")
        pub.put(f"Hello #{i}")
        time.sleep(1)
```

and the subscriber as `sub.py`:

```python
import time
import zenoh

def listener(sample):
    print(f"{sample.key_expr}: {sample.payload.to_string()}")

with zenoh.open(zenoh.Config()) as session:
    session.declare_subscriber("demo/example/hello", listener)
    print("Listening on 'demo/example/hello'...")
    while True:
        time.sleep(1)
```

Run them together:

```sh
python sub.py   # terminal 1
python pub.py   # terminal 2
```

### From latest source

Building from source compiles the Rust core, so a [Rust toolchain](https://rustup.rs/)
is required. zenoh-python builds with [maturin](https://www.maturin.rs/); then run
the bundled examples:

```sh
git clone https://github.com/eclipse-zenoh/zenoh-python.git
cd zenoh-python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
maturin develop --release
python examples/z_sub.py   # terminal 1
python examples/z_pub.py   # terminal 2
```

---

## C — zenoh-c

Repository: <https://github.com/eclipse-zenoh/zenoh-c>

### From the official distribution

Download the prebuilt `standalone` archive (headers + library):

```sh
curl -LO https://download.eclipse.org/zenoh/zenoh-c/1.9.0/zenoh-c-1.9.0-x86_64-unknown-linux-gnu-standalone.zip
unzip zenoh-c-1.9.0-x86_64-unknown-linux-gnu-standalone.zip -d zenoh-c
```

Save the publisher as `pub.c`:

```c
#include <stdio.h>
#include "zenoh.h"

int main(void) {
    z_owned_config_t config;
    z_config_default(&config);
    z_owned_session_t s;
    z_open(&s, z_move(config), NULL);

    z_view_keyexpr_t ke;
    z_view_keyexpr_from_str(&ke, "demo/example/hello");
    z_owned_publisher_t pub;
    z_declare_publisher(z_loan(s), &pub, z_loan(ke), NULL);

    char buf[64];
    for (int i = 0; i < 10; i++) {
        snprintf(buf, sizeof(buf), "Hello #%d", i);
        printf("Sent %s\n", buf);
        z_owned_bytes_t payload;
        z_bytes_copy_from_str(&payload, buf);
        z_publisher_put(z_loan(pub), z_move(payload), NULL);
        z_sleep_s(1);
    }
    z_drop(z_move(pub));
    z_drop(z_move(s));
    return 0;
}
```

and the subscriber as `sub.c`:

```c
#include <stdio.h>
#include "zenoh.h"

void data_handler(z_loaned_sample_t *sample, void *arg) {
    z_view_string_t key;
    z_keyexpr_as_view_string(z_sample_keyexpr(sample), &key);
    z_owned_string_t payload;
    z_bytes_to_string(z_sample_payload(sample), &payload);
    printf("%.*s: %.*s\n",
           (int)z_string_len(z_loan(key)), z_string_data(z_loan(key)),
           (int)z_string_len(z_loan(payload)), z_string_data(z_loan(payload)));
    z_drop(z_move(payload));
}

int main(void) {
    z_owned_config_t config;
    z_config_default(&config);
    z_owned_session_t s;
    z_open(&s, z_move(config), NULL);

    z_view_keyexpr_t ke;
    z_view_keyexpr_from_str(&ke, "demo/example/hello");
    z_owned_closure_sample_t callback;
    z_closure(&callback, data_handler, NULL, NULL);
    z_owned_subscriber_t sub;
    z_declare_subscriber(z_loan(s), &sub, z_loan(ke), z_move(callback), NULL);

    printf("Listening on 'demo/example/hello'...\n");
    while (1) {
        z_sleep_s(1);
    }
    z_drop(z_move(sub));
    z_drop(z_move(s));
    return 0;
}
```

Build and run them together:

```sh
cc pub.c -Izenoh-c/include -Lzenoh-c/lib -lzenohc -o pub
cc sub.c -Izenoh-c/include -Lzenoh-c/lib -lzenohc -o sub
LD_LIBRARY_PATH=zenoh-c/lib ./sub   # terminal 1
LD_LIBRARY_PATH=zenoh-c/lib ./pub   # terminal 2
```

> The release page also offers Debian packages (`libzenohc-*-debian.zip`) if you
> prefer installing the library system-wide with `dpkg -i`.

### From latest source

Build the library from `main` with CMake (needs [Rust](https://rustup.rs/),
`git`, `cmake` and a C compiler) and run the bundled examples:

```sh
git clone https://github.com/eclipse-zenoh/zenoh-c.git
cmake -S zenoh-c -B zenoh-c/build -DCMAKE_BUILD_TYPE=Release
cmake --build zenoh-c/build --target examples
./zenoh-c/build/target/release/examples/z_sub   # terminal 1
./zenoh-c/build/target/release/examples/z_pub   # terminal 2
```

---

## C++ — zenoh-cpp

Repository: <https://github.com/eclipse-zenoh/zenoh-cpp>

zenoh-cpp is a header-only wrapper built on top of **zenoh-c**, so it needs the
zenoh-c library underneath. `-DZENOHCXX_ZENOHC=1` selects that backend.

### From the official distribution

Download the zenoh-cpp headers and the zenoh-c distribution from the
[C section](#c--zenoh-c):

```sh
curl -LO https://download.eclipse.org/zenoh/zenoh-c/1.9.0/zenoh-c-1.9.0-x86_64-unknown-linux-gnu-standalone.zip
unzip zenoh-c-1.9.0-x86_64-unknown-linux-gnu-standalone.zip -d zenoh-c
curl -LO https://download.eclipse.org/zenoh/zenoh-cpp/1.9.0/zenohcpp-1.9.0-standalone.zip
unzip zenohcpp-1.9.0-standalone.zip -d zenoh-cpp
```

Save the publisher as `pub.cpp`:

```cpp
#include <iostream>
#include <thread>
#include "zenoh.hxx"
using namespace zenoh;
using namespace std::chrono_literals;

int main() {
    auto session = Session::open(Config::create_default());
    auto pub = session.declare_publisher(KeyExpr("demo/example/hello"));
    for (int i = 0; i < 10; i++) {
        std::string msg = "Hello #" + std::to_string(i);
        std::cout << "Sent " << msg << "\n";
        pub.put(msg);
        std::this_thread::sleep_for(1s);
    }
}
```

and the subscriber as `sub.cpp`:

```cpp
#include <iostream>
#include <thread>
#include "zenoh.hxx"
using namespace zenoh;
using namespace std::chrono_literals;

int main() {
    auto session = Session::open(Config::create_default());
    auto sub = session.declare_subscriber(
        KeyExpr("demo/example/hello"),
        [](const Sample &sample) {
            std::cout << sample.get_keyexpr().as_string_view() << ": "
                      << sample.get_payload().as_string() << "\n";
        },
        closures::none);
    std::cout << "Listening on 'demo/example/hello'...\n";
    while (true) {
        std::this_thread::sleep_for(1s);
    }
}
```

Build and run them together:

```sh
c++ -std=c++17 -DZENOHCXX_ZENOHC=1 pub.cpp -Izenoh-cpp/include -Izenoh-c/include -Lzenoh-c/lib -lzenohc -o pub
c++ -std=c++17 -DZENOHCXX_ZENOHC=1 sub.cpp -Izenoh-cpp/include -Izenoh-c/include -Lzenoh-c/lib -lzenohc -o sub
LD_LIBRARY_PATH=zenoh-c/lib ./sub   # terminal 1
LD_LIBRARY_PATH=zenoh-c/lib ./pub   # terminal 2
```

### From latest source

Build and install zenoh-c first (needs [Rust](https://rustup.rs/), `git`,
`cmake` and a C++ compiler), then build the zenoh-cpp examples against it:

```sh
git clone https://github.com/eclipse-zenoh/zenoh-c.git
cmake -S zenoh-c -B zenoh-c/build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PWD/zenoh-c/install"
cmake --build zenoh-c/build --target install --config Release

git clone https://github.com/eclipse-zenoh/zenoh-cpp.git
cmake -S zenoh-cpp -B zenoh-cpp/build -DZENOHCXX_ZENOHC=ON -DCMAKE_PREFIX_PATH="$PWD/zenoh-c/install"
cmake --build zenoh-cpp/build --target examples
LD_LIBRARY_PATH="$PWD/zenoh-c/install/lib" ./zenoh-cpp/build/examples/zenohc/z_sub   # terminal 1
LD_LIBRARY_PATH="$PWD/zenoh-c/install/lib" ./zenoh-cpp/build/examples/zenohc/z_pub   # terminal 2
```

---

## Embedded C — zenoh-pico

Repository: <https://github.com/eclipse-zenoh/zenoh-pico>

zenoh-pico is the lightweight implementation for constrained/embedded targets.
Unlike the other bindings it runs in **client** mode, so it needs a running
router. Start one as described in
[Running a Zenoh router](#running-a-zenoh-router) (or, quickly,
`docker run --init -p 7447:7447 eclipse/zenoh`) before running the demo.
The headers pick the system layer from a platform macro, so `-DZENOH_LINUX=1`
is required when compiling on Linux.

### From the official distribution

```sh
curl -LO https://download.eclipse.org/zenoh/zenoh-pico/1.9.0/zenoh-pico-1.9.0-linux-x64-standalone.zip
unzip zenoh-pico-1.9.0-linux-x64-standalone.zip -d zenoh-pico
```

Save the publisher as `pub.c`. It connects to the local router on
`tcp/127.0.0.1:7447`:

```c
#include <stdio.h>
#include "zenoh-pico.h"

int main(void) {
    z_owned_config_t config;
    z_config_default(&config);
    zp_config_insert(z_loan_mut(config), Z_CONFIG_MODE_KEY, "client");
    zp_config_insert(z_loan_mut(config), Z_CONFIG_CONNECT_KEY, "tcp/127.0.0.1:7447");

    z_owned_session_t s;
    z_open(&s, z_move(config), NULL);

    z_view_keyexpr_t ke;
    z_view_keyexpr_from_str(&ke, "demo/example/hello");
    z_owned_publisher_t pub;
    z_declare_publisher(z_loan(s), &pub, z_loan(ke), NULL);

    char buf[64];
    for (int i = 0; i < 10; i++) {
        snprintf(buf, sizeof(buf), "Hello #%d", i);
        printf("Sent %s\n", buf);
        z_owned_bytes_t payload;
        z_bytes_copy_from_str(&payload, buf);
        z_publisher_put(z_loan(pub), z_move(payload), NULL);
        z_sleep_s(1);
    }
    z_drop(z_move(pub));
    z_drop(z_move(s));
    return 0;
}
```

and the subscriber as `sub.c`:

```c
#include <stdio.h>
#include "zenoh-pico.h"

void data_handler(z_loaned_sample_t *sample, void *ctx) {
    (void)ctx;
    z_view_string_t key;
    z_keyexpr_as_view_string(z_sample_keyexpr(sample), &key);
    z_owned_string_t payload;
    z_bytes_to_string(z_sample_payload(sample), &payload);
    printf("%.*s: %.*s\n",
           (int)z_string_len(z_loan(key)), z_string_data(z_loan(key)),
           (int)z_string_len(z_loan(payload)), z_string_data(z_loan(payload)));
    z_drop(z_move(payload));
}

int main(void) {
    z_owned_config_t config;
    z_config_default(&config);
    zp_config_insert(z_loan_mut(config), Z_CONFIG_MODE_KEY, "client");
    zp_config_insert(z_loan_mut(config), Z_CONFIG_CONNECT_KEY, "tcp/127.0.0.1:7447");

    z_owned_session_t s;
    z_open(&s, z_move(config), NULL);

    z_owned_closure_sample_t callback;
    z_closure(&callback, data_handler, NULL, NULL);
    z_view_keyexpr_t ke;
    z_view_keyexpr_from_str(&ke, "demo/example/hello");
    z_owned_subscriber_t sub;
    z_declare_subscriber(z_loan(s), &sub, z_loan(ke), z_move(callback), NULL);

    printf("Listening on 'demo/example/hello'...\n");
    while (1) {
        z_sleep_s(1);
    }
    z_drop(z_move(sub));
    z_drop(z_move(s));
    return 0;
}
```

With a router running, build and run them together. Linking the static
`libzenohpico.a` directly (instead of `-lzenohpico`) makes the binaries
self-contained, so they need no `LD_LIBRARY_PATH`:

```sh
cc pub.c -DZENOH_LINUX=1 -Izenoh-pico/include zenoh-pico/lib/libzenohpico.a -pthread -o pub
cc sub.c -DZENOH_LINUX=1 -Izenoh-pico/include zenoh-pico/lib/libzenohpico.a -pthread -o sub
./sub   # terminal 1
./pub   # terminal 2
```

### From latest source

Build from `main` with CMake (needs `git`, `cmake` and a C compiler); the
bundled examples are built under `build/examples/`. With a router running:

```sh
git clone https://github.com/eclipse-zenoh/zenoh-pico.git
cd zenoh-pico
make
./build/examples/z_sub -m client -e tcp/127.0.0.1:7447   # terminal 1
./build/examples/z_pub -m client -e tcp/127.0.0.1:7447   # terminal 2
```

---

## Go

Repository: <https://github.com/eclipse-zenoh/zenoh-go>

zenoh-go is a cgo wrapper around zenoh-c. As stated in its README it requires
zenoh-c built **with unstable features** (`-DZENOHC_BUILD_WITH_UNSTABLE_API=ON`),
which the prebuilt archives do not enable — so build zenoh-c from source once and
point cgo at it (needs [Rust](https://rustup.rs/), `git`, `cmake` and a C
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

### From the official distribution

Create a module (keep the environment variables from above). Save the publisher
as `mypub/main.go`:

```go
package main

import (
	"fmt"
	"time"

	"github.com/eclipse-zenoh/zenoh-go/zenoh"
)

func main() {
	session, _ := zenoh.Open(zenoh.NewConfigDefault(), nil)
	defer session.Drop()
	keyexpr, _ := zenoh.NewKeyExpr("demo/example/hello")
	pub, _ := session.DeclarePublisher(keyexpr, nil)
	defer pub.Drop()

	for i := 0; i < 10; i++ {
		msg := fmt.Sprintf("Hello #%d", i)
		fmt.Println("Sent", msg)
		pub.Put(zenoh.NewZBytesFromString(msg), &zenoh.PublisherPutOptions{})
		time.Sleep(time.Second)
	}
}
```

and the subscriber as `mysub/main.go`:

```go
package main

import (
	"fmt"
	"os"
	"os/signal"

	"github.com/eclipse-zenoh/zenoh-go/zenoh"
)

func main() {
	session, _ := zenoh.Open(zenoh.NewConfigDefault(), nil)
	defer session.Drop()
	keyexpr, _ := zenoh.NewKeyExpr("demo/example/hello")
	sub, _ := session.DeclareSubscriber(
		keyexpr,
		zenoh.Closure[zenoh.Sample]{
			Call: func(sample zenoh.Sample) {
				fmt.Printf("%s: %s\n", sample.KeyExpr().String(), sample.Payload().String())
			},
		},
		nil,
	)
	defer sub.Drop()

	fmt.Println("Listening on 'demo/example/hello'...")
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt)
	<-stop
}
```

Pull the published module and run the two programs together:

```sh
go mod init example.com/zenoh-demo
go get github.com/eclipse-zenoh/zenoh-go@v1.9.0
go mod tidy
go run ./mysub   # terminal 1
go run ./mypub   # terminal 2
```

### From latest source

Clone with submodules, build the bundled zenoh-c with unstable features and run
the bundled examples:

```sh
git clone --recurse-submodules https://github.com/eclipse-zenoh/zenoh-go.git
cd zenoh-go
mkdir -p build && cd build
cmake ../zenoh-c -DZENOHC_BUILD_WITH_UNSTABLE_API=ON -DCMAKE_INSTALL_PREFIX="$PWD"
cmake --build . --target install --config Release
cd ..
export CGO_CFLAGS="-I$PWD/build/include"
export CGO_LDFLAGS="-L$PWD/build/lib"
export LD_LIBRARY_PATH="$PWD/build/lib"
make z_sub z_pub
./bin/z_sub   # terminal 1
./bin/z_pub   # terminal 2
```

---

## Java

Repository: <https://github.com/eclipse-zenoh/zenoh-java>

The Java library is published on Maven Central as
[`org.eclipse.zenoh:zenoh-java`](https://central.sonatype.com/artifact/org.eclipse.zenoh/zenoh-java);
the artifact bundles the native library for common platforms. The example below
uses Gradle (8+) with JDK 21.

### From the official distribution

Create the project layout:

```sh
mkdir -p zenoh-demo/src/main/java
cd zenoh-demo
```

`settings.gradle.kts`:

```kotlin
rootProject.name = "zenoh-demo"
```

`build.gradle.kts`:

```kotlin
plugins { java }
repositories { mavenCentral() }
dependencies {
    implementation("org.eclipse.zenoh:zenoh-java:1.9.0")
}
java {
    toolchain { languageVersion.set(JavaLanguageVersion.of(21)) }
}
tasks.register<JavaExec>("pub") {
    classpath = sourceSets["main"].runtimeClasspath
    mainClass.set("Pub")
}
tasks.register<JavaExec>("sub") {
    classpath = sourceSets["main"].runtimeClasspath
    mainClass.set("Sub")
}
```

`src/main/java/Pub.java`:

```java
import io.zenoh.Config;
import io.zenoh.Session;
import io.zenoh.Zenoh;
import io.zenoh.keyexpr.KeyExpr;
import io.zenoh.pubsub.Publisher;

public class Pub {
    public static void main(String[] args) throws Exception {
        try (Session session = Zenoh.open(Config.loadDefault())) {
            KeyExpr keyExpr = KeyExpr.tryFrom("demo/example/hello");
            Publisher publisher = session.declarePublisher(keyExpr);
            for (int i = 0; i < 10; i++) {
                String payload = "Hello #" + i;
                System.out.println("Sent " + payload);
                publisher.put(payload);
                Thread.sleep(1000);
            }
        }
    }
}
```

`src/main/java/Sub.java`:

```java
import io.zenoh.Config;
import io.zenoh.Session;
import io.zenoh.Zenoh;
import io.zenoh.keyexpr.KeyExpr;

public class Sub {
    public static void main(String[] args) throws Exception {
        Session session = Zenoh.open(Config.loadDefault());
        KeyExpr keyExpr = KeyExpr.tryFrom("demo/example/hello");
        System.out.println("Listening on 'demo/example/hello'...");
        session.declareSubscriber(keyExpr, sample ->
            System.out.println(sample.getKeyExpr() + ": " + sample.getPayload()));
        new java.util.concurrent.CountDownLatch(1).await();
    }
}
```

Run them together:

```sh
gradle sub   # terminal 1
gradle pub   # terminal 2
```

### From latest source

The repository ships the `z_pub` / `z_sub` examples as Gradle tasks that compile
the native JNI library on the first run (needs [Rust](https://rustup.rs/) and a
JDK; the repo ships a Gradle wrapper):

```sh
git clone https://github.com/eclipse-zenoh/zenoh-java.git
cd zenoh-java
./gradlew ZSub   # terminal 1
./gradlew ZPub   # terminal 2
```

---

## Kotlin

Repository: <https://github.com/eclipse-zenoh/zenoh-kotlin>

The Kotlin library is published on Maven Central as
[`org.eclipse.zenoh:zenoh-kotlin`](https://central.sonatype.com/artifact/org.eclipse.zenoh/zenoh-kotlin);
the artifact bundles the native library for common platforms. The example below
uses Gradle (8+) with JDK 21.

### From the official distribution

Create the project layout:

```sh
mkdir -p zenoh-demo/src/main/kotlin
cd zenoh-demo
```

`settings.gradle.kts`:

```kotlin
rootProject.name = "zenoh-demo"
```

`build.gradle.kts`:

```kotlin
plugins { kotlin("jvm") version "2.0.21" }
repositories { mavenCentral() }
dependencies {
    implementation("org.eclipse.zenoh:zenoh-kotlin:1.9.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
}
kotlin { jvmToolchain(21) }
tasks.register<JavaExec>("pub") {
    classpath = sourceSets["main"].runtimeClasspath
    mainClass.set("PubKt")
}
tasks.register<JavaExec>("sub") {
    classpath = sourceSets["main"].runtimeClasspath
    mainClass.set("SubKt")
}
```

`src/main/kotlin/Pub.kt`:

```kotlin
import io.zenoh.Config
import io.zenoh.Zenoh
import io.zenoh.bytes.ZBytes
import io.zenoh.keyexpr.intoKeyExpr

fun main() {
    val session = Zenoh.open(Config.default()).getOrThrow()
    val keyExpr = "demo/example/hello".intoKeyExpr().getOrThrow()
    val publisher = session.declarePublisher(keyExpr).getOrThrow()
    for (i in 0..9) {
        val payload = "Hello #$i"
        println("Sent $payload")
        publisher.put(ZBytes.from(payload))
        Thread.sleep(1000)
    }
    session.close()
}
```

`src/main/kotlin/Sub.kt`:

```kotlin
import io.zenoh.Config
import io.zenoh.Zenoh
import io.zenoh.keyexpr.intoKeyExpr
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.runBlocking

fun main() {
    val session = Zenoh.open(Config.default()).getOrThrow()
    val keyExpr = "demo/example/hello".intoKeyExpr().getOrThrow()
    val subscriber = session.declareSubscriber(keyExpr, Channel()).getOrThrow()
    println("Listening on 'demo/example/hello'...")
    runBlocking {
        for (sample in subscriber.receiver) {
            println("${sample.keyExpr}: ${sample.payload}")
        }
    }
}
```

Run them together:

```sh
gradle sub   # terminal 1
gradle pub   # terminal 2
```

### From latest source

The repository ships the `z_pub` / `z_sub` examples as Gradle tasks that compile
the native JNI library on the first run (needs [Rust](https://rustup.rs/) and a
JDK; the repo ships a Gradle wrapper):

```sh
git clone https://github.com/eclipse-zenoh/zenoh-kotlin.git
cd zenoh-kotlin
./gradlew ZSub   # terminal 1
./gradlew ZPub   # terminal 2
```

---

## TypeScript / JavaScript

Repository: <https://github.com/eclipse-zenoh/zenoh-ts>

The library is published on npm as
[`@eclipse-zenoh/zenoh-ts`](https://www.npmjs.com/package/@eclipse-zenoh/zenoh-ts).
It reaches the Zenoh network over a WebSocket connection to the
`zenoh-plugin-remote-api`, so you run the **remote-api bridge** alongside it. The
command-line examples use [Deno](https://deno.com/) (the library targets browsers
and Deno, not Node.js).

### From the official distribution

Download and start the bridge (listens on `ws://localhost:10000` by default):

```sh
curl -LO https://github.com/eclipse-zenoh/zenoh-ts/releases/download/1.9.0/zenoh-ts-1.9.0-x86_64-unknown-linux-gnu-standalone.zip
unzip zenoh-ts-1.9.0-x86_64-unknown-linux-gnu-standalone.zip -d zenoh-bridge
chmod +x zenoh-bridge/zenoh-bridge-remote-api
./zenoh-bridge/zenoh-bridge-remote-api &
```

Map the npm package for Deno in `deno.json`:

```json
{
  "imports": {
    "@eclipse-zenoh/zenoh-ts": "npm:@eclipse-zenoh/zenoh-ts@1.9.0"
  }
}
```

Save the publisher as `pub.ts`:

```typescript
import { Config, KeyExpr, Session, Encoding } from "@eclipse-zenoh/zenoh-ts";

const session = await Session.open(new Config("ws/127.0.0.1:10000"));
const publisher = await session.declarePublisher(KeyExpr.autocanonize("demo/example/hello"));

for (let i = 0; i < 10; i++) {
  const msg = `Hello #${i}`;
  console.log("Sent", msg);
  await publisher.put(msg, { encoding: Encoding.TEXT_PLAIN });
  await new Promise((r) => setTimeout(r, 1000));
}

await session.close();
```

and the subscriber as `sub.ts`:

```typescript
import { Config, Session, KeyExpr, RingChannel, ChannelReceiver, Sample } from "@eclipse-zenoh/zenoh-ts";

const session = await Session.open(new Config("ws/127.0.0.1:10000"));
const sub = await session.declareSubscriber(new KeyExpr("demo/example/hello"), {
  handler: new RingChannel(10),
});

console.log("Listening on 'demo/example/hello'...");
for await (const sample of sub.receiver() as ChannelReceiver<Sample>) {
  console.log(`${sample.keyexpr()}: ${sample.payload().toString()}`);
}
```

Run them together (both connect to the bridge):

```sh
deno run -A sub.ts   # terminal 1
deno run -A pub.ts   # terminal 2
```

### From latest source

The repository contains both the bridge and the library. Run the bridge from
source with Cargo (needs [Rust](https://rustup.rs/)), build the library with
[yarn](https://classic.yarnpkg.com/), then run the bundled examples with Deno:

```sh
git clone https://github.com/eclipse-zenoh/zenoh-ts.git
cd zenoh-ts
cargo run            # starts zenoh-bridge-remote-api on ws://localhost:10000
```

In another shell, build the library and run the examples:

```sh
cd zenoh-ts/zenoh-ts
yarn install
yarn build
yarn start example deno z_sub   # terminal 1
yarn start example deno z_pub   # terminal 2
```

Run `yarn start` with no arguments to print the available run variants (the Deno
command-line examples, the test suite, and the browser examples). One browser
variant is a [Nuxt](https://nuxt.com/) app, `yarn start example browser nuxt`,
which exercises the Zenoh API from a graphical web UI.

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
