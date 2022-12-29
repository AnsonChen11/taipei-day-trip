from flask import request
from modules import connect_to_db
from modules.connect_to_db import conn
import math
#------------get attraction by page and keywords model-------------
def get_attraction_by_page_and_keyword():
    num = 0
    page = int(request.args.get("page"))
    keyword = request.args.get("keyword")
    if keyword:
        c = conn()
        cur = c.cursor(dictionary=True)
        sql = '''
        SELECT 
            attraction.id, 
            attraction.name,
            attraction.category,
            attraction.description,
            attraction.address,
            attraction.direction,
            attraction.mrt,
            attraction.lat,
            attraction.lng,
        GROUP_CONCAT(attractionimages.images SEPARATOR ',') 
        AS 
            images 
        FROM 
            attraction 
        INNER JOIN attractionimages 
        ON 
            attraction.id = attractionimages.image_id
        WHERE 
            category = %s 
        OR 
            name LIKE '%' %s '%' 
        GROUP BY 
            id 
        LIMIT %s,%s
        ''' #'%' %s '%'中間要空隔
        value = (keyword, keyword, (page * 12), 12)
        cur.execute(sql, value)
        query = cur.fetchall()
        cur.close()

        cur = c.cursor(dictionary=True)
        count_sql = '''
        SELECT COUNT(*) 
        FROM 
            attraction 
        WHERE 
            category = %s 
        OR name LIKE '%' %s '%'
        '''
        value = (keyword, keyword)
        cur.execute(count_sql, value)
        num = cur.fetchone()["COUNT(*)"]
        cur.close()
        c.close()

    else:
        c = conn()
        cur = c.cursor(dictionary=True)
        sql = '''
        SELECT 
            attraction.id, 
            attraction.name,
            attraction.category,
            attraction.description,
            attraction.address,
            attraction.direction,
            attraction.mrt,
            attraction.lat,
            attraction.lng,
        GROUP_CONCAT(attractionimages.images SEPARATOR ',') 
        AS 
            images 
        FROM 
            attraction 
        INNER JOIN 
            attractionimages 
        ON 
            attraction.id = attractionimages.image_id
        GROUP BY 
            id
        LIMIT %s,%s
        '''
        value = ((page * 12), 12)
        cur.execute(sql, value)
        query = cur.fetchall()
        cur.close()
        c.close()

        c = conn()
        cur = c.cursor(dictionary=True)
        count_sql = "SELECT count(*) FROM attraction"
        cur.execute(count_sql)
        num = cur.fetchone()["count(*)"]
        cur.close()
        c.close()

    lastPage = math.ceil(num / 12) #無條件進位
    nextPage = page + 1
    if nextPage >= lastPage:
        nextPage = None

    i = 0 
    list = []
    try:
        while i < len(query): 
            images_list = query[i]["images"].split(",")
            result = {				
                "id" : query[i]["id"],
                "name" : query[i]["name"],
                "category" : query[i]["category"],
                "description" : query[i]["description"],
                "address" : query[i]["address"],
                "transport" : query[i]["direction"],
                "mrt" : query[i]["mrt"],
                "lat" : query[i]["lat"],
                "lng" : query[i]["lng"],
                "images" : images_list
            }
            
            list.append(result)
            i = i + 1
        return (nextPage, list)

    except:
        return "伺服器錯誤"

#--------------------get attraction by id model--------------------
def get_attraction_id(id):
    c = conn()
    cur = c.cursor(dictionary=True)
    sql = '''
    SELECT 
            attraction.id, 
            attraction.name,
            attraction.category,
            attraction.description,
            attraction.address,
            attraction.direction,
            attraction.mrt,
            attraction.lat,
            attraction.lng,
        GROUP_CONCAT(attractionimages.images SEPARATOR ',') 
        AS 
            images 
        FROM 
            attraction 
        INNER JOIN 
            attractionimages 
        ON 
            attraction.id = attractionimages.image_id
        WHERE 
            attraction.id = %s
        GROUP BY 
            id
    '''
    cur.execute(sql, (id,))
    query = cur.fetchone()
    try:
        if query:
            result = {
                    "id" : query["id"],
                    "name" : query["name"],
                    "category" : query["category"],
                    "description" : query["description"],
                    "address" : query["address"],
                    "transport" : query["direction"],
                    "mrt" : query["mrt"],
                    "lat" : query["lat"],
                    "lng" : query["lng"],
                    "images" : query["images"].split(",")
                    }
            return result
        else:
            return False
    except:
        return "伺服器錯誤"
    finally:
        cur.close()
        c.close()

#--------------------get attraction categories list model--------------------
def get_attraction_categories():
    c = conn()
    cur = c.cursor()
    sql = '''SELECT DISTINCT category FROM attraction'''
    cur.execute(sql)
    query = cur.fetchall()
    i = 0
    list = []
    try:
        while i < len(query):
            result = query[i][0]
            list.append(result)
            i = i + 1
        return list
    except:
        return False
    finally:
        cur.close()
        c.close()