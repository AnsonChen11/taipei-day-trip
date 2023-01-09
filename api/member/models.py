from flask import request
from modules import connect_to_db
from modules.connect_to_db import conn

def get_auth_data():
    cookiesToken = request.cookies.get("token")
    if cookiesToken == None:
        return False