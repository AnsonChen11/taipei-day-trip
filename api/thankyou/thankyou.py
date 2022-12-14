from flask import Blueprint, render_template, session, request, redirect, url_for
from modules import connect_to_db
from modules.connect_to_db import conn

thankyou = Blueprint(
    'thankyou', __name__,
    static_folder='static',
    template_folder='templates'
    )

@thankyou.route("/thankyou")
def base():
	return render_template("thankyou.html")