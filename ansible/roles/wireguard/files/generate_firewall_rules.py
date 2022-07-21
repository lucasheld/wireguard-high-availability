#!/usr/bin/env python3
import argparse
import ipaddress
import json


def build_command(rule):
    cmd = ""
    if rule["type"] == "ipv4":
        cmd += "iptables -A wg0-filter"
    else:
        cmd += "ip6tables -A wg0-filter6"
    cmd += f" -s {rule['src']} -d {rule['dst']}"
    if rule.get("protocol"):
        cmd += f" -p {rule['protocol']}"
    if rule.get("port"):
        cmd += f" --dport {rule['port']}"
    return cmd


def build_commands(rules):
    cmds = []
    for rule in rules:
        cmd = build_command(rule)
        cmds.append(cmd)
    return cmds


def get_ip_version(ip_address):
    try:
        return "ipv4" if type(ipaddress.ip_address(ip_address)) is ipaddress.IPv4Address else "ipv6"
    except ValueError:
        return


def find_peers_and_services_by_allowed_tag(peers, allowed_tag):
    out = []
    for peer in peers:
        for service in peer.get("services", []):
            for allowed_tags in service.get("allowed_tags", []):
                if allowed_tag in allowed_tags:
                    out.append((peer, service))
    return out


def allowed_ips_to_ips(allowed_ips):
    ips = []
    for allowed_ip in allowed_ips:
        ip = allowed_ip.split("/")[0]
        ips.append(ip)
    return ips


def generate_rules_by_peers(peers):
    rules = []
    for peer in peers:
        for tag in peer.get("tags", []):
            allowed_peers_and_services = find_peers_and_services_by_allowed_tag(peers, tag)
            for allowed_peer, service in allowed_peers_and_services:
                peer_ips = allowed_ips_to_ips(peer["allowed_ips"])
                allowed_peer_ips = allowed_ips_to_ips(allowed_peer["allowed_ips"])
                for peer_ip in peer_ips:
                    for allowed_peer_ip in allowed_peer_ips:
                        peer_ip_version = get_ip_version(peer_ip)
                        allowed_peer_ip_version = get_ip_version(allowed_peer_ip)
                        if peer_ip_version == allowed_peer_ip_version:
                            for service_rule in service.get("rules", []):
                                for port in service_rule.get("ports", [None]):
                                    rule = {
                                        "src": peer_ip,
                                        "dst": allowed_peer_ip,
                                        "port": port,
                                        "protocol": service_rule.get("protocol"),
                                        "type": peer_ip_version
                                    }
                                    rules.append(rule)
    return rules


def add_rule_for_each_port(rules):
    rules_new = []
    for rule in rules:
        ports = rule.get("ports")
        if ports:
            for port in ports:
                new_rule = rule.copy()
                new_rule["port"] = port
                new_rule.pop("ports")
                rules_new.append(new_rule)
        else:
            rules_new.append(rule)
    return rules_new


def get_args():
    parser = argparse.ArgumentParser(description="generate firewall rules based on wireguard peers config")
    parser.add_argument("--peers", help="wireguard peers config")
    parser.add_argument("--custom-rules", help="wireguard custom rules config")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    all_cmds = []

    peers = args.peers
    if peers:
        peers = json.loads(peers)
        rules = generate_rules_by_peers(peers)
        cmds = build_commands(rules)
        all_cmds.extend(cmds)

    custom_rules = args.custom_rules
    if custom_rules:
        custom_rules = json.loads(args.custom_rules)
        rules = add_rule_for_each_port(custom_rules)
        cmds = build_commands(rules)
        all_cmds.extend(cmds)

    print(json.dumps(all_cmds))


if __name__ == "__main__":
    main()
