from uptimekumacli import sio


__all__ = [
    "get_tags",
    "edit_tag",
    "delete_tag",
    "add_tag"
]


def get_tags():
    return sio.call('getTags')


def edit_tag(tag):
    return sio.call('editTag', tag)


def delete_tag(id_):
    return sio.call('deleteTag', id_)


def add_tag(color, name, value):
    return sio.call('addTag', {
        "color": color,
        "name": name,
        "value": value,
        "new": True
    })
