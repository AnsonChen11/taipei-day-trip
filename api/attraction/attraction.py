from flask import Blueprint, request, jsonify, render_template
import math
from modules import connect_to_db
from modules.connect_to_db import conn

attraction = Blueprint(
    "attraction", __name__,
    static_folder = "static",
    template_folder = "templates"
    )

@attraction.route("/api/attractions", methods = ["GET"])
def api_attractions():
	num = 0
	page = int(request.args.get("page"))
	keyword = request.args.get("keyword")
	if keyword:
		c = conn()
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

@attraction.route("/api/attraction/<id>", methods = ["GET"])
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
		
@attraction.route("/api/categories", methods = ["GET"])
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

