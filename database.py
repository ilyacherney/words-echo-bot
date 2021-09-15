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
  id = cursor.fetchone()[0]
 
  return id

def get_random_word_id(usr_id):
  random_id = random.choice(get_today_pull_id(usr_id))[0]
  print(random_id)
  return random_id

def get_word(id):
  query = "SELECT word FROM words WHERE id = '{}'".format(id)
  cursor.execute(query)
  word = cursor.fetchone()[0]
  print(word)
  return word

def level_up(usr_id):
  query = "UPDATE words SET level = level + 1 WHERE is_active = true AND user_id = {}".format(usr_id)
  cursor.execute(query)
  db.commit()
  print(query)

def level_down(usr_id):
  query = "UPDATE words SET level = level - 1 WHERE is_active = true AND user_id = {}".format(usr_id)
  cursor.execute(query)
  db.commit()
  print(query)

def activate_word(id):
  query = "UPDATE words SET is_active = true WHERE id = '{}'".format(id)
  cursor.execute(query)
  db.commit()
  print(query)

def deactivate_word():
  query = "UPDATE words SET is_active = false WHERE is_active = true"
  cursor.execute(query)
  db.commit()
  print(query)
 
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

def get_today_pull_id(usr_id):
  query = "SELECT id FROM words WHERE next_repeat = '%s' AND user_id = %d" % (today, usr_id)
  print(query)
  cursor.execute(query)
  # print(cursor.fetchall())
  
  today_pull = cursor.fetchall()
  print(today_pull)
  return today_pull

def has_active_word():
  query = "SELECT COUNT(id) is_active FROM words WHERE is_active = 1;"
  cursor.execute(query)
  count = cursor.fetchone()[0]

  if (count > 0):
    return True
  else:
    return False
  

# get_random_word()
print(has_active_word())
# get_word(get_random_word_id())
# activate_word(2)
# deactivate_word(1)