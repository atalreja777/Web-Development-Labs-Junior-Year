from flask import Flask, render_template, redirect, url_for
import random

app = Flask(__name__)
app.debug = True

@app.route('/')
@app.route('/ask')
def ask():
    num = random.randint(1, 3)
    if num == 1:
        return redirect(url_for('yes'))
    elif num == 2:
        return redirect(url_for('no'))
    else:
        return redirect(url_for('maybe'))

@app.route('/yes')
def yes():
    return render_template('yes.html')

@app.route('/no')
def no():
    return render_template('no.html')

@app.route('/maybe')
def maybe():
    return render_template('maybe.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
