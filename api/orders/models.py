from flask import request
from modules import connect_to_db
from modules.connect_to_db import conn
from modules.create_jwt import decode_token
from datetime import datetime
import requests, json, datetime, random, os, re
from dotenv import load_dotenv

#------------Generate Order Number Randomly-------------
current_date = datetime.datetime.now().strftime("%Y%m%d")

def generate_order_number(current_date):
    suffix = str(random.randint(0, 1000000)).zfill(6)
    return current_date + suffix

#------------post orders data model-------------
def post_orders_data():
    cookiesToken = request.cookies.get("token")
    if cookiesToken == None:
        return False

    try:
        data = request.get_json()
        cookiesToken = request.cookies.get("token")
        decodeToken = decode_token(cookiesToken)
        order_number = generate_order_number(current_date)
        order_price = data["order"]["price"]
        user_id = decodeToken["id"]
        contact_name = data["contact"]["name"]
        contact_email = data["contact"]["email"]
        contact_phone = data["contact"]["phone"]
        if order_number == "" or contact_name == "" or contact_email == "" or contact_phone == "" :
            return "欄位有空"

        if check_contact_name(contact_name) == False:
            return "姓名格式錯誤"

        if check_contact_email(contact_email) == False: 
            return "email格式錯誤"

        if check_contact_phone(contact_phone) == False: 
            return "電話號碼格式錯誤"

        c = conn()
        cur = c.cursor(dictionary=True)
        orders_sql = '''
        INSERT INTO 
            orders(
                order_number,
                order_price,
                user_id,
                contact_name,
                contact_email,
                contact_phone
            )
        VALUES(%s, %s, %s, %s, %s, %s)
        '''
        payment_sql = '''
            INSERT INTO 
            payment(
                order_number,
                payment_status
            )
        VALUES(%s, %s)
        '''
        orders_values = (
            order_number, 
            order_price, 
            user_id, 
            contact_name, 
            contact_email, 
            contact_phone,
            )

        attraction_list = data["order"]["trip"]
        attraction_ids = []
        for attraction in attraction_list:
            attraction_id = attraction["attraction"]["id"]
            attraction_ids.append(attraction_id)

        update_order_number_to_booking_sql = '''
            UPDATE 
                booking  
            SET  
                order_number = %s
            WHERE 
                order_number IS NULL
        '''
        cur.execute(orders_sql, orders_values)
        cur.execute(payment_sql, (order_number, 1))
        cur.execute(update_order_number_to_booking_sql, (order_number,))
        c.commit()
        cur.close()

        payment_result = pay_by_prime_to_TapPay(data)

        if payment_result["status"] == 0:
            update_payment_result = update_payment_details(order_number, payment_result)

            if update_payment_result == True:
                return (True, order_number)

            else:
                return ("付款失敗", order_number)

        else:
            return ("付款失敗", order_number)

    except:
        return "內部伺服器錯誤"

    finally:
        c.close()



#------------Send Request to TapPay-------------
def pay_by_prime_to_TapPay(data):
    load_dotenv()
    partner_key = os.getenv("tapPay_partner_key")
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    pay_by_prime  = {
        "prime": data["prime"],
        "partner_key": partner_key,
        "merchant_id": "ab5661_CTBC",
        "details": "TapPay Test",
        "amount": data["order"]["price"],
        "cardholder": {
            "phone_number": data["contact"]["phone"],
            "name": data["contact"]["name"],
            "email": data["contact"]["email"],
    },
        "remember": True
        }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": partner_key
        }

    response = requests.post(url, data = json.dumps(pay_by_prime), headers = headers)
    payment_result = response.json()
    return payment_result


#------------Update Payment Status and Time-------------
def update_payment_details(order_number, payment_result):
    try:
        c = conn()
        cur = c.cursor()
        update_payment_details_sql = '''
        UPDATE 
            payment  
        SET  
            payment_status = 0,
            msg = %s,
            payment_time = CURRENT_TIMESTAMP,
            transaction_time_millis = %s,
            bank_transaction_id = %s,
            rec_trade_id = %s
        WHERE 
            order_number = %s
        '''
        cur.execute(update_payment_details_sql, 
                        (payment_result["msg"], 
                        payment_result["transaction_time_millis"], 
                        payment_result["bank_transaction_id"], 
                        payment_result["rec_trade_id"], 
                        order_number,)
                    )
        c.commit()
        cur.close()
        return True

    except:
        return False

    finally:
        c.close()


#------------Get OrdersNumber Details model-------------
def get_orderNumber_details(orderNumber):
    cookiesToken = request.cookies.get("token")
    if cookiesToken == None:
        return False

    else:
        try:    
            c = conn()
            cur = c.cursor(dictionary=True)
            get_orderNumber_details_sql = '''
            SELECT 
                user.name,
                user.email,
                attraction.id, 
                attraction.name, 
                attraction.address,  
                attractionimages.images,
                booking.date, 
                booking.time, 
                booking.price,
                orders.order_number,
                orders.contact_name,
                orders.contact_email,
                orders.contact_phone,
                payment.payment_status
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
            INNER JOIN
                attractionimages
            ON
                booking.attractionId = attractionimages.image_id
            INNER JOIN
                orders
            ON
                booking.order_number = orders.order_number
            INNER JOIN
                payment
            ON
                booking.order_number = payment.order_number
            WHERE
                orders.order_number = %s
            GROUP BY booking.booking_id
            '''
            cur.execute(get_orderNumber_details_sql, (orderNumber,))
            query = cur.fetchall()
            if query:
                i = 0
                attraction_list = []
                total_price = 0
                while i < len(query):
                    attraction = {
                        "attraction": {
                            "id": query[i]["id"],
                            "name": query[i]["name"],
                            "address": query[i]["address"],
                            "image": query[i]["images"]
                        },
                        "date": query[i]["date"],
                        "time": query[i]["time"],
                        "price": query[i]["price"],
                    } 
                    attraction_list.append(attraction)
                    total_price += query[i]["price"]
                    i = i + 1
                result = {
                    "data": {
                        "number": query[0]["order_number"],
                        "totalPrice": total_price,
                        "trip": attraction_list,
                        "contact": {
                            "name": query[0]["contact_name"],
                            "email": query[0]["email"],
                            "phone": query[0]["contact_phone"]
                        },
                        "status": query[0]["payment_status"]
                    }
                }
            else:
                result = {
                    "data": None
                }
        finally:
            cur.close()
            c.close()
            
        return result

#------------Get Orders History Details model-------------
def get_orders_history_details(user_id):
    cookiesToken = request.cookies.get("token")
    if cookiesToken == None:
        return False
    
    else:
        try:
            c = conn()
            cur = c.cursor(dictionary=True)
            # get_orders_number_by_user_sql = '''
            # SELECT
            #     order_number
            # FROM
            #     orders
            # WHERE
            #     user_id = %s
            # '''
            # cur.execute(get_orders_number_by_user_sql, (user_id,))
            # orders_number_by_user = cur.fetchall()

            get_orders_history_details_sql = '''
            SELECT 
                user.name,
                user.email,
                attraction.id, 
                attraction.name, 
                attraction.address,  
                attractionimages.images,
                booking.date, 
                booking.time, 
                booking.price,
                orders.order_number,
                orders.order_time,
                orders.contact_name,
                orders.contact_email,
                orders.contact_phone,
                payment.payment_status
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
            INNER JOIN
                attractionimages
            ON
                booking.attractionId = attractionimages.image_id
            INNER JOIN
                orders
            ON
                booking.order_number = orders.order_number
            INNER JOIN
                payment
            ON
                booking.order_number = payment.order_number
            WHERE
                booking.user_id = %s
            GROUP BY 
                booking.booking_id
            ORDER BY 
                orders.order_time DESC
            '''
            cur.execute(get_orders_history_details_sql, (user_id,))
            orders_details = cur.fetchall()
            if orders_details:
                result = {}
                for order in orders_details:
                    order_number = order['order_number']

                    if order_number not in result:
                        result[order_number] = {
                            'number': order_number,
                            'totalPrice': 0,
                            'order_time': order['order_time'],
                            'trip': [],
                            'contact': {
                                'name': order['contact_name'],
                                'email': order['contact_email'],
                                'phone': order['contact_phone']
                            },
                            'status': order['payment_status']
                        }
                        
                    total_price = result[order_number]['totalPrice']
                    total_price += order['price']
                    result[order_number]['totalPrice'] = total_price

                    result[order_number]['trip'].append({
                        'attraction': {
                            'id': order['id'],
                            'name': order['name'],
                            'address': order['address'],
                            'image': order['images']
                        },
                        'date': order['date'],
                        'time': order['time'],
                        'price': order['price']
                    }) 
                new_data = []
                for data in result.items():
                    new_data.append(data[1])
                
                result = {
                    "data": new_data
                }
                
            else:
                result = {
                    "data": None
                } 

        finally:
            cur.close()
            c.close()

        return result

#--------------------function of Rex contact username--------------------
def check_contact_name(contact_name):
    regex = re.compile(r'^[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFFa-zA-Z0-9]+$')
    if not regex.search(contact_name):
        return False

    return True

#--------------------function of Rex contact email--------------------
def check_contact_email(contact_email):
    regex = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
    if not regex.search(contact_email):
      return False
    
    return True

#--------------------function of Rex contact email--------------------
def check_contact_phone(contact_phone):
    regex = re.compile(r"^09\d{8}$")
    if not regex.search(contact_phone):
      return False
    
    return True

