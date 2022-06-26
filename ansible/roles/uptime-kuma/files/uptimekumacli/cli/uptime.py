from uptimekumacli import event_data
from . import cli
from .decorators import need_connection, wait_for_event


@cli.command("uptime")
@need_connection
@wait_for_event("uptime")
def uptime():
    print(event_data.uptime)
