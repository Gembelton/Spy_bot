import telebot, os, logging, flask
from config import TOKEN, APP_NAME
from flask import Flask, request
from telebot import types
from db_functions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'restart',
                               "Start", "Restart"])
def start_message(message):
    if not db_check_user_exist(message.chat.id):
        db_insert_user(message.chat.id)  # Добавляет пользователя и задает ему дефолтный список
        bot.send_message(message.chat.id, "Добро пожаловать" + u'\u2757',
                         reply_markup=keyboard_default)
    else:
        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, "С возвращением" + u'\u2757',
                             reply_markup=keyboard_default)
        elif message.text.lower() == "/restart":
            bot.send_message(message.chat.id, "Перезапуск прошел успешно" + u'\u2757',
                             reply_markup=keyboard_default)
    db_change_curent_tier(message.chat.id, "START")


@bot.message_handler(commands=['exit',
                               'Exit'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "START"):
        bot.send_message(message.chat.id, "Бот выключен" + u'\u2757',
                         reply_markup=keyboard_only_start_button)
        db_change_curent_tier(message.chat.id, "EXIT")


@bot.message_handler(commands=['play',
                               'Play'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "START"):
        bot.send_message(message.chat.id, "Количество игроков" + u'\u2753',
                         reply_markup=keyboard_count_player)
        db_change_curent_tier(message.chat.id, "PLAY")


@bot.message_handler(commands=['3', '4', '5', '6', '7', '8', '9', '10'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "PLAY"):
        db_change_curent_CoP(message.chat.id, message.text[1:])# Задали кол-во игроков
        db_change_spy_number(message.chat.id,message.text[1:]) # Задали номер шпиона

        bot.send_message(message.chat.id, "Роли распределены"+ u'\u2757'+
                                          "\nНажмите /show - чтобы увидеть вашу роль\n"
                                          "Нажмите /restart - для перезапуска\n",
                         reply_markup=keyboard_show)
        db_change_curent_tier(message.chat.id, message.text[1:])# меняет на "3", "4", "5" и тд

###########################################################################

# Default keyboard
keyboard_default = types.ReplyKeyboardMarkup(row_width=1)
key_1 = types.KeyboardButton(text="/Play")
key_2 = types.KeyboardButton(text="/Options")
key_3 = types.KeyboardButton(text="/Exit")
keyboard_default.add(key_1, key_2, key_3)

# Only start button
keyboard_only_start_button = types.ReplyKeyboardMarkup(row_width=1)
keyboard_only_start_button.add(types.KeyboardButton(text="/Start"))

# Keyboard with count of players
keyboard_count_player = types.ReplyKeyboardMarkup(row_width=2)
for i in range(3, 11, 2):
    key_count_1 = types.KeyboardButton(text="/" + str(i))
    key_count_2 = types.KeyboardButton(text="/" + str(i + 1))
    keyboard_count_player.add(key_count_1, key_count_2)  # Для того чтобы кнопки в 2 столбика заносились
keyboard_count_player.add(types.KeyboardButton(text="/Restart"))

# Keyboard show
keyboard_show = types.ReplyKeyboardMarkup(row_width=1)
keyboard_show.add(types.KeyboardButton(text="/Show"))
keyboard_show.add(types.KeyboardButton(text="/Restart"))

###########################################################################
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)


    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://test-new-new.herokuapp.com")
        return "?", 200


    server.run(host="0.0.0.0", port=os.environ.get('PORT', 60))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)

server = flask.Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(
        flask.request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
    return "Hello from Heroku!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
