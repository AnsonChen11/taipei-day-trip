from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False #可避免json自動排序


import mysql.connector, math
from mysql.connector import pooling
# conn = mysql.connector.connect(
#   host = "localhost",
#   user = "root",
#   password = "12345678",
#   database = "taipeitrip",
#   charset = "utf8",
# )
#create connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "taipeitrip_pool",
    pool_size = 5,
    pool_reset_session = True,
    host = "localhost",
	user = "root",
	password = "12345678",
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


# API
@app.route("/api/attractions", methods = ["GET"])
def api_attractions():
	num = 0
	page = int(request.args.get("page"))
	keyword = request.args.get("keyword")
	if keyword:
		c = conn() #連線 connetion pool
		cur = c.cursor()
		# cur = conn.cursor(buffered=True)
		sql = "SELECT * FROM attraction WHERE category = %s OR name LIKE '%' %s '%' LIMIT %s,%s" #'%' %s '%'中間要空隔
		value = (keyword, keyword, (page * 12), 12)
		cur.execute(sql, value)
		query = cur.fetchall()
		cur.close()

		cur = c.cursor()
		# cur = conn.cursor(buffered=True)
		count_sql = "SELECT COUNT(*) FROM attraction WHERE category = %s OR name LIKE '%' %s '%'"
		value = (keyword, keyword)
		cur.execute(count_sql, value)
		num = cur.fetchone()[0]
		cur.close()
		c.close()

	else:
		c = conn()
		cur = c.cursor()
		# cur = conn.cursor(buffered=True)
		sql = "SELECT * FROM attraction LIMIT %s,%s"
		value = ((page * 12), 12)
		cur.execute(sql, value)
		query = cur.fetchall()
		cur.close()
		c.close()

		c = conn()
		cur = c.cursor()
		# cur = conn.cursor(buffered=True)
		count_sql = "SELECT count(*) FROM attraction"
		cur.execute(count_sql)
		num = cur.fetchone()[0]
		cur.close()
		c.close()

	lastPage = math.ceil(num / 12) #無條件進位
	nextPage = page + 1
	if nextPage >= lastPage:
		nextPage = None

	i = 0 
	list = []
	try:
		while i < len(query): 
			result = {				
				"id" : query[i][0],
				"name" : query[i][1],
				"category" : query[i][2],
				"description" : query[i][3],
				"address" : query[i][4],
				"transport" : query[i][5],
				"mrt" : query[i][6],
				"lat" : query[i][7],
				"lng" : query[i][8],
				"images" : eval(query[i][9])
			}
			
			list.append(result)
			i = i + 1
		return jsonify({"nextPage" : nextPage, 
					"data" : list})
	except:
		return jsonify({"error": True,
				"message": "Internal Server Error"}), 500

@app.route("/api/attraction/<id>", methods = ["GET"])
def api_attractions_id(id):
	c = conn()
	cur = c.cursor()
	# cur = conn.cursor(buffered=True)
	sql = "SELECT * FROM attraction WHERE id = %s"
	cur.execute(sql, (id,))
	query = cur.fetchone()
	try:
		if query:
			result = {
					"id" : query[0],
					"name" : query[1],
					"category" : query[2],
					"description" : query[3],
					"address" : query[4],
					"transport" : query[5],
					"mrt" : query[6],
					"lat" : query[7],
					"lng" : query[8],
					"images" : eval(query[9])
				}
			return jsonify({"data" : result})
		else:
			return jsonify({"error": True,
  				"message": "id does not exist"}), 400
	except:
		return jsonify({"error": True,
				"message": "Internal Server Error"}), 500
	finally:
		cur.close()
		c.close()
		
@app.route("/api/categories", methods = ["GET"])
def api_categories():
	c = conn()
	cur = c.cursor()
	# cur = conn.cursor(buffered=True)
	sql = "SELECT DISTINCT category FROM attraction"
	cur.execute(sql)
	query = cur.fetchall()
	

	i = 0
	list = []
	try:
		while i < len(query):
			result = query[i][0]
			list.append(result)
			i = i + 1
		return jsonify({"data" : list})
	except:
		return jsonify({"error": True,
				"message": "Internal Server Error"}), 500
	finally:
		cur.close()
		c.close()

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)