import mysql.connector
from mysql.connector import errorcode

HOST = 'localhost'
USER = 'nselman'
PASSWD = 'Gametime23!'
DB_NAME = 'rapbot'

TABLE = (
	"CREATE TABLE raw_text ("
	"	url VARCHAR(200) NOT NULL, "
	"	text MEDIUMTEXT NOT NULL, "
	"	PRIMARY KEY (url));"
	)

CLEAN_TEXT_TABLE = (
	"CREATE TABLE clean_text ("
	"	url VARCHAR(200) NOT NULL, " 
	" 	title VARCHAR(100) NOT NULL, "
	"	artist VARCHAR(105) NOT NULL, "
	"	album VARCHAR(100) NOT NULL, "
	"	lyrics MEDIUMTEXT NOT NULL) "
	# "	INDEX par_ind (customer_id) "
	# "	CONSTRAINT fk_raw_text FOREIGN KEY (raw_text_url)"
	# "	REFERENCES raw_text(url))"
	)


def does_table_exist(cnx, table_name):

    c = cnx.cursor()
    c.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = %s
        """, (table_name,))

    rv = c.fetchone()[0] == 1
    c.close()
    
    return rv


def create_clean_text_table(cnx):

	c = cnx.cursor()
	

	# return "did it"
	# break
	try:
		print('creating table...')
		c.execute(CLEAN_TEXT_TABLE)

	except:
		print('fuck it failed')
		c.close()
		return 0

	c.close()
	return 1


def add_row(cursor, url, text):
	cursor.execute(ADD_RAW_TEXT, (url, text))



def setup_db_and_raw_text():

	### ESTABLISH CONNECTS
	cnx = mysql.connector.connect(
			host=HOST,
			user=USER,
			passwd=PASSWD)

	c = cnx.cursor()

	try:
	    c.execute("USE {}".format(DB_NAME))
	except mysql.connector.Error as err:
	    print("Database {} does not exists.".format(DB_NAME))
	    if err.errno == errorcode.ER_BAD_DB_ERROR:
	        create_db(c, DB_NAME)
	        print("Database {} created successfully.".format(DB_NAME))
	        cnx.database = DB_NAME
	    else:
	        print(err)
	        exit(1)

	print("creating table...")
	c.execute(TABLE)



	### CREATE DATABASE

	### CREATE TABLE

	### 


def get_cnx():

	cnx = mysql.connector.connect(
		host=HOST,
		user=USER,
		passwd=PASSWD,
		database=DB_NAME)

	return cnx


def pull_table(cnx, cols, table_name):

	c = cnx.cursor()
	col_text = ", ".join(cols)
	statement = "SELECT {} FROM {}".format(col_text, table_name)
	print(statement)
	c.execute(statement)
	return c.fetchall()


def create_db(cursor, db_name):

	try:
		cursor.execute(
			"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))

	except mysql.connector.Error as err:
		print("Failed creating database: {}".format(err))
        # exit(1)


