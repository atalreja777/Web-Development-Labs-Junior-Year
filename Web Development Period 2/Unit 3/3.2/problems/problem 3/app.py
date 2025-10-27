from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.debug = True

@app.route('/')
def root():
    return redirect(url_for('dogs'))

@app.route('/dogs')
def dogs():
    return render_template('dogs.html')

@app.route('/cats')
def cats():
    return render_template('cats.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
