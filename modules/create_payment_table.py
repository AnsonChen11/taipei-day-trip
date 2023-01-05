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


def create_table_payment():
  cur = conn.cursor(buffered=True)
  sql_create_table_payment = '''
  CREATE TABLE payment( 
      order_number VARCHAR(255) PRIMARY KEY,
      payment_status VARCHAR(255) NOT NULL, 
      payment_time DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(order_number) REFERENCES orders(order_number)
      )'''
  cur.execute(sql_create_table_payment) 
  print("Create table orders Successfully")
  conn.commit()
  cur.close()
  conn.close()

# create_table_payment()

def insert_table_payment():
  cur = conn.cursor(buffered=True)
  sql_create_table_payment = '''
  INSERT INTO payment( 
      order_number,
      payment_status)
  VALUES('20221220000002', 1)
      '''
  cur.execute(sql_create_table_payment) 
  print("Insert table payment Successfully")
  conn.commit()
  cur.close()
  conn.close()

insert_table_payment()