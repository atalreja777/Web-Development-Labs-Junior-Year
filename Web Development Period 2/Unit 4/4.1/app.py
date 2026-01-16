from flask import Flask, jsonify, render_template

app = Flask(__name__)

votesup = 0
votesdown = 0
app.debug = True


@app.route('/')
def index():
    return render_template('countingvotes.html')


@app.route('/votingupward')
def votingupward():
    global votesup
    votesup += 1
    return jsonify({'upvote': votesup, 'downvote': votesdown})


@app.route('/votingdownward')
def votingdownward():
    global votesdown
    votesdown += 1
    return jsonify({'upvote': votesup, 'downvote': votesdown})


@app.route('/total')
def total():
    return jsonify({'upvote': votesup, 'downvote': votesdown})


if __name__ == '_main_':
   app.run(host='127.0.0.1', port=3000)