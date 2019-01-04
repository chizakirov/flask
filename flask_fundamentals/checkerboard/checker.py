from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def checker():
    return render_template("index.html", num1 = 4)

@app.route("/<x>")
def newboard(x):
    return render_template("index.html", num1 = int(x))

if __name__=="__main__":
    app.run(debug=True)