import click

from uptimekumacli import api


class Settings(object):
    def __init__(self, url, user, pass_):
        self.url = url
        self.user = user
        self.pass_ = pass_


@click.group()
@click.option("--url", required=True, help="The uptime-kuma webinterface url. Example: http://192.168.20.160:3001/")
@click.option("--user", required=True, help="The uptime-kuma username.")
@click.option("--pass", "pass_", required=True, help="The uptime-kuma password.")
@click.pass_context
def cli(ctx, url, user, pass_):
    ctx.obj = Settings(url, user, pass_)


@cli.result_callback()
def process_result(result, **kwargs):
    api.disconnect()
