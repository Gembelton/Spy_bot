import telebot, copy, time,os
from entities.chat_main import Chat_main
from entities.player import Player
from entities.game_lists.list_main import List_main
from entities.game_lists.list_dlc_1 import List_dlc_1
from flask import Flask, request
import logging
from telebot import types
TOKEN = '1325565413:AAHPO5MfJDdkUh4DiokDnZrKq8xMF36JGiE'
bot = telebot.TeleBot(TOKEN)

all_chat_list = []

current_chat = None
current_user = None
global admin_kakoy_confi, help_list, spy_kakoy_confi, help_list_spy
admin_kakoy_confi = {'admin_id': 0, 'chat_id': 0, 'confa': True}
help_list = []
spy_kakoy_confi = {'spy_id': 0, 'chat_id': 0}
help_list_spy = []


@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        online = False if message.chat.id == message.from_user.id else True  # Если боту в личку написать то будет офлайн игра

        if not message.chat.id == message.from_user.id:  # Если онлайн
            if message.from_user.username == None:
                bot.send_message(message.chat.id,
                                 u'\u2757' + "У вас не указано имя пользователя (username) в настройках аккаунта\n Задайте и попробуйте еще раз")
                return 0
            current_user = (bot.get_chat_member(message.chat.id, message.from_user.id))  # текущий пользователь
            if current_user.status == "creator" or current_user.status == 'administrator':
                """Описание бота, начальная команда для запуска"""
                if not bot.get_chat_members_count(message.chat.id)  <= 2: #####
                    current_chat = Chat_main(True,  # Чат начат
                                             message.chat.id,  # айди чата
                                             message.chat.title,  # Название
                                             online)  # Тип игры (онлайн/офлайн)

                    current_list = (List_main())  # создание объекта
                    current_list.fill_lications()  # заполнение локаций
                    current_chat.current_object_of_roles = current_list  # задать текущий список

                    if any(message.chat.id == chat.chat_id for chat in all_chat_list):
                        for id, chat in enumerate(all_chat_list):
                            if chat.chat_id == message.chat.id:  # Перезаписать конфу
                                # all_chat_list[id].chat_id = current_chat.chat_id
                                # all_chat_list[id].list_of_players = []
                                bot.send_message(message.chat.id, u'\u2757' + "Бот уже запущен")

                    else:
                        all_chat_list.append(current_chat)

                        for i in all_chat_list:
                            if i.chat_id == message.chat.id:
                                bot.send_message(i.chat_id,
                                                 "Добро пожаловать в игру Шпион [онлайн]\nДля игры с нескольких устройств")
                                send_list_of_locations(i.current_object_of_roles, i.chat_id, True)
                                send_all_users_buttons_for_commands(i, "~Выбор команды: ~")

                        return 0
                else:
                    bot.send_message(message.chat.id,
                                     u'\u2757' + "Минимальное кол-во игроков должно быть 3 или больше для игры в группе")
                    return 0
            else:
                bot.send_message(message.chat.id,
                                 u'\u2757' + "@" + message.from_user.username + ", у вас нет прав создателя группы или администратора")
                return 0
        else:
            if not any(message.chat.id == i.chat_id for i in all_chat_list):
                current_chat = Chat_main(True,  # Чат начат
                                         message.chat.id,  # айди чата
                                         "офлайн режима",  # Название
                                         online)  # Тип игры (онлайн/офлайн)

                current_list = (List_main())  # создание объекта
                current_list.fill_lications()  # заполнение локаций
                current_chat.current_object_of_roles = current_list  # задать текущий список

                all_chat_list.append(current_chat)
                for i in all_chat_list:
                    if i.chat_id == current_chat.chat_id:
                        send_all_users_buttons_for_commands(i,
                                                            "Добро пожаловать в игру Шпион [офлайн]\nДля игры с одного устройства")
                        send_list_of_locations(i.current_object_of_roles, i.chat_id, True)
                        return 0

            if any(message.chat.id == chat.chat_id for chat in all_chat_list):
                for id, chat in enumerate(all_chat_list):
                    if chat.chat_id == message.chat.id:  # Перезаписать конфу
                        # all_chat_list[id] = current_chat
                        bot.send_message(message.chat.id, u'\u2757' + "Бот уже запущен")





    except:

        time.sleep(2)


@bot.message_handler(commands=['restart'])
def start_message_restart(message):
    time.sleep(2)
    try:
        for i in all_chat_list:
            if message.from_user.username == None:
                bot.send_message(i.chat_id,
                                 u'\u2757' + "У вас не указано имя пользователя (username) в настройках аккаунта\n Задайте и попробуйте еще раз")
                time.sleep(2)
                return 0
            if i.id_of_kills_buttons_message != None:
                bot.delete_message(i.chat_id, i.id_of_kills_buttons_message)
                i.id_of_kills_buttons_message = None
            if i.chat_id == message.chat.id:
                current_user = (bot.get_chat_member(message.chat.id, message.from_user.id))  # текущий пользователь
                if current_user.status == "creator" or current_user.status == 'administrator':
                    for i in all_chat_list:
                        if i.chat_id == message.chat.id and i.game_for_online:  # Найти игру
                            if any(message.chat.id == chat.chat_id for chat in all_chat_list):
                                for id, chat in enumerate(all_chat_list):
                                    if chat.chat_id == message.chat.id:  # Перезаписать конфу
                                        all_chat_list[id].list_of_players = []
                                        send_list_of_locations(i.current_object_of_roles, i.chat_id, True)
                                        all_chat_list[id].current_location = ""
                                        all_chat_list[id].game_begin = False
                                        bot.send_message(message.chat.id, "Ручной рестарт [онлайн] прошел успешно!\n"
                                                                          "Количество текущих игроков : " + str(
                                            bot.get_chat_members_count(i.chat_id) - 1))
                                        send_all_users_buttons_for_commands(i, "~Выбор команды: ~")
                                        time.sleep(2)
                                        return 0

                if current_user.status == "member":
                    for i in all_chat_list:
                        if i.chat_id == message.chat.id and not i.game_for_online:  # Найти игру офлайн
                            i.game_begin = False
                            i.list_of_players = []
                            bot.send_message(message.chat.id, "Ручной рестарт [офлайн] прошел успешно!")
                            send_list_of_locations(i.current_object_of_roles, i.chat_id, True)
                            send_all_users_buttons_for_commands(i, "~Выбор команды: ~")
                            return 0
                        elif i.chat_id == message.chat.id and i.game_for_online:  # Найти игру офлайн
                            bot.send_message(message.chat.id,
                                             u'\u2757' + "@" + message.from_user.username + ", у вас нет прав создателя группы или администратора")
                            time.sleep(2)
                            return 0
        else:
            bot.send_message(message.chat.id,
                             u'\u2757' + "Бот не запущен!\nCоздателю(restart) группы или администратору необходимо запустить бота командой /start")
    except:
        time.sleep(2)


def send_for_spy_list_of_lications(from_user_id, message, current_list):
    """Отправка шпиону списка локаций и кнопок"""
    try:
        key = types.InlineKeyboardMarkup()
        for id, i in enumerate(current_list.list_of_location):
            if id == len(current_list.list_of_location) / 2:
                break
            if not i.in_game:
                text_1 = '\u0336'.join((str(id)) + ". " + i.name)
            else:
                text_1 = str(id) + ". " + i.name
            if not current_list.list_of_location[id + 15].in_game:
                text_2 = '\u0336'.join((str(id + 15)) + ". " + current_list.list_of_location[id + 15].name)
            else:
                text_2 = str(id + 15) + ". " + current_list.list_of_location[id + 15].name

            key_start = types.InlineKeyboardButton(text=text_1, callback_data="spy_list_" + str(id))
            key_start1 = types.InlineKeyboardButton(text=text_2, callback_data="spy_list_" + str(id + 15))
            key.add(key_start, key_start1)
        bot.send_message(from_user_id, "Список локаций: " + message.chat.title, reply_markup=key)
        time.sleep(2)
    except:

        time.sleep(2)


def send_list_of_locations(current_list_object, chat_id, need_pin):
    try:
        text = " Текущий список локаций :\n[" + current_list_object.list_name + "]" + "\n" + u'**```\n'

        num = 0
        for j in current_list_object.list_of_location:
            # text += str(num) + ". " + str(j.name) + "            " +str(j.ingame)+"\n"
            raznica = 20 - len(str(j.name))
            current_smile = u'\u2705' if j.in_game else u'\u274C'
            if num <= 9:
                text += u'{0}. {1}{3}{2:5}\n'.format(str(num), str(j.name), str(current_smile), (raznica * (" ")))
                num += 1
            elif num >= 10:
                text += u'{0}.{1}{3}{2:5}\n'.format(str(num), str(j.name), str(current_smile), (raznica * (" ")))
                num += 1
        text += u'```**'

        message_id = bot.send_message(chat_id, text, parse_mode='Markdown').message_id

        if need_pin:
            try:

                bot.pin_chat_message(chat_id, message_id)

                return message_id
            except:
                bot.send_message(chat_id, "Для большего удобства, предоставьте боту права администратора")
                return message_id
        else:
            return message_id
    except:
        bot.send_message(chat_id, u'\u2757' + "Слишком много запросов в секунду\nПовторите введенную команду")
        time.sleep(2)


@bot.message_handler(commands=['ready'])
def start_message(message):
    try:
        for i in all_chat_list:
            if i.chat_id == message.chat.id and i.game_for_online:  # Найти игру
                if message.from_user.username == None:
                    bot.send_message(i.chat_id,
                                     u'\u2757' + "У вас не указано имя пользователя (username) в настройках аккаунта\n Задайте и попробуйте еще раз")

                    return 0
                if any(message.from_user.id == player.id for player in i.list_of_players):  # Найти человека
                    bot.send_message(i.chat_id,
                                     u'\u2757' + "@" + message.from_user.username + ", вы уже готовы")  # Если уже писал /ready и добавлен в список участников
                    break
                else:  # Если нет
                    current_user = (bot.get_chat_member(message.chat.id, message.from_user.id))  # создать пользователя
                    status = 'admin' if current_user.status == "creator" or current_user.status == 'administrator' else 'user'
                    current_user = Player(message.from_user.id,
                                          message.from_user.username,
                                          status=status)
                    i.list_of_players.append(current_user)  # Поместить в список
                    count_of_players = bot.get_chat_members_count(message.chat.id)
                    string = "@" + message.from_user.username + " приготовился,\n" + "готово " + str(
                        len(i.list_of_players)) + " из " + str(
                        count_of_players - 1) + " игроков"

                    bot.send_message(i.chat_id, string)  # Сказать сколько не готовых

                    if len(i.list_of_players) == count_of_players - 1:  # Если кол-во игроков заполненно
                        i.get_roles()  # раздать текущие роли
                        i.game_begin = True  # зарегистрировать начало игры
                        send_list_of_locations(i.current_object_of_roles, i.chat_id, True)
                        bot.send_message(i.chat_id, "Игра началась!")

                        send_all_users_buttons_for_vote(i)
                        time.sleep(2)
                        for j in i.list_of_players:  # каждому игроку
                            try:
                                caption = "В группе: " + str(i.chat_name) + "\nВаша локация: " + str(j.current_role.name)
                                bot.send_photo(j.id, photo=open(j.current_role.image, "rb"),
                                               caption=caption)  # выслать картинку

                                time.sleep(2)
                                if j.current_role.name == "Шпион":
                                    send_for_spy_list_of_lications(j.id, message, i.current_object_of_roles)
                                    spy_kakoy_confi['spy_id'] = j.id
                                    spy_kakoy_confi['chat_id'] = i.chat_id
                                    help_list_spy.append(copy.deepcopy(spy_kakoy_confi))
                                    time.sleep(2)
                            except telebot.apihelper.ApiException:
                                bot.send_message(i.chat_id, u'\u2757' + "Все игроки должны начать диаолог с ботом!")
                                time.sleep(2)
                                return 0
                            except AttributeError:
                                print(AttributeError)
                                bot.send_message(i.chat_id,
                                                 u'\u2757' + "Не выбрано ни одной локации!\nНапишите /restart и выберите в меню админа минимум 1 локацию")
                                time.sleep(2)
                                return 0

                        time.sleep(2)
                        break
                    else:  # Не регистрировать игру, если остались неготовые люди

                        break
        else:  # Для офлайн игры
            for i in all_chat_list:
                if i.chat_id == message.chat.id and not i.game_for_online and not i.game_begin:
                    bot.send_message(i.chat_id, "*Офлайн игра готова*", parse_mode='Markdown')
                    i.game_begin = True
                    send_solo_user_buttons(i)

                    break
                elif i.game_begin and not i.game_for_online:
                    bot.send_message(i.chat_id, "Игра уже идет")
                    break

            else:
                bot.send_message(message.chat.id,
                                 u'\u2757' + "Бот не запущен!\nCоздателю(ready) группы или администратору необходимо запустить бота командой /start")
    except:

        time.sleep(2)


chat_id = None


def send_all_users_buttons_for_vote(current_chat):
    try:
        key = types.ReplyKeyboardMarkup()
        for player in current_chat.list_of_players:
            key_start = types.KeyboardButton(text="/kill @" + str(player.name))
            key.add(key_start)
        time.sleep(2)
        current_chat.id_of_kills_buttons_message = (
            bot.send_message(current_chat.chat_id, "~Проголосовать за: ~", reply_markup=key)).message_id
    except:
        bot.send_message(current_chat.chat.id,
                         u'\u2757' + "Слишком много запросов в секунду\nПовторите введенную команду")
        time.sleep(2)


def send_all_users_buttons_for_commands(current_chat, hello_text):
    try:
        key = types.ReplyKeyboardMarkup()
        key_start = types.KeyboardButton(text="/start")
        key.add(key_start)
        key_ready = types.KeyboardButton(text="/ready")
        key.add(key_ready)
        key_restart = types.KeyboardButton(text="/restart")
        if current_chat.game_for_online:
            key_admin = types.KeyboardButton(text="/admin")
        else:
            key_admin = types.KeyboardButton(text="/Админ меню")
        ######
        key_rules = types.KeyboardButton(text="/rules")
        key.add(key_rules)
        key_contacts = types.KeyboardButton(text="/contacts")
        key.add(key_admin)
        key.add(key_restart)
        key.add(key_contacts)

        bot.send_message(current_chat.chat_id, hello_text, reply_markup=key)
    except:
        bot.send_message(current_chat.chat.id,
                         u'\u2757' + "Слишком много запросов в секунду\nПовторите введенную команду")
        time.sleep(2)


@bot.message_handler(commands=["kill"])
def start_message(message):
    try:
        time.sleep(2)
        for i in all_chat_list:
            if i.chat_id == message.chat.id and i.game_for_online and i.game_begin and message.text != "/kill":
                for j in i.list_of_players:
                    if message.from_user.id == j.id:
                        name = message.text[message.text.find(" ") + 2:]
                        if name != j.name:
                            j.vote = name
                            res = i.kill_guy()
                            time.sleep(2)
                            if res[0] == "mir":
                                bot.send_message(i.chat_id, "Игрок @" + res[2] + " не шпион :(")
                                time.sleep(2)
                                if len(i.list_of_players) == 2:
                                    send_all_users_buttons_for_vote(i)
                                    loc_string = "[Текущая локация: " + i.current_location + "]"
                                    type_of_loose_string = "*Шпион выйграл оставшись 1 на 1!*"
                                    for spy in i.list_of_players:
                                        if spy.current_role.name == "Шпион":
                                            time.sleep(2)
                                            spy_string = "[Шпионом был: @" + spy.name + "]"
                                            bot.send_message(i.chat_id, (
                                                    type_of_loose_string + "\n" + spy_string + "\n" + loc_string + "\n"),
                                                             parse_mode='Markdown')
                                    time.sleep(2)
                                    i.list_of_players = []
                                    bot.delete_message(i.chat_id, i.id_of_kills_buttons_message)
                                    i.id_of_kills_buttons_message = None
                                    send_all_users_buttons_for_commands(i, "~Выбор команды: ~")
                                    time.sleep(2)
                                else:

                                    send_all_users_buttons_for_vote(i)
                            elif res[0] == "spy":
                                send_all_users_buttons_for_vote(i)
                                time.sleep(2)
                                loc_string = "[Текущая локация: " + i.current_location + "]"
                                type_of_loose_string = "*Шпиона нашли!*"
                                for spy in i.list_of_players:
                                    if spy.current_role.name == "Шпион":
                                        time.sleep(2)
                                        spy_string = "[Шпионом был: @" + spy.name + "]"
                                        bot.send_message(i.chat_id,
                                                         type_of_loose_string + "\n" + spy_string + "\n" + loc_string + "\n",
                                                         parse_mode="Markdown")
                                        break
                                i.list_of_players = []
                                time.sleep(2)
                                bot.delete_message(i.chat_id, i.id_of_kills_buttons_message)
                                i.id_of_kills_buttons_message = None
                                send_all_users_buttons_for_commands(i, "~Выбор команды: ~")
                                time.sleep(2)
                                break


                        else:
                            bot.send_message(i.chat_id, "@" + j.name + " за себя голосовать нельзя!")
    except:

        time.sleep(2)


@bot.message_handler(commands=['admin'])
def start_message_admin(message):
    try:
        for i in all_chat_list:
            if message.chat.id == i.chat_id:
                if message.from_user.username == None:
                    bot.send_message(i.chat_id,
                                     u'\u2757' + "У вас не указано имя пользователя (username) в настройках аккаунта\n Задайте и попробуйте еще раз")
                    return 0
                current_user = (bot.get_chat_member(message.chat.id, message.from_user.id))  # текущий пользователь
                if current_user.status == "creator" or current_user.status == 'administrator':
                    if i.chat_id == message.chat.id and i.game_for_online:
                        chat_id = (message.chat.id)
                        admin_kakoy_confi['chat_id'] = chat_id
                        admin_kakoy_confi['admin_id'] = message.from_user.id
                        admin_kakoy_confi['confa'] = True
                        if not any(
                                chat_id == dict_y['chat_id'] and message.from_user.id == dict_y['admin_id'] for dict_y
                                in
                                help_list):
                            help_list.append(admin_kakoy_confi)
                        key = types.InlineKeyboardMarkup()

                        key_start = types.InlineKeyboardButton(text="1.Изменить текущий список",
                                                               callback_data="change_list")
                        key_change_list = types.InlineKeyboardButton(text="2.Редактировать текущий список",
                                                                     callback_data="edit_list")
                        key_end = types.InlineKeyboardButton(text="0.Выход", callback_data="exit")
                        key.add(key_start)
                        key.add(key_change_list)
                        key.add(key_end)

                        mess = "*Админ меню группы: " + i.chat_name + "*\nТекущий список: " + str(
                            i.current_object_of_roles.list_name)

                        bot.send_message(message.from_user.id, mess, reply_markup=key, parse_mode='Markdown')
                        time.sleep(2)
                        break

                elif i.chat_id == message.from_user.id and not i.game_for_online:
                    bot.send_message(i.chat_id, "Для входа в админ меню воспользуйтесь командной /Админ")
                    time.sleep(2)

                    break
                elif i.game_for_online and current_user.status != "creator" or current_user.status != 'administrator':
                    bot.send_message(i.chat_id,
                                     u'\u2757' + "@" + message.from_user.username + ", у вас нет прав создателя группы или администратора")
                    return 0

        else:
            bot.send_message(message.chat.id,
                             u'\u2757' + "Бот не запущен!\nCоздателю(admin) группы или администратору необходимо запустить бота командой /start")
    except:

        time.sleep(2)


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    try:

        if not "офлайн" in call.message.text:
            chat_id = get_conf(call.from_user.id)
        else:
            chat_id = get_conf(call.from_user.id, False)
        help_list = list(range(0, 30))
        if call.data == "admin":
            process_admin_menu(call, chat_id)
        elif call.data == "change_list":
            bot.delete_message(call.from_user.id, call.message.message_id)
            process_change_list(call)
        elif call.data == "edit_list":
            bot.delete_message(call.from_user.id, call.message.message_id)
            process_edit_list_main(call, chat_id)
        elif call.data == "change_list_1":
            bot.delete_message(call.from_user.id, call.message.message_id)
            process_change_list_1(call, 1, chat_id)
            process_admin_menu(call, chat_id)
        elif call.data == "change_list_2":

            bot.delete_message(call.from_user.id, call.message.message_id)

            process_change_list_1(call, 2, chat_id)

            process_admin_menu(call, chat_id)
        elif call.data == "change_list_back":
            bot.delete_message(call.from_user.id, call.message.message_id)
            process_admin_menu(call, chat_id)
        elif call.data == "edit_list_back":
            bot.delete_message(call.from_user.id, call.message.message_id)

            process_admin_menu(call, chat_id)

        elif call.data == "exit":

            exit(call)
        elif call.data == 'edit_list_clear':
            process_admin_clear_all(call, chat_id, False)

        elif call.data == 'edit_list_offline_clear':
            process_admin_clear_all(call, call.from_user.id, False,True)

        elif call.data == 'edit_list_offline_all':
            process_admin_clear_all(call, call.from_user.id, True,True)

        elif call.data == 'edit_list_all':
            process_admin_clear_all(call, chat_id, True)

        for i in help_list:
            if call.data == "edit_list_" + str(i):
                process_edit_list_1(call, chat_id, i)

        for i in help_list:
            if call.data == "spy_list_" + str(i):
                process_spy_know_location(call, i)

        for i in help_list:
            if call.data == "edit_list_offline_" + str(i):
                print(i)
                process_offline_change_in_game(call,i)

    except:

        time.sleep(2)

def process_offline_change_in_game(call,number):

    for i in all_chat_list:
        if i.chat_id == call.from_user.id:

            if i.current_object_of_roles.list_of_location[number].in_game:
                i.current_object_of_roles.list_of_location[number].in_game = False
            else:
                i.current_object_of_roles.list_of_location[number].in_game = True

            m_id = send_list_of_locations(i.current_object_of_roles, i.chat_id, False)
            bot.delete_message(i.chat_id,m_id-1)


def process_admin_clear_all(call, chat_id, signal,offline = False):
    for i in all_chat_list:
        if i.chat_id == chat_id:
            if not signal:
                for j in i.current_object_of_roles.list_of_location:
                    j.in_game = False

            else:
                for j in i.current_object_of_roles.list_of_location:
                    j.in_game = True

            if not offline:
                a = send_list_of_locations(i.current_object_of_roles, call.from_user.id, False)
                bot.delete_message(call.from_user.id, a - 2)
                smile = u'\u2705' if signal else u'\u274C'
                bot.send_message(i.chat_id, "[Админ]: Все локации изменены на " + smile)
            else:

                m_id = send_list_of_locations(i.current_object_of_roles, i.chat_id, False)
                bot.delete_message(i.chat_id, m_id - 1)

def process_spy_know_location(call, number_of_location):
    try:
        for i in all_chat_list:
            for dict in help_list_spy:
                if call.message.chat.id == dict['spy_id']:
                    chat_id = dict['chat_id']

                    if i.chat_id == chat_id and i.chat_name in call.message.text:

                        for id, j in enumerate(i.current_object_of_roles.list_of_location):
                            if i.current_location == j.name:
                                if id == number_of_location:
                                    type_of_loose_string = "*Шпион победил угадыванием локации!* \nОн выбрал: " + str(
                                        i.current_object_of_roles.list_of_location[number_of_location].name)
                                    for spy in i.list_of_players:
                                        if spy.current_role.name == "Шпион":
                                            spy_string = "[Шпионом был: @" + str(spy.name) + "]"
                                            loc_string = "[Текущая локация: " + str(i.current_location) + "]"
                                            full_string = type_of_loose_string + "\n" + spy_string + "\n" + loc_string + "\n"
                                            bot.send_message(i.chat_id, full_string, parse_mode="Markdown")
                                            break
                                        bot.send_message(i.chat_id, type_of_loose_string, parse_mode='Markdown')

                                    i.list_of_players = []
                                    bot.delete_message(i.chat_id, i.id_of_kills_buttons_message)
                                    i.id_of_kills_buttons_message = None
                                    send_all_users_buttons_for_commands(i, "~Выбор команды: ~")
                                    time.sleep(2)
                                    return 0

                                else:
                                    type_of_loose_string = "*Шпион проиграл не угадав локацию!* \nОн выбрал: " + str(
                                        i.current_object_of_roles.list_of_location[number_of_location].name)
                                    for spy in i.list_of_players:
                                        if spy.current_role.name == "Шпион":
                                            spy_string = "[Шпионом был: @" + str(spy.name) + "]"
                                            loc_string = "[Текущая локация: " + str(i.current_location) + "]"
                                            bot.send_message(i.chat_id,
                                                             type_of_loose_string + "\n" + spy_string + "\n" + loc_string + "\n",
                                                             parse_mode="Markdown")
                                            break
                                    i.list_of_players = []
                                    bot.delete_message(i.chat_id, i.id_of_kills_buttons_message)
                                    i.id_of_kills_buttons_message = None
                                    send_all_users_buttons_for_commands(i, "~Выбор команды: ~")
                                    time.sleep(2)
                                    return 0

    except:

        time.sleep(2)


def process_edit_list_1(call, chat_id, number):
    try:
        for i in all_chat_list:  # изменить текущий список
            if i.chat_id == chat_id:  # Найти игру

                if i.current_object_of_roles.list_of_location[number].in_game:
                    i.current_object_of_roles.list_of_location[number].in_game = False
                else:

                    i.current_object_of_roles.list_of_location[number].in_game = True
                a = send_list_of_locations(i.current_object_of_roles, call.from_user.id, False)
                bot.delete_message(call.from_user.id, a - 2)

                smile = u'\u2705' if i.current_object_of_roles.list_of_location[number].in_game else u'\u274C'
                name = i.current_object_of_roles.list_of_location[number].name
                bot.send_message(i.chat_id, "[Админ]: " + str(number) + ". " + name + " изменено на " + smile)
                time.sleep(2)
                break
    except:

        time.sleep(2)


def process_edit_list_main(call, chat_id):
    try:
        key = types.InlineKeyboardMarkup(row_width=6)

        for i in range(0, 30, 6):
            key_1 = types.InlineKeyboardButton(text=str(i), callback_data=("edit_list_" + str(i)))
            key_2 = types.InlineKeyboardButton(text=str(i + 1), callback_data=("edit_list_" + str(i + 1)))
            key_3 = types.InlineKeyboardButton(text=str(i + 2), callback_data=("edit_list_" + str(i + 2)))
            key_4 = types.InlineKeyboardButton(text=str(i + 3), callback_data=("edit_list_" + str(i + 3)))
            key_5 = types.InlineKeyboardButton(text=str(i + 4), callback_data=("edit_list_" + str(i + 4)))
            key_6 = types.InlineKeyboardButton(text=str(i + 5), callback_data=("edit_list_" + str(i + 5)))
            key.add(key_1, key_2, key_3, key_4, key_5, key_6)
        key_clear = types.InlineKeyboardButton(text="Очистить", callback_data=("edit_list_clear"))
        key_all = types.InlineKeyboardButton(text="Выбрать всё", callback_data=("edit_list_all"))
        key.add(key_clear, key_all)
        key_end = types.InlineKeyboardButton(text="0.Назад", callback_data="edit_list_back")
        key.add(key_end)
        time.sleep(2)
        for i in all_chat_list:
            if i.chat_id == chat_id:
                bot.send_message(call.from_user.id, "Номера локации текущего списка: ", reply_markup=key)
                send_list_of_locations(i.current_object_of_roles, call.from_user.id, True)
                break

    except:

        time.sleep(2)


def process_change_list(call):
    try:
        key = types.InlineKeyboardMarkup()
        key_main = types.InlineKeyboardButton(text="1. Основной", callback_data="change_list_1")
        key_start = types.InlineKeyboardButton(text="2. Дополнительный", callback_data="change_list_2")
        key_end = types.InlineKeyboardButton(text="0. Назад", callback_data="change_list_back")
        key.add(key_main)
        key.add(key_start)
        key.add(key_end)
        bot.send_message(call.from_user.id, "Готовые списки локаций: ", reply_markup=key)
    except:

        time.sleep(2)


def process_admin_menu(call, chat_id):
    try:
        key = types.InlineKeyboardMarkup()
        key_start = types.InlineKeyboardButton(text="1.Изменить текущий список", callback_data="change_list")
        key_change_list = types.InlineKeyboardButton(text="2.Редактировать текущий список",
                                                     callback_data="edit_list")
        key_end = types.InlineKeyboardButton(text="0.Выход", callback_data="exit")
        key.add(key_start)
        key.add(key_change_list)
        key.add(key_end)

        for i in all_chat_list:

            if i.chat_id == chat_id:
                mess = "*Админ меню группы: " + i.chat_name + "*\nТекущий список: " + str(
                    i.current_object_of_roles.list_name)

                bot.send_message(call.message.chat.id, mess, reply_markup=key, parse_mode='Markdown')

                break
    except:

        time.sleep(2)


def process_change_list_1(call, number, chat_id):
    try:
        for i in all_chat_list:
            if i.chat_id == chat_id:  # Найти игру
                if number == 1:
                    current_list = (List_main())  # создание объекта
                elif number == 2:
                    current_list = (List_dlc_1())  # создание объекта
                current_list.fill_lications()  # заполнение локаций
                i.current_object_of_roles = current_list  # задать текущий список
                bot.send_message(i.chat_id, "[Админ]: Cписок изменен на " + current_list.list_name)

    except:

        time.sleep(2)


def exit(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.from_user.id, "Сохранения измененны" + u'\u2757')
    except:

        time.sleep(2)


@bot.message_handler(commands=['rules'])
def start_message(message):
    line_online = " Правила онлайн игры" + u'\u2757' + "\n" \
                                                       "1. Для запуска самого бота - необходимо написать администратору или создателю группы /start в групповом чате\n" \
                                                       "2. Для редактирования списка локаций - администратор или создатель группы может зайти в админ меню командой /admin в групповом чате\n" \
                                                       "3. Все игроки должны начать личный диалог с ботом(любой фразой,буквой командой)" \
                                                       "4. Если у игрока нет имени пользователя (username), необходимо его задать в настройках профиля (можно временно - на время игры)\n" \
                                                       "5. Для запуска игры, необходимо каждому игроку выбрать команду /ready, после чего каждому в Л.С. придет его локация\n" \
                                                       "6. Шпиону придет не только локация, но и список локаций, его задача угадать о чем идет речь\n" \
                                                       "6.1 Если шпион угадал - он выйграл, не угадал - проиграл (у шпиона только одна попытка угадать, тем самым себя рассекретив)\n" \
                                                       "7. Обычным игрокам предстоит выявить шпиона в ходе игры вопрос/ответ\n" \
                                                       "7.1 Человек попавший под подозрение может быть кикнут командой /kill + имя пользователя, если за него больше на 1 единицу голосов чем половина участников\n" \
                                                       "7.2 Если выбывший человек не шпион, игра продолжается. Как только осталось 2 человека, 1 из которых шпион, то шпиону присуждается победа\n" \
                                                       "7.3 Если в ходе голосования был выбран шпион, то остальным игрокам присуждается победа\n" \
                  + u'\u2728' + "Приятной игры" + u'\u2728' + "\n" \
                                                              "P.S. Для просмотра правил офлайн режима необходимо написать боту /rules в личные сообщения (после запуска бота командой /start в личных сообщениях)"

    line_ofline = " Правила офлайн игры" + u'\u2757' + "\n" \
                                                       "1. Для запуска бота - необходимо написать /start в личном сообщений\n" \
                                                       "2. Для начала игры следует написать /ready, после чего ответить боту сколько человек участвует в игре\n" \
                                                       "3. Далее по очереди будет выдана случайным образом локация, которую необходимо будет запомнить\n" \
                                                       "4. После запоминания своей роли участником, следует передать доступ к устройству другому игроку для ознакомления со своей локацияю, и так для всех участников\n" \
                                                       "5. По окончанию раздачи ролей станет доступна кнопка просмотра информации о том, кому среди участников досталась локация шпиона" \
                  + u'\u2728' + "Приятной игры" + u'\u2728' + "\n" \
                                                              "P.S. Для просмотра правил для онлайн режима необходимо написать в групповом чате (где уже приглашен этот бот) команду /rules (после запуска бота командой /start в групповом чате)"
    if message.chat.id != message.from_user.id:
        bot.send_message(message.chat.id, line_online)
    else:
        bot.send_message(message.chat.id, line_ofline)


@bot.message_handler(commands=['contacts'])
def start_message(message):
    line = "Контакты с разработчиком:\n" \
           "Если есть пожелания по улучшению или если найдете баг, то опишите его и шаги для его воспроизведения, и отправьте на удобный вам контакт:\n" \
           "1. https://vk.com/josephgembelton VK\n" \
           "2. @super_volodya Telegram\n" \
           "3. gembeltonwork@gmail.com Mail\n" \
           "4. https://steamcommunity.com/id/2209199f/ Steam"
    bot.send_message(message.chat.id, line)


@bot.message_handler(commands=['3', '4', '5', '6', '7', '8', '9', '10'])
def start_message_players(message):
    text = message.text[1:]

    for i in all_chat_list:
        if i.chat_id == message.chat.id and not i.game_for_online:

            for num in range(int(text)):
                i.list_of_players.append(Player(0, "Игрок " + str(num + 1), ""))
            key = types.ReplyKeyboardMarkup(row_width=4)
            key_3 = types.KeyboardButton(text="/Показать")
            key_4 = types.KeyboardButton(text="/restart")
            key.add(key_3, key_4)
            i.get_roles()
            bot.send_message(i.chat_id, "Игрок 1: нажмите кнопку чтобы увидеть локация: ", reply_markup=key)
            return 0
    else:
        bot.send_message(message.chat.id,
                         u'\u2757' + "Бот не запущен!\nВам(numbers) необходимо запустить бота командой /start")


@bot.message_handler(commands=['Показать'])
def start_message_players(message):
    for i in all_chat_list:
        if i.chat_id == message.chat.id and not i.game_for_online:
            try:
                key = types.ReplyKeyboardMarkup(row_width=4)
                key_3 = types.KeyboardButton(text="/Скрыть")
                key_4 = types.KeyboardButton(text="/restart")
                key.add(key_3, key_4)
                if i.list_of_players[0].current_role.name == "Шпион":
                    i.spy_name = i.list_of_players[0].name

                text = "Нажмите кнопку и передайте доступ к устройству другому игроку "

                caption = i.list_of_players[0].name + " ваша локация: " + str(
                    i.list_of_players[0].current_role.name) + "\n\n" + text
                bot.send_photo(i.chat_id, photo=open(i.list_of_players[0].current_role.image, "rb"),
                               caption=caption, reply_markup=key)  # выслать картинку

                i.list_of_players.pop(0)

                return 0
            except:
                bot.send_message(i.chat_id,"Не выбрано ни одной локации! зайдите в админ меню и выберите минимум 1")
                return 0
    else:
        bot.send_message(message.chat.id,
                         u'\u2757' + "Бот не запущен!\nВам(pokazat) необходимо запустить бота командой /start")


@bot.message_handler(commands=['Скрыть'])
def start_message_players(message):
    for i in all_chat_list:
        if i.chat_id == message.chat.id and not i.game_for_online:
            key = types.ReplyKeyboardMarkup(row_width=4)
            key_3 = types.KeyboardButton(text="/Показать")
            key_4 = types.KeyboardButton(text="/restart")
            key.add(key_3, key_4)
            bot.delete_message(i.chat_id, message.message_id - 1)
            try:
                bot.send_message(i.chat_id, i.list_of_players[0].name + ": нажмите кнопку  чтобы увидеть локацию: ",
                                 reply_markup=key)
            except (IndexError):
                key = types.ReplyKeyboardMarkup(row_width=4)
                key_3 = types.KeyboardButton(text="/Закончить")
                key.add(key_3)
                bot.send_message(i.chat_id, "По окончанию игры нажмите кнопку и увидите кто был шпионом",
                                 reply_markup=key)
            return 0
    else:
        bot.send_message(message.chat.id,
                         u'\u2757' + "Бот не запущен!\nВам(skrit) необходимо запустить бота командой /start")


def get_conf(user_id, confa=True):
    for dict_y in help_list:
        if user_id == dict_y['admin_id'] and confa == dict_y['confa']:
            return (dict_y['chat_id'])


@bot.message_handler(commands=['Закончить'])
def start_message_players(message):
    for i in all_chat_list:
        if i.chat_id == message.chat.id and not i.game_for_online:
            bot.send_message(i.chat_id, "Шпионом был: " + i.spy_name)
            i.game_begin = False
            send_all_users_buttons_for_commands(i, "~Выбор команды: ~")


def get_conf_spy(user_id):
    for dict_y in help_list_spy:
        if user_id == dict_y['spy_id']:
            return (dict_y['chat_id'])


def send_solo_user_buttons(current_chat):
    try:
        key = types.ReplyKeyboardMarkup(row_width=4)
        key_3 = types.KeyboardButton(text="/3")
        key_4 = types.KeyboardButton(text="/4")
        key_5 = types.KeyboardButton(text="/5")
        key_6 = types.KeyboardButton(text="/6")
        key_7 = types.KeyboardButton(text="/7")
        key_8 = types.KeyboardButton(text="/8")
        key_9 = types.KeyboardButton(text="/9")
        key_10 = types.KeyboardButton(text="/10")
        key.add(key_3, key_4, key_5, key_6)
        key.add(key_7, key_8, key_9, key_10)
        bot.send_message(current_chat.chat_id, "Выберите сколько игроков: ", reply_markup=key)
    except:
        bot.send_message(current_chat.chat.id,
                         u'\u2757' + "Слишком много запросов в секунду\nПовторите введенную команду")
        time.sleep(2)


@bot.message_handler(commands=['info'])
def start_message_es(message):
    line = "*[Выберите готовый список]*"
    bot.send_message(message.chat.id, line, parse_mode='Markdown')


@bot.message_handler(commands=['bot_stop'])
def start_message_players(message):
    if message.chat.type == 'group':
        current_user = (bot.get_chat_member(message.chat.id, message.from_user.id))  # текущий пользователь
        if current_user.status == "creator" or current_user.status == 'administrator':
            bot.send_message(message.chat.id, "Бот остановлен")
            bot.stop_polling()
        else:
            bot.send_message(message.chat.id,
                             u'\u2757' + "@" + message.from_user.username + ", у вас нет прав создателя группы или администратора")
    else:
        bot.send_message(message.chat.id, "Бот остановлен")
        bot.stop_polling()


print("start")


@bot.message_handler(commands=['Админ'])
def start_message_players(message):
    for i in all_chat_list:
        if i.chat_id == message.chat.id and not i.game_for_online:
            key = types.ReplyKeyboardMarkup(row_width=1)
            key_3 = types.KeyboardButton(text="/Сменить текущий список")
            key_4 = types.KeyboardButton(text="/Редактировать текущий список")
            key_10 = types.KeyboardButton(text="/Выход")
            key.add(key_3, key_4, key_10)
            bot.send_message(i.chat_id,
                             "*Админ меню офлайн игры: *\n" ,
                             reply_markup=key, parse_mode='Markdown')
            send_list_of_locations(i.current_object_of_roles, i.chat_id, False)
            return 0


@bot.message_handler(commands=['Редактировать'])
def start_message_players(message):
    for i in all_chat_list:
        key_keyboard = types.ReplyKeyboardMarkup(row_width=1)
        key_inline = types.InlineKeyboardMarkup(row_width=6)

        for j in range(0, 30, 6):
            key_1 = types.InlineKeyboardButton(text=str(j), callback_data=("edit_list_offline_" + str(j)))
            key_2 = types.InlineKeyboardButton(text=str(j + 1), callback_data=("edit_list_offline_" + str(j + 1)))
            key_3 = types.InlineKeyboardButton(text=str(j + 2), callback_data=("edit_list_offline_" + str(j + 2)))
            key_4 = types.InlineKeyboardButton(text=str(j + 3), callback_data=("edit_list_offline_" + str(j + 3)))
            key_5 = types.InlineKeyboardButton(text=str(j + 4), callback_data=("edit_list_offline_" + str(j + 4)))
            key_6 = types.InlineKeyboardButton(text=str(j + 5), callback_data=("edit_list_offline_" + str(j + 5)))
            key_inline.add(key_1, key_2, key_3, key_4, key_5, key_6)
        key_clear = types.InlineKeyboardButton(text="Очистить", callback_data=("edit_list_offline_clear"))
        key_all = types.InlineKeyboardButton(text="Выбрать всё", callback_data=("edit_list_offline_all"))
        key_inline.add(key_clear, key_all)

        if i.chat_id == message.chat.id and not i.game_for_online:
            key_10 = types.KeyboardButton(text="/Админ меню главная")
            key_keyboard.add(key_10)
            bot.send_message(i.chat_id, "Редактирование текущего списка локаций", reply_markup=key_keyboard)
            bot.send_message(i.chat_id, "Порядковый номер локации:", reply_markup=key_inline)
            send_list_of_locations(i.current_object_of_roles, i.chat_id, False)

            return 0


@bot.message_handler(commands=['Выход'])
def start_message_players(message):
    for i in all_chat_list:
        key = types.ReplyKeyboardMarkup(row_width=1)
        if i.chat_id == message.chat.id and not i.game_for_online:
            bot.send_message(i.chat_id, "Сохранения успешно применены!")
            send_all_users_buttons_for_commands(i, "~Выбор команды: ~")
            return 0


@bot.message_handler(commands=['Сменить'])
def start_message_players(message):
    for i in all_chat_list:
        if i.chat_id == message.chat.id and not i.game_for_online:
            key = types.ReplyKeyboardMarkup(row_width=1)
            key_3 = types.KeyboardButton(text="/Основной")
            key_4 = types.KeyboardButton(text="/Дополнительный")
            key_10 = types.KeyboardButton(text="/Админ меню главная")
            key.add(key_3, key_4, key_10)
            bot.send_message(i.chat_id,
                             "*Админ меню офлайн игры: *\n[Текущий список: " + i.current_object_of_roles.list_name+"]",
                             reply_markup=key, parse_mode='Markdown')
            return 0


@bot.message_handler(commands=['Основной', 'Дополнительный'])
def start_message_players(message):
    for i in all_chat_list:
        if i.chat_id == message.chat.id and not i.game_for_online:
            if message.text[1:] == "Дополнительный":
                current_list = (List_dlc_1())  # создание объекта
                current_list.fill_lications()  # заполнение локаций
                i.current_object_of_roles = current_list  # задать текущий список
            elif message.text[1:] == "Основной":
                current_list = (List_main())  # создание объекта
                current_list.fill_lications()  # заполнение локаций
                i.current_object_of_roles = current_list  # задать текущий список
            bot.send_message(i.chat_id, "Список был изменен на: " + message.text[1:])
            return 0



#Залить на сервер
"""План на потом"""
# Словить все ошибки на все команды от пользователя
# Проверка на синтаксические ошибки
# Добавление красивых смайликов для приятного восприятия информации пользователем (в меру)
