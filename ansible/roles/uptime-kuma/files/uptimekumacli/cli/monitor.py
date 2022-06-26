import click

from uptimekumacli import api
from uptimekumacli import event_data
from . import cli
from .decorators import need_connection, wait_for_event


@cli.group()
def monitor():
    pass


@monitor.command("list")
@need_connection
@wait_for_event("monitorList")
def monitor_list():
    print(event_data.monitorList)


@monitor.command("get")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def monitor_get(id_):
    r = api.get_monitor(id_)
    print(r)


@monitor.command("add")
@click.argument("type_", metavar="type".upper(), type=str)
@click.argument("name", type=str)
@click.option("--url", type=str, help="Monitor url.")
@click.option("--keyword", type=str, help="Monitor keyword.")
@need_connection
def monitor_add(type_, name, url, keyword):
    r = api.add_monitor(monitor_type=type_, friendly_name=name, url=url, keyword=keyword)
    print(r)


@monitor.command("edit")
@click.argument("id_", metavar="id".upper(), type=str)
@click.option("--type", "type_", type=str)
@click.option("--name", type=str)
@click.option("--url", type=str, help="Monitor url.")
@click.option("--keyword", type=str, help="Monitor keyword.")
@need_connection
def monitor_edit(id_, type_, name, url, keyword):
    # Achtung! Alle nicht angegebenen Werte werden einfach gelöscht
    # ToDo: umgehen, indem bestehender monitor geholt und mit den argumenten geupdated wird
    r = api.edit_monitor(id_, monitor_type=type_, friendly_name=name, url=url, keyword=keyword)
    print(r)


@monitor.command("pause")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def monitor_pause(id_):
    r = api.pause_monitor(id_)
    print(r)


@monitor.command("resume")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def monitor_resume(id_):
    r = api.resume_monitor(id_)
    print(r)


@monitor.command("delete")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def monitor_delete(id_):
    r = api.delete_monitor(id_)
    print(r)


@monitor.command("beats")
@click.argument("id_", metavar="id".upper(), type=int)
@click.argument("period", type=int)
@need_connection
def monitor_beats(id_, period):
    r = api.get_monitor_beats(id_, period)
    print(r)
