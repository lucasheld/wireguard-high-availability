from uptimekumacli.events import sio


__all__ = ["connect", "disconnect", "login", "logout"]


def connect(url):
    url = url.rstrip("/")
    sio.connect(f'{url}/socket.io/')


def disconnect():
    sio.disconnect()


def login(username, password):
    return sio.call('login', {
        "username": username,
        "password": password,
        "token": ""
    })


def logout():
    return sio.call('logout')
