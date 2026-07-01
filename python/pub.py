import time
import zenoh

zenoh.init_log_from_env_or("INFO")

config = zenoh.Config().from_file("config_pub.json")

with zenoh.open(config) as session:
    pub = session.declare_publisher("forkyeah/network/test")

    # info = session.info
    # print(f"zid: {info.zid()}")
    # print(f"routers: {info.routers_zid()}")
    # print(f"peers: {info.peers_zid()}")
    # print("transports:")
    # for t in info.transports():
    #     print(f"  - {t}")
    # print("links:")
    # for l in info.links():
    #     print(f"  - {l}")

    for i in range(100):
        print(f"Sent Hello #{i}")
        pub.put(f"Hello #{i}")
        time.sleep(1)