import crawler
import database
import mysql.connector

HOST = 'localhost'
USER = 'nselman'
PASSWD = 'Gametime23!'
DB_NAME = 'rapbot'

STARTING_URL = "http://ohhla.com/favorite.html"

ADD_RAW_TEXT = (
	"INSERT INTO raw_text "
	"(url, text) "
	"VALUES (%s, %s) "
	)

def main():

	data = crawler.get_lyrics(STARTING_URL, set())
	# print(data)
	# return data

	### Connect to database
	cnx = mysql.connector.connect(
		host=HOST,
		user=USER,
		passwd=PASSWD,
		database=DB_NAME)

	c = cnx.cursor()

	c.executemany(ADD_RAW_TEXT, data)

	cnx.commit()
	cnx.close()

