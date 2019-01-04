import random 
from flask import Flask, render_template, request, redirect, session
app =  Flask(__name__)
app.secret_key = "must be secret"


@app.route("/")
def index():
    if "times" in session:
        session["times"] += 1
        print (session['times'])
    else: 
        session['times'] = 1
        print("no session keys exists yet")
    return render_template("index.html")

@app.route("/destroy_session") #it matters to capitalize this 'post' in Python, but not in html
def destroy():
    session.clear()
    return redirect("/")

@app.route("/clear", methods = ['POST']) #it matters to capitalize this 'post' in Python, but not in html
def clear():
    session.clear()
    return redirect("/")

@app.route("/addthree", methods = ['POST'])
def addthree():
    session['times'] += 2
    return redirect("/")

@app.route("/increment", methods = ['POST'])
def increment():
    session['incre'] = request.form['increment']
    session['times'] += int(session['incre']) - 1
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)

