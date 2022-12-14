import json, mysql.connector, re, os

conn = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "12345678",
  database = "taipeitrip",
  charset = "utf8",
)

def create_table_booking():
  cur = conn.cursor(buffered=True)
  sql_create_table_booking = '''CREATE TABLE booking(
      booking_id BIGINT PRIMARY KEY AUTO_INCREMENT, 
      user_id BIGINT NOT NULL,
      attractionId BIGINT NOT NULL, 
      date DATE NOT NULL, 
      time VARCHAR(255) NOT NULL, 
      price BIGINT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES user(id),
      FOREIGN KEY(attractionId) REFERENCES attraction(id)
      )'''
  cur.execute(sql_create_table_booking) 
  print("Create table booking Successfully")
  conn.commit()
  cur.close()
  conn.close()

def insert_table_booking():
  cur = conn.cursor(buffered=True)
  sql_insert_table_booking = "INSERT INTO booking(user_id, attractionId, date, time, price) values(13, 1, '2022-12-31', 'afternoon', 2500)"
  cur.execute(sql_insert_table_booking) 
  print("Insert value booking Successfully")
  conn.commit()
  cur.close()
  conn.close()

# create_table_booking()
insert_table_booking()
