from uptimekumacli import sio


__all__ = [
    "clear_events",
    "clear_heartbeats",
    "clear_statistics"
]


def clear_events():
    return sio.call('clearEvents')


def clear_heartbeats():
    return sio.call('clearHeartbeats')


def clear_statistics():
    return sio.call('clearStatistics')
