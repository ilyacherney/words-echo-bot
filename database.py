import config
import random
from datetime import date

db = config.database
cursor = config.database.cursor()
today = date.today()


## creating tables at start
def create_tables():
  query_words_table = """
    CREATE TABLE IF NOT EXISTS words (
      id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
      word VARCHAR(255), 
      user_id INT(11), 
      date_added DATE, 
      last_repeat DATE, 
      next_repeat DATE, 
      level INT(11), 
      is_active BOOLEAN DEFAULT false
    )
    """
  cursor.execute(query_words_table)
  
  query_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
      username VARCHAR(255),
      tg_user_id BIGINT
    )
    """
  cursor.execute(query_users_table)

def create_user(username, tg_user_id):
  query = "INSERT IGNORE INTO users (username, tg_user_id) VALUES (%s, %s)"
  values = (username, tg_user_id)
  cursor.execute(query, values)

def save_word(word, user_id):
  query = """
  INSERT INTO words 
    (word, user_id, date_added, last_repeat, next_repeat, level)
    VALUES (%s, %s, %s, %s, %s, %s)
  """
  values = (word, user_id, today, today, today, 1)
  cursor.execute(query, values)
  db.commit()
  print(cursor.rowcount, "word inserted")

def get_user_id(tg_user_id):
  query = "SELECT id FROM users WHERE tg_user_id = {}".format(tg_user_id)
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

def level_down(usr_id):
  query = "UPDATE words SET level = level - 1 WHERE is_active = true AND user_id = {}".format(usr_id)
  cursor.execute(query)
  db.commit()

def activate_word(id):
  query = "UPDATE words SET is_active = true WHERE id = '{}'".format(id)
  cursor.execute(query)
  db.commit()

def deactivate_word():
  query = "UPDATE words SET is_active = false WHERE is_active = true"
  cursor.execute(query)
  db.commit()

def get_today_pull_id(usr_id):
  query = "SELECT id FROM words WHERE next_repeat = '%s' AND user_id = %d" % (today, usr_id)
  cursor.execute(query)
  today_pull = cursor.fetchall()
  return today_pull

def has_active_word():
  query = "SELECT COUNT(id) is_active FROM words WHERE is_active = 1;"
  cursor.execute(query)
  count = cursor.fetchone()[0]

  if (count > 0):
    return True
  else:
    return False
