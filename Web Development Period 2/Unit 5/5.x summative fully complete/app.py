from flask import Flask, render_template, request, redirect, url_for, session
import time

# flask setup
app = Flask(__name__)
app.secret_key = "escape-room-secret"

TIME_LIMIT_SECONDS = 300

# helper functions
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

# time check, we run this on every req
def time_guard():
    elapsed, remaining = get_time_info()
    if session.get("game_started") != True:
        return False, elapsed, remaining
    if remaining <= 0:
        return False, elapsed, remaining
    return True, elapsed, remaining

# game data
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
    {"id": "star", "file": "star.png"},  # ezier to change during debug
]

# routes
@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return render_template("start.html", error="Type your name to start.")

        session.clear()
        session["player_name"] = name
        session["start_time"] = time.time()
        session["game_started"] = True
        session["locks"] = {"piano": False, "memory": False, "rebus": False, "connections": False}
        session.modified = True
        return redirect(url_for("game"))

    return render_template("start.html", error=None)


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

    return render_template("game.html", locks=locks, final_error=final_error)




# piano room
@app.route("/piano", methods=["GET", "POST"])
def piano():
    if session.get("game_started") != True:
        return redirect(url_for("start"))

    ok, elapsed, remaining = time_guard()
    if not ok:
        return redirect(url_for("game_over"))

    locks = get_locks()
    error = None

    if request.method == "POST":
        piano_answer = request.form.get("piano_answer", "").strip().upper()
        if piano_answer == "A":
            locks["piano"] = True
            session["locks"] = locks
            session.modified = True
            return redirect(url_for("game"))
        else:
            error = "Wrong note. Try counting: C, D, E, F, G, A, B, C, D, E, F, G, A..."

    return render_template("piano.html", locks=locks, time_limit=TIME_LIMIT_SECONDS, game_started=session.get("game_started", False), start_time=session.get("start_time"), error=error)

# memory room
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
        final_code = request.form.get("final_code", "").strip().upper()
        if final_code == "MUSEUM":
            locks["memory"] = True
            session["locks"] = locks
            session.modified = True
            return redirect(url_for("game"))
        else:
            return render_template("memory.html", locks=locks, time_limit=TIME_LIMIT_SECONDS, game_started=session.get("game_started", False), start_time=session.get("start_time"), error="Incorrect code.")

    return render_template("memory.html", locks=locks, time_limit=TIME_LIMIT_SECONDS, game_started=session.get("game_started", False), start_time=session.get("start_time"))

# riddle room
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

# connections room
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

# final escape
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

# win screen
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

    return render_template("victory.html", elapsed=elapsed, time_limit=TIME_LIMIT_SECONDS, game_started=session.get("game_started", False), start_time=session.get("start_time"))

# lose screen
@app.route("/game_over")
def game_over():
    elapsed, remaining = get_time_info()
    return render_template("game_over.html", elapsed=elapsed, time_limit=TIME_LIMIT_SECONDS, game_started=session.get("game_started", False), start_time=session.get("start_time"))

# reset game
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("start"))

# run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
