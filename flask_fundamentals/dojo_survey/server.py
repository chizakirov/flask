from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/users', methods=['POST'])
# def create_user():
#     print("Got Post Info")
#     print(request.form)
#     name_from_form = request.form['name']
#     email_from_form = request.form['email']
#     return render_template("index.html", name_on_template=name_from_form, email_on_template=email_from_form)

@app.route("/survey", methods = ['POST'])
def create_survey():
    print("*"*50)
    username = request.form['name']
    userlocation = request.form['location']
    usercomment = request.form['comment']
    return render_template("result.html", name_variable = username, location_variable = userlocation, comment_variable = usercomment)


if __name__=="__main__":
    app.run(debug=True)