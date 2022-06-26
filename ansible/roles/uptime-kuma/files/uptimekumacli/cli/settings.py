import click

from uptimekumacli import api
from . import cli
from .decorators import need_connection


@cli.group()
def settings():
    pass


@settings.command("get")
@need_connection
def settings_get():
    r = api.socket_settings_get()
    print(r)


@settings.command("set")
@click.argument("data", type=str)
@click.argument("password", type=str)
@need_connection
def settings_set(data, password):
    r = api.socket_settings_set(data, password)
    print(r)


@settings.command("changepassword")
@click.argument("oldpass", type=str)
@click.argument("newpass", type=str)
@need_connection
def settings_changepassword(oldpass, newpass):
    r = api.socket_change_password(oldpass, newpass)
    print(r)
