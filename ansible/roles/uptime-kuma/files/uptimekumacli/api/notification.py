from uptimekumacli.data import NotificationType
from uptimekumacli import sio

__all__ = ["test_notification", "add_notification", "edit_notification", "delete_notification"]


def build_notification_data(name: str, type_: NotificationType, default: bool, **kwargs):
    kwargs_set = {}
    for k, v in kwargs.items():
        if v is not None:
            kwargs_set[k] = v
    return {
        "name": name,
        "type": type_,
        "isDefault": default,
        **kwargs_set
    }


def test_notification(*args, **kwargs):
    data = build_notification_data(*args, **kwargs)
    return sio.call('testNotification', data)


def add_notification(*args, **kwargs):
    data = build_notification_data(*args, **kwargs)
    return sio.call('addNotification', (data, None))


def edit_notification(id_: int, *args, **kwargs):
    data = build_notification_data(*args, **kwargs)
    return sio.call('addNotification', (data, id_))


def delete_notification(id_: int):
    return sio.call('deleteNotification', id_)
