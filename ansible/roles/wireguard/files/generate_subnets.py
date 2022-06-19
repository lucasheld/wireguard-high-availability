#!/usr/bin/env python3
import json
import argparse
import ipaddress


IPV4_PREFIX = 24
IPV6_PREFIX = 112


def get_ip_version(ip_address):
    try:
        return "ipv4" if type(ipaddress.ip_address(ip_address)) is ipaddress.IPv4Address else "ipv6"
    except ValueError:
        return


def generate_subnets(peers):
    subnets = []
    for peer in peers:
        for allowed_ip in peer["allowed_ips"]:
            ip = allowed_ip.split("/")[0]
            ip_version = get_ip_version(ip)
            if ip_version:
                prefix = IPV4_PREFIX if ip_version == "ipv4" else IPV6_PREFIX
                network = f"{ip[:-1]}0/{prefix}"
                if network not in [i["network"] for i in subnets]:
                    subnets.append({
                        "type": ip_version,
                        "network": network
                    })
    return subnets


def get_args():
    parser = argparse.ArgumentParser(description="generate subnetes based on wireguard peers config")
    parser.add_argument("--peers", required=True, help="wireguard peers config")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    peers = json.loads(args.peers)

    subnets = generate_subnets(peers)
    print(json.dumps(subnets))


if __name__ == "__main__":
    main()
