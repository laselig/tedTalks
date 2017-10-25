import sqlite3
from bs4 import BeautifulSoup
import requests, csv

from bs4.element import Comment
import urllib



# @ desc visits the transcript page for the tedTalkURL that it's passed and scrapes the transcript for it
# @ param - tedTalkURL the url for the ted talk
# @ return string - the trancript of the ted talk
def getTranscript(tedTalkURL):
	tedTalkURL += "/transcript?language=en"
	request = requests.get(tedTalkURL)
	content = request.content
	soup = BeautifulSoup(content)
	text = soup.findAll("p")
	transcript = ""

	# there are always 15 "junk" paragraphs after the speaker is done, don't include those.
	for i in range(len(text) - 15):

		sentence = text[i]
		words = sentence.getText().replace("\t", "")
		transcript += words

	return transcript
# print getTranscript("https://www.ted.com/talks/larry_brilliant_wants_to_stop_pandemics" + "/transcript")



# @ desc populateTedTalks opens the ted talk spreadsheet, parse out information and insert it into the ted talk table in database
# @ return none - just po
def populateTedTalks():
	conn = sqlite3.connect("tedTalks.db")
	cur = conn.cursor()

	with open('tedTalks.csv', 'rb') as csvfile:
		ttreader = csv.reader(csvfile, delimiter=',')
		for i, row in enumerate(ttreader):
			# data starts at row[1], skip row[0]
			# bad rows have row[1] as empty, skip these
			if(i != 0 and row[1] != ""):
				row = row[1:]
				transcript = getTranscript(row[0] + "/transcript") # row[0] is the url of the ted talk
				row.append(transcript)
				values = tuple(row)
				print i
				# some have unicode errors, no time to fix, just skip them
				try:
					query = "INSERT INTO TedTalks(url, speaker, headline, desc, event, duration, language, published, tags, transcript) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
					cur.execute(query, values)
				except:
					print "unicode error"
	conn.commit()
	conn.close()

 
# print populateTedTalks()