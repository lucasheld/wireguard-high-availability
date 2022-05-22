terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "1.33.2"
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

resource "hcloud_floating_ip" "master" {
  type      = "ipv4"
  name      = "wireguard-floating"
  server_id = hcloud_server.wireguard[0].id
}
