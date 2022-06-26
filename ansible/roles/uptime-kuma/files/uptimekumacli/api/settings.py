from uptimekumacli import sio


__all__ = ["socket_settings_get", "socket_settings_set", "socket_change_password"]


def socket_settings_get():
    return sio.call('getSettings')


def socket_settings_set(data, password):
    return sio.call('setSettings', (data, password))


def socket_change_password(oldpass, newpass):
    return sio.call('changePassword', {
        "currentPassword": oldpass,
        "newPassword": newpass,
    })
