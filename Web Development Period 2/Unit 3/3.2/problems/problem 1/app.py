from flask import Flask, render_template

app = Flask(__name__)


page_visits = 0

@app.route('/')
def index():
    global page_visits
    page_visits += 1  
    return render_template('foo.html', number_pagevisits=page_visits)
app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
