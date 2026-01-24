from flask import Flask, render_template, request, redirect, url_for, session
import time

app = Flask(__name__)
app.secret_key = "escape-room-secret"

TIME_LIMIT_SECONDS = 300

def get_time_info():
    if "start_time" not in session:
        return 0, TIME_LIMIT_SECONDS
    elapsed = int(time.time() - session["start_time"])
    remaining = max(0, TIME_LIMIT_SECONDS - elapsed)
    return elapsed, remaining

def get_locks():
    locks = session.get("locks")
    if locks is None:
        locks = {"piano": False, "memory": False, "rebus": False, "connections": False}
        session["locks"] = locks
    return locks

def time_guard():
    elapsed, remaining = get_time_info()
    if session.get("game_started") != True:
        return False, elapsed, remaining
    if remaining <= 0:
        return False, elapsed, remaining
    return True, elapsed, remaining


CONN_ITEMS = [
    {"id": "coffee", "file": "coffee.png"},
    {"id": "tea", "file": "tea.png"},
    {"id": "soda", "file": "soda.png"},
    {"id": "guitar", "file": "guitar.png"},
    {"id": "piano", "file": "piano.png"},
    {"id": "drums", "file": "drums.png"},
    {"id": "hat", "file": "hat.png"},
    {"id": "shirt", "file": "shirt.png"},
    {"id": "shoe", "file": "shoe.png"},
    {"id": "sun", "file": "sun.png"},
    {"id": "moon", "file": "moon.png"},
    {"id": "star", "file": "star.png"},
]


@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return render_template(
                "game.html",
                started=False,
                error="Type your name to start.",
                locks=get_locks(),
                time_limit=TIME_LIMIT_SECONDS,
                game_started=session.get("game_started", False),
                conn_items=CONN_ITEMS,
                final_error=None,
                start_time=session.get("start_time"),
            )

        session.clear()
        session["player_name"] = name
        session["start_time"] = time.time()
        session["game_started"] = True
        session["locks"] = {"piano": False, "memory": False, "rebus": False, "connections": False}
        session.modified = True
        return redirect(url_for("game"))

    return render_template(
        "game.html",
        started=False,
        error=None,
        locks=get_locks(),
        time_limit=TIME_LIMIT_SECONDS,
        game_started=session.get("game_started", False),
        conn_items=CONN_ITEMS,
        final_error=None,
        start_time=session.get("start_time"),
    )


@app.route("/game")
def game():
    if session.get("game_started") != True:
        return redirect(url_for("start"))

    ok, elapsed, remaining = time_guard()
    if not ok:
        return redirect(url_for("game_over"))

    locks = get_locks()

    final_error = None
    if request.args.get("final") == "bad":
        final_error = "Wrong code."

    return render_template(
        "game.html",
        started=True,
        error=None,
        locks=locks,
        time_limit=TIME_LIMIT_SECONDS,
        game_started=session.get("game_started", False),
        conn_items=CONN_ITEMS,
        final_error=final_error,
        start_time=session.get("start_time"),
    )




@app.route("/piano", methods=["GET", "POST"])
def piano():
    if session.get("game_started") != True:
        return redirect(url_for("start"))

    ok, elapsed, remaining = time_guard()
    if not ok:
        return redirect(url_for("game_over"))

    locks = get_locks()

    if request.method == "POST":
        locks["piano"] = True
        session["locks"] = locks
        session.modified = True
        return redirect(url_for("game"))

    return render_template("piano.html", locks=locks, time_limit=TIME_LIMIT_SECONDS, game_started=session.get("game_started", False), start_time=session.get("start_time"))

@app.route("/memory", methods=["GET", "POST"])
def memory():
    if session.get("game_started") != True:
        return redirect(url_for("start"))

    ok, elapsed, remaining = time_guard()
    if not ok:
        return redirect(url_for("game_over"))

    locks = get_locks()
    if not locks.get("piano"):
        return redirect(url_for("piano"))

    if request.method == "POST":
        locks["memory"] = True
        session["locks"] = locks
        session.modified = True
        return redirect(url_for("game"))

    return render_template("memory.html", locks=locks, time_limit=TIME_LIMIT_SECONDS, game_started=session.get("game_started", False), start_time=session.get("start_time"))

@app.route("/rebus", methods=["GET", "POST"])
def rebus():
    if session.get("game_started") != True:
        return redirect(url_for("start"))

    ok, elapsed, remaining = time_guard()
    if not ok:
        return redirect(url_for("game_over"))

    locks = get_locks()
    if not locks.get("memory"):
        return redirect(url_for("memory"))

    error = None
    if request.method == "POST":
        ans = request.form.get("rebus_answer", "").strip().lower()
        if ans == "connections":
            locks["rebus"] = True
            session["locks"] = locks
            session.modified = True
            return redirect(url_for("game"))
        else:
            error = "Wrong answer."

    return render_template("riddle.html", locks=locks, time_limit=TIME_LIMIT_SECONDS, game_started=session.get("game_started", False), error=error, start_time=session.get("start_time"))

@app.route("/connections", methods=["GET", "POST"])
def connections():
    if session.get("game_started") != True:
        return redirect(url_for("start"))

    ok, elapsed, remaining = time_guard()
    if not ok:
        return redirect(url_for("game_over"))

    locks = get_locks()
    if not locks.get("rebus"):
        return redirect(url_for("rebus"))

    if request.method == "POST":
        locks["connections"] = True
        session["locks"] = locks
        session.modified = True
        return redirect(url_for("game"))

    return render_template("connections.html", locks=locks, time_limit=TIME_LIMIT_SECONDS, game_started=session.get("game_started", False), conn_items=CONN_ITEMS, start_time=session.get("start_time"))

@app.route("/escape_check", methods=["POST"])
def escape_check():
    if session.get("game_started") != True:
        return redirect(url_for("start"))

    ok, elapsed, remaining = time_guard()
    if not ok:
        return redirect(url_for("game_over"))

    locks = get_locks()
    if locks.get("connections") != True:
        return redirect(url_for("game"))

    code = request.form.get("final_code", "").strip()
    if code == "4531":
        return redirect(url_for("victory"))
    return redirect(url_for("game", final="bad"))

@app.route("/victory")
def victory():
    if session.get("game_started") != True:
        return redirect(url_for("start"))

    elapsed, remaining = get_time_info()
    locks = get_locks()
    if locks.get("connections") != True:
        return redirect(url_for("game"))
    if remaining <= 0:
        return redirect(url_for("game_over"))

    return render_template(
        "victory.html",
        elapsed=elapsed,
        time_limit=TIME_LIMIT_SECONDS,
        game_started=session.get("game_started", False),
        start_time=session.get("start_time"),
    )

@app.route("/game_over")
def game_over():
    elapsed, remaining = get_time_info()
    return render_template(
        "game_over.html",
        elapsed=elapsed,
        time_limit=TIME_LIMIT_SECONDS,
        game_started=session.get("game_started", False),
        start_time=session.get("start_time"),
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("start"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
