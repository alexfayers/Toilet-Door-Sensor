from flask import Flask
from flask import render_template

from calculations import calc_average_minutes
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

    if status == "open":
        status = "No"
        color = "status-0"
        subtext = "You can probably use it"
        wait_message = f"Average in-use time: {average_wait} minutes"
    elif status == "closed":
        previous_prediction = None
        future_timestamp = timestamp + timedelta(minutes=average_wait)
        wait_info = ""

        while datetime.now() > future_timestamp:
            wait_info = f" (for usages longer than {average_wait} minutes)"
            average_wait = calc_average_minutes('../status_log', min_diff=60*average_wait)
            future_timestamp = timestamp + timedelta(minutes=average_wait)

            if future_timestamp == previous_prediction:
                break
            else:
                previous_prediction = future_timestamp

        status = "Yes"
        color = "status-4"
        subtext = "You can try to use it but it might be awkward"

        wait_message = f"Predicted wait time: {average_wait} minutes{wait_info}"
        wait_message += f" (probably free at like <b>{future_timestamp.strftime('%H:%M')}</b>)"

    minutes_ago = f" - {int((datetime.now() - timestamp).total_seconds() // 60)} minutes ago"

    
    return render_template('index.jinja.html', status=status, color=color, subtext=subtext, timestamp=timestamp.strftime('%H:%M'), wait_message=wait_message, minutes_ago=minutes_ago)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)