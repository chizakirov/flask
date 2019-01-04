from flask import Flask, render_template, request, redirect, session,flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt        
import re


app = Flask(__name__)
bcrypt = Bcrypt(app)  
app.secret_key = "nothing crazy" #for hasing the session(use time & key to hack it)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-copyZ]+$') 

@app.route("/")
def index():
    return render_template("index.html")
#----------------------------------------
@app.route("/register", methods = ['POST'])
def register():
    # Validation check
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

    if len(request.form['password']) <8: #Need to require email unique!!!
        is_valid = False
        flash("Password must be at least 8 characters")

    if len(request.form['pwconfirm']) <8 or request.form['pwconfirm'] != request.form['password']:
        is_valid = False
        flash("Password must match. Retype your password")

    if is_valid == False:
        return redirect("/")

    #store the newly registered user into DB
    pw_hash = bcrypt.generate_password_hash(request.form['password'])  
    print(pw_hash)

    data = {
        'fname':request.form['fname'],
        'lname':request.form['lname'],
        'email':request.form['email'],
        'password':pw_hash,
    }
    query = "INSERT INTO users(first_name,last_name, email, password) VALUES(%(fname)s, %(lname)s, %(email)s, %(password)s);"
    db = connectToMySQL("myusers")
    new_user_id = db.query_db(query, data)
    return redirect("/wall")
#-----------------------------------------
@app.route("/login", methods = ['POST'])
def login():
    #look for the email in the DB
    db = connectToMySQL("myusers")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form["email"] }
    result = db.query_db(query, data)
    print(result)
    print("**********")

    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['user'] = result[0]['first_name']
            session['user_id'] = result[0]['user_id']
            session['login'] = True
            return redirect('/wall')
    
    flash('You cannot be logged in. Try again')
    return redirect("/")
#----------------------------------------
@app.route("/create_msg", methods = ['POST'])
def create_msg():
    db = connectToMySQL("myusers")
    data = {
        'content': request.form['message'],
        'user_id': session['user_id'],
        'friend_id': request.form['friend_id']
    }
    query = "INSERT INTO messages(content, user_id, friend_id) VALUES (%(content)s, %(user_id)s, %(friend_id)s);"
    session['new_message_id'] = db.query_db(query, data) 

    return redirect("/wall")
#-----------------------------------------
@app.route("/wall")
def wall():
    if not 'user_id' in session:
        flash('You need to log in first')
        return redirect('/')

    db = connectToMySQL("myusers")
    friend_query = 'SELECT user_id, first_name FROM users WHERE user_id != ' + str(session['user_id']) + ';'
    friends = db.query_db(friend_query)
    friends_length = len(friends)

    db = connectToMySQL("myusers")
    user_query = 'SELECT messages.msg_id, users.first_name, messages.friend_id AS friend_id, friend.first_name AS friend_first_name, messages.content FROM users LEFT JOIN messages ON users.user_id = messages.user_id LEFT JOIN users AS friend ON messages.friend_id = friend.user_id WHERE messages.friend_id = ' + str(session['user_id']) + ';'
    wall_msg = db.query_db(user_query)
    print(wall_msg)
    length = len(wall_msg)

    db = connectToMySQL("myusers")
    user_query = 'SELECT messages.msg_id, users.first_name, messages.friend_id AS friend_id, friend.first_name AS friend_first_name, messages.content FROM users LEFT JOIN messages ON users.user_id = messages.user_id LEFT JOIN users AS friend ON messages.friend_id = friend.user_id WHERE messages.user_id = ' + str(session['user_id']) + ';'
    sent_msg = db.query_db(user_query)
    print(sent_msg)
    length_sent = len(sent_msg)

    return render_template("wall.html", content = wall_msg, length = length, length_sent = length_sent, friends_length = friends_length, friends = friends)

#-----------------------------------------
@app.route('/delete', methods = ['POST'])
def delete():
    db = connectToMySQL("myusers")
    data = {
        'msg_id':request.form['msg_id'],
    }
    print(data)
    delete_query = 'DELETE FROM messages WHERE msg_id = '+ '%(msg_id)s' + ";"
    db.query_db(delete_query, data)
    return redirect("/wall")
#------------------------------------------
@app.route("/logout", methods = ['POST'])
def logout():
    session['login'] = False
    if session['login'] == False:
        session.clear()
    return redirect("/") 

#------------------------------------------


if __name__=="__main__":
    app.run(debug=True)