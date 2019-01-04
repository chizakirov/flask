import random 
from flask import Flask, render_template, request, redirect, session
app =  Flask(__name__)
app.secret_key = "shht terrible secret"

@app.route("/")
def index():
    if "message" not in session:
        session['message'] = ""
    if 'count' in session:
        session['count'] += 1
    else: 
        session['count'] = 0

    if 'computer' not in session:
        session['computer'] = random.randint(1,100)
        print(session['computer'])
        print("*******")

    if 'winner' not in session:
        session['winner'] = []
    else: 
        print(session['winner'])
    return render_template("index.html")

@app.route("/num", methods = ['POST'])
def num():
    print("**************")
    print(request.form)

    num = int(request.form['guess'])
    if num > session['computer']:
        session['message'] = "too high" 
        print(session['message'])
    elif num < session['computer']:
        session['message'] = "too low"
        print(session['message'])
    else:
        session['message'] = "correct"
        print(session['message'])

    return redirect("/")

@app.route("/reset", methods = ['POST'])
def reset():
    print("!!!!!!!!!")
    print(request.form)
    session.pop('message')
    session.pop('count')
    session.pop('computer')
    return redirect("/")

@app.route("/winnerboard", methods = ['POST'])
def winner():
    session['winner'].append(request.form['winnername'])
    listlength = len(session['winner'])
    return render_template("winner.html",length = listlength)

@app.route("/reset", methods = ['POST'])
def goback():
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True)