from hcloud import Client

API_TOKEN = "ZUmwoCyaSyHzoYbnjtDMecS1rLXXaboLJ4ZIppaVQJjbKInvty5O82V7KlHra3AS"
FLOATING_IP_NAME = "wg-floating"


def get_current_server(floating_ip):
    server = floating_ip.data_model.server
    if server:
        current_server = server.data_model.id
        return current_server


def get_floating_ip_server(client, floating_ip):
    servers = client.servers.get_all()
    for server in servers:
        floating_ips = server.data_model.public_net.floating_ips
        for floating_ip_2 in floating_ips:
            if floating_ip_2.data_model.id == floating_ip.data_model.id:
                return server.data_model.id


def main():
    client = Client(token=API_TOKEN)
    floating_ip = client.floating_ips.get_by_name(FLOATING_IP_NAME)

    # client.floating_ips.assign(floating_ip, server)


    current_server = get_current_server(floating_ip)
    floating_ip_server = get_floating_ip_server(client, floating_ip)

    if current_server == floating_ip_server:
        print("same server")
    else:
        print("not same server")


if __name__ == "__main__":
    main()
