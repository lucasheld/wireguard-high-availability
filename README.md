#  wireguard-high-availability

This project automatically creates a high available WireGuard cloud infrastructure using Terraform and Ansible.

A zero trust achitecture ensures that the clients that are connected to the WireGuard server can communicate with each other, but only on specified protocols and ports.
Uptime Kuma is used to monitor the WireGuard backup servers, the connected WireGuard clients and the services that are running on the clients.

The WireGuard server config, the iptables firewall rules and the Uptime Kuma monitoring configuration are automatically generated based on the Ansible variables defined in the group_vars.


## Infrastucture
- Install Terraform

- Open the terraform directory:
  ```shell
  $ cd terraform
  ```

- Create a Hetzner API-Token with the permission to read and write (Hetzner Cloud Console > Security > API-Tokens).
  Export the Hetzner API-Token as environment variable `HCLOUD_TOKEN`.

- Adjust the Terraform configuration `main.tf`.

- Initialize the Terraform configuration:
  ```shell
  $ terraform init
  ```

- Apply the Terraform configuration:
  ```shell
  $ terraform apply
  ```


## Installation
- Install ansible.

- Open the ansible directory:
  ```shell
  $ cd ansible
  ```

- Open the Hetzner webinterface and extract the Server IP addresses (Hetzner Cloud Console > Server).
  Replace them in the `[servers]` section of the file `inventory/hosts.ini`.

- To adjust the Ansible Playbook config, open the file `group_vars/all`.
  - Replace `hetzner.api_token` with the Hetzner API-Token.

  - Replace `hetzner.floating_ipv4` with the name of the Floating IP type ipv4.
  
  - (Optional) Replace `hetzner.floating_ipv6` with the name of the Floating IP type ipv6.
    
    If the ipv6 Floating IP is not required, the variable can be removed.
    
    An ipv6 Floating IP is only required if the client that connects to the WireGuard server does not have an ipv4 address.
    Even if the client does not have an ipv6 address, it will get the ipv6 address of the WireGuard server after the WireGuard tunnel is estabished.
    
    If the Floating IP address is for example `2a01:4f8:1c0c:a058::/64`, the Endpoint in the client config will be `Endpoint = [2a01:4f8:1c0c:a058::]:51820`.
  
  - Replace `wireguard.interface.private_key` with a WireGuard private key.
    The key can be generated with the command:
    ```shell
    $ wg genkey
    ```
  
  - Adjust each peer of `wireguard.peers`.
    - Replace the `public_key` and the `allowed_ips`.
      These values are written to the WireGuard server `[Peer]` config.
  
    - Add the services that are running on the peer to `services`.
      Each service can have multiple rules and one `allowed_tags` list.
      Each rule can have a protocol and port defined.
      Peers that have a tag that is listed in the `allowed_tags` are allowed to communicate with this service.
  
    - Adjust the `tags` to assign a tag to the peer.
  
  - Adjust the custom rules in `wireguard.custom_rules` to extend the firewall rules on the WireGuard server.
  
  The whole WireGuard config file can be found at `roles/wireguard/templates/wg0.conf.j2`.

- Install Ansible dependencies:
  ```shell
  $ ansible-galaxy install -r requirements.yml
  ```

- Run the Ansible Playbook:
  ```shell
  $ ansible-playbook setup-servers.yml -u root
  ```

- Open the Hetzner webinterface and extract the Floating IP address (Hetzner Cloud Console > Floating IPs).
  Use this IP as `Endpoint` in the `[Peer]` section of the WireGuard client config.
