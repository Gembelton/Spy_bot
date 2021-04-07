import telebot
from config import TOKEN
from flask import Flask, request

from telebot import types
from time import sleep
from db_functions import *

from entities.game_lists.list_first_default import List_first_default
from entities.game_lists.list_second_dlc import List_second_dlc

bot = telebot.TeleBot(TOKEN, threaded=False)


@bot.message_handler(commands=['start', 'restart',
                               "Start", "Restart"])
def start_message(message):
    if not db_check_user_exist(message.chat.id):
        db_insert_user(message.chat.id)  # Добавляет пользователя и задает ему дефолтный список
        bot.send_message(message.chat.id,
                         "Добро пожаловать" + u'\u2757\n' + '/Play - начать игру\n'
                                                            '/Options - настройки игры\n'
                                                            '/Rules - правила\n'
                                                            '/Contacts - контакты разработчика\n'
                                                            '/Exit - выход',
                         reply_markup=keyboard_default)
        db_set_field(message.chat.id, "START","curent_tier")
    else:
        if message.text.lower() == "/start":
            bot.send_message(message.chat.id,
                             "С возвращением" + u'\u2757\n' + '/Play - начать игру\n'
                                                              '/Options - настройки игры\n'
                                                              '/Rules - правила\n'
                                                              '/Contacts - контакты разработчика\n'
                                                              '/Exit - выход',
                             reply_markup=keyboard_default)
        elif message.text.lower() == "/restart":
            bot.send_message(message.chat.id,
                             "Перезапуск прошел успешно" + u'\u2757\n' + '/Play - начать игру\n'
                                                                         '/Options - настройки игры\n'
                                                                         '/Rules - правила\n'
                                                                         '/Contacts - контакты разработчика\n'
                                                                         '/Exit - выход',
                             reply_markup=keyboard_default)
        db_clear_user_info(message.chat.id)
    sleep(1)

@bot.message_handler(commands=['exit',
                               'Exit'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "START"):
        bot.send_message(message.chat.id, "Бот выключен" + u'\u2757',
                         reply_markup=keyboard_only_start_button)
        db_clear_user_info(message.chat.id)
        db_set_field(message.chat.id, "EXIT","curent_tier")
    sleep(1)

@bot.message_handler(commands=['play',
                               'Play'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "START"):
        show_list_of_locations_UI(message.chat.id)
        bot.send_message(message.chat.id, "Сколько участников" + u'\u2753\n/Back - назад',
                         reply_markup=keyboard_count_player)
        db_set_field(message.chat.id, "PLAY","curent_tier")
    sleep(1)

@bot.message_handler(commands=['1', '2', '3', '4', '5',
                               '6', '7', '8', '9', '10',
                               '11', '12', '13', '14', '15',
                               '16', '17', '18', '19', '20',
                               '21', '22', '23', '24', '25',
                               '26', '27', '28', '29', '30'])
def start_message(message):

    if db_check_user_exist(message.chat.id):
        number = int(message.text[1:]) - 1

        if db_check_curent_tier(message.chat.id, "PLAY") and \
                3 <= number + 1 <= 10:

            number += 1

            db_set_field(message.chat.id, number,"cop")  # Задали кол-во игроков
            db_set_field(message.chat.id, number,"cop_FINAL") # необходимо для корректного счетчика
            db_set_field(message.chat.id, number,"spy_number")  # Задали номер шпиона
            default_count = [1, 2, 3, 4, 5,
                             6, 7, 8, 9, 10,
                             11, 12, 13, 14,
                             15, 16, 17, 18,
                             19, 20, 21, 22,
                             23, 24, 25, 26,
                             27, 28, 29, 0]  # Вычитание списков друг из друга, чтобы остались разрешенные
            access_locations = list(set(default_count) - set(db_get_all_disabled_from_jurnal(message.chat.id)))

            if not (access_locations):  # Если локаций не выбрано
                bot.send_message(message.chat.id,
                                 "Список локаций пуск, добавьте хотябы 1 локацию" + u'\u2757\n' + '/Play - начать игру\n'
                                                                                                  '/Options - настройки игры\n'
                                                                                                  '/Rules - правила\n'
                                                                                                  '/Contacts - контакты разработчика\n'
                                                                                                  '/Exit - выход',
                                 reply_markup=keyboard_default)
                db_set_field(message.chat.id, "START","curent_tier")
                return 0
            db_set_field(message.chat.id, access_locations,"location")  # задает id локации в бд

            bot.send_message(message.chat.id, "Роли распределены" + u'\u2757' +
                             "\n Игрок " + str(1) + "\n /Show - чтобы увидеть вашу локацию\n"
                                                                " /Restart - для перезапуска\n",
                             reply_markup=keyboard_show)
            db_set_field(message.chat.id, "GIVE_ROLES","curent_tier")
        elif db_check_curent_tier(message.chat.id, "EDIT_LIST"):
            if not (db_check_jurnal_exist(message.chat.id, number)):
                db_insert_jurnal_one(message.chat.id, number)  # Вставка записи выключения локации
            else:
                db_delete_from_jurnal_one(message.chat.id, number)
            bot.delete_message(message.chat.id, message.message_id)  # Удалил цифру
            bot.delete_message(message.chat.id, db_get_field(message.chat.id,"delete_message_id"))  # Удалил таблицу
            db_set_field(message.chat.id,
                                     show_list_of_locations_UI(message.chat.id),"delete_message_id")  # отобразил, и запомнил ее айди
    sleep(1)

@bot.message_handler(commands=['options',
                               'Options'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "START"):
        show_list_of_locations_UI(message.chat.id)
        bot.send_message(message.chat.id, "Настройки:\n"
                                          "/Change_list - изменить список\n"
                                          "/Edit_list - редактировать список\n"
                                          "/Back - назад", reply_markup=keyboard_options)
        db_set_field(message.chat.id, "OPTIONS","curent_tier")
    sleep(1)

@bot.message_handler(commands=['show',
                               'Show'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "GIVE_ROLES"):
        player_number = db_get_field(message.chat.id,"cop_FINAL")-db_decrease_CoP(message.chat.id)


        if db_get_field(message.chat.id,"cop") >= 0:  # Если не 0
            if (db_get_field(message.chat.id,"spy_number")) == player_number:
                caption_text = ("Игрок " + str(player_number) + "\nВаша роль: Шпион \n/Hide - спрятать роль")
                spy_image_path = get_current_list(message.chat.id).spy_location.image
                message_id = bot.send_photo(message.chat.id, photo=open(spy_image_path, "rb"),
                                            caption=caption_text, reply_markup=keyboard_hide).message_id
            else:
                role = get_current_list(message.chat.id).list_of_locations[db_get_field(message.chat.id,"location")]
                caption_text = ("Игрок " + str(player_number) + "\nВаша локация: " + role.name + "\n/Hide - спрятать локацию")
                message_id = bot.send_photo(message.chat.id, photo=open(role.image, "rb"),
                                            caption=caption_text, reply_markup=keyboard_hide).message_id

            db_set_field(message.chat.id, message_id,"delete_message_id")
            db_set_field(message.chat.id, "HIDE_ROLE","curent_tier")
    sleep(1)

@bot.message_handler(commands=['hide',
                               'Hide'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "HIDE_ROLE"):

        player_number = db_get_field(message.chat.id,"cop_FINAL")-db_get_field(message.chat.id,"cop")+1
        if db_get_field(message.chat.id,"cop") > 0:
            bot.send_message(message.chat.id, "Игрок " + str(player_number) + "\n /Show - чтобы увидеть вашу локацию\n"
                                                                              " /Restart - для перезапуска",
                             reply_markup=keyboard_show)
            bot.delete_message(message.chat.id, db_get_field(message.chat.id,"delete_message_id"))
            db_set_field(message.chat.id, "GIVE_ROLES","curent_tier")
        else:
            bot.send_message(message.chat.id, "/Show_results - чтобы узнать результаты",
                             reply_markup=keyboard_result)
            bot.delete_message(message.chat.id, db_get_field(message.chat.id,"delete_message_id"))
            db_set_field(message.chat.id, "SHOW_RESULTS","curent_tier")
    sleep(1)

@bot.message_handler(commands=['show_results',
                               'Show_results'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "SHOW_RESULTS"):
        role = get_current_list(message.chat.id).list_of_locations[db_get_field(message.chat.id,"location")]
        caption_text = "Текущая локация: " + role.name + "\nИгрок " + str(db_get_field(
            message.chat.id,"spy_number")) + ": Шпион\n" \
                                "/Play - начать игру\n" \
                                "/Options - настройки игры\n" \
                                "/Rules - правила\n" \
                                "/Contacts - контакты разработчика\n" \
                                "/Exit - выход"
        bot.send_photo(message.chat.id, photo=open(role.image, "rb"),
                       caption=caption_text, reply_markup=keyboard_default)

        db_clear_user_info(message.chat.id)
    sleep(1)

@bot.message_handler(commands=['change_list',
                               'Change_list'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "OPTIONS"):
        bot.send_message(message.chat.id, "Выбор готового списка" + u'\u2757\n' +
                         "/List_first_default - основной\n"
                         "/List_second_DLC - дополнительный\n"
                         "/List_third_DLC - в разработке\n"
                         "",
                         reply_markup=keyboard_change_list)
        db_set_field(message.chat.id, "CHANGE_LIST","curent_tier")
    sleep(1)

@bot.message_handler(commands=['list_first_default', 'List_first_default',
                               'list_second_DLC', 'List_second_DLC',
                               'list_third_DLC(in progress...)', 'List_third_DLC(in progress...)'
                               ])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "CHANGE_LIST"):
        if message.text.lower()[1:] == "list_first_default":
            db_set_field(message.chat.id, 1,"list_number")
        elif message.text.lower()[1:] == "list_second_dlc":
            db_set_field(message.chat.id, 2,"list_number")

        elif message.text.lower()[1:] == "list_third_dlc(in progress...)":
            db_set_field(message.chat.id, 1,"list_number")  # Временно 1
        bot.send_message(message.chat.id, "Список был изменен" + u'\u2757'+"/Change_list - изменить список\n"
                                          "/Edit_list - редактировать список\n"
                                          "/Back - назад",
                         reply_markup=keyboard_options)
        db_set_field(message.chat.id, "OPTIONS","curent_tier")
    sleep(1)

@bot.message_handler(commands=['edit_list',
                               'Edit_list'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "OPTIONS"):
        bot.send_message(message.chat.id, "Редактирование " + u'\u2757' + "\n/1,/2,.../30 - изменение одной локации"
                                                                          "\n/remove_all - выключить всё"
                                                                          "\n/set_all - включить всё"
                                                                          "\n/back - назад",
                         reply_markup=keyboard_edit_list)
        db_set_field(message.chat.id, show_list_of_locations_UI(message.chat.id),"delete_message_id")
        db_set_field(message.chat.id, "EDIT_LIST","curent_tier")
    sleep(1)

@bot.message_handler(commands=['remove_all',
                               'Remove_all'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "EDIT_LIST"):
        db_delete_from_jurnal_all(message.chat.id)
        db_set_all_jurnal(message.chat.id)
        bot.delete_message(message.chat.id, message.message_id)  # Удалить надпись
        bot.delete_message(message.chat.id, db_get_field(message.chat.id,"delete_message_id"))  # Удалил таблицу
        db_set_field(message.chat.id,
                                 show_list_of_locations_UI(message.chat.id),"delete_message_id")  # отобразил, и запомнил ее айди
    sleep(1)

@bot.message_handler(commands=['set_all',
                               'Set_all'])
def start_message(message):
    if db_check_user_exist(message.chat.id) and \
            db_check_curent_tier(message.chat.id, "EDIT_LIST"):
        db_delete_from_jurnal_all(message.chat.id)
        bot.delete_message(message.chat.id, message.message_id)  # Удалить надпись
        bot.delete_message(message.chat.id, db_get_field(message.chat.id,"delete_message_id"))  # Удалил таблицу
        db_set_field(message.chat.id,
                                 show_list_of_locations_UI(message.chat.id),"delete_message_id")  # отобразил, и запомнил ее айди
sleep(1)

@bot.message_handler(commands=['back',
                               'Back'])
def start_message(message):
    if db_check_user_exist(message.chat.id):
        if db_check_curent_tier(message.chat.id, "PLAY"):
            bot.send_message(message.chat.id, "/Play - начать игру\n"
                                              "/Options - настройки игры\n"
                                              "/Rules - правила\n"
                                              "/Contacts - контакты разработчика\n"
                                              "/Exit - выход",
                             reply_markup=keyboard_default)
            db_set_field(message.chat.id, "START","curent_tier")

        elif db_check_curent_tier(message.chat.id, "OPTIONS"):
            bot.send_message(message.chat.id, "/Play - начать игру\n"
                                              "/Options - настройки игры\n"
                                              "/Rules - правила\n"
                                              "/Contacts - контакты разработчика\n"
                                              "/Exit - выход",
                             reply_markup=keyboard_default)
            db_set_field(message.chat.id, "START","curent_tier")

        elif db_check_curent_tier(message.chat.id, "CHANGE_LIST"):
            bot.send_message(message.chat.id, "Настройки:\n"
                                              "/Change_list - изменить список\n"
                                              "/Edit_list - редактировать список\n"
                                              "/Back - назад", reply_markup=keyboard_options)
            db_set_field(message.chat.id, "OPTIONS","curent_tier")

        elif db_check_curent_tier(message.chat.id, "EDIT_LIST"):
            bot.send_message(message.chat.id, "Настройки:\n"
                                              "/Change_list - изменить список\n"
                                              "/Edit_list - редактировать список\n"
                                              "/Back - назад", reply_markup=keyboard_options)
            db_set_field(message.chat.id, "OPTIONS","curent_tier")
    sleep(1)

@bot.message_handler(commands=['rules',
                               'Rules'])
def start_message(message):
    text = " Правила" + u'\u2757' + "\n" \
                                                       "    1. Для запуска бота необходимо написать /Start в личном сообщений\n" \
                                                       "    2. Чтобы начать, следует написать /Play, после чего ответить боту сколько человек участвует в игре\n" \
                                                       "    3. Далее по очереди будет выдана случайным образом локация, которую необходимо будет запомнить\n" \
                                                       "    4. После запоминания своей роли участником, следует передать доступ к устройству другому игроку для ознакомления со своей локацияю, и так для всех участников\n" \
                                                       "    5. По окончанию раздачи ролей станет доступна кнопка просмотра информации о том, кому среди участников досталась роль шпиона\n" \
                  + u'\u2728' + "Приятной игры" + u'\u2728'

    bot.send_message(message.chat.id, text)
    sleep(1)

@bot.message_handler(commands=['contacts',
                               'Contacts'])
def start_message(message):
    text = "Контакты с разработчиком"+ u'\u2757\n' \
           "Если есть пожелания по улучшению или если найдете баг(описывайте шаги для его воспроизведения) можете написать на удобный вам контакт:\n" \
           "1. VK - https://vk.com/josephgembelton\n" \
           "2. Mail - gembeltonwork@gmail.com\n"\
           "3. Telegram - @super_volodya"

    bot.send_message(message.chat.id, text)
    sleep(1)
###########################################################################

def show_list_of_locations_UI(chat_id):
    current_list = get_current_list(chat_id)
    list_of_disabled = db_get_all_disabled_from_jurnal(chat_id)
    text = ' Текущий список локаций :\n' + current_list.list_name + ' \n' + u'**```\n'
    num = 0
    for i, loc in enumerate(current_list.list_of_locations):
        raznica = 20 - len(str(loc.name))
        current_smile = u'\u2705' if i not in list_of_disabled else u'\u274C'
        if num < 9:
            text += u'{0}. {1}{3}{2:5}\n'.format(str(num + 1), str(loc.name), str(current_smile), (raznica * (" ")))
            num += 1
        elif num >= 9:
            text += u'{0}.{1}{3}{2:5}\n'.format(str(num + 1), str(loc.name), str(current_smile), (raznica * (" ")))
            num += 1
    text += u'```**'
    message_id = bot.send_message(chat_id, text, parse_mode='Markdown').message_id
    return message_id


def get_current_list(chat_id):
    number_of_list = db_get_field(chat_id,"list_number")
    if number_of_list == 1:
        return List_first_default
    elif number_of_list == 2:
        return List_second_dlc


###########################################################################
# Default keyboard
keyboard_default = types.ReplyKeyboardMarkup(row_width=1)
key_1 = types.KeyboardButton(text="/Play")
key_2 = types.KeyboardButton(text="/Options")
key_3 = types.KeyboardButton(text="/Rules")
key_4 = types.KeyboardButton(text="/Contacts")
key_5 = types.KeyboardButton(text="/Exit")
keyboard_default.add(key_1, key_2, key_3, key_4, key_5)

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

# Keyboard results
keyboard_result = types.ReplyKeyboardMarkup(row_width=1)
keyboard_result.add(types.KeyboardButton(text="/Show_results"))

# Keyboard hide
keyboard_hide = types.ReplyKeyboardMarkup(row_width=1)
keyboard_hide.add(types.KeyboardButton(text="/Hide"))
keyboard_hide.add(types.KeyboardButton(text="/Restart"))

# Keyboard options
keyboard_options = types.ReplyKeyboardMarkup(row_width=1)
keyboard_options.add(types.KeyboardButton(text="/Change_list"))
keyboard_options.add(types.KeyboardButton(text="/Edit_list"))
keyboard_options.add(types.KeyboardButton(text="/Back"))

# Keyboard options->change_list
keyboard_change_list = types.ReplyKeyboardMarkup(row_width=1)
keyboard_change_list.add(types.KeyboardButton(text="/List_first_default"))
keyboard_change_list.add(types.KeyboardButton(text="/List_second_DLC"))
keyboard_change_list.add(types.KeyboardButton(text="/List_third_DLC(in progress...)"))
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

#for run on pythonanywhere.com
# bot.remove_webhook()
# sleep(1)
# bot.set_webhook(url='https://gembelton.pythonanywhere.com/') # there username on pytnonanywhere.com
#
# app = Flask(__name__)
#
# @app.route('/', methods=["POST"])
# def webhook():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200
#

# for run on PC
if __name__ == '__main__':
     bot.remove_webhook()
     bot.polling(none_stop=True)