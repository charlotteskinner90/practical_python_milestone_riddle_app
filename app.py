import os
import json
from flask import Flask, render_template, request, redirect, session, url_for
from operator import itemgetter

app = Flask(__name__)
app.secret_key = os.urandom(24)

answersArray = []
riddle_data = []
riddle_index = 0
score = 0
is_last_question = False
score_list = []

# Load riddle data
with open("data/riddles.json", "r") as json_data:
    riddle_data = json.load(json_data)

# Load leaderboard data
with open("data/results.json", "r") as leaderboard_data:
    score_list = json.load(leaderboard_data)


# Record User Scores
def results_table(username, result):
    global score_list

    score_list.append({
        'username': session['username'],
        'score': result,
    })

    with open('data/results.json', 'w') as outfile:
        json.dump(score_list, outfile)

# Homepage Routing
@app.route('/', methods=["GET", "POST"])
def index():
    reset_data()
    session.pop('username', None)

    # Homepage with instructions
    if request.method == "POST":
        """
        If user fills in a username, returns riddle template else returns
        to the index page rather than displaying an error
        """
        session['username'] = request.form["username"]
        if session['username'] == "":
            return render_template("index.html")
        else:
            return redirect("/riddle/" + session['username'])

    return render_template("index.html")

# Riddle Page Routing
@app.route('/riddle/<username>', methods=["GET", "POST"])
def riddle(username):
    global riddle_index
    global is_last_question
    global score
    hasEnded = False
    
    if "username" not in session:
        return redirect(url_for("index"))

    if is_last_question:
        hasEnded = True
    if riddle_index == len(riddle_data) - 2:
        is_last_question = True
    if request.form:
        session['user_response'] = request.form["answer"]
        """
        Checks to see if user's answer is correct compared with answer
        in riddles.json
        """
        if session['user_response'].lower() in riddle_data[riddle_index]["answer".lower()]:
            answersArray.append(
                {
                    "status": 1,
                    "userAnswer": session['user_response'],
                    "realAnswer": riddle_data[riddle_index]["answer"]
                }
            )
            # Adds +1 to the score if correct
            score += 1
            print("Correct!")
            riddle_index += 1

        elif session['user_response'].lower() not in riddle_data[riddle_index]["answer".lower()]:
            answersArray.append(
                {
                    "status": 0,
                    "userAnswer": session['user_response'],
                    "realAnswer": riddle_data[riddle_index]["answer"]
                }
            )
            print("Incorrect!")
            riddle_index += 1

    # Routing for answers page if quiz has ended
    if hasEnded:
        results_table(username, score)
        return redirect("/riddle/" + session['username'] + "/answers")
    else:
        return render_template(
            "riddle.html",
            riddle_data=riddle_data,
            riddle_index=riddle_index,
            is_last_question=is_last_question,
            username=session['username'],
            score=score
        )

# Routing for answers page
@app.route('/riddle/<username>/answers', methods=["GET", "POST"])
def answers(username):
    return render_template(
        "answers.html",
        answers=answersArray,
        riddle_data=riddle_data,
        riddle_index=riddle_index,
        score=score
    )

# Routing for leaderboard
@app.route('/leaderboard')
def leaderboard():
    session.pop('username', None)
    score_list
    reset_data()
    scores = sorted(score_list, key=itemgetter('score'), reverse=True)
    
    return render_template("leaderboard.html", leaderboard=scores)


# Resets data so that previous users answers are not displayed on answer page
def reset_data():
    session.pop('answersArray', None)
    session.pop('riddle_index', None)
    session.pop('score', None),
    is_last_question = False

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
