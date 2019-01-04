from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route("/")
def index():
    db = connectToMySQL("crpets")
    all_pets = db.query_db("SELECT * FROM pets;") 
    print(all_pets)
    return render_template("index.html", pets = all_pets)

@app.route("/addpet", methods =['POST'])
def addpet():
    query = "INSERT INTO pets(name, type) VALUES (%(name)s, %(type)s);"
    data = {
        'name': request.form["name"],
        'type': request.form["type"],
    }
    db = connectToMySQL("crpets")
    new_pet_id = db.query_db(query, data)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)