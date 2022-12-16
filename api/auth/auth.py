from flask import Blueprint, request, jsonify, make_response
from modules.create_jwt import make_token, decode_token
from flask_bcrypt import Bcrypt
import time, re
from modules import connect_to_db
from modules.connect_to_db import conn


auth = Blueprint(
    "auth", __name__,
    static_folder = "static",
    template_folder = "templates"
    )

#User SignUp
@auth.route("/api/user", methods = ["POST"])
def api_user():
	data = request.get_json()
	if check_username(data["name"]) == False:
		return jsonify({
			"error": True,
			"message": "輸入的名稱格式不正確"
			}), 400
	if check_email(data["email"]) == False:
		return jsonify({
			"error": True,
			"message": "輸入的email格式不正確"
			}), 400
	if check_password(data["password"]) == False:
		return jsonify({
			"error": True,
			"message": "輸入的密碼格式不正確"
			}), 400
	c = conn()
	cur = c.cursor()
	sql = "SELECT email FROM user WHERE email = %s"
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
			bcrypt = Bcrypt()
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

#User Login(PUT method), Login Auth(GET method), Logout(DELETE method)
@auth.route("/api/user/auth", methods = ["GET", "PUT", "DELETE"])
def api_user_auth():
	if request.method == "PUT":
		data = request.get_json()
		if check_email(data["email"]) == False:
			return jsonify({
				"error": True,
				"message": "輸入的email格式不正確"
				}), 400
		if check_password(data["password"]) == False:
			return jsonify({
				"error": True,
				"message": "輸入的密碼格式不正確"
				}), 400
		else:
			c = conn()
			cur = c.cursor()
			sql = "SELECT * FROM user WHERE email = %s"
			cur.execute(sql, (data["email"],))
			query = cur.fetchone()
			cur.close()
			try:
				if query:
					bcrypt = Bcrypt()
					passwordIsVerified = bcrypt.check_password_hash(query[3], data["password"])
					if passwordIsVerified == True:
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


#--------------------function of Rex email--------------------
def check_email(email):
    regex = re.compile (r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
    if not regex.search(email):
      return False
    
    return True

#--------------------function of Rex Password--------------------
def check_password(password):
    regex = re.compile(r'^[a-zA-Z0-9_]+$')
    if not regex.search(password):
        return False

    if len(password) < 6 or len(password) > 20:
        return False

    return True
#--------------------function of Rex username--------------------
def check_username(username):
    regex =  re.compile(r'^[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFFa-zA-Z0-9]+$')
    if not regex.search(username):
        return False

    return True