from flask import Flask
from flask import render_template

from src.calculations import calc_average_minutes
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/')
def status():
    with open('../current_status', 'r') as status_file:
        status = status_file.read()

    timestamp = status.split(', ')[0]
    status = status.split(', ')[1]

    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    average_wait = calc_average_minutes('../status_log')

    output = {
        'status': 'No',
        'color': 'status-0',
        'subtext': 'You can probably use it',
        'timestamp': timestamp.strftime('%H:%M'),
        'wait_message':  f"Average in-use time: {average_wait} minutes",
        'minutes_ago': f" - {int((datetime.now() - timestamp).total_seconds() // 60)} minutes ago",
    }

    if status == "closed":  # (and status != "open")
        previous_prediction = None
        future_timestamp = timestamp + timedelta(minutes=average_wait)
        wait_info = ""

        while datetime.now() > future_timestamp:
            wait_info = f" (for usages longer than {average_wait} minutes)"
            average_wait = calc_average_minutes(
                '../status_log', min_diff=60*average_wait)
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

    return render_template(
        'index.jinja.html',
        output=output
    )


@app.route("/api/current")
def current_status():
    with open('../current_status', 'r') as status_file:
        status = status_file.read()

    status = status.split(', ')
    timestamp = status[0].strip()
    status = status[1].strip()

    # return the data as a json object
    return {
        "timestamp": timestamp,
        "status": status
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
