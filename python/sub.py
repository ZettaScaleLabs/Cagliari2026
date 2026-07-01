import time
import zenoh

def print_info(session):
    info = session.info
    print(f"zid: {info.zid()}")
    print(f"routers: {info.routers_zid()}")
    print(f"peers: {info.peers_zid()}")
    print("transports:")
    for t in info.transports():
        print(f"  - {t}")
    print("links:")
    for l in info.links():
        print(f"  - {l}")

def listener(sample):
    print(f"{sample.key_expr}: {sample.payload.to_string()}")

zenoh.init_log_from_env_or("INFO")

config = zenoh.Config().from_file("config_sub.json")

with zenoh.open(config) as session:

    print_info(session)
    
    session.declare_subscriber("forkyeah/network/test", listener)
    print("Listening on 'forkyeah/network/test'...")
    while True:
        time.sleep(5)
        print_info(session)