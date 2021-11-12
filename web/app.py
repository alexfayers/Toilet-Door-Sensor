from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def status():
    with open('current_status', 'r') as status_file:
        status = status_file.read()

    timestamp = status.split(', ')[0]
    status = status.split(', ')[1]

    if status == "open":
        status = "No"
        color = "status-0"
        subtext = "You can probably use it"
    elif status == "closed":
        status = "Yes"
        color = "status-4"
        subtext = "You can try to use it but it might be awkward"
    
    return render_template('index.jinja.html', status=status, color=color, subtext=subtext, timestamp=timestamp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)