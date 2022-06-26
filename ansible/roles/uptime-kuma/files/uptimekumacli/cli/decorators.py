import time

import click

from uptimekumacli import api
from uptimekumacli import event_data


def need_connection(func):
    def inner(*args, **kwargs):
        @click.pass_obj
        def inner2(ctx):
            url = ctx.url
            user = ctx.user
            pass_ = ctx.pass_

            api.connect(url)
            api.login(user, pass_)
        inner2()
        func(*args, **kwargs)
    return inner


def wait_for_event(event):
    def inner(func):
        def inner2(*args, **kwargs):
            while event_data.__dict__[event] is None:
                time.sleep(0.01)
            time.sleep(0.01)  # wait for multiple messages
            func(*args, **kwargs)
        return inner2
    return inner
