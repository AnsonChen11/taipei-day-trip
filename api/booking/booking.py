from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from modules import connect_to_db
from modules.create_jwt import make_token, decode_token
from modules.connect_to_db import conn

booking = Blueprint(
    "booking", __name__,
    static_folder = "static",
    template_folder = "templates"
    )

@booking.route("/api/booking", methods = ["GET", "POST", "DELETE"])
def api_booking():
    if request.method == "GET":
        cookiesToken = request.cookies.get("token")
        if cookiesToken == None:
            return jsonify({
                        "error": True,
                        "message": "未登入系統"
                        }), 403
        else:
            try:
                decodeToken = decode_token(cookiesToken)
                c = conn()
                cur = c.cursor()
                sql = '''
                SELECT 
                    user.name,
                    user.email,
                    attraction.id, 
                    attraction.name, 
                    attraction.address, 
                    attraction.images, 
                    booking.date, 
                    booking.time, 
                    booking.price,
                    booking.booking_id
                FROM 
                    booking 
                INNER JOIN 
                    attraction 
                ON 
                    booking.attractionId = attraction.id
                INNER JOIN 
                    user 
                ON 
                    booking.user_id = user.id
                WHERE
                    user.id = %s
                '''
                cur.execute(sql,(decodeToken["id"],))
                query = cur.fetchall()
                if query:
                    i = 0
                    list = []
                    while i < len(query):
                        result = {
                            "attraction": {
                            "id": query[i][2],
                            "name": query[i][3],
                            "address": query[i][4],
                            "image": eval(query[i][5])[0]
                            },
                        "date": query[i][6],
                        "time": query[i][7],
                        "price": query[i][8],
                        "booking_id": query[i][9]
                        } 
                        list.append(result)
                        i = i + 1
                    return jsonify({
                        "data": list
                    }), 200
                else:
                    return jsonify({
                        "data": None
                        }), 200
            finally:
                c.close()

                    
    if request.method == "POST":
        try:
            data = request.get_json()
            cookiesToken = request.cookies.get("token")
            decodeToken = decode_token(cookiesToken)
            c = conn()
            if data["attractionId"] == None or data["date"] == None or data["time"] == None or data["price"] == None:
                return jsonify({
                        "error": True,
                        "message": "建立失敗，請確認是否欄位都有填寫"
                        }), 400
            elif cookiesToken == None:
                return jsonify({
                        "error": True,
                        "message": "未登入系統"
                        }), 403
            else:
                cur = c.cursor()
                sql = "INSERT INTO booking (user_id, attractionId, date, time, price) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(sql, (decodeToken["id"], data["attractionId"], data["date"], data["time"], data["price"],))
                c.commit()
                cur.close()
                return jsonify({
                        "ok": True
                        }), 200
        except:
            return jsonify({
                "error": True,
                "message": "內部伺服器錯誤"
                }), 500
        finally:
            c.close()

    if request.method == "DELETE":
        cookiesToken = request.cookies.get("token")
        if cookiesToken == None:
            return jsonify({
                        "error": True,
                        "message": "未登入系統"
                        }), 403
        else:
            try:
                data = request.get_json()
                c = conn()
                cur = c.cursor()
                sql = "DELETE FROM booking WHERE booking_id = %s"
                cur.execute(sql, (data["booking_id"],))
                c.commit()
                cur.close()
                return jsonify({
                            "ok": True
                            }), 200
            finally:
                c.close()


@booking.route("/booking")
def base():
	return render_template("booking.html")