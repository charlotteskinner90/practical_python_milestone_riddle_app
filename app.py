import os
import json
from flask import Flask, render_template, request, redirect
from operator import itemgetter

app = Flask(__name__)
answersArray = []
riddle_data = []
riddle_index = 0
score = 0
is_last_question = False

# Load riddle data
with open("data/riddles.json", "r") as json_data:
	riddle_data = json.load(json_data)
	
# Add usernames and results to file
score_list = []

def results_table(username, result):
    score_list.append({
        'username': username,
        'score': result,
    })
    
    with open('data/results.json', 'w') as outfile:
        json.dump(score_list, outfile)

# ROUTING 

@app.route('/', methods=["GET", "POST"])
def index():
	reset_data()
	
	# Homepage with instructions
	if request.method == "POST":
		"""
		If user fills in a username, returns riddle template else returns to the
		index page rather than displaying an error
		"""
		username = request.form["username"]
		if username == "":
			return render_template("index.html")
		else:
			return redirect("/riddle/" + username)

	return render_template("index.html")

# Riddle page routing
@app.route('/riddle/<username>', methods=["GET", "POST"])
def riddle(username):

	global riddle_index
	global is_last_question
	global score
	hasEnded = False

	if is_last_question:
		hasEnded = True
	if riddle_index == len(riddle_data)-2:
		is_last_question = True
	if request.form:
		user_response = request.form["answer"]
		# Checks to see if user's answer is correct compared with answer in riddles.json
		if user_response.lower() in riddle_data[riddle_index]["answer".lower()]:
			answersArray.append({"status": 1, "userAnswer": user_response, "realAnswer": riddle_data[riddle_index]["answer"]})
			# Adds +1 to the score if correct
			score += 1
			print ("Correct!")
			riddle_index += 1
		elif user_response.lower() not in riddle_data[riddle_index]["answer".lower()]:
			answersArray.append({"status": 0, "userAnswer": user_response, "realAnswer": riddle_data[riddle_index]["answer"]})
			print ("Incorrect!")
			riddle_index += 1
	# Routing for answers page if quiz has ended
	if hasEnded:
		results_table(username, score) 
		return redirect("/riddle/" + username + "/answers")
	else:
		return render_template("riddle.html", riddle_data=riddle_data, riddle_index=riddle_index, is_last_question=is_last_question, username=username, score=score)

# Routing for answers page
@app.route('/riddle/<username>/answers', methods=["GET", "POST"])
def answers(username):
	return render_template("answers.html", answers=answersArray, riddle_data=riddle_data, riddle_index=riddle_index, score=score)
	
# Routing for leaderboard
@app.route('/leaderboard')
def leaderboard():
	reset_data()
	with open("data/results.json", "r") as leaderboard_data: 
		data = json.load(leaderboard_data)

	scores = sorted(data, key=itemgetter('score'), reverse=True)
	return render_template("leaderboard.html", leaderboard=scores)

def reset_data():
	global riddle_index
	global is_last_question
	global score
	global answersArray
	answersArray = []
	riddle_data = []
	riddle_index = 0
	score = 0
	is_last_question = False

if __name__ == '__main__':
	app.run(host=os.environ.get('IP'),
	port=int(os.environ.get('PORT')),
	debug=True)