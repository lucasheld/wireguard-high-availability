import os
import requests
from hcloud import Client


API_TOKEN = os.environ['HETZNER_API_TOKEN']
FLOATING_IP_NAME = "wg-floating"
OTHER_SERVER_IPS = ["49.12.232.10", "78.47.156.66"]


def get_server_by_ip(client, ip):
    servers = client.servers.get_all()
    for server in servers:
        if server.data_model.public_net.ipv4.ip == ip:
            return server


def is_healthy(ip):
    url = f"http://{ip}"
    r = requests.get(url)
    return r.ok


def get_healthy_server(client, current_ip):
    for new_ip in OTHER_SERVER_IPS:
        if new_ip != current_ip and is_healthy(new_ip):
            return get_server_by_ip(client, new_ip)


def main():
    client = Client(token=API_TOKEN)

    floating_ip = client.floating_ips.get_by_name(FLOATING_IP_NAME)
    current_ip = floating_ip.data_model.ip

    if is_healthy(current_ip):
        print(f"current server healthy")
    else:
        print(f"current server unhealthy")
        server = get_healthy_server(client, current_ip)
        if server:
            client.floating_ips.assign(floating_ip, server)
            print(f"floating ip assigned to {server.data_model.name}")
        else:
            print("no healthy server available")


if __name__ == "__main__":
    main()
