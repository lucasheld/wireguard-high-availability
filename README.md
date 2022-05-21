# wg-high-availability

## Configuration

1. Create a Hetzner api token and insert it into `hetzner.api_token` in the file `group_vars/all`
1. Create one floating ip and multiple servers at Hetzner
1. Adjust the floating ip name and ip inside `hetzner.floating_ip` of the file `group_vars/all`
1. Add all server ips to the `[servers]` section of the file `inventory/hosts.ini`
1. Adjust the private key of the wireguard interface and the public key of the peer inside `wireguard.interface` of the file `group_vars/all`. The whole wireguard config file can be found at `roles/wireguard/templates/wg0.conf.j2` 

## Installation

```bash
ansible-playbook setup-servers.yml -u root
```
