#!/usr/bin/python3.3
import config
import database
import telebot
import ast
import time
from telebot import types

bot = telebot.TeleBot(config.token)

## adding user to database at start
@bot.message_handler(commands=['start'])
def start(message):
  database.create_user(message.from_user.username, message.from_user.id)

@bot.message_handler(commands=['listwords'])
def list_words(message):
  user_id = database.get_user_id(message.from_user.id)
  words = database.get_words(user_id)
  markup = types.InlineKeyboardMarkup()
  for word in words:
    markup.add(
      types.InlineKeyboardButton(text=word[1], callback_data= "['tap', '" + str(word[0]) + "', '" + word[1] + "']"),
      types.InlineKeyboardButton(text='DELETE', callback_data= "['delete', '" + str(word[0]) + "', '" + word[1] + "']"))
      # types.InlineKeyboardButton(text='EDIT', callback_data= "['edit', '" + str(word[0]) + "', '" + word[1] + "', '" + str(message.chat.id) + "']"))
  bot.send_message(message.chat.id, 'List of your saved words', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
  actionFromCallBack = ast.literal_eval(call.data)[0]
  idFromCallBack = ast.literal_eval(call.data)[1]
  wordFromCallBack = ast.literal_eval(call.data)[2] 
  # micFromCallBack = ast.literal_eval(call.data)[3]
  if actionFromCallBack == 'delete':
    database.delete_word(idFromCallBack)
    bot.answer_callback_query(callback_query_id=call.id, text="'" + wordFromCallBack + "' deleted")
  # elif actionFromCallBack == 'edit':
  #   bot.send_message(micFromCallBack, "Input new value for '" + wordFromCallBack + "' ")


## saving received word to database
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  database.save_word(message.text, database.get_user_id(message.from_user.id))
  bot.reply_to(message, 'Saved')

while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)  # или просто print(e) если у вас логгера нет,
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)