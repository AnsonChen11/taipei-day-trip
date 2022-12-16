from flask import request
from modules import connect_to_db
from modules.connect_to_db import conn
from modules.create_jwt import decode_token

#------------get booking data model-------------
def get_booking_data():
    cookiesToken = request.cookies.get("token")
    if cookiesToken == None:
        return False
    else:
        try:
            decodeToken = decode_token(cookiesToken)
            c = conn()
            cur = c.cursor(dictionary=True)
            sql = '''
            SELECT 
                user.name,
                user.email,
                attraction.id, 
                attraction.name, 
                attraction.address, 
                attraction.images, 
                booking.date, 
                booking.time, 
                booking.price,
                booking.booking_id
            FROM 
                booking 
            INNER JOIN 
                attraction 
            ON 
                booking.attractionId = attraction.id
            INNER JOIN 
                user 
            ON 
                booking.user_id = user.id
            WHERE
                user.id = %s
            '''
            cur.execute(sql,(decodeToken["id"],))
            query = cur.fetchall()
            if query:
                i = 0
                list = []
                while i < len(query):
                    result = {
                        "attraction": {
                        "id": query[i]["id"],
                        "name": query[i]["name"],
                        "address": query[i]["address"],
                        "image": eval(query[i]["images"])[0]
                        },
                    "date": query[i]["date"],
                    "time": query[i]["time"],
                    "price": query[i]["price"],
                    "booking_id": query[i]["booking_id"]
                    } 
                    list.append(result)
                    i = i + 1
                return list
            else:
                return None
        finally:
            c.close()

#------------post booking data model-------------
def post_booking_data():               
    if request.method == "POST":
        try:
            data = request.get_json()
            cookiesToken = request.cookies.get("token")
            decodeToken = decode_token(cookiesToken)
            if data["attractionId"] == None or data["date"] == None or data["time"] == None or data["price"] == None:
                return "建立失敗"
            elif cookiesToken == None:
                return False
            else:
                c = conn()
                cur = c.cursor()
                sql = '''
                INSERT INTO 
                    booking (
                        user_id, 
                        attractionId, 
                        date, 
                        time, 
                        price
                        ) 
                    VALUES (%s, %s, %s, %s, %s)'''
                cur.execute(sql, (decodeToken["id"], data["attractionId"], data["date"], data["time"], data["price"],))
                c.commit()
                cur.close()
                return True
        except:
            return "內部伺服器錯誤"
        finally:
            c.close()

#------------delete booking data model-------------
def delete_booking_data():
    if request.method == "DELETE":
        cookiesToken = request.cookies.get("token")
        if cookiesToken == None:
            return False
        else:
            try:
                data = request.get_json()
                c = conn()
                cur = c.cursor()
                sql = '''
                DELETE FROM 
                    booking 
                WHERE 
                    booking_id = %s
                '''
                cur.execute(sql, (data["booking_id"],))
                c.commit()
                cur.close()
                return True
            finally:
                c.close()