from uptimekumacli import sio


__all__ = [
    "settings_get",
    "settings_set",
    "change_password"
]


def settings_get():
    return sio.call('getSettings')


def settings_set(data, password):
    return sio.call('setSettings', (data, password))


def change_password(oldpass, newpass):
    return sio.call('changePassword', {
        "currentPassword": oldpass,
        "newPassword": newpass,
    })
