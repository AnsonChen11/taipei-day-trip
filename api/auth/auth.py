from flask import Blueprint, request, jsonify, make_response
from .models import *

auth = Blueprint(
    "auth", __name__,
    static_folder = "static",
    template_folder = "templates"
    )

#--------------------signup user controller--------------------
@auth.route("/api/user", methods = ["POST"])
def api_user():
	data = signup_user()
	if data == "輸入的名稱格式不正確":
		return jsonify({
            "error": True,
            "message": "輸入的名稱格式不正確"
            }), 400 

	if data == "輸入的email格式不正確":
		return jsonify({
            "error": True,
            "message": "輸入的email格式不正確"
            }), 400

	if data == "輸入的密碼格式不正確":
		return jsonify({
            "error": True,
            "message": "輸入的密碼格式不正確"
            }), 400

	if data == False:
		return jsonify({
			"error": True,
			"message": "該email已被註冊"
			}), 400

	if data == True:
		return jsonify({
			"ok": True
			}), 200
	
	if data == "伺服器內部錯誤":
		return jsonify({
            "error": True,
            "message": "伺服器內部錯誤"
            }), 500


#--------------------login controller--------------------
@auth.route("/api/user/auth", methods = ["GET", "PUT", "DELETE"])
def api_user_auth():
	if request.method == "PUT":
		data = user_login()
		print(data)
		if data[0] == True:
			return data[1]

		if data == "輸入的email格式不正確":
			return jsonify({
				"error": True,
				"message": "輸入的email格式不正確"
				}), 400

		if data == "輸入的密碼格式不正確":
			return jsonify({
				"error": True,
				"message": "輸入的密碼格式不正確"
				}), 400

		if data == "帳號或密碼錯誤":
			return jsonify({
				"error": True,
				"message": "帳號或密碼錯誤"
				}), 400

		if data == "伺服器內部錯誤":
			return jsonify({
				"error": True,
				"message": "伺服器內部錯誤"
				}), 500

#--------------------auth login controller--------------------
	if request.method == 'GET':
		data = user_auth()

		if data == None:
			return jsonify({
				"data": None
			}), 200

		if data:
			return jsonify({
            	"data": data
        	})
#--------------------logout model controller--------------------		
	if request.method == "DELETE":
		return user_logout()


