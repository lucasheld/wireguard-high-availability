#!/usr/bin/env python3
import json
import time

import click
import socketio
from enum import Enum

sio = socketio.Client()

initial_data = {
    "monitorList": None,
    "notificationList": None,
    "proxyList": None,
    "statusPageList": None,
    "heartbeatList": None,
    "importantHeartbeatList": None,
    "avgPing": None,
    "uptime": None,
    "heartbeat": None,
    "info": None,
}


# @sio.event
# def connect():
#     print('connection established')


@sio.event
def monitorList(data):
    # print(f'monitorList:\n----\n{data}\n----\n')
    # print("monitorList")
    initial_data["monitorList"] = data


@sio.event
def notificationList(data):
    # print(f'notificationList:\n----\n{data}\n----\n')
    # print("notificationList")
    initial_data["notificationList"] = data


@sio.event
def proxyList(data):
    # print(f'proxyList:\n----\n{data}\n----\n')
    # print("proxyList")
    initial_data["proxyList"] = data


@sio.event
def statusPageList(data):
    # print(f'statusPageList:\n----\n{data}\n----\n')
    # print("statusPageList")
    initial_data["statusPageList"] = data


@sio.event
def heartbeatList(id, data, bool):
    # print(f'heartbeatList:\n----\n{id}\n{data}\n{bool}\n----\n')
    # print("heartbeatList")
    if not initial_data["heartbeatList"]:
        initial_data["heartbeatList"] = []
    initial_data["heartbeatList"].append({
        "id": id,
        "data": data,
        "bool": bool,
    })


@sio.event
def importantHeartbeatList(id, data, b):
    # print(f'importantHeartbeatList:\n----\n{id}\n{data}\n{bool}\n----\n')
    # print("importantHeartbeatList")
    if not initial_data["importantHeartbeatList"]:
        initial_data["importantHeartbeatList"] = []
    initial_data["importantHeartbeatList"].append({
        "id": id,
        "data": data,
        "bool": bool,
    })


@sio.event
def avgPing(id, data):
    # print(f'avgPing:\n----\n{id}\n{data}\n----\n')
    # print("avgPing")
    if not initial_data["avgPing"]:
        initial_data["avgPing"] = []
    initial_data["avgPing"].append({
        "id": id,
        "data": data,
    })


@sio.event
def uptime(id, hours_24, days_30):
    # print(f'uptime:\n----\n{id}\n{hours_24}\n{days_30}\n----\n')
    # print("uptime")
    if not initial_data["uptime"]:
        initial_data["uptime"] = []
    initial_data["uptime"].append({
        "id": id,
        "hours_24": hours_24,
        "days_30": days_30,
    })


@sio.event
def heartbeat(data):
    # print(f'heartbeat:\n----\n{data}\n----\n')
    # print("heartbeat")
    if not initial_data["heartbeat"]:
        initial_data["heartbeat"] = []
    initial_data["heartbeat"].append(data)


@sio.event
def info(data):
    # print(f'info:\n----\n{data}\n----\n')
    # print("info")
    initial_data["info"] = data


@sio.on('*')
def catch_all(event, data):
    print(f'UNHANDLED: {event}:\n----\n{data}\n----\n')


# @sio.event
# def disconnect():
#     print('disconnected from server')


# missing functions
# -----------------
# loginByToken
# prepare2FA
# save2FA
# disable2FA
# verifyToken
# twoFAStatus
# needSetup
# setup

# editMonitor
# getMonitorList
# getMonitor

# getMonitorBeats
# editMonitorTag
# deleteMonitorTag

# uploadBackup

# checkApprise

def login(username, password):
    return sio.call('login', {
        "username": username,
        "password": password,
        "token": ""
    })


def logout():
    return sio.call('logout')


def pause_monitor(id_):
    return sio.call('pauseMonitor', id_)


def resume_monitor(id_):
    return sio.call('resumeMonitor', id_)


def delete_monitor(id_):
    return sio.call('deleteMonitor', id_)


def get_monitor_beats(id_, period):
    return sio.call('getMonitorBeats', (id_, period))


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


def add_monitor_tag(tag_id, monitor_id, value):
    return sio.call('addMonitorTag', (tag_id, monitor_id, value))


def edit_monitor_tag(tag_id, monitor_id, value):
    return sio.call('editMonitorTag', (tag_id, monitor_id, value))


def delete_monitor_tag(tag_id, monitor_id, value):
    return sio.call('deleteMonitorTag', (tag_id, monitor_id, value))


class NotificationType(str, Enum):
    ALERTA = "alerta"
    ALIYUNSMS = "AliyunSMS"
    APPRISE = "apprise"
    BARK = "Bark"
    CLICKSENDSMS = "clicksendsms"
    DINGDING = "DingDing"
    DISCORD = "discord"
    FEISHU = "Feishu"
    GOOGLECHAT = "GoogleChat"
    GORUSH = "gorush"
    GOTIFY = "gotify"
    LINE = "line"
    LUNASEA = "lunasea"
    MATRIX = "matrix"
    MATTERMOST = "mattermost"
    NTFY = "ntfy"
    OCTOPUSH = "octopush"
    ONEBOT = "OneBot"
    PAGERDUTY = "PagerDuty"
    PROMOSMS = "promosms"
    PUSHBULLET = "pushbullet"
    PUSHBYTECHULUS = "PushByTechulus"
    PUSHDEER = "PushDeer"
    PUSHOVER = "pushover"
    PUSHY = "pushy"
    ROCKET = "rocket.chat"
    SERWERSMS = "serwersms"
    SIGNAL = "signal"
    SLACK = "slack"
    SMTP = "smtp"
    STACKFIELD = "stackfield"
    TEAMS = "teams"
    TELEGRAM = "telegram"
    WEBHOOK = "webhook"
    WECOM = "WeCom"


def build_notification_data(
        name: str, type_: NotificationType, default: bool,
        # # ALERTA
        # alertaApiEndpoint
        # alertaEnvironment
        # alertaApiKey
        # alertaAlertState
        # alertaRecoverState
        # # AliyunSMS
        # accessKeyId
        # secretAccessKey
        # phonenumber
        # templateCode
        # signName
        # # APPRISE
        # appriseURL
        # title
        # # BARK
        # barkEndpoint
        # # CLICKSENDSMS
        # clicksendsmsLogin
        # clicksendsmsPassword
        # clicksendsmsToNumber
        # clicksendsmsSenderName
        # TELEGRAM
        telegram_bot_token: str, telegram_chat_id: str,
):
    if type != NotificationType.TELEGRAM:
        raise NotImplementedError()

    return {
        "name": name,
        "type": type,
        "isDefault": default,
        "telegramBotToken": telegram_bot_token,
        "telegramChatID": telegram_chat_id
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


class MonitorType(str, Enum):
    HTTP = "http"
    PORT = "port"
    PING = "ping"
    KEYWORD = "keyword"
    DNS = "dns"
    PUSH = "push"
    STEAM = "steam"
    MQTT = "mqtt"
    SQLSERVER = "sqlserver"


class AuthMethod(str, Enum):
    NONE = ""
    HTTP_BASIC = "basic"
    NTLM = "ntlm"


def add_proxy():
    pass


def get_monitor(id_):
    return sio.call('getMonitor', id_)


def build_monitor_data(
        monitor_type: MonitorType,
        friendly_name: str,
        heartbeat_interval: int = 60,
        heartbeat_retry_interval: int = 60,
        retries: int = 0,
        upside_down_mode: bool = False,
        tags: list = None,
        notification_ids: list[int] = None,
        # HTTP, KEYWORD
        url: str = None,
        certificate_expiry_notification: bool = False,
        ignore_tls_error: bool = False,
        max_redirects: int = 10,
        accepted_status_codes: list[str] = None,
        proxy_id: int = None,
        http_method: str = "GET",
        http_body: str = None,
        http_headers: str = None,
        auth_method: AuthMethod = AuthMethod.NONE,
        auth_user: str = None,
        auth_pass: str = None,
        auth_domain: str = None,
        auth_workstation: str = None,
        # KEYWORD
        keyword: str = None,
        # DNS, PING, STEAM, MQTT
        hostname: str = None,
        # DNS, STEAM, MQTT
        port: int = 53,
        # DNS
        dns_resolve_server: str = "1.1.1.1",
        dns_resolve_type: str = "A",
        # MQTT
        mqtt_username: str = None,
        mqtt_password: str = None,
        mqtt_topic: str = None,
        mqtt_success_message: str = None,
        # SQLSERVER
        sqlserver_connection_string: str = "Server=<hostname>,<port>;Database=<your database>;User Id=<your user id>;Password=<your password>;Encrypt=<true/false>;TrustServerCertificate=<Yes/No>;Connection Timeout=<int>",
        sqlserver_query: str = None,
):
    if not accepted_status_codes:
        accepted_status_codes = ["200-299"]

    dict_notification_ids = {}
    if notification_ids:
        for notification_id in notification_ids:
            dict_notification_ids[notification_id] = True
    notification_ids = dict_notification_ids

    data = {
        "type": monitor_type,
        "name": friendly_name,
        "interval": heartbeat_interval,
        "retryInterval": heartbeat_retry_interval,
        "maxretries": retries,
        "notificationIDList": notification_ids,
        "upsideDown": upside_down_mode,
    }

    if monitor_type == MonitorType.KEYWORD:
        data.update({
            "keyword": keyword,
        })

    if monitor_type in [MonitorType.HTTP, MonitorType.KEYWORD]:
        data.update({
            "url": url,
            "expiryNotification": certificate_expiry_notification,
            "ignoreTls": ignore_tls_error,
            "maxredirects": max_redirects,
            "accepted_statuscodes": accepted_status_codes,
            "proxyId": proxy_id,
            "method": http_method,
            "body": http_body,
            "headers": http_headers,
            "authMethod": auth_method,
        })

        if auth_method in [AuthMethod.HTTP_BASIC, AuthMethod.NTLM]:
            data.update({
                "basicauth-user": auth_user,
                "basicauth-pass": auth_pass,
            })

        if auth_method == AuthMethod.NTLM:
            data.update({
                "basicauth-domain": auth_domain,
                "basicauth-workstation": auth_workstation,
            })

    if monitor_type in [MonitorType.DNS, MonitorType.PING, MonitorType.STEAM, MonitorType.MQTT]:
        data.update({
            "hostname": hostname,
        })

    if monitor_type in [MonitorType.DNS, MonitorType.STEAM, MonitorType.MQTT]:
        data.update({
            "port": port,
        })

    if monitor_type == MonitorType.DNS:
        data.update({
            "dns_resolve_server": dns_resolve_server,
            "dns_resolve_type": dns_resolve_type,
        })

    if monitor_type == MonitorType.MQTT:
        data.update({
            "mqttUsername": mqtt_username,
            "mqttPassword": mqtt_password,
            "mqttTopic": mqtt_topic,
            "mqttSuccessMessage": mqtt_success_message,
        })

    if monitor_type == MonitorType.SQLSERVER:
        data.update({
            "databaseConnectionString": sqlserver_connection_string,
            "sqlserverQuery": sqlserver_query,
        })

    return data


def add_monitor(*args, **kwargs):
    data = build_monitor_data(*args, **kwargs)
    return sio.call('add', data)


def edit_monitor(id_, *args, **kwargs):
    data = build_monitor_data(*args, **kwargs)
    data.update({
        "id": id_
    })
    return sio.call('editMonitor', data)


def socket_clear_events():
    return sio.call('clearEvents')


def socket_clear_heartbeats():
    return sio.call('clearHeartbeats')


def socket_clear_statistics():
    return sio.call('clearStatistics')


def socket_settings_get():
    return sio.call('getSettings')


def socket_settings_set(data, password):
    return sio.call('setSettings', (data, password))


def socket_change_password(oldpass, newpass):
    return sio.call('changePassword', {
        "currentPassword": oldpass,
        "newPassword": newpass,
    })


class Settings(object):
    def __init__(self, url, user, pass_):
        self.url = url
        self.user = user
        self.pass_ = pass_


def need_connection(func):
    def inner(*args, **kwargs):
        @click.pass_obj
        def inner2(ctx):
            url = ctx.url
            user = ctx.user
            pass_ = ctx.pass_

            url = url.rstrip("/")
            sio.connect(f'{url}/socket.io/')
            login(user, pass_)
        inner2()
        func(*args, **kwargs)
    return inner


def wait_for_event(event):
    def inner(func):
        def inner2(*args, **kwargs):
            while initial_data[event] is None:
                time.sleep(0.01)
            time.sleep(0.01)  # wait for multiple messages
            func(*args, **kwargs)
        return inner2
    return inner


@click.group()
@click.option("--url", required=True, help="The uptime-kuma webinterface url. Example: http://192.168.20.160:3001/")
@click.option("--user", required=True, help="The uptime-kuma username.")
@click.option("--pass", "pass_", required=True, help="The uptime-kuma password.")
@click.pass_context
def cli(ctx, url, user, pass_):
    ctx.obj = Settings(url, user, pass_)


@cli.group()
def monitor():
    pass


@monitor.command("list")
@need_connection
@wait_for_event("monitorList")
def monitor_list():
    print(initial_data["monitorList"])


@monitor.command("get")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def monitor_get(id_):
    r = get_monitor(id_)
    print(r)


@monitor.command("add")
@click.argument("type_", metavar="type".upper(), type=str)
@click.argument("name", type=str)
@click.option("--url", type=str, help="Monitor url.")
@click.option("--keyword", type=str, help="Monitor keyword.")
@need_connection
def monitor_add(type_, name, url, keyword):
    r = add_monitor(monitor_type=type_, friendly_name=name, url=url, keyword=keyword)
    print(r)


@monitor.command("edit")
@click.argument("id_", metavar="id".upper(), type=str)
@click.option("--type", "type_", type=str)
@click.option("--name", type=str)
@click.option("--url", type=str, help="Monitor url.")
@click.option("--keyword", type=str, help="Monitor keyword.")
@need_connection
def monitor_edit(id_, type_, name, url, keyword):
    # Achtung! Alle nicht angegebenen Werte werden einfach gelöscht
    # ToDo: umgehen, indem bestehender monitor geholt und mit den argumenten geupdated wird
    r = edit_monitor(id_, monitor_type=type_, friendly_name=name, url=url, keyword=keyword)
    print(r)


@monitor.command("pause")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def monitor_pause(id_):
    r = pause_monitor(id_)
    print(r)


@monitor.command("resume")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def monitor_resume(id_):
    r = resume_monitor(id_)
    print(r)


@monitor.command("delete")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def monitor_delete(id_):
    r = delete_monitor(id_)
    print(r)


@monitor.command("beats")
@click.argument("id_", metavar="id".upper(), type=int)
@click.argument("period", type=int)
@need_connection
def monitor_beats(id_, period):
    r = get_monitor_beats(id_, period)
    print(r)


@cli.group()
def tag():
    pass


@tag.command("add")
@click.argument("color", type=str)
@click.argument("name", type=str)
@click.argument("value", type=str)
@need_connection
def tag_add(color, name, value):
    r = add_tag(color, name, value)
    print(r)


@tag.command("list")
@need_connection
def tag_list():
    r = get_tags()
    if not r["ok"]:
        exit(1)
    print(r["tags"])


@tag.command("edit")
@need_connection
def tag_edit():
    pass


@tag.command("delete")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def tag_delete(id_):
    r = delete_monitor(id_)
    print(r)


@cli.group()
def notification():
    pass


@notification.command("list")
@need_connection
@wait_for_event("notificationList")
def notification_list():
    print(initial_data["notificationList"])


@notification.command("add")
@click.argument("name", type=str)
@click.argument("type_", metavar="type".upper(), type=str)
@click.argument("default", type=str)
@click.option("--telegram_bot_token", type=str, help="Telegram Bot Token")
@click.option("--telegram_chat_id", type=str, help="Telegram Chat ID")
@need_connection
def notification_add(
        name, type_, default,
        telegram_bot_token, telegram_chat_id
):
    r = add_notification(
        name, type_, default,
        telegram_bot_token=telegram_bot_token, telegram_chat_id=telegram_chat_id
    )
    print(r)


@notification.command("edit")
@click.argument("name", type=str)
@click.argument("type_", metavar="type".upper(), type=str)
@click.argument("default", type=str)
@click.option("--telegram_bot_token", type=str, help="Telegram Bot Token")
@click.option("--telegram_chat_id", type=str, help="Telegram Chat ID")
@need_connection
def notification_edit(
        name, type_, default,
        telegram_bot_token, telegram_chat_id
):
    r = edit_notification(
        name, type_, default,
        telegram_bot_token=telegram_bot_token, telegram_chat_id=telegram_chat_id
    )
    print(r)


@notification.command("delete")
@click.argument("id_", metavar="id".upper(), type=int)
@need_connection
def notification_delete(id_):
    r = delete_notification(id_)
    print(r)


@cli.group()
def proxy():
    pass


@proxy.command("list")
@need_connection
@wait_for_event("proxyList")
def proxy_list():
    print(initial_data["proxyList"])


@proxy.command("add")
@need_connection
def proxy_add():
    r = add_proxy()
    print(r)


@cli.command("info")
@need_connection
@wait_for_event("info")
def info():
    print(initial_data["info"])


@cli.group()
def statuspage():
    pass


@statuspage.command("list")
@need_connection
@wait_for_event("statusPageList")
def statuspage_list():
    print(initial_data["statusPageList"])


@cli.group()
def heartbeat():
    pass


@heartbeat.command("list")
@need_connection
@wait_for_event("heartbeatList")
def heartbeat_list():
    print(initial_data["heartbeatList"])


@heartbeat.command("listimportant")
@need_connection
@wait_for_event("importantHeartbeatList")
def heartbeat_list_important():
    print(initial_data["importantHeartbeatList"])


@heartbeat.command("get")
@need_connection
@wait_for_event("heartbeat")
def heartbeat_get():
    print(initial_data["heartbeat"])


@cli.command("avgping")
@need_connection
@wait_for_event("avgPing")
def avgping():
    print(initial_data["avgPing"])


@cli.command("uptime")
@need_connection
@wait_for_event("uptime")
def uptime():
    print(initial_data["uptime"])


@cli.group()
def clear():
    pass


@clear.command("events")
@need_connection
def clear_events():
    r = socket_clear_events()
    print(r)


@clear.command("heartbeats")
@need_connection
def clear_heartbeats():
    r = socket_clear_heartbeats()
    print(r)


@clear.command("statistics")
@need_connection
def clear_statistics():
    r = socket_clear_statistics()
    print(r)


@cli.group()
def settings():
    pass


@settings.command("get")
@need_connection
def settings_get():
    r = socket_settings_get()
    print(r)


@settings.command("set")
@click.argument("data", type=str)
@click.argument("password", type=str)
@need_connection
def settings_set(data, password):
    r = socket_settings_set(data, password)
    print(r)


@settings.command("changepassword")
@click.argument("oldpass", type=str)
@click.argument("newpass", type=str)
@need_connection
def settings_changepassword(oldpass, newpass):
    r = socket_change_password(oldpass, newpass)
    print(r)


@cli.group()
def monitortag():
    pass


@monitortag.command("add")
@click.argument("tag_id", type=str)
@click.argument("monitor_id", type=str)
@click.argument("value", type=str)
@need_connection
def monitortag_add(tag_id, monitor_id, value):
    r = add_monitor_tag(tag_id, monitor_id, value)
    print(r)


@monitortag.command("edit")
@click.argument("tag_id", type=str)
@click.argument("monitor_id", type=str)
@click.argument("value", type=str)
@need_connection
def monitortag_edit(tag_id, monitor_id, value):
    r = edit_monitor_tag(tag_id, monitor_id, value)
    print(r)


@monitortag.command("delete")
@click.argument("tag_id", type=str)
@click.argument("monitor_id", type=str)
@click.argument("value", type=str)
@need_connection
def monitortag_delete(tag_id, monitor_id, value):
    r = delete_monitor_tag(tag_id, monitor_id, value)
    print(r)


@cli.result_callback()
def process_result(result, **kwargs):
    sio.disconnect()


if __name__ == "__main__":
    cli()
