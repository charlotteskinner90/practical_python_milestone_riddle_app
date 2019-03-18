import os
import json
from flask import Flask, render_template, request, redirect, session, url_for
from operator import itemgetter


app = Flask(__name__)
app.secret_key = os.urandom(24)

riddle_data = []
score_list = []

# Load riddle data
with open("data/riddles.json", "r") as json_data:
    riddle_data = json.load(json_data)


# Load leaderboard data
with open("data/results.json", "r") as leaderboard_data:
    score_list = json.load(leaderboard_data)


# Record User Scores
def results_table(username, score):
    global score_list

    score_list.append({
        'username': session['username'],
        'score': session['score'],
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
        session['username'] = request.form["username"]
        session['answersArray'] = []
        session['riddle_index'] = 0
        session['is_last_question'] = False
        session['score'] = 0

        # If user fills in a username, returns riddle template else returns
        # to the index page rather than displaying an error
        if session['username'] == "":
            return render_template("index.html")
        else:
            return redirect("/riddle/" + session['username'])

    return render_template("index.html")


# Riddle Page Routing
@app.route('/riddle/<username>', methods=["GET", "POST"])
def riddle(username):
    hasEnded = False

    if 'username' not in session:
        return redirect(url_for("index"))

    if session['is_last_question']:
        hasEnded = True
    if session['riddle_index'] == len(riddle_data) - 2:
        session['is_last_question'] = True

    if request.form:
        session['user_response'] = request.form["answer"]
        check_answer = riddle_data[session['riddle_index']]["answer".lower()]
        riddle_answer = riddle_data[session['riddle_index']]["answer"]

        # Checks to see if user's answer is correct compared with answer
        # in riddles.json

        if session['user_response'].lower() in check_answer:
            session['answersArray'].append(
                {
                    # Gives a status of 1 if correct
                    "status": 1,
                    "userAnswer": session['user_response'],
                    "realAnswer": riddle_answer
                }
            )
            # Adds +1 to the score if correct
            session['score'] += 1
            print("Correct!")
            # Moves to next question
            session['riddle_index'] += 1

        elif session['user_response'].lower() not in check_answer:
            session['answersArray'].append(
                {
                    # Gives a status of 0 if incorrect
                    "status": 0,
                    "userAnswer": session['user_response'],
                    "realAnswer": riddle_answer
                }
            )
            print("Incorrect!")
            session['riddle_index'] += 1

    # Redirect to answers page if quiz has ended
    if hasEnded:
        results_table(session['username'], session['score'])
        return redirect("/riddle/" + session['username'] + "/answers")
    else:
        return render_template(
            "riddle.html",
            riddle_data=riddle_data,
            riddle_index=session['riddle_index'],
            is_last_question=session['is_last_question'],
            username=session['username'],
            score=session['score']
        )


# Routing for answers page
@app.route('/riddle/<username>/answers', methods=["GET", "POST"])
def answers(username):
    return render_template(
        "answers.html",
        answers=session['answersArray'],
        riddle_data=riddle_data,
        riddle_index=session['riddle_index'],
        score=session['score']
    )


# Routing for leaderboard
@app.route('/leaderboard')
def leaderboard():
    session.pop('username', None)
    reset_data()
    score_list
    # Sorts scores numerically, then reverses order for leaderboard
    scores = sorted(score_list, key=itemgetter('score'), reverse=True)

    return render_template("leaderboard.html", leaderboard=scores)


# Resets data so that previous users answers are not displayed on answer page
def reset_data():
    session.pop('answersArray', None)
    session.pop('riddle_index', None)
    session.pop('score', None),


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=False
        )
