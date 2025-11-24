from flask import Flask, session, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = "thisisthesecretkey"


def init_user_state():
    session['user_state'] = {'visits': 0,'cars': 0,'cows': 0}
    session.modified = True


def create_or_retrieve():
    if 'user_state' not in session:
        init_user_state()
    return session['user_state']


@app.route('/')
def home():
    user_state = create_or_retrieve()
    user_state['visits'] += 1
    session.modified = True
    return render_template("home.html", data=user_state)


@app.route('/buycar')
def buy_car():
    user_state = create_or_retrieve()
    user_state['cars'] += 1
    session.modified = True
    return redirect(url_for("home"))


@app.route('/buycow')
def buy_cow():
    user_state = create_or_retrieve()
    user_state['cows'] += 1
    session.modified = True
    return redirect(url_for("home"))


@app.route('/clear')
def clear_all():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.debug = True
    app.run()
