import crawler
import song
import database
import mysql.connector

HOST = 'localhost'
USER = 'nselman'
PASSWD = 'Gametime23!'
DB_NAME = 'rapbot'

STARTING_URL = "http://ohhla.com/favorite.html"

ADD_CLEAN_TEXT = (
	"INSERT INTO clean_text "
	"(url, title, artist, album, lyrics) "
	"VALUES (%s, %s, %s, %s, %s) "
	)


def load_raw_text():

	# print(data)
	# return data

	### Connect to database
	cnx = mysql.connector.connect(
		host=HOST,
		user=USER,
		passwd=PASSWD,
		database=DB_NAME)

	c = cnx.cursor()

	crawler.get_lyrics(cnx, c, STARTING_URL, set())
	# c.executemany(ADD_RAW_TEXT, data)

	# cnx.commit()
	cnx.close()


def load_clean_text(cnx):
	

	c = cnx.cursor(buffered=True)
	if database.does_table_exist(cnx, 'clean_text'):
		c.execute("DROP TABLE clean_text")
		cnx.commit()

	success = database.create_clean_text_table(cnx)
	if not success:
		print("exiting...")
		return None

	c.execute("SELECT * FROM raw_text")

	### CREATE TABLE

	c2 = cnx.cursor() # cursor for uploading data
	while True:

		# try:
		row = c.fetchone()
		# print("row:", row)

		# except:
		# print("there was an exception")
		# break

		if not row:
			print("no row")
			break

		print("executing for url:", row[0])
		# print("song text:", row[1])

		s = song.Song(row[1])

		new_row = ([row[0], s.title, s.artist, s.album, s.lyrics])

		c2.execute(ADD_CLEAN_TEXT, new_row)
		cnx.commit()
		# print(new_row)

	c.close()
	c2.close()
	return "finished"

def add_to_table(cursor, args):

	cursor.execute(ADD_RAW_TEXT, args)

