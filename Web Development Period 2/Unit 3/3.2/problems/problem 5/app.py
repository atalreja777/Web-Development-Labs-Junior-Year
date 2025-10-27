from flask import Flask, render_template, url_for, redirect
import random

app = Flask(__name__)
app.debug = True

numwins = 0
numlosses = 0

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/gamble')
def gamble():
    global numwins, numlosses
    outcome = random.randint(0, 1)
    if outcome == 1:
        numwins += 1
        return render_template('win.html', wins=numwins)
    else:
        numlosses += 1
        return render_template('lose.html')

@app.route('/stats')
def stats():
    return render_template('stats.html', wins=numwins, losses=numlosses)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
