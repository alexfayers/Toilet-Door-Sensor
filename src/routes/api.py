from flask import Blueprint
from src.helper.calculations import calc_average_minutes
from datetime import datetime, timedelta
from os.path import join as path_join
from config import DATA_DIRECTORY


api = Blueprint('api', __name__)


@api.route("/api/current")
def current_status():
    with open(path_join(DATA_DIRECTORY, 'current_status'), 'r') as status_file:
        status = status_file.read()

    status = status.split(', ')
    timestamp = status[0].strip()
    status = status[1].strip()

    # return the data as a json object
    return {
        "timestamp": timestamp,
        "status": status
    }


@api.route("/api/current_full")
def current_status_full():
    with open(path_join(DATA_DIRECTORY, 'current_status'), 'r') as status_file:
        status = status_file.read()

    timestamp = status.split(', ')[0]
    status = status.split(', ')[1]

    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    average_wait = calc_average_minutes(path_join(DATA_DIRECTORY, 'status_log'))

    time_ago = (datetime.now() - timestamp).total_seconds()
    time_ago_text = 'seconds'
    if time_ago > 60:
        time_ago = time_ago / 60
        time_ago_text = 'minutes'
        if time_ago > 60:
            time_ago = time_ago / 60
            time_ago_text = 'hours'
            if time_ago > 24:
                time_ago = time_ago / 24
                time_ago_text = 'days'

    output = {
        'status': 'No',
        'color': 'status-0',
        'subtext': 'You can probably use it',
        'timestamp': timestamp.strftime('%H:%M'),
        'wait_message':  f"Average in-use time: {average_wait} minutes",
        'minutes_ago': f' - {int(time_ago)} {time_ago_text} ago',
    }

    if status == "closed":  # (and status != "open")
        previous_prediction = None
        future_timestamp = timestamp + timedelta(minutes=average_wait)
        wait_info = ""

        while datetime.now() > future_timestamp:
            wait_info = f" (for usages longer than {average_wait} minutes)"
            average_wait = calc_average_minutes(
                path_join(DATA_DIRECTORY, 'status_log'), min_diff=60*average_wait)
            future_timestamp = timestamp + timedelta(minutes=average_wait)

            if future_timestamp == previous_prediction:
                break
            else:
                previous_prediction = future_timestamp

        output['status'] = "Yes"
        output['color'] = "status-4"
        output['subtext'] = "You can try to use it but it might be awkward"

        wait_message = f"Predicted wait time: {average_wait} minutes{wait_info}"
        wait_message += f" (probably free at like <b>{future_timestamp.strftime('%H:%M')}</b>)"
        output['wait_message'] = wait_message

    return output
