from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route("/")
def index():
    print("*"*50, "\nIN INDEX METHOD\n", "*"*50)
    db = connectToMySQL("art_works") #schema
    all_artists = db.query_db("SELECT * FROM artists") 
    return render_template("index.html", artists = all_artists)

@app.route("/create", methods=["POST"])
def add_artist_to_db():
    print("*"*50, "\nIN CREATE METHOD\n", "*"*50)
    query = "INSERT INTO artists(name, birthday, deathday) VALUES (%(name)s, %(birthday)s, %(deathday)s);"
    data = {
        'name': request.form["name"],
        'birthday': request.form["birth"],
        'deathday': request.form["death"],
    }
    db = connectToMySQL("art_works")
    new_artist_id = db.query_db(query, data)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)