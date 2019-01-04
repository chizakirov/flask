from flask import Flask, render_template, request, redirect, session,flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import bcrypt        
import re


app = Flask(__name__)
bcrypt = Bcrypt(app)  
app.secret_key = "nothing crazy"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-copyZ]+$') 

@app.route('/')
def root():
    return render_template("root.html")
##################################################
@app.route("/validate", methods = ['POST'])
def validate():
    #  can also user: error =[]; if len(err)>, then flash errors
    is_valid = True 

    if len(request.form['fname']) <2 or request.form['fname'].isalpha() == False:
        is_valid = False
        flash("First name must contain at least 2 letters and contains only letters")

    if len(request.form['lname']) <2 or request.form['lname'].isalpha() == False:
        is_valid = False
        flash("Last name must contain at least 2 letters and contains only letters")

    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address")

    if len(request.form['pw']) <8: ########NEED TO GO BACK to validate this!!
        is_valid = False
        flash("Password must contain a number, a capital letter, and be between 8-15 characters")

    if len(request.form['confirm_pw']) <8 or request.form['confirm_pw'] != request.form['pw']:
        is_valid = False
        flash("Password must match")

    if is_valid == False:
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['pw'])  
    print(pw_hash) 

    db = connectToMySQL("login_register")
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'pw': pw_hash,
    }
    query = "INSERT INTO users(first_name,last_name, email, password) VALUES(%(fname)s, %(lname)s, %(email)s, %(pw)s);"
    new_user = db.query_db(query, data)
    if new_user:
        flash('You have successfully registered!')
        # session['new_user'][0['first_name']
        # session['register'] =True
    return redirect("/success")
#######################
@app.route("/login", methods = ['POST'])
def login():
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address")

    if len(request.form['password']) <8:
        is_valid = False
        flash('Enter the correct password')

    if is_valid == False:
        return redirect("/")

    db = connectToMySQL("login_register")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["email"] }
    result = db.query_db(query, data)
    print(result)
    print("**********")

    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            flash("You've successfully logged in ")
            session['user'] = result[0]['first_name']
            session['login'] = True
            return redirect('/success')
    else:
        flash('You cannot be logged in. Try again!')
    return redirect("/")
#########################
@app.route("/success")
def success():
    return render_template("success.html")
########################
@app.route("/logout", methods = ['POST'])
def logout():
    session['login'] == False
    if session['login'] == False:
        flash('You have been logged out!')
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)