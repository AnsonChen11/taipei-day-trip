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

