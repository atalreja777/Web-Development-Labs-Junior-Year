from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/roll', methods=['POST'])
def roll_from_form():
    # read inputs from the form
    sides_raw = request.form.get('sides', '')
    dice_raw = request.form.get('dice', '1')

    # validate they are ints
    try:
        sides = int(sides_raw)
        dice = int(dice_raw)
    except ValueError:
        return render_template('invalid.html')

    # reuse the param route (keeps logic in one place)
    return redirect(url_for('roll', num_sides=sides, num_dice=dice))

@app.route('/roll/<int:num_sides>')
@app.route('/roll/<int:num_sides>/<int:num_dice>')
def roll(num_sides, num_dice=1):
    # bounds check (minimal, as required)
    if num_sides < 2 or num_dice < 1 or num_dice > 20:
        return render_template('invalid.html')

    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    return render_template('roll.html', sides=num_sides, dice=num_dice, rolls=rolls)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
