from uptimekumacli import api
from uptimekumacli import event_data
from . import cli
from .decorators import need_connection, wait_for_event


@cli.group()
def proxy():
    pass


@proxy.command("list")
@need_connection
@wait_for_event("proxyList")
def proxy_list():
    print(event_data.proxyList)


@proxy.command("add")
@need_connection
def proxy_add():
    r = api.add_proxy()
    print(r)
