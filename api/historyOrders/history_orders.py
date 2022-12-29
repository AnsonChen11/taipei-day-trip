from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from modules import connect_to_db
from modules.connect_to_db import conn
from .models import *

history_orders = Blueprint(
    'history_orders', __name__,
    static_folder='static',
    template_folder='templates'
    )

@history_orders.route("/historyOrders")
def base():
    data = get_auth_data()
    if data == False:
        return render_template("index.html")

    return render_template("historyOrders.html")