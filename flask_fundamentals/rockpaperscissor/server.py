
import random 
from flask import Flask, render_template, request, redirect, session
app =  Flask(__name__)
app.secret_key = 'anything'

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/result", methods = ['POST'])
def result():
    # print ("*"*40)
    # print(request.form)
    session['x'] = request.form['choice']
    session['computer'] = {'rock': {'rock':'tie','paper':"win","scissor":"lose"},
    "paper": {"rock": "lose", "paper":"tie","scissor":"win"},
    "scissor": {"rock":"win","paper":"lose","scissor":"tie"}}
    options = ["rock","paper","scissor"]
    session['computerpick'] = options[random.randint(0,2)]
    return redirect("/show")

@app.route('/show')
def show():
    return render_template("result.html")


if __name__=="__main__":
    app.run(debug=True)