import sqlite3

def insertUser(signupHash):
	# @ desc takes in the signupHash returned from the signup form and inserts that user into the database
	# @ param signupHash the hash map returned from the signup form
	# @ return none 
	conn = sqlite3.connect("tedTalks.db")
	cur = conn.cursor()

	query = "INSERT INTO User(email, username, password) VALUES(?, ?, ?)"
	cur.execute(query, (signupHash["email"], signupHash["username"], signupHash["password"]))

	conn.commit()
	conn.close()


def getTedTalks():
	# @ desc selects all ted talks from the database
	# @ return a list of all ted talks

	conn = sqlite3.connect("tedTalks.db")
	cur = conn.cursor()



	query = "SELECT * FROM TedTalks"
	cur.execute(query)
	tedTalks = cur.fetchall()
	conn.close()
	return tedTalks


def getTedTalksTranscriptContaining(searchTerm):
	# @ desc selects all ted talks from the database where the transcript contains the search term
	# @ return a list of all ted talks satisfying above condition

	conn = sqlite3.connect("tedTalks.db")
	cur = conn.cursor()
	query = "SELECT * FROM TedTalks WHERE transcript LIKE ?"
	cur.execute(query, ('%'+searchTerm+'%',))
	tedTalks = cur.fetchall()
	conn.close()
	return tedTalks

def getTranscriptText(id):
	conn = sqlite3.connect("tedTalks.db")
	cur = conn.cursor()
	query = "SELECT transcript FROM TedTalks WHERE id = ?"
	cur.execute(query, (id,))
	transcripts = cur.fetchone()[0]
	conn.close()
	return transcripts

# results = getTedTalksWithTranscripts("about 10")
# print len(results)
# print getTranscriptText(11)
