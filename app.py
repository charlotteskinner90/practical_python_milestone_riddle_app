import os
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
correct_answer = ""
incorrect_answer = ""

@app.route('/', methods=["GET", "POST"])
def index():
    # Homepage with instructions
    if request.method == "POST":
        # If user fills in a username, returns riddle template
        username = request.form["username"]
        """ If user does not enter a username but hits submit, returns to index
         rather than displaying an error page """
        if username == "":
            return render_template("index.html")
        else:
            return redirect("/riddle/" + username)
    return render_template("index.html")
   
@app.route('/riddle/<username>', methods=["GET", "POST"])
def riddle(username):
    # Page to display riddles
    data = []
    # Load in json file containing riddles
    with open("data/riddles.json", "r") as json_data:
        data = json.load(json_data)
    
    riddle_index = 0
    global correct_answer
    global incorrect_answer
    
    if request.method == "POST":
        
        user_response = request.form["answer"]
        if data[riddle_index]["answer"] == user_response:
            riddle_index += 1
            correct_answer = user_response + " is correct!"
            print ("Correct!")
        elif data[riddle_index]["answer"] != user_response:
            incorrect_answer = user_response + " is incorrect!"
            print ("Incorrect!")
            
    return render_template("riddle.html", riddle_data=data, riddle_index=riddle_index, correct_answer=correct_answer, incorrect_answer=incorrect_answer)

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)