terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "1.42.0"
    }
  }
}

variable "location" {
  default = "nbg1"
}

variable "server-count" {
  default = "2"
}

resource "hcloud_ssh_key" "default" {
  name       = "hcloud_ssh_key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "hcloud_server" "wireguard" {
  count       = var.server-count
  name        = "wireguard-${count.index}"
  image       = "debian-11"
  server_type = "cx11"
  location    = var.location
  ssh_keys    = [hcloud_ssh_key.default.id]
}

resource "hcloud_floating_ip" "floating-ipv4" {
  type      = "ipv4"
  name      = "wireguard-floating-ipv4"
  server_id = hcloud_server.wireguard[0].id
}

# resource "hcloud_floating_ip" "floating-ipv6" {
#   type      = "ipv6"
#   name      = "wireguard-floating-ipv6"
#   server_id = hcloud_server.wireguard[0].id
# }
