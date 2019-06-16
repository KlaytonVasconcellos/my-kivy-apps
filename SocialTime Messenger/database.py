import MySQLdb


db_host2 = "sql309.byetcluster.com"
db_host = "sql10.freemysqlhosting.net"
db_name = "sql10292541"
db_user = "sql10292541"
db_pass = "cDtJHUVljT"
db_table = ""
sql = MySQLdb

def connect_db():
	db = MySQLdb.connect(db_host, db_user, db_pass, db_name)
	cursor = db.cursor()
	cursor.execute("SELECT VERSION()")
	data = cursor.fetchone()
	print("Database version : {} ".format(data))

"""while True:
	try:
		connect_db(db_host, db_user, db_pass, db_name)
	except Exception as log:
		print("Erro de Conexão:", log)"""


"""try:
	db = MySQLdb.connect(db_host, db_user, db_pass, db_name)
	cursor = db.cursor()
	cursor.execute("SELECT VERSION()")
	data = cursor.fetchone()
	print("Database version : {} ".format(data))
except Exception as log:
	print("Erro de Conexão:", log)"""