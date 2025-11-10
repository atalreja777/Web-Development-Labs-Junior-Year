
from flask import Flask, jsonify

app = Flask(__name__)

word_list = open('enable1.txt').read().splitlines()

lowercase_words = [w.strip().lower() for w in word_list]                 
length_five = [w for w in words_lower if w.isalpha() and len(w) == 5]  

@app.route('/ban/<letters>')
def ban_letters(letters):
    banned = set(letters.lower())
    res = []
    for w in words_5:
        works = True
        for c in w:
            if c in banned:  
                works = False
                break
        if works:
            res.append(w)

    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
