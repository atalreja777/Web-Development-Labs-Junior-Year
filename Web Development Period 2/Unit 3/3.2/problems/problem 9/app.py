import random
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/roll/<int:num_sides>")
@app.route("/roll/<int:num_sides>/<int:num_dice>")
def roll(num_sides, num_dice=1):
    if num_sides < 2 or num_sides > 20 or num_dice < 1 or num_dice > 20:
        return render_template("invalid.html")
    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    return render_template(
        "roll.html",
        num_sides=num_sides,
        num_dice=num_dice,
        rolls=rolls,
    )

@app.route("/invalid")
def invalid():
    return render_template("invalid.html")


if __name__ == "__main__":
    app.run(debug=True)
