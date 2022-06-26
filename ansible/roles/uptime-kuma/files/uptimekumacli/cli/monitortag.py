import click

from uptimekumacli import api
from . import cli
from .decorators import need_connection


@cli.group()
def monitortag():
    pass


@monitortag.command("add")
@click.argument("tag_id", type=str)
@click.argument("monitor_id", type=str)
@click.argument("value", type=str)
@need_connection
def monitortag_add(tag_id, monitor_id, value):
    r = api.add_monitor_tag(tag_id, monitor_id, value)
    print(r)


@monitortag.command("edit")
@click.argument("tag_id", type=str)
@click.argument("monitor_id", type=str)
@click.argument("value", type=str)
@need_connection
def monitortag_edit(tag_id, monitor_id, value):
    r = api.edit_monitor_tag(tag_id, monitor_id, value)
    print(r)


@monitortag.command("delete")
@click.argument("tag_id", type=str)
@click.argument("monitor_id", type=str)
@click.argument("value", type=str)
@need_connection
def monitortag_delete(tag_id, monitor_id, value):
    r = api.delete_monitor_tag(tag_id, monitor_id, value)
    print(r)
