from uptimekumacli import event_data
from uptimekumacli import sio


@sio.event
def connect():
    print('connection established')


@sio.event
def monitorList(data):
    event_data.monitorList = data


@sio.event
def notificationList(data):
    event_data.notificationList = data


@sio.event
def proxyList(data):
    event_data.proxyList = data


@sio.event
def statusPageList(data):
    event_data.statusPageList = data


@sio.event
def heartbeatList(id, data, bool):
    if event_data.heartbeatList is None:
        event_data.heartbeatList = []
    event_data.heartbeatList.append({
        "id": id,
        "data": data,
        "bool": bool,
    })


@sio.event
def importantHeartbeatList(id, data, b):
    if event_data.importantHeartbeatList is None:
        event_data.importantHeartbeatList = []
    event_data.importantHeartbeatList.append({
        "id": id,
        "data": data,
        "bool": bool,
    })


@sio.event
def avgPing(id, data):
    if event_data.avgPing is None:
        event_data.avgPing = []
    event_data.avgPing.append({
        "id": id,
        "data": data,
    })


@sio.event
def uptime(id, hours_24, days_30):
    if event_data.uptime is None:
        event_data.uptime = []
    event_data.uptime.append({
        "id": id,
        "hours_24": hours_24,
        "days_30": days_30,
    })


@sio.event
def heartbeat(data):
    if event_data.heartbeat is None:
        event_data.heartbeat = []
    event_data.heartbeat.append(data)


@sio.event
def info(data):
    event_data.info = data


@sio.on('*')
def catch_all(event, data):
    print(f'UNHANDLED: {event}:\n----\n{data}\n----\n')


@sio.event
def disconnect():
    print('disconnected from server')
