import random
from telebot.types import Message
import database
import telebot;

bot = telebot.TeleBot('1996263018:AAG3t3kljK3R_9GEBBtkskYC3kLrf-wjV0I');

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
  word = message.text;
  
  if (word == 't'):
    send_today_pull(tg_user_id)
  elif (word == 'y'):
    send_random_word(tg_user_id)
  else:
    database.save_word(word, user_id)
    save_report(word, tg_user_id)
  
  
## report user about saving
def save_report(word, tg_user_id):
  message = "Word '" + word + "' saved."
  bot.send_message(tg_user_id, message)


## sending today pull
def send_today_pull(tg_usr_id):

  print('test today pull')
  words_to_send = database.get_today_pull()
  for x in words_to_send:
    bot.send_message(tg_usr_id, x)
    
def send_random_word(tg_usr_id):
  word_to_send = database.get_today_pull()
  rndm = random.choice (word_to_send)
  print(rndm)
  bot.send_message(tg_usr_id, rndm)

## makes the bot works constantly. though i'm not really sure
bot.polling(none_stop=True, interval=0)
