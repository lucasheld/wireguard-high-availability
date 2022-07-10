# wg-high-availability

## Create infrastucture

1. Install terraform
1. Create a Hetzner api token and export it as environment variable `HCLOUD_TOKEN`
1. Adjust and apply the terraform configuration from the terraform folder
```bash
terraform apply
```

## Installation

1. Install ansible
1. Run `ansible-galaxy install -r requirements.yml`
1. Create a Hetzner api token and insert it into `hetzner.api_token` of the file `group_vars/all`
1. Adjust the floating ip names `hetzner.floating_ipv4` and `hetzner.floating_ipv6` (optional) of the file `group_vars/all`
1. Create a wireguard private key and insert it into `wireguard.interface.private_key`
```bash
wg genkey
```
3. Adjust the peers inside `wireguard.peers` and `wireguard.custom_rules` (optional). The whole wireguard config file can be found at `roles/wireguard/templates/wg0.conf.j2`.
4. Insert the Hetzner VM ips to the `[servers]` section of the file `inventory/hosts.ini`
5. Run the ansible playbook:
```bash
ansible-playbook setup-servers.yml -u root
```




# Notes

floating ipv6 nutzen
--------------------
wird nur gebraucht, wenn keine ipv4 am client vorhanden ist
nur die verbindung wird darüber aufgebaut, danach bekommt der client eine ipv4 und ipv6, egal ob der client vorher eine ipv4 oder ipv6 bessessen hat

wenn floating ip
2a01:4f8:1c0c:a058::/64
dann
Endpoint = [2a01:4f8:1c0c:a058::]:51820
