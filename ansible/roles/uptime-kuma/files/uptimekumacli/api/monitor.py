from uptimekumacli.data import MonitorType, AuthMethod
from uptimekumacli.events import sio

__all__ = ["get_monitor", "add_monitor", "edit_monitor", "pause_monitor", "resume_monitor", "delete_monitor", "get_monitor_beats"]


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


def pause_monitor(id_):
    return sio.call('pauseMonitor', id_)


def resume_monitor(id_):
    return sio.call('resumeMonitor', id_)


def delete_monitor(id_):
    return sio.call('deleteMonitor', id_)


def get_monitor_beats(id_, period):
    return sio.call('getMonitorBeats', (id_, period))
