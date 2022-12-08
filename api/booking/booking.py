from flask import Blueprint, render_template, session, request, redirect, url_for
from modules import connect_to_db
from modules.connect_to_db import conn

booking = Blueprint(
    'booking', __name__,
    static_folder='static',
    template_folder='templates'
    )

@booking.route("/booking")
def base():
	return render_template("booking.html")