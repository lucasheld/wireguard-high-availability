from uptimekumacli import event_data
from . import cli
from .decorators import need_connection, wait_for_event


@cli.command("info")
@need_connection
@wait_for_event("info")
def info():
    print(event_data.info)
