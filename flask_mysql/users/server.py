from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route("/users")
def index():
    db = connectToMySQL("users")
    all_users = db.query_db("SELECT * FROM friends;") 
    print(all_users)
    return render_template("users.html", users = all_users)


@app.route("/users/form")
def new():
    return render_template("newuser.html")

@app.route("/users/new", methods = ['POST'])
def create():
    db = connectToMySQL("users")
    
    query = "INSERT INTO friends(first_name,last_name, email) VALUES (%(fname)s, %(lname)s, %(email)s);"
    data = {
        'fname': request.form["fname"],
        'lname': request.form["lname"],
        'email': request.form["email"],
    }
    new_user_id = db.query_db(query, data)
    print(new_user_id)
    return redirect("/users/<id>")


@app.route("/users/<id>")
def user(id):
    print("**************")
    db = connectToMySQL("users")
    user = db.query_db('SELECT * FROM friends WHERE id =' +id+';')
    print(user)
    return render_template("id.html", user = user)

@app.route("/users/<id>/edit")
def edit():
    return render_template("edit.html")

@app.route("/users/<id>/update")
def update():
    db = connectToMySQL("users")
    
    query = 'UPDATE friends SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s;'
    data = {
        'fname': request.form["fname"],
        'lname': request.form["lname"],
        'email': request.form["email"],
    }
    new_user_id = db.query_db(query, data)
    print(new_user_id)
    return redirect("/users/<id>")

if __name__ == "__main__":
    app.run(debug=True)