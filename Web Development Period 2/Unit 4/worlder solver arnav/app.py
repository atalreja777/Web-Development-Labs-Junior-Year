from flask import Flask, render_template, jsonify, request
import re  # not used for now:

app = Flask(__name__)
words = set(open('enable1.txt').read().splitlines())


@app.route("/")
def index():
    amount_blocks = 30
    return render_template("index.html", amount_blocks=range(1, amount_blocks + 1))


@app.route("/get-words/<path:index_color_letter_information>")
def get_words(index_color_letter_information):
   
    worlde_information = { "greens": {},"yellows": {},"grey_not_acceptable_values": set(),"part_of_wordle_word_set": set()}

    # if nothing in past remember we return a blank thing
    if not index_color_letter_information:
        return jsonify([])

    #remember the format of the incoming information is split byt index, letter, color, and each delimeter between is ; and: between each part
    sections = index_color_letter_information.split(";")
    for section in sections:
        if not section:
            continue

        parts = section.split(":")
        #if not t3 parts, we knmow this doesnt work so we just skip it with the use of contineu
        if len(parts) != 3:
            continue

        # remember this is parametric route ukwis
        index_string, leter, col = parts
        leter = leter.lower() #checks like make sure all is same
        col = col.lower() #color 

        if (leter == "" or leter == "_") or col == "none":
            continue
        #if letter or color not there, we just skip over this particular word
        tile_index = int(index_string) #remember it was a str befrore
        index_per_row = tile_index % 5
        ##if its 0 its the actual row 5
        if index_per_row == 0:
            index_per_row = 5
        if col == "green":
            if index_per_row in worlde_information["greens"]and worlde_information["greens"][index_per_row] != leter:
                # bro we already have one there, this means its a user error tnot error on you
                return { "error": "two letters green, but they have same positioning on board, so something you inputted must be wrong"}
            worlde_information["greens"][index_per_row] = leter #upadte that particular index
            worlde_information["part_of_wordle_word_set"].add(leter) #add that to part of the set, continue for a yellow and greay color

        elif col == "yellow":
            #we know if yellow this word should be smwhere in the word, maybe not at that secific pos
            if leter not in worlde_information["yellows"]:
                worlde_information["yellows"][leter] = set()
            worlde_information["yellows"][leter].add(index_per_row)
            worlde_information["part_of_wordle_word_set"].add(leter)

        elif col == "gray":
            #if grey it not in the world at all so put it in that according set ukwim saying
            worlde_information["grey_not_acceptable_values"].add(leter)

    gray_only_letters = (worlde_information["grey_not_acceptable_values"] - worlde_information["part_of_wordle_word_set"])
     
    words_possible = set()
    for word in words:
        wd = word.lower()
        if len(wd) != 5:
            continue
        not_valid_possibility = False
        for pos, leter in worlde_information["greens"].items():
            if wd[pos - 1] != leter:
                not_valid_possibility = True
                break
        if not_valid_possibility:
            continue
        for leter, bad_positions in worlde_information["yellows"].items():
            if leter not in wd:
                not_valid_possibility = True
                break
            for pos in bad_positions:
                if wd[pos - 1] == leter:
                    not_valid_possibility = True
                    break
            if not_valid_possibility:
                break
        if not_valid_possibility:
            continue
        for leter in gray_only_letters:
            if leter in wd:
                not_valid_possibility = True
                break
        if not_valid_possibility:
            continue
        words_possible.add(word)
    return jsonify(list(words_possible))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
