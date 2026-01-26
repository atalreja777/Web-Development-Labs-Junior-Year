import sqlite3
from flask import Flask, render_template, request, redirect, url_for

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


@app.route('/hero/<int:c_id>')
def hero(c_id):
    conn = get_db_connection()
    character_data = conn.execute(
        "SELECT * FROM characters WHERE c_id = ?",
        (c_id,)
    ).fetchall()
    conn.close()

    return render_template("hero.html", characters=character_data)



@app.route('/updating_smth', methods=['POST', 'GET'])
def updating_smth():
    
    if request.method == 'GET':
        return redirect('/')

    c_id = request.form.get('c_id')
    curr_n_streng = request.form.get('f_strength')
    n_streng = int(curr_n_streng)

    conn = get_db_connection()
    cur = conn.cursor()
    q_chosen_tp_do= "UPDATE characters SET c_strength = ? WHERE c_id = ?"
    cur.execute(q_chosen_tp_do, (n_streng, c_id))
    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)