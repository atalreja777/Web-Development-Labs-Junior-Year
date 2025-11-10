from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def root_page():
    return render_template('index.html')

@app.route('/get_schedule_from_ion')
def get_schedule_from_ion():

    url = "https://ion.tjhsst.edu/api/schedule/2016-04-12?format=json"
    response = requests.get(url)

    return response.json()
 
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    