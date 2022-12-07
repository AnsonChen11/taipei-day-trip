import os, jwt, datetime
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("token_key")


def make_token(query):
    key = "AE2BF4465C7E95B4703779787616BBF1A8DE1C8D23A4755F3BA663DB9DE8E18F"
    expiretime = datetime.utcnow() + timedelta(days = 7) 
    payload = {
        "id": query[0], 
        "name": query[1], 
        "email": query[2],
        "exp": expiretime,
        }
    token = jwt.encode(payload, key, algorithm = "HS256")
    return token
    

def decode_token(cookiesToken):
    key = "AE2BF4465C7E95B4703779787616BBF1A8DE1C8D23A4755F3BA663DB9DE8E18F"
    decodeToken = jwt.decode(cookiesToken, key, algorithms=['HS256'])
    return decodeToken
