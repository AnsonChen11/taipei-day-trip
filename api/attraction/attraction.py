from flask import Blueprint, request, jsonify, render_template
from .models import *

attraction = Blueprint(
    "attraction", __name__,
    static_folder = "static",
    template_folder = "templates"
)

@attraction.route("/attraction/<id>")
def attraction_base(id):
	return render_template("attraction.html")

#--------------------get attraction by page and keywords controller--------------------
@attraction.route("/api/attractions", methods = ["GET"])
def api_attractions():
	data = get_attraction_by_page_and_keyword()
	if data:	
		nextPage = data[0]
		list = data[1]
		return jsonify({
			"nextPage" : nextPage,
			"data" : list}), 200
	if data == "伺服器錯誤":
		return jsonify({
			"error": True,
            "message": "Internal Server Error"
			}), 500

#--------------------get attraction by id controller--------------------
@attraction.route("/api/attraction/<id>", methods = ["GET"])
def api_attractions_id(id):
	data = get_attraction_id(id)
	if data:
		return jsonify({
			"data" : data
			}), 200
	if data == False:
		return jsonify({
			"error": True,
  			"message": "id does not exist"
			}), 400
	if data == "伺服器錯誤":
		return jsonify({
			"error": True,
			"message": "Internal Server Error"
			}), 500

#--------------------get attraction categories list controller--------------------		
@attraction.route("/api/categories", methods = ["GET"])
def api_categories():
	data = get_attraction_categories()
	if data == False:
		return jsonify({
			"error": True,
			"message": "Internal Server Error"
			}), 500

	else:
		return jsonify({
			"data" : data
			}), 200