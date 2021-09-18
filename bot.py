import config
import database
import telebot

bot = telebot.TeleBot(config.token)

database.create_tables()

## adding user to database at start
@bot.message_handler(commands=['start'])
def start(message):
  tg_user_id = message.from_user.id
  user_name = message.from_user.username
  
  database.create_user(user_name, tg_user_id)

## saving received word to database
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  tg_user_id = message.from_user.id
  user_id = database.get_user_id(tg_user_id)
  word = message.text
  
  # word_id = 
  
  # if (word == 't'):
  #   send_today_pull(tg_user_id)
  if (word == 'y'): ##have to add a check if we have unrepeated words
    if (database.has_active_word(user_id) == True):
      bot.send_message(tg_user_id, 'already have an active word')
    elif (database.has_active_word(user_id) == False):
        send_random_word(user_id, tg_user_id)
  elif (word == 'k'):
    active_word_id = database.get_active_word_id(user_id)
    know_word(active_word_id)
    bot.send_message(tg_user_id, 'glad to hear you know the word!')
    if database.has_unrepeated_words:
      send_random_word(user_id, tg_user_id)
    else:
      bot.send_message(tg_user_id, 'all words repeated')
  elif (word == 'd'):
    dont_know_word(user_id)
    bot.send_message(tg_user_id, 'well... we will repeat that one later')
  else:
    database.save_word(word, user_id)
    save_report(word, tg_user_id)
  
  
## report user about saving
def save_report(word, tg_user_id):
  message = "Word '" + word + "' saved."
  bot.send_message(tg_user_id, message)


# ## sending today pull
# def send_today_pull(tg_usr_id):
#   print('test today pull')
#   words_to_send = database.get_today_pull()
#   for x in words_to_send:
#     bot.send_message(tg_usr_id, x)
    
## Y
def send_random_word(usr_id, tg_usr_id):
  id = database.get_random_word_id(usr_id)
  word = database.get_word(id)
  bot.send_message(tg_usr_id, word)
  database.activate_word(id)

def know_word(wrd_id):
  database.level_up(wrd_id)
  database.edit_next_repeat(wrd_id)
  database.deactivate_word(wrd_id)
  database.edit_last_repeat(wrd_id)

def dont_know_word(wrd_id):
  database.level_down(wrd_id)
  database.edit_next_repeat(wrd_id)
  database.deactivate_word(wrd_id)
  database.edit_last_repeat(wrd_id)

## makes the bot works constantly. though i'm not really sure
bot.polling(none_stop=True, interval=0)
