import os
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    # Homepage with instructions
    if request.method == "POST":
        username = request.form["username"]
        return redirect("/riddle/" + username)
    return render_template("index.html")
   
@app.route('/riddle/<username>', methods=["GET", "POST"])
def riddle(username):
        # Page to display riddles
    data = []
    # Load in json file containing riddles
    with open("data/riddles.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("riddle.html", riddle_data=data)

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)