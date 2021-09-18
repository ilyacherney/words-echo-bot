import config
import random
from datetime import date

db = config.database
cursor = config.database.cursor()
today = date.today()
interval_1 = 1
interval_2 = 2
interval_3 = 3

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

def get_active_word_id(usr_id):
  query = "SELECT id FROM words WHERE user_id = %d AND is_active = 1" % (usr_id)
  cursor.execute(query)
  id = cursor.fetchone()[0]
  print(id)
  return id

def level_up(wrd_id):
  query = "UPDATE words SET level = level + 1 WHERE id = %d" % (wrd_id)
  cursor.execute(query)
  db.commit()

def level_down(wrd_id):
  query = "UPDATE words SET level = level - 1 WHERE id = %d" % (wrd_id)
  cursor.execute(query)
  db.commit()

def activate_word(id):
  query = "UPDATE words SET is_active = true WHERE id = '{}'".format(id)
  cursor.execute(query)
  db.commit()

def deactivate_word(wrd_id):
  query = "UPDATE words SET is_active = false WHERE id = %d" % (wrd_id)
  cursor.execute(query)
  db.commit()

def get_today_pull_id(usr_id):
  query = "SELECT id FROM words WHERE next_repeat = '%s' AND user_id = %d" % (today, usr_id)
  cursor.execute(query)
  today_pull = cursor.fetchall()
  return today_pull

def has_active_word(usr_id):
  query = "SELECT COUNT(id) is_active FROM words WHERE is_active = 1 AND user_id = %d" % (usr_id)
  cursor.execute(query)
  count = cursor.fetchone()[0]
  if (count > 0):
    return True
  else:
    return False

def has_unrepeated_words(usr_id):
  query = "SELECT COUNT(id) is_active FROM words WHERE next_repeat = '%s' AND user_id = %d" % (today, usr_id)
  cursor.execute(query)
  count = cursor.fetchone()[0]
  if (count > 0):
    print('true')
    return True
  else:
    print('false')
    return False

def count_urepeated_words(usr_id):
  query = "SELECT COUNT(id) is_active FROM words WHERE next_repeat = '%s' AND user_id = %d" % (today, usr_id)
  cursor.execute(query)
  count = cursor.fetchone()[0]
  return count

def edit_next_repeat(wrd_id):
  
  level = get_level(wrd_id)
  if level == 1:
    interval = interval_1
  elif level == 2:
    interval = interval_2
  elif level == 3:
    interval = interval_3
  elif level > 3:
    interval = 5
  elif level < 1:
    interval = 0

  query = "UPDATE words SET next_repeat = date_add(curdate(), interval %d day) WHERE id = %d" % (interval, wrd_id)
  print(query)
  cursor.execute(query)
  db.commit()

def get_level(wrd_id):
   query = "SELECT level FROM words WHERE id = %d" % (wrd_id)
   cursor.execute(query)
   level = cursor.fetchone()[0]
   return level

def edit_last_repeat(wrd_id):
  query = "UPDATE words SET last_repeat = curdate() WHERE id = %d" % (wrd_id)
  cursor.execute(query)
  db.commit()


has_unrepeated_words(1)