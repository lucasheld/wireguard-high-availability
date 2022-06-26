from uptimekumacli.events import sio


__all__ = ["socket_clear_events", "socket_clear_heartbeats", "socket_clear_statistics"]


def socket_clear_events():
    return sio.call('clearEvents')


def socket_clear_heartbeats():
    return sio.call('clearHeartbeats')


def socket_clear_statistics():
    return sio.call('clearStatistics')
