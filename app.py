from flask import *
from modules.token import make_token, decode_token
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False #可避免json自動排序

import mysql.connector, math, time
from mysql.connector import pooling

#hash password
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

#connection pool
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


# Attractions APIs
@app.route("/api/attractions", methods = ["GET"])
def api_attractions():
	num = 0
	page = int(request.args.get("page"))
	keyword = request.args.get("keyword")
	if keyword:
		c = conn() #連線 connetion pool
		cur = c.cursor()
		sql = "SELECT * FROM attraction WHERE category = %s OR name LIKE '%' %s '%' LIMIT %s,%s" #'%' %s '%'中間要空隔
		value = (keyword, keyword, (page * 12), 12)
		cur.execute(sql, value)
		query = cur.fetchall()
		cur.close()

		cur = c.cursor()
		count_sql = "SELECT COUNT(*) FROM attraction WHERE category = %s OR name LIKE '%' %s '%'"
		value = (keyword, keyword)
		cur.execute(count_sql, value)
		num = cur.fetchone()[0]
		cur.close()
		c.close()

	else:
		c = conn()
		cur = c.cursor()
		sql = "SELECT * FROM attraction LIMIT %s,%s"
		value = ((page * 12), 12)
		cur.execute(sql, value)
		query = cur.fetchall()
		cur.close()
		c.close()

		c = conn()
		cur = c.cursor()
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

# User APIs
@app.route("/api/user", methods = ["POST"])
def api_user():
	data = request.get_json()
	c = conn()
	cur = c.cursor()
	sql = "SELECT * FROM user WHERE email = %s"
	cur.execute(sql, (data["email"],))
	query = cur.fetchone()
	cur.close()
	try:
		if query :
			return jsonify({
				"error": True,
				"message": "該email已被註冊"
				}), 400
		else:
			cur = c.cursor()
			sql = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
			hashed_password = bcrypt.generate_password_hash(password=data["password"])
			cur.execute(sql, (data["name"], data["email"], hashed_password,))
			c.commit()
			cur.close()
			return jsonify({
				"ok": True
				}), 200
	except:
		return jsonify({
			"error": True,
			"message": "伺服器內部錯誤"
			}), 500
	finally:
		c.close()

@app.route("/api/user/auth", methods = ["GET", "PUT", "DELETE"])
def api_user_auth():
	if request.method == "PUT":
		data = request.get_json()
		c = conn()
		cur = c.cursor()
		sql = "SELECT * FROM user WHERE email = %s AND password = %s"
		cur.execute(sql, (data["email"], data["password"],))
		query = cur.fetchone()
		cur.close()
		try:
			if query:
				token = make_token(query)
				resp = make_response(jsonify({
					"ok": True
					}), 200)
				resp.set_cookie(key = "token", value = token, expires = time.time() + 24*60*60*7)
				return resp
			else:
				return jsonify({
					"error": True,
					"message": "帳號或密碼錯誤"
					}), 400
		except:
			return jsonify({
				"error": True,
				"message": "伺服器內部錯誤"
				}), 500
		finally:
			c.close()
	if request.method == 'GET':
		cookiesToken = request.cookies.get("token")
		if cookiesToken == None:
			return jsonify({
				"data": None
			})
		else:
			decodeToken = decode_token(cookiesToken)
			return jsonify({
				"data": decodeToken
			})
	if request.method == "DELETE":
		resp = make_response(jsonify({"ok": True}), 200)
		resp.set_cookie(key = "token", value = "", expires = 0)
		return resp

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