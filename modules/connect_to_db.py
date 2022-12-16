import mysql.connector, os
from mysql.connector import pooling

#connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "taipeitrip_pool",
    pool_size = 5,
    pool_reset_session = True,
    host = "localhost",
	user = "root",
	password = os.getenv("mysql_password"),
	database = "taipeitrip",
	charset = "utf8",
)
#將 .get_connection() 存入 conn function
def conn():
	try:
		c = connection_pool.get_connection()
		return c
	except:
		print ("connection error")