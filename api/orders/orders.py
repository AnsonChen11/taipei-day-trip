from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from .models import *

orders = Blueprint(
    'orders', __name__,
    static_folder='static',
    template_folder='templates'
    )

@orders.route("/api/orders", methods = ["POST"])
def api_orders():
    data = post_orders_data()
    if data == "欄位有空":
        return jsonify({
            "error": True,
            "message": "建立失敗，請確認是否欄位都有填寫"
        }), 400

    if data == "姓名格式錯誤":
        return jsonify({
            "error": True,
            "message": "建立失敗，姓名不得輸入特殊符號"
        }), 400
        
    if data == "email格式錯誤":
        return jsonify({
            "error": True,
            "message": "建立失敗，請確認email格式是否正確"
        }), 400

    if data == "電話號碼格式錯誤":
        return jsonify({
            "error": True,
            "message": "建立失敗，請確認電話號碼格式是否正確"
        }), 400

    if data == False:
        return jsonify({
            "error": True,
            "message": "未登入系統"
        }), 403

    if data[0] == True:
        return jsonify({
            "data": {
                "number": data[1],
                "payment": {
                    "status": 0,
                    "message": "付款成功"
                }
            }
        }), 200

    if data[0] == "付款失敗":
        return jsonify({
            "data": {
                "number": data[1],
                "payment": {
                    "status": 1,
                    "message": "付款失敗"
                }
            }
        }), 200

    if data == "內部伺服器錯誤":
        return jsonify({
            "error": True,
            "message": "內部伺服器錯誤"
        }), 500


@orders.route("/api/order/<orderNumber>")
def api_order_number(orderNumber):
    orderNumber_details = get_orderNumber_details(orderNumber)
    if orderNumber_details == False:
        return jsonify({
            "error": True,
            "message": "未登入系統"
            }), 403

    return orderNumber_details

@orders.route("/api/orders/<user_id>")
def orders_history(user_id):
    orders_history_details = get_orders_history_details(user_id)
    if orders_history_details == False:
        return jsonify({
            "error": True,
            "message": "未登入系統"
            }), 403

    return orders_history_details