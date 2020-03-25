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




def add_row(cursor, url, text):
	cursor.execute(ADD_RAW_TEXT, (url, text))


def go():

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


def insert_into_databse():
	pass


def get_cnx(host, user, passwd, database=None):

	if database:
		cnx = mysql.connector.connect(
			host=host,
			user=user,
			passwd=passwd,
			database=database)

	else:
		cnx = mysql.connector.connect(
			host=host,
			user=user,
			passwd=passwd)

	return cnx
	# # print('hi')
	# args = {'host': host, 'user': user, 'passwd': passwd, 'database': database}
	# params = ', '.join(["{}='{}'".format(k, v) for k, v in args.items() if v])
	# # print(params)
	# # return params
	# print(params)
	# cnx = mysql.connector.connect(eval(params))

	# return cnx


def create_db(cursor, db_name):

	try:
		cursor.execute(
			"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))

	except mysql.connector.Error as err:
		print("Failed creating database: {}".format(err))
        # exit(1)



	# if db_name not in cursor.execute("SHOW DATABASES"):
	
	# 	cursor.execute("CREATE DATABASE %s", db_name)
	# 	print("{} successfully created".format(db_name))

	# else:
	# 	print("{} already exists".format(db_name))



# mycursor.execute("CREATE DATABASE testdb")
# mycursor.execute("SHOW DATABASES")

# for db in mycursor:
# 	print(db)

# mycursor.execute("CREATE TABLE songs (name VARCHAR(100), year INTEGER(4))")

# mycursor.execute("SHOW TABLES")

# for t in mycursor:
# 	print(t)