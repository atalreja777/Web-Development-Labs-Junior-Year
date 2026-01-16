from flask import Flask, render_template, jsonify, request
import re

app = Flask(__name__)
words = set(open('enable1.txt').read().splitlines())

@app.route("/")
def index():
    num_blocks = 30
    return render_template("index.html", num_blocks=range(1, num_blocks + 1))

@app.route("/get-words")
def get_words():
    args = request.args.items()
    info_dict = {1: [], 2: [], 3: [], 4: [], 5: [], "possibles": [], "impossibles": []}

    for index, letter_and_color in args:
        letter, color = letter_and_color.split(",")
        letter = letter.lower()
        if letter == "" or color == "none":
            continue
        real_index = int(index) % 5
        if real_index == 0:
            real_index = 5
        if color == "green":
            info_dict[real_index].append(letter)
            if len(info_dict[real_index]) != 1:
                return {"error": "invalid; two letters appear to be green for the same index"}
        elif color == "yellow":
            info_dict["possibles"].append(letter)
            info_dict["impossibles"].append((real_index, letter))
        elif color == "gray":
            info_dict["impossibles"].append((-1, letter))

    valid_words = set()

    for word in words:
        w = word.lower()
        if len(w) != 5:
            continue
        invalid = False
        for i in range(1, 6):
            if info_dict[i] and w[i-1] != info_dict[i][0]:
                invalid = True
                break
        if invalid:
            continue
        for idx, letter in info_dict["impossibles"]:
            if idx != -1 and w[idx-1] == letter:
                invalid = True
                break
        if invalid:
            continue
        for letter in info_dict["possibles"]:
            if letter not in w:
                invalid = True
                break
        if invalid:
            continue
        for idx, letter in info_dict["impossibles"]:
            if idx == -1:
                if letter not in info_dict["possibles"] and letter not in [info_dict[i][0] for i in range(1,6) if info_dict[i]]:
                    if letter in w:
                        invalid = True
                        break
        if invalid:
            continue
        valid_words.add(word)

    return jsonify(list(valid_words))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
