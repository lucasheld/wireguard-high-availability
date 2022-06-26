from uptimekumacli import event_data
from . import cli
from .decorators import need_connection, wait_for_event


@cli.command("avgping")
@need_connection
@wait_for_event("avgPing")
def avgping():
    print(event_data.avgPing)
