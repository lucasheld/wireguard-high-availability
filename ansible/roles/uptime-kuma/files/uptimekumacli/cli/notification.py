import click

from uptimekumacli import api
from uptimekumacli import event_data
from uptimekumacli.data import notification_provider_options
from . import cli
from .decorators import need_connection, wait_for_event


def add_notification_options(func):
    for type_, options in reversed(notification_provider_options.items()):
        for option in reversed(options):
            click_option = click.option(f"--{option}", option, type=str, help=f"{type_} - {option}")
            func = click_option(func)
    return func


@cli.group()
def notification():
    pass


@notification.command("list")
@need_connection
@wait_for_event("notificationList")
def notification_list():
    print(event_data.notificationList)


@notification.command("test")
@click.argument("name", type=str)
@click.argument("type_", metavar="type".upper(), type=str)
@click.argument("default", type=str)
@add_notification_options
@need_connection
def notification_add(name, type_, default, **kwargs):
    r = api.test_notification(name, type_, default, **kwargs)
    print(r)


@notification.command("add")
@click.argument("name", type=str)
@click.argument("type_", metavar="type".upper(), type=str)
@click.argument("default", type=str)
@add_notification_options
@need_connection
def notification_add(name, type_, default, **kwargs):
    r = api.add_notification(name, type_, default, **kwargs)
    print(r)


@notification.command("edit")
@click.argument("name", type=str)
@click.argument("type_", metavar="type".upper(), type=str)
@click.argument("default", type=str)
@add_notification_options
@need_connection
def notification_edit(name, type_, default, **kwargs):
    r = api.edit_notification(name, type_, default, **kwargs)
    print(r)


@notification.command("delete")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def notification_delete(id_):
    r = api.delete_notification(id_)
    print(r)
