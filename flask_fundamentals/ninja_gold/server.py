import random 
from datetime import datetime, date, time
from flask import Flask, render_template, request, redirect, session
app =  Flask(__name__)
app.secret_key = "super secret"

@app.route("/")
def index():

    if 'building' not in session:
        session['building'] = {}
    if 'gold' not in session:
        session['gold'] = 0
        print(session['gold'])
    if 'activities' not in session:
        session['activities'] = []
    return render_template("index.html")

@app.route("/process_money", methods = ['POST'])
def process_money():
    print("***********")
    request.form['building']
    print(request.form)
    if request.form['building'] == "farm":
        x = random.randint(10,20)
        session['gold'] += x
        session['activities'].append("Earned " + str(x) + " golds from the farm (" + str(datetime.now().strftime("%B %Y %I:%M%p") +")"))
    elif request.form['building'] == "cave":
        y = random.randint(5,10)
        session['gold'] += y
        session['activities'].append("Earned " + str(y) + " golds from the cave (" + str(datetime.now().strftime("%B %Y %I:%M%p") +")"))
    elif request.form['building'] == "house":
        z = random.randint(2,5)
        session['gold'] += z
        session['activities'].append("Earned " + str(z) + " golds from the house (" + str(datetime.now().strftime("%B %Y %I:%M%p") +")"))
    elif request.form['building'] == "casino":
        w = random.randint(-50,50)
        session['gold'] += w
        if w<0:
            session['activities'].append("Entered a casino and lost " + str(w) + " golds...Ouch (" + str(datetime.now().strftime("%B %Y %I:%M%p") +")"))
        else:
            session['activities'].append("Earned " + str(w) + " golds from the casino (" + str(datetime.now().strftime("%B %Y %I:%M%p") +")"))

    return redirect("/")
@app.route("/reset", methods = ['POST'])
def reset():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)