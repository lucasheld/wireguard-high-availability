from uptimekumacli import event_data
from . import cli
from .decorators import need_connection, wait_for_event


@cli.group()
def statuspage():
    pass


@statuspage.command("list")
@need_connection
@wait_for_event("statusPageList")
def statuspage_list():
    print(event_data.statusPageList)
