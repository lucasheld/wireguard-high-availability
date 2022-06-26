from uptimekumacli import sio


__all__ = [
    "add_monitor_tag",
    "edit_monitor_tag",
    "delete_monitor_tag"
]


def add_monitor_tag(tag_id, monitor_id, value):
    return sio.call('addMonitorTag', (tag_id, monitor_id, value))


def edit_monitor_tag(tag_id, monitor_id, value):
    return sio.call('editMonitorTag', (tag_id, monitor_id, value))


def delete_monitor_tag(tag_id, monitor_id, value):
    return sio.call('deleteMonitorTag', (tag_id, monitor_id, value))
