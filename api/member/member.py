from flask import Blueprint, render_template
from modules import connect_to_db
from modules.connect_to_db import conn

member = Blueprint(
    'member', __name__,
    static_folder='static',
    template_folder='templates'
    )

@member.route("/member")
def base():
	return render_template("member.html")