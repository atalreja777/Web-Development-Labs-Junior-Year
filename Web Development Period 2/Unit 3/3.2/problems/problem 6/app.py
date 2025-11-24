from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
app.debug = True

log_allvisits = []
previous_visit = None


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/log')
def log_here():
    global previous_visit
    curr_time =datetime.now()
    if previous_visit is None:
        difference = None
    else:
        difference = int((curr_time - previous_visit).total_seconds())
    previous_visit = curr_time
    new_visit = {
        'ip': request.remote_addr,
        'agent':request.headers.get('User-Agent'),
        'time':curr_time.strftime('%Y-%m-%d %H:%M:%S'),
        'since_last':difference
    }

    log_allvisits.append(new_visit)
    return render_template('log.html',log=log_allvisits)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)
