from uptimekumacli import api
from . import cli
from .decorators import need_connection


@cli.group()
def clear():
    pass


@clear.command("events")
@need_connection
def clear_events():
    r = api.clear_events()
    print(r)


@clear.command("heartbeats")
@need_connection
def clear_heartbeats():
    r = api.clear_heartbeats()
    print(r)


@clear.command("statistics")
@need_connection
def clear_statistics():
    r = api.clear_statistics()
    print(r)
