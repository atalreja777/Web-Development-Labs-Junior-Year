import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    character_data = conn.execute("SELECT * FROM characters").fetchall()
    conn.close()

    return render_template("characters.html", characters=character_data)


@app.route('/hero/<c_id>')
def hero(c_id):
    conn = get_db_connection()
    character_data = conn.execute("SELECT * FROM characters WHERE c_id = ?",(c_id,)).fetchall()
    conn.close()

    return render_template("hero.html", characters=character_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
