## Connecting to the database

## importing 'mysql.connector' as mysql for convenient
import mysql.connector as mysql
import random

from datetime import date
today = date.today()

## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'passwd'
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "45a14S24d",
    database = "words_echo_bot"
)
cursor = db.cursor()

## creating tables at start
cursor.execute("CREATE TABLE IF NOT EXISTS words (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, word VARCHAR(255), user_id INT(11), date_added DATE, last_repeat DATE, next_repeat DATE, level INT(11), is_active BOOLEAN DEFAULT false)")
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), tg_user_id BIGINT)")

def create_user(username, tg_user_id):
  query = "INSERT IGNORE INTO users (username, tg_user_id) VALUES (%s, %s)"
  values = (username, tg_user_id)
  cursor.execute(query, values)

def save_word(word, user_id):
  query = "INSERT INTO words (word, user_id, date_added, last_repeat, next_repeat, level) VALUES (%s, %s, %s, %s, %s, %s)"
  values = (word, user_id, today, today, today, 1)
  cursor.execute(query, values)

  db.commit()
  print(cursor.rowcount, "record inserted")

def get_user_id(tg_user_id):
  query = "SELECT id FROM users WHERE tg_user_id = {}".format(tg_user_id)
  db.commit()
  
  cursor.execute(query)
  id = cursor.fetchone()
 
  return id[0]

# def choose_word():
#   random_id = random.randint(1, 6)
#   query = "SELECT word FROM words WHERE id = {}".format(random_id)
#   print(query)
#   cursor.execute(query)
  
#   chosen_id = cursor.fetchone()
#   print(chosen_id[0])
#   return chosen_id[0]

def get_today_pull():
  query = "SELECT word FROM words WHERE next_repeat = '{}'".format(today)
  cursor.execute(query)
  # print(query)
  # print(cursor.fetchall())
  
  today_pull = cursor.fetchall()
  print(today_pull)
  return today_pull
