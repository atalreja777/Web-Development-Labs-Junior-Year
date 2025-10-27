from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

tier_list = [
    'Galarian Stunfisk',
    'Wobbuffet',
    'Magikarp',
    'Throh',
    'Mega Charizard'
]

@app.route('/')
def show_tier_list():
    return render_template('tierlist.html', tier_list=tier_list)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
