from uptimekumacli import event_data
from . import cli
from .decorators import need_connection, wait_for_event


@cli.group()
def heartbeat():
    pass


@heartbeat.command("list")
@need_connection
@wait_for_event("heartbeatList")
def heartbeat_list():
    print(event_data.heartbeatList)


@heartbeat.command("listimportant")
@need_connection
@wait_for_event("importantHeartbeatList")
def heartbeat_list_important():
    print(event_data.importantHeartbeatList)


@heartbeat.command("get")
@need_connection
@wait_for_event("heartbeat")
def heartbeat_get():
    print(event_data.heartbeat)
