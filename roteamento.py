import os
import subprocess
import socket
import json
import threading
import time
import ipaddress

PORT = 5000
UPDATE_INTERVAL = 5
TIMEOUT = 15

routes = {}     # destino -> { "nexthop": ip, "latency": ms }
neighbors = {}  # vizinho -> { "last_seen": timestamp, "delay": ms }
my_ips = []


def get_my_ips():
    # Pega todos os ips locais, ignorando os ips de loopback
    res = subprocess.check_output(
        "ip -o -4 addr show | awk '{print $4}'",
        shell=True
    ).decode().splitlines()
    return [ip.split("/")[0] for ip in res if not ip.startswith("127.")]


def discover_neighbors():
    # Ping all possible hosts in the subnet to find neighbors
    for ip in my_ips:
        net = ipaddress.ip_network(ip + "/24", strict=False)
        for host in net.hosts():
            host = str(host)
            if host != ip:
                if subprocess.call(
                    ["ping", "-c", "1", "-W", "1", host],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                ) == 0:
                    neighbors[host] = {"last_seen": time.time(), "delay": 1.0}
                    print(f"Discovered neighbor {host}")


def measure_latency(ip):
    # Measure RTT to a neighbor using ping
    try:
        out = subprocess.check_output(
            ["ping", "-c", "1", "-W", "1", ip],
            stderr=subprocess.DEVNULL
        ).decode()
        return float(out.split("time=")[1].split(" ms")[0])
    except:
        return None


def send_table(sock):
    # Send routing table to all neighbors
    msg = json.dumps(routes).encode()
    for neigh in neighbors:
        sock.sendto(msg, (neigh, PORT))


def recv_loop(sock):
    # Receive routing tables from neighbors
    while True:
        data, addr = sock.recvfrom(4096)
        neigh = addr[0]

        neighbors.setdefault(neigh, {"last_seen": time.time(), "delay": 1.0})
        neighbors[neigh]["last_seen"] = time.time()

        table = json.loads(data.decode())
        for dest, info in table.items():
            new_cost = info["latency"] + neighbors[neigh]["delay"]
            if dest not in routes or new_cost < routes[dest]["latency"]:
                routes[dest] = {"nexthop": neigh, "latency": new_cost}
                subprocess.run(["ip", "route", "replace", dest, "via", neigh])


def update_loop(sock):
    # Periodically measure latency and update routing table
    while True:
        for neigh in list(neighbors.keys()):
            delay = measure_latency(neigh)
            if delay:
                neighbors[neigh]["delay"] = delay
            elif time.time() - neighbors[neigh]["last_seen"] > TIMEOUT:
                for dest in list(routes.keys()):
                    if routes[dest]["nexthop"] == neigh:
                        routes[dest]["latency"] = 999999

        send_table(sock)
        time.sleep(UPDATE_INTERVAL)


def main():
    global my_ips
    my_ips = get_my_ips()
    print("My IPs:", my_ips)

    discover_neighbors()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for ip in my_ips:
        try:
            sock.bind((ip, PORT))
            break
        except:
            continue

    threading.Thread(target=recv_loop, args=(sock,), daemon=True).start()
    update_loop(sock)


if __name__ == "__main__":
    main()
