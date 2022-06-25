#!/usr/bin/env python3
import json
import click
import socketio
from enum import Enum

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


# @sio.event
# def monitorList(data):
#     print(f'monitorList:\n----\n{data}\n----\n')

# @sio.event
# def notificationList(data):
#     print(f'notificationList:\n----\n{data}\n----\n')

# @sio.event
# def proxyList(data):
#     print(f'proxyList:\n----\n{data}\n----\n')

# @sio.event
# def statusPageList(data):
#     print(f'statusPageList:\n----\n{data}\n----\n')

# @sio.event
# def heartbeatList(id, data, bool):
#     print(f'heartbeatList:\n----\n{id}\n{data}\n{bool}\n----\n')

# @sio.event
# def importantHeartbeatList(id, data, bool):
#     print(f'importantHeartbeatList:\n----\n{id}\n{data}\n{bool}\n----\n')

# @sio.event
# def avgPing(id, data):
#     print(f'avgPing:\n----\n{id}\n{data}\n----\n')

# @sio.event
# def uptime(id, hours_24, days_30):
#     print(f'uptime:\n----\n{id}\n{hours_24}\n{days_30}\n----\n')

# @sio.event
# def heartbeat(data):
#     print(f'heartbeat:\n----\n{data}\n----\n')

# @sio.event
# def info(data):
#     print(f'info:\n----\n{data}\n----\n')

# @sio.on('*')
# def catch_all(event, data):
#     print(f'UNHANDLED: {event}:\n----\n{data}\n----\n')

@sio.event
def disconnect():
    print('disconnected from server')


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
# editTag
# deleteTag
# editMonitorTag
# deleteMonitorTag
# changePassword
# getSettings
# setSettings
# checkApprise
# uploadBackup
# clearEvents
# clearHeartbeats
# clearStatistics

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


def get_tags():
    return sio.call('getTags')


def add_tag(color, name, value):
    return sio.call('addTag', {
        "color": color,
        "name": name,
        "value": value,
        "new": True
    })


def add_monitor_tag(tag_id, monitor_id, value):
    return sio.call('addMonitorTag', tag_id, monitor_id, value)


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
        name: str, type: NotificationType, default: bool,
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
    return sio.call('addNotification', data, None)


def edit_notification(id_: int, *args, **kwargs):
    data = build_notification_data(*args, **kwargs)
    return sio.call('addNotification', data, id_)


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


def add_monitor(
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

    print(json.dumps(data))
    return sio.call('add', data)


@click.group()
@click.option("--url", required=True, help="The uptime-kuma webinterface url. Example: http://192.168.20.160:3001/")
@click.option("--user", required=True, help="The uptime-kuma username.")
@click.option("--pass", "pass_", required=True, help="The uptime-kuma password.")
def cli(url, user, pass_):
    url = url.rstrip("/")
    sio.connect(f'{url}/socket.io/')
    login(user, pass_)


@cli.group()
def monitor():
    pass


@monitor.command("add")
@click.argument("type_", metavar="type".upper(), type=str)
@click.argument("name", type=str)
@click.option("--url", type=str, help="Monitor url.")
@click.option("--keyword", type=str, help="Monitor keyword.")
def monitor_add(type_, name, url, keyword):
    r = add_monitor(monitor_type=type_, friendly_name=name, url=url, keyword=keyword)
    print(r)


@monitor.command("pause")
@click.argument("id_", metavar="id".upper(), type=int)
def monitor_pause(id_):
    r = pause_monitor(id_)
    print(r)


@monitor.command("resume")
@click.argument("id_", metavar="ID", type=int)
def monitor_resume(id_):
    r = resume_monitor(id_)
    print(r)


@monitor.command("delete")
@click.argument("id_", metavar="ID", type=int)
def monitor_delete(id_):
    r = delete_monitor(id_)
    print(r)


@cli.result_callback()
def process_result(result, **kwargs):
    sio.disconnect()


if __name__ == "__main__":
    cli()
