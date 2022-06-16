#!/usr/bin/env python3
import os
import json
import ipaddress


def validIPAddress(IP):
    try:
        return "ipv4" if type(ipaddress.ip_address(IP)) is ipaddress.IPv4Address else "ipv6"
    except ValueError:
        return


peers = json.loads(os.environ['ANSIBLE_WIREGUARD_PEERS'])

subnets = []
for peer in peers:
    for allowed_ip in peer["allowed_ips"]:
        ip = allowed_ip.split("/")[0]
        ip_version = validIPAddress(ip)
        if ip_version:
            sub = "24" if ip_version == "ipv4" else "64"
            subnet = f"{ip[:-1]}0/{sub}"
            if subnet not in [i["subnet"] for i in subnets]:
                subnets.append({
                    "type": ip_version,
                    "subnet": subnet
                })

print(json.dumps(subnets))
