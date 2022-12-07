import json, mysql.connector, re, os


conn = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "12345678",
  database = "taipeitrip",
  charset = "utf8",
)

cur = conn.cursor(buffered=True)

def create_table_attraction():
    sql_create_table = '''CREATE TABLE attraction(
        id BIGINT PRIMARY KEY AUTO_INCREMENT, 
        name TEXT, 
        category TEXT, 
        description TEXT, 
        address TEXT,
        direction TEXT,
        mrt TEXT,
        lat DOUBLE,
        lng DOUBLE,
        images json)'''

    cur.execute(sql_create_table) 
    print("Create table Successfully")

    with open("taipei-attractions.json", mode = "r", encoding = "utf-8") as f:
        data = json.load(f)

    num = len(data["result"]["results"])
    i = 0
    while i < num:
        name = data["result"]["results"][i]["name"]
        category = data["result"]["results"][i]["CAT"]
        description = data["result"]["results"][i]["description"]
        address = data["result"]["results"][i]["address"]
        transport = data["result"]["results"][i]["direction"]
        mrt = data["result"]["results"][i]["MRT"]
        lat = data["result"]["results"][i]["latitude"]
        lng = data["result"]["results"][i]["longitude"]
        #圖片另外處理
        file = data["result"]["results"][i]["file"]
        imageURL = file.split("https://")
        imageURLList = []
        for j in imageURL[1:]:
            URL = "https://" + j
            if ".jpg" in URL or ".JPG" in URL or ".png" in URL or ".PNG" in URL:
                imageURLList.append(URL)
        images = json.dumps(imageURLList)
        sql_insert = '''INSERT INTO 
                    attraction (name, category, description, address, direction, mrt, lat, lng, images) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        value = (name, category, description, address, transport, mrt, lat, lng, images)
        cur.execute(sql_insert, value)
        i = i + 1

    conn.commit()
    conn.close()


def create_table_attractionImages():
    sql_create_table = '''CREATE TABLE attractionImages(
        id BIGINT PRIMARY KEY AUTO_INCREMENT, 
        image_id BIGINT NOT NULL,
        images TEXT,
        FOREIGN KEY(image_id) REFERENCES attraction(id)
        )'''

    cur.execute(sql_create_table) 
    print("Create table_attractionImages Successfully")

    with open("taipei-attractions.json", mode = "r", encoding = "utf-8") as f:
        data = json.load(f)

    num = len(data["result"]["results"])
    i = 0
    while i < num:
    #處理圖片
        file = data["result"]["results"][i]["file"] #連在一起的URL
        imageURL = file.split("https://")
        for j in imageURL[1:]:
            image_id = i + 1
            images = "https://" + j
            if ".jpg" in images or ".JPG" in images or ".png" in images or ".PNG" in images:
                sql_insert = "INSERT INTO attractionImages (image_id, images) VALUES(%s, %s)"
                value = (image_id, images)
                cur.execute(sql_insert, value)
        i = i + 1

    conn.commit()
    conn.close()

create_table_attractionImages()

# create_table_attraction()