from flask import Flask, render_template # Import Flask to allow us to create our app - treat Flask like a class!
app = Flask(__name__) # Create a new instance of the Flask class called "app"

@app.route('/<name>/<val>') # The "@" decorator associates this route with the function immediately following
def hello_world(name,val):
    return render_template('index.html', some_name = name, times = int(val)) #client will see this

# @app.route('/dojo')
# def dojo():
#     return "dojo"

# @app.route('/<input>')
# def print_hello(input):
#     return "Hi " + input + "!"

# @app.route('/repeat/<int:num>/<text>') # for a route '/users/____/____', two parameters in the url get passed as username and id
# def show_user_profile(num,text): #users here can be typed as anything, like /chi/username/10
#     # if (print(isinstance(text,str)) is True: #check to make sure text input is string 
#         return f"{text*int(num)}"
#     # else:
#     #     return "wrong text input"
# @app.errorhandler(404)
# def not_found(error):
#     return "sorry, no response. Try again",404

# @app.errorhandler(500)
# def internal_error(error):
#     return "500 error"

if __name__=="__main__": #Ensure this file is being run directly and not from a different module (like in a package)  
    app.run(debug=True) # Run the app in debug mode