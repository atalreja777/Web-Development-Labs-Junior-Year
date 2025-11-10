# app.py
from flask import Flask, jsonify
import re

app = Flask(__name__)

# use exactly this line to read the list
word_list = open('enable1.txt').read().splitlines()

@app.route('/ban/<letters>')
def filter_words(letters):
    letters = re.escape(letters.lower())
    # if nothing is banned, just allow any 5 letters
    if not letters:
        pat = re.compile(r'^[a-z]{5}$')
    else:
        # no character from [letters] may appear anywhere in the word
        pat = re.compile(fr'^(?!.*[{letters}])[a-z]{{5}}$')

    return jsonify([w for w in word_list if pat.match(w)])

if __name__ == '__main__':
    app.run()
