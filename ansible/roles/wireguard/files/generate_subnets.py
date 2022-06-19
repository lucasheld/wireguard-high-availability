#!/usr/bin/env python3
import os
import json
import ipaddress


IPV4_PREFIX = 24
IPV6_PREFIX = 112


def get_ip_version(ip_address):
    try:
        return "ipv4" if type(ipaddress.ip_address(ip_address)) is ipaddress.IPv4Address else "ipv6"
    except ValueError:
        return


peers = json.loads(os.environ['ANSIBLE_WIREGUARD_PEERS'])

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

print(json.dumps(subnets))
