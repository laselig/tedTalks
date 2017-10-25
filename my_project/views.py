from flask import render_template, redirect, flash, request, Flask, session, send_file
from forms import *
import sqlite3, time, json, re
from queries import *

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret_key'



@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	loginForm = login_form()
	username = loginForm.data['username']
	password = loginForm.data['password']
	if (loginForm.validate_on_submit()):
		session['username'] = username
		session['logged_in'] = True

		return render_template('index.html')
	else:
		return render_template('login.html', title='Sign In', form= loginForm)

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	signupForm = signup_form()
	if(signupForm.validate_on_submit()):
		session['username'] = signupForm.data["username"]
		session['logged_in'] = True
		insertUser(signupForm.data)

		return render_template('index.html')
	else:
		return render_template('signUp.html', title='signUp', form = signupForm)


@app.route("/browseTedTalks")
def browseTedTalks():
	tedTalks = getTedTalks()
	return render_template("tedTalks.html", tedTalks = tedTalks)

@app.route("/ttSearch", methods=['GET', 'POST'])
def searchTedTalks():
	ttSearchForm = tt_form()
	searchText = ttSearchForm.data['ted_talk']
	if (ttSearchForm.validate_on_submit()):
		tedTalks = getTedTalksTranscriptContaining(searchText)
		return render_template('tedTalksSearch.html', tedTalks = tedTalks, searchTerm = searchText)


	else:
		return render_template('ttSearch.html', title='Search', form= ttSearchForm)

@app.route('/transcript/<id>/<searchTerm>', methods=['GET', 'POST'])
def transcript(id, searchTerm):
	transcriptText = getTranscriptText(id)
	markedTranscript = re.compile(re.escape(searchTerm), re.IGNORECASE)
	markedTranscript = markedTranscript.sub("<mark>" + searchTerm + "</mark>", transcriptText)
	return render_template("transcript.html", transcriptText = markedTranscript, searchTerm = searchTerm)

if(__name__ == "__main__"):
	app.run(debug = True)

