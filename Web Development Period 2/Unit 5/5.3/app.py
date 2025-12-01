from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib

app = Flask(__name__)
app.secret_key = "abc123"

with open('credentials.json', 'r') as file:
    credentials = json.load(file)

def using_hashlib(test_string):
    b_teststring = test_string.encode('utf-8')  # encoded to a bytestring
    sha_obj = hashlib.sha256()                  # Create a sha256 hash object
    sha_obj.update(b_teststring)                # pass the string to the hash object
    hashed_val = sha_obj.hexdigest()            
    return hashed_val

@app.route("/")
def home():
    logged_in = session.get("logged_in", False)
    username = session.get("user", "")
    return render_template("home.html", logged_in=logged_in, username=username)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    hashedPwrd = using_hashlib(password)
    stored = credentials.get(username)

    if stored != None and stored == hashedPwrd:
        session["logged_in"] = True
        session["user"] = username
        return redirect(url_for("home"))
    else:
        return redirect("/?success=false")

@app.route("/premiumcontent")
def premiumcontent():
    if session.get("logged_in") != True:
        return redirect("/?auth_error=true")
    usr_nm = session.get("user","")
    return render_template("premium.html", usr_nm=usr_nm)

@app.route("/logout")
def logout():
    session.clear()
    