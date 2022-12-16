from flask import Blueprint, render_template, request, jsonify
from .models import *

booking = Blueprint(
    "booking", __name__,
    static_folder = "static",
    template_folder = "templates"
    )

@booking.route("/booking")
def base():
	return render_template("booking.html")

@booking.route("/api/booking", methods = ["GET", "POST", "DELETE"])
def api_booking():
#------------get booking data controller-------------
    if request.method == "GET":
        data = get_booking_data()
        if data == False:
            return jsonify({
                "error": True,
                "message": "未登入系統"
                }), 403

        if data:
            return jsonify({
                "data": data
                }), 200

        if data == None:
            return jsonify({
                "data": None
                }), 200
#------------post booking data controller-------------
    if request.method == "POST":
        data = post_booking_data()
        if data == "建立失敗":
             return jsonify({
                "error": True,
                "message": "建立失敗，請確認是否欄位都有填寫"
                }), 400

        if data == False:
            return jsonify({
                "error": True,
                "message": "未登入系統"
                }), 403

        if data == True:
            return jsonify({
                "data": None
                }), 200

        if data == "內部伺服器錯誤":
            return jsonify({
                "error": True,
                "message": "內部伺服器錯誤"
                }), 500
#------------delete booking data controller-------------
    if request.method == "DELETE":
        data = delete_booking_data()
        if data == False:
            return jsonify({
                "error": True,
                "message": "未登入系統"
                }), 403

        if data == True:
            return jsonify({
                    "ok": True
                    }), 200