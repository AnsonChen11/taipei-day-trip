import jwt, datetime, os
from datetime import timedelta
from dotenv import load_dotenv


def token_key():
    load_dotenv()
    key = os.getenv("token")
    return key


def make_token(query):
    key = token_key()
    payload = {
        "id": query[0], 
        "name": query[1], 
        "email": query[2],
        }
    token = jwt.encode(payload, key, algorithm = "HS256")
    return token

def decode_token(cookiesToken):
    key = token_key()
    decodeToken = jwt.decode(cookiesToken, key, algorithms=['HS256'])
    return decodeToken
