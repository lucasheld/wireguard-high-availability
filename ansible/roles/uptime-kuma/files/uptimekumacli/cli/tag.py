import click

from uptimekumacli import api
from . import cli
from .decorators import need_connection


@cli.group()
def tag():
    pass


@tag.command("add")
@click.argument("color", type=str)
@click.argument("name", type=str)
@click.argument("value", type=str)
@need_connection
def tag_add(color, name, value):
    r = api.add_tag(color, name, value)
    print(r)


@tag.command("list")
@need_connection
def tag_list():
    r = api.get_tags()
    print(r)


@tag.command("edit")
@need_connection
def tag_edit():
    pass


@tag.command("delete")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def tag_delete(id_):
    r = api.delete_monitor(id_)
    print(r)
