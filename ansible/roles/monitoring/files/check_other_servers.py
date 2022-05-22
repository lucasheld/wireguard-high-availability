#!/usr/bin/env python3
import argparse
import requests
from hcloud import Client


def get_server_by_ip(client, ip):
    servers = client.servers.get_all()
    for server in servers:
        if server.data_model.public_net.ipv4.ip == ip:
            return server


def is_healthy(ip):
    url = f"http://{ip}"
    try:
        r = requests.get(url, timeout=10)
        return r.ok
    except:
        return False


def get_floating_ip_server(client, floating_ip):
    servers = client.servers.get_all()
    for server in servers:
        floating_ips = server.data_model.public_net.floating_ips
        for floating_ip_1 in floating_ips:
            if floating_ip_1.data_model.id == floating_ip.data_model.id:
                return server


def get_healthy_server(client, current_ip, server_ips):
    for new_ip in server_ips:
        if new_ip != current_ip and is_healthy(new_ip):
            return get_server_by_ip(client, new_ip)


def get_args():
    parser = argparse.ArgumentParser(description="wireguard server check")
    parser.add_argument("--token", required=True, help="hetzner api token")
    parser.add_argument("--floating-ip-name", required=True, help="floating ip name")
    parser.add_argument("--server-ips", nargs='*', required=True, help="server ips")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    token = args.token
    floating_ip_name = args.floating_ip_name
    server_ips = args.server_ips

    client = Client(token=token)

    floating_ip = client.floating_ips.get_by_name(floating_ip_name)
    current_server = get_floating_ip_server(client, floating_ip)
    current_ip = current_server.data_model.public_net.ipv4.ip

    if is_healthy(current_ip):
        print(f"current server healthy")
    else:
        print(f"current server unhealthy")
        server = get_healthy_server(client, current_ip, server_ips)
        if server:
            client.floating_ips.assign(floating_ip, server)
            print(f"floating ip assigned to {server.data_model.name}")
        else:
            print("no healthy server available")


if __name__ == "__main__":
    main()
