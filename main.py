import json
from tinytuya.wizard import tuyaPlatform
import time

json_data = json.loads(open('config.json').read())

REGION = json_data.get('apiRegion')
CLIENT_ID = json_data.get('apiKey')
SECRET = json_data.get('apiSecret')
DEVICE_ID = json_data.get('apiDeviceID')

# get oauth token


def readable_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def log(*args, **kwargs):
    args = [f'{readable_timestamp()} -', *args]
    print(*args, **kwargs)


def get_oauth():
    data = tuyaPlatform(REGION, CLIENT_ID, SECRET, 'token?grant_type=1')

    if data['success'] is False:
        log('Error:', data['error'])
        exit()

    token = data['result']['access_token']

    return token


def monitor():
    token = None
    prev_status = None
    while True:
        request_success = False

        while request_success is False:
            uri = f'devices/{DEVICE_ID}/status'
            data = tuyaPlatform(REGION, CLIENT_ID, SECRET, uri, token)

            if data['success'] is False:
                log("Authentication failed, fetching new oauth token")
                request_success = False
                token = get_oauth()
            else:
                request_success = True

        contact_status = data['result'][0]['value']
        battery_level = data['result'][1]['value']

        assert type(contact_status) == bool
        assert type(battery_level) == str

        readable_status = 'open' if contact_status else 'closed'

        if prev_status != readable_status:
            with open('status_log', 'a') as status_file:
                status_file.write(f"{readable_timestamp()}, {readable_status}\n")

            with open('current_status', 'w') as status_file:
                status_file.write(f"{readable_timestamp()}, {readable_status}")

            log(readable_status)
            prev_status = readable_status

        time.sleep(60)


if __name__ == '__main__':
    monitor()
