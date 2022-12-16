import json, mysql.connector, re, os

conn = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = os.getenv("mysql_password"),
  database = "taipeitrip",
  charset = "utf8",
)

def create_table_user():
  cur = conn.cursor(buffered=True)
  sql_create_table_user = '''CREATE TABLE user(
      id BIGINT PRIMARY KEY AUTO_INCREMENT, 
      name varchar(255) not null, 
      email varchar(255) not null, 
      password varchar(255) not null, 
      time datetime not null default current_timestamp
      )'''
  cur.execute(sql_create_table_user) 
  print("Create table user Successfully")
  conn.commit()
  cur.close()
  conn.close()

def insert_table_user():
  cur = conn.cursor(buffered=True)
  sql_insert_table_user = "INSERT INTO user(name, email, password) values('testname', 'test@gmail.com', 'testpassword')"
  cur.execute(sql_insert_table_user) 
  print("Insert value user Successfully")
  conn.commit()
  cur.close()
  conn.close()

# create_table_user()
insert_table_user()
