from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib

app = Flask(__name__)
app.secret_key = "abc123"

with open('credentials.json', 'r') as file:
    credentials = json.load(file)
    
def using_hashlib(test_string):
    b_teststring = test_string.encode('utf-8') 
    sha_obj = hashlib.sha256()                 
    sha_obj.update(b_teststring)               
    hashed_val = sha_obj.hexdigest()            
    return hashed_val

@app.route("/")
def home():
    l_in = session.get("logged_in", False)
    user = session.get("user", "")
    return render_template("home.html", logged_in=l_in, username=user)

@app.route("/login", methods=["POST"])
def login():
    user= request.form.get("username", "")
    password = request.form.get("password", "")

    hashedPwrd= using_hashlib(password)
    storred = credentials.get(user)

    if storred != None and storred == hashedPwrd:
        session["logged_in"] = True
        session["user"] = user
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
    