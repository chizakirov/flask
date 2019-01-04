from flask import Flask, render_template
app = Flask(__name__)

@app.route("/<val>")
def play(val):
    return render_template("index.html",input_here = val, times = 3, color = "blue")

@app.route("/<val>/<num>")
def play2(val,num):
    return render_template("index.html",input_here = val, times = int(num), color = "blue")

@app.route('/<val>/<num>/<co>')
def play3(val,num,co):
    return render_template("index.html",input_here = val, times = int(num), color = co)

if __name__=="__main__":
    app.run(debug =True)