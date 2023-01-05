import json, mysql.connector, re, os
from dotenv import load_dotenv

load_dotenv()
conn = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = os.getenv("mysql_password"),
  database = "taipeitrip",
  charset = "utf8",
)


def create_table_orders():
  cur = conn.cursor(buffered=True)
  sql_create_table_orders = '''
  CREATE TABLE orders(
      id BIGINT PRIMARY KEY AUTO_INCREMENT, 
      order_number INT NOT NULL UNIQUE,
      order_price BIGINT NOT NULL,
      user_id BIGINT NOT NULL,
      contact_name VARCHAR(255) NOT NULL, 
      contact_email VARCHAR(255) NOT NULL, 
      contact_phone VARCHAR(255) NOT NULL, 
      order_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(user_id) REFERENCES user(id)
      )'''
  cur.execute(sql_create_table_orders) 
  print("Create table orders Successfully")
  conn.commit()
  cur.close()
  conn.close()

create_table_orders()

