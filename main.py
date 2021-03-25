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


@bot.message_handler(commands=['1', '2', '3', '4', '5',
                               '6', '7', '8', '9', '10',
                               '11', '12', '13', '14', '15',
                               '16', '17', '18', '19', '20',
                               '21', '22', '23', '24', '25',
                               '26', '27', '28', '29', '30'])
def start_message(message):
    if db_check_user_exist(message.chat.id):
        if db_check_curent_tier(message.chat.id, "PLAY") and \
                3 <= int(message.text[1:]) <= 10:
            db_change_curent_CoP(message.chat.id, message.text[1:])  # Задали кол-во игроков
            db_change_spy_number(message.chat.id, message.text[1:])  # Задали номер шпиона
            ###Задать локацию, исходя из настроек
            # Алгоритм который вычитает -1 каждый раз при нажатии /show
            ### когда доходит до нуля - роли распределены
            bot.send_message(message.chat.id, "Роли распределены" + u'\u2757' +
                             "\nНажмите /show - чтобы увидеть вашу роль\n"
                             "Нажмите /restart - для перезапуска\n",
                             reply_markup=keyboard_show)
            db_change_curent_tier(message.chat.id, message.text[1:])  # меняет на "3", "4", "5" и тд
        elif db_check_curent_tier(message.chat.id, "EDIT_LIST"):
            if not (db_check_jurnal_exist(message.chat.id, message.text[1:])):
                db_insert_jurnal_one(message.chat.id, message.text[1:])  # Вставка записи выключения локации
            else:
                db_delete_from_jurnal_one(message.chat.id, message.text[1:])


@bot.message_handler(commands=['options',
                               'Options'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "START"):
        bot.send_message(message.chat.id, "Настройки:",
                         reply_markup=keyboard_options)
        db_change_curent_tier(message.chat.id, "OPTIONS")


@bot.message_handler(commands=['change_list',
                               'Change_list'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "OPTIONS"):
        bot.send_message(message.chat.id, "Выберите готовый список:",
                         reply_markup=keyboard_change_list)
        db_change_curent_tier(message.chat.id, "CHANGE_LIST")


@bot.message_handler(commands=['list_default', 'List_default',
                               'list_dlc_first(none)', 'List_dlc_first(none)',
                               'list_dlc_second(none)', 'List_dlc_second(none)'
                               ])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "CHANGE_LIST"):
        if message.text.lower()[1:] == "list_default":
            db_change_curent_list(message.chat.id, 1)
        elif message.text.lower()[1:] == "list_dlc_first(none)":
            db_change_curent_list(message.chat.id, 1)  # Временно 1
        elif message.text.lower()[1:] == "list_dlc_second(none)":
            db_change_curent_list(message.chat.id, 1)  # Временно 1
        bot.send_message(message.chat.id, "Готовый список был изменен" + u'\u2757',
                         reply_markup=keyboard_options)
        db_change_curent_tier(message.chat.id, "OPTIONS")


@bot.message_handler(commands=['edit_list',
                               'Edit_list'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "OPTIONS"):
        bot.send_message(message.chat.id, "Текущий список: " + str(db_get_current_list(message.chat.id)),
                         reply_markup=keyboard_edit_list)
        db_change_curent_tier(message.chat.id, "EDIT_LIST")


@bot.message_handler(commands=['remove_all',
                               'Remove_all'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "EDIT_LIST"):
        db_delete_from_jurnal_all(message.chat.id)


@bot.message_handler(commands=['set_all',
                               'Set_all'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "EDIT_LIST"):
        db_delete_from_jurnal_all(message.chat.id)
        db_set_all_jurnal(message.chat.id)


@bot.message_handler(commands=['back',
                               'Back'])
def start_message(message):
    if db_check_user_exist(message.chat.id):
        if db_check_curent_tier(message.chat.id, "PLAY"):
            bot.send_message(message.chat.id, "Текущий список: " +
                             str(db_get_current_list(message.chat.id)),
                             reply_markup=keyboard_default)
            db_change_curent_tier(message.chat.id, "START")

        elif db_check_curent_tier(message.chat.id, "OPTIONS"):
            bot.send_message(message.chat.id, "Текущий список: " +
                             str(db_get_current_list(message.chat.id)),
                             reply_markup=keyboard_default)
            db_change_curent_tier(message.chat.id, "START")

        elif db_check_curent_tier(message.chat.id, "CHANGE_LIST"):
            bot.send_message(message.chat.id, "Настройки:",
                             reply_markup=keyboard_options)
            db_change_curent_tier(message.chat.id, "OPTIONS")

        elif db_check_curent_tier(message.chat.id, "EDIT_LIST"):
            bot.send_message(message.chat.id, "Настройки:",
                             reply_markup=keyboard_options)
            db_change_curent_tier(message.chat.id, "OPTIONS")


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
keyboard_count_player.add(types.KeyboardButton(text="/back"))

# Keyboard show
keyboard_show = types.ReplyKeyboardMarkup(row_width=1)
keyboard_show.add(types.KeyboardButton(text="/Show"))
keyboard_show.add(types.KeyboardButton(text="/Restart"))

# Keyboard hide

# Keyboard options
keyboard_options = types.ReplyKeyboardMarkup(row_width=1)
keyboard_options.add(types.KeyboardButton(text="/Change_list"))
keyboard_options.add(types.KeyboardButton(text="/Edit_list"))
keyboard_options.add(types.KeyboardButton(text="/Back"))

# Keyboard options->change_list
keyboard_change_list = types.ReplyKeyboardMarkup(row_width=1)
keyboard_change_list.add(types.KeyboardButton(text="/List_default"))
keyboard_change_list.add(types.KeyboardButton(text="/List_dlc_first(none)"))
keyboard_change_list.add(types.KeyboardButton(text="/List_dlc_second(none)"))
keyboard_change_list.add(types.KeyboardButton(text="/Back"))

# Keyboard options->edit_list
keyboard_edit_list = types.ReplyKeyboardMarkup(row_width=6)
for j in range(0, 30, 6):
    key_1a = types.KeyboardButton(text="/" + str(j + 1))
    key_2a = types.KeyboardButton(text="/" + str(j + 2))
    key_3a = types.KeyboardButton(text="/" + str(j + 3))
    key_4a = types.KeyboardButton(text="/" + str(j + 4))
    key_5a = types.KeyboardButton(text="/" + str(j + 5))
    key_6a = types.KeyboardButton(text="/" + str(j + 6))
    keyboard_edit_list.add(key_1a, key_2a, key_3a, key_4a, key_5a, key_6a)
key_clear = types.KeyboardButton(text="/remove_all")
key_all = types.KeyboardButton(text="/set_all")
key_back = types.KeyboardButton(text="/back")
keyboard_edit_list.add(key_clear, key_all, key_back)
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
