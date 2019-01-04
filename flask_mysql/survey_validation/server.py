from flask import Flask, redirect, render_template, request, session, flash
from mysqlconnection import MySQLConnection

app = Flask(__name__)
app.secret_key = "secret things"

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/create', methods =['post'])
def create():
    data = {
        "name": request.form['name'],
        "location": request.form['location'],
        "language": request.form['language'],
        "comments": request.form['comments']
    }
    if len(data['name']) < 1:
        flash("enter name")
        return redirect('/')
    elif len(data['comments']) > 120:
        flash("comment too long")
        return redirect('/')
    else:
        query = "INSERT INTO surveys (name, location, language, comment) VALUES (%(name)s, %(location)s, %(language)s, %(comments)s);"
        db = MySQLConnection('mydb')
        insert = db.query_db(query, data)
        flash("Successfully Added")
    return redirect("/results")

@app.route('/results/')
def results():
    db = MySQLConnection('mydb')
    query = "SELECT * FROM surveys ORDER BY id DESC LIMIT 1"
    results = db.query_db(query)
    print(results)

    return render_template('results.html', results = results)


if __name__ == "__main__":
    app.run(debug=True)
    