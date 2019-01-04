from flask import Flask, render_template, request, redirect, session,flash
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = "nothing crazy"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-copyZ]+$') 


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods = ['POST'])
def validate():
    db = connectToMySQL("email_validation")
    data = {'email': request.form['email']}
    if len(request.form['email'])<1:
        flash("please enter an email")
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address")
        return redirect("/")
    else:
        query_string = "INSERT INTO emails(email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
        new_email = db.query_db(query_string, data)
        print("************")
        print("new_email")
        flash("Successully added email!")
    return redirect("/success")

@app.route("/success")
def success():
    db = connectToMySQL("email_validation")
    all_emails = db.query_db("SELECT * FROM emails;")
    return render_template("success.html", emails = all_emails)
    

if __name__ == "__main__":
    app.run(debug=True)