import json
import time
from datetime import datetime
import os

from tuya_iot import TuyaOpenAPI, TuyaOpenMQ
from config import (
    DATA_DIRECTORY,
    CONFIG_JSON,
    DEBUG_MODE
)


def readable_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def log(*args, **kwargs):
    args = [f'{readable_timestamp()} -', *args]
    print(*args, **kwargs)


def on_message(msg, target_device_id):
    print(msg)
    data = msg.get('data', {})
    device_id = data.get('devId', None)
    if device_id is None:
        return
    if device_id != target_device_id:
        return

    status = data.get('status', [])
    if len(status) == 0:
        return
    status = status[0]
    if status.get('code', '') != 'doorcontact_state':
        return
    state = status.get('value', '')
    update_time = status.get('t', '0')
    update_time = int(update_time)
    if update_time == 0:
        return
    update_time = datetime.fromtimestamp(update_time)

    # if state is True, door is open
    print(f"{device_id} - {state} - {update_time}")

    readable_status = 'open' if state else 'closed'

    with open('status_log', 'a') as status_file:
        status_file.write(f"{readable_timestamp()}, {readable_status}\n")

    with open('current_status', 'w') as status_file:
        status_file.write(f"{readable_timestamp()}, {readable_status}")

    log(readable_status)


def monitor():
    if DEBUG_MODE is True:
        from tuya_iot import TUYA_LOGGER
        import logging
        TUYA_LOGGER.setLevel(logging.DEBUG)

    if not os.path.exists(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY)

    if not os.path.exists(CONFIG_JSON):
        log("Config file not found")
        exit(1)

    with open(CONFIG_JSON) as config_file:
        json_data = json.load(config_file)

    REGION = json_data.get('apiRegion')
    CLIENT_ID = json_data.get('apiKey')
    SECRET = json_data.get('apiSecret')
    DEVICE_ID = json_data.get('apiDeviceID')
    USERNAME = json_data.get('apiUsername')
    PASSWORD = json_data.get('apiPassword')

    ENDPOINT = f"https://openapi.tuya{REGION}.com"

    log("Config loaded")

    # Initialization of Tuya OpenAPI
    openapi = TuyaOpenAPI(ENDPOINT, CLIENT_ID, SECRET)
    res = openapi.connect(USERNAME, PASSWORD, REGION, "smartlife")
    if res.get('success', False) is False:
        log("Connection failed")
        exit(1)

    # Receive device messages

    openmq = TuyaOpenMQ(openapi)
    openmq.start()
    openmq.add_message_listener(lambda message: on_message(message, DEVICE_ID))
    log("Listening for messages...")


if __name__ == '__main__':
    monitor()
