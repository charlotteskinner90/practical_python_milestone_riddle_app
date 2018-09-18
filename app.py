import os
import json
from flask import Flask, render_template, request, redirect
from pprint import pprint

app = Flask(__name__)
answersArray = []
riddle_data = []
riddle_index = 0
is_last_question = False


with open("data/riddles.json", "r") as json_data:
		riddle_data = json.load(json_data)

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
	global riddle_index
	global is_last_question
	hasEnded = False
	
	if is_last_question:
	    hasEnded = True
            
    	pprint(riddle_index)
    	pprint(hasEnded)
    	pprint(is_last_question)        
    
    
	if riddle_index == len(riddle_data)-2:
		is_last_question = True
	
	if request.method == "POST":
			
		user_response = request.form["answer"]
		if riddle_data[riddle_index + 1]["answer"] == user_response:
			answersArray.append({1, user_response})
			print ("Correct!")
			riddle_index += 1
		elif riddle_data[riddle_index]["answer"] != user_response:
			answersArray.append({0, user_response})
			print ("Incorrect!")
			riddle_index += 1
					
    	if hasEnded:
        	return redirect("/riddle/" + username + "/answers")
        else:
    	    return render_template("riddle.html", riddle_data=riddle_data, riddle_index=riddle_index, is_last_question=is_last_question)


@app.route('/riddle/<username>/answers', methods=["GET", "POST"])
def answers(username, answersArray):
	return render_template("answers.html", answers=answersArray)


@app.route('/leaderboard')
def leaderboard():
		return render_template("leaderboard.html")
				
if __name__ == '__main__':
		app.run(host=os.environ.get('IP'),
						port=int(os.environ.get('PORT')),
						debug=True)