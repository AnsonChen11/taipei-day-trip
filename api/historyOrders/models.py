from flask import request
from modules import connect_to_db
from modules.connect_to_db import conn
from modules.create_jwt import decode_token

def get_auth_data():
    cookiesToken = request.cookies.get("token")
    if cookiesToken == None:
        return False