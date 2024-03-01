# ----------------------------------------------------------------------------------------------------
#                                          DEFERRED MESSAGE                                          |
# ----------------------------------------------------------------------------------------------------
#                                                                                                    |
#  This module is designed for recording and sending deferred messages.                              |
#  All recorded data is stored in the SQLite database.                                               |
#  (Script for making tables of DB located in sqlite.create_tables.sql)                              |
#  If the database is not in the folder with the directory, it will be created automatically.        |
#                                                                                                    |
#  To send a message, the following conditions must be met:                                          |
#       1. The bot must be enabled (Well, how else =D)                                               |
#       2. The time of sending the message must match the current time on the computer               |
#          (The time is checked with an interval of 10 seconds)                                      |
#       3. The message must be entered in the scheduler                                              |
#                                                                                                    |
#  Functional:                                                                                       |
#       1. Create an unlimited number of deferred messages.                                          |
#       2. The ability to change the parameters of any message at any time.                          |
#       3. Basic input check (the bot will warn you if you entered a non-existent date, etc.).       |
#       4. If a delayed message was added to the scheduler and for some reason was NOT sent,         |
#          the bot will warn you about it.                                                           |
#       5. The ability to interact with multiple messages at once:                                   |
#          forcibly send all messages from the scheduler,                                            |
#          enter all messages into the scheduler,                                                    |
#          remove all messages from the scheduler.                                                   |
#                                                                                                    |
#  Almost every function in this module has a (1. bot), (2. event) in its input data:                |
#       1. bot - Is a unique instance of a bot with its own properties,                              |
#                which we set in Start.py                                                            |
#       2. event - The type of event and its inherent properties.                                    |
#                  Each type of event has its own handler.                                           |
#                                                                                                    |
#  There are 9 event types in total, but we use only 2:                                              |
#       1. event = NEW_MESSAGE; eventHandler = MessageHandler                                        |
#           1.1 Sending text                                                                         |
#           1.2 Sending no media file                                                                |
#       2. event = CALLBACK_QUERY; eventHandler = CommandHandler                                     |
#                                                                                                    |
#  All global constants from this module are in deferred_message_config.py                           |
#  All templates from this module are in deferred_message_templates.ini                              |
#                                                                                                    |
# ----------------------------------------------------------------------------------------------------


import logging
import configparser
import os
import re
import sqlite3
import threading
import time
from datetime import datetime

from bot.filter import Filter
from bot.handler import BotButtonCommandHandler
from bot.handler import MessageHandler

from main_menu.main_menu_open import sender
from main_menu.messages.deferred_messages import deferred_messages_menus
from main_menu.messages.deferred_messages.deferred_messages_config import *

try:
    # Creating a parser templates object
    deferred_message_templates = configparser.ConfigParser()

    path_to_templates = "main_menu/messages/deferred_messages/deferred_message_templates.ini"

    # Read file with templates
    deferred_message_templates.read(path_to_templates, encoding="utf-8")

    logging.info("Файл с шаблонами успешно прочитан")

except FileNotFoundError:
    logging.info("Не удалось прочитать файл с шаблонами")


# -------------------------------------------
#                BOT  SENDER                |
# -------------------------------------------
# Main BOT API functions to send in chat:   |
# 1. menu with buttons (send_menu)          |
# 2. popup window (send_popup_window)       |
# 3. text (send_text)                       |
# -------------------------------------------

def send_menu(bot, event, message, markup):
    """
    This function is needed for send menu with buttons to necessary chat
    _______
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param message: Text above the buttons
    :param markup: The template of the menu that will be sent.
                   All menus are in deferred_message_menus.py
    """
    sender(bot,
           chat_id=event.from_chat,
           message=message,
           markup=markup
           )


def send_popup_window(bot, event, popup_text):
    """
    This function is needed for send popup window to necessary chat
    _______
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param popup_text: The text that will be in the pop-up window
    """
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=popup_text
    )


def send_text(bot, event, text):
    """
    This function is needed for send text to necessary chat
    _______
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param text: The text to be sent to the chat
    """
    bot.send_text(
        chat_id=event.from_chat,
        text=text
    )


# ----------------------------------------------------------------------------------------------------------------------
#                                                     OPEN MENU SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                              |
# The functions to open menus  |
#                              |
# ------------------------------

def open_deferred_message_menu(bot, event):
    global is_deferred_message_menu_open

    clear_all_booleans()

    popup_text = "Меню отложенного сообщения"
    markup = deferred_messages_menus.deferred_message_menu
    message = "|                      Меню отложенного сообщения           |"

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)
    is_deferred_message_menu_open = True


def go_back(bot, event):
    """
    The function is needed for correct output
    after pressing the "Назад" button
    """
    popup_text = "Не выбран номер сообщения"
    send_popup_window(bot, event, popup_text)
    if get_messages():
        show_deferred_messages(bot, event)
    else:
        open_deferred_message_menu(bot, event)


# ----------------------------------------------------------------------------------------------------------------------
#                                                      GET  SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                            |
# The functions to get information about:    |
# 1.  Number of messages (int)               |
# 2.  Numbers of messages (list)             |
# 3.  Message id (int)                       |
# 4.  Send date and time                     |
# 5.  Chats and channels (list)              |
# 6.  Chats and channels stamps (list)       |
# 7.  Chat or channel info                   |
# 8.  Attached file (boolean)                |
# 9.  Attached files (list)                  |
# 10. Text                                   |
# 11. Message (list)                         |
# 12. Messages (list)                        |
# --------------------------------------------

# --------------------------
# 1. Get number of messages
# --------------------------
def get_number_of_messages():
    """
    This function is needed to display
    a pop-up window with the number of messages ('_')
    _______
    :return: int
    """
    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        count_of_messages_query = \
            """
            SELECT COUNT(id)
            FROM messages
            """

        cursor.execute(count_of_messages_query)

        # Т.к. из fetchone мы получаем кортеж с одним элементом,
        # то для упрощения просто берем этот элемент
        number_of_messages = cursor.fetchone()[0]
        sqlite_connection.commit()
        cursor.close()

        return number_of_messages

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получении количества сообщений: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ---------------------------
# 2. Get numbers of messages
# ---------------------------
def get_numbers_of_messages():
    """
    This function is used to set the correct number for a new message
    _______
    :return: list with messages numbers
    """
    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        get_numbers_of_messages_query = \
            """
            SELECT number
            FROM messages
            """

        cursor.execute(get_numbers_of_messages_query)

        numbers_of_messages = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()

        return numbers_of_messages

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получения номеров сообщений: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ------------------
# 3. Get message id
# ------------------
def get_message_id(message_number):
    """
    It is needed in order to find out the id by the message number,
    and to carry out all further manipulations with the id
    _______
    :param message_number:
    :return: int
    """
    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        get_message_id_query = \
            """
            SELECT id 
            FROM messages
            WHERE number = ?
            """
        cursor.execute(get_message_id_query, (message_number,))
        message_id = cursor.fetchone()[0]
        cursor.close()
        return message_id

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получения id сообщения: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# --------------------------
# 4. Get send date and time
# --------------------------
def get_send_date_and_time():
    """
    Divides the date and time into 2 parts and
    saves them in global variables
    """
    global \
        deferred_message_id, \
        deferred_message_send_date, \
        deferred_message_send_time

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        get_send_date_and_time_query = \
            """
            SELECT send_date_and_time
            FROM messages
            WHERE id = ?
            """

        data = (deferred_message_id,)
        cursor.execute(get_send_date_and_time_query, data)

        send_date_and_time = cursor.fetchone()[0]

        sqlite_connection.commit()
        cursor.close()

        if send_date_and_time == unspecified:
            deferred_message_send_date = unspecified
            deferred_message_send_time = unspecified
        else:
            deferred_message_send_date = send_date_and_time.split(", ")[0]
            deferred_message_send_time = send_date_and_time.split(", ")[1]

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получения даты и времени отправки: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# --------------------------
# 5. Get chats and channels
# --------------------------
def get_chats_and_channels():
    """
    This function is needed to find out
    which chats and channels the message will be sent to
    _______
    :return: list with chats and channels
    """
    global \
        deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        get_chats_and_channels_query = \
            """
            SELECT *
            FROM chats_and_channels
            WHERE id_message = ?
            """

        data = (deferred_message_id,)
        cursor.execute(get_chats_and_channels_query, data)
        chats_and_channels = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()
        return chats_and_channels

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получении информации о сообщениях: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ---------------------------------
# 6. Get chats and channels stamps
# ---------------------------------
def get_chats_and_channels_stamps():
    """
    This function is used to check for the presence
    of a chat or channel being added
    _______
    :return: list with stamps
    """
    global \
        deferred_message_id, \
        deferred_message_chat_or_channel_stamp

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        data = (deferred_message_id,)

        get_chats_and_channel_stamps_query = \
            """
            SELECT stamp 
            FROM chats_and_channels
            WHERE id_message = ?
            """

        cursor.execute(get_chats_and_channel_stamps_query, data)
        chats_and_channel_stamps = cursor.fetchall()
        cursor.close()
        return chats_and_channel_stamps

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получения stamp(ов): " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ----------------------------
# 7. Get chat or channel info
# ----------------------------
def get_chat_or_channel_info(number, template):
    """
    Takes chat or channel data from a file "deferred_message_templates.ini"
    and writes the data to global variables
    """
    global \
        deferred_message_chat_or_channel_name, \
        deferred_message_chat_or_channel_stamp

    if template == "chat":
        name_and_stamp = deferred_message_templates['chats']['chat_' + str(number)].split('; ')
    if template == "channel":
        name_and_stamp = deferred_message_templates['channels']['channel_' + str(number)].split('; ')

    deferred_message_chat_or_channel_name = name_and_stamp[0]
    deferred_message_chat_or_channel_stamp = name_and_stamp[1]


# ---------------------
# 8. Get attached file
# ---------------------
def get_attached_file(file_name):
    """
    This function is needed to check that
    each attached file has a unique name
    _______
    :param file_name: string
    :return: boolean
    """
    global \
        deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        get_attached_files_query = \
            """
            SELECT *
            FROM files
            WHERE id_message = ? AND name = ?
            """

        data = (deferred_message_id, file_name,)
        cursor.execute(get_attached_files_query, data)

        attached_files = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()

        if len(attached_files) == 0:
            return False
        else:
            return True

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получения информации о файле: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ----------------------
# 9. Get attached files
# ----------------------
def get_attached_files():
    """
    This function is needed to find out
    which files will be sent along with the message
    _______
    :return:
    """
    global \
        deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        get_file_name_and_id_query = \
            """
            SELECT name, file_id
            FROM files
            WHERE id_message = ?
            """

        data = (deferred_message_id,)
        cursor.execute(get_file_name_and_id_query, data)

        attached_files = cursor.fetchall()

        sqlite_connection.commit()
        cursor.close()

        return attached_files

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время просмотра приложенных файлов: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ------------------------
# 10. Get text of message
# ------------------------
def get_text():
    """
    This function is needed to fast check
    whether the text is set or not
    _______
    :return: text of message
    """
    global deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        get_text_query = \
            """
            SELECT text
            FROM messages
            WHERE id = ?
            """

        date = (deferred_message_id,)
        cursor.execute(get_text_query, date)
        text = cursor.fetchone()[0]
        sqlite_connection.commit()
        cursor.close()
        return text

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получения текста сообщения: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ----------------
# 11. Get message
# ----------------
def get_message():
    """
    This function is needed to output all message parameters
    _______
    :return: list with message parameters
    """
    global deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        get_message_query = \
            """
            SELECT * 
            FROM messages 
            WHERE id = ?
            """

        data = (deferred_message_id,)
        cursor.execute(get_message_query, data)
        message = cursor.fetchone()
        cursor.close()
        return message

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получении информации о сообщении: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# -----------------
# 12. Get messages
# -----------------
def get_messages():
    """
    This function is needed to output
    the main parameters for each message
    _______
    :return: list with messages
    """
    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        info_about_messages_query = \
            """
            SELECT * 
            FROM messages
            """
        cursor.execute(info_about_messages_query)
        deferred_messages = cursor.fetchall()
        cursor.close()
        return deferred_messages

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время получения информации о сообщениях: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ----------------------------------------------------------------------------------------------------------------------
#                                                     CHECK  SECTOR
# ----------------------------------------------------------------------------------------------------------------------

# ----------------
#  1. Input check
# ----------------
def deferred_messages_input_check(bot, event):
    """
    Any text you enter goes through this function.

    Depending on the boolean variables,
    it assigns the entered text to one or another field
    """
    global \
        deferred_message_number_boolean, \
        deferred_message_text_boolean, \
        deferred_message_send_date_boolean, \
        deferred_message_send_time_boolean, \
        deferred_message_chat_or_channel_name_boolean, \
        deferred_message_chat_or_channel_stamp_boolean, \
        deferred_message_chat_or_channel_name, \
        deferred_message_chat_or_channel_stamp

    if deferred_message_number_boolean:
        check_deferred_message_number(bot, event, event.text)
    elif deferred_message_text_boolean:
        deferred_message_text_boolean = False
        set_deferred_message_text(bot, event, event.text)
    elif deferred_message_send_date_boolean:
        check_send_date(bot, event, event.text)
    elif deferred_message_send_time_boolean:
        check_send_time(bot, event, event.text)
    elif deferred_message_chat_or_channel_name_boolean:
        deferred_message_chat_or_channel_name_boolean = False
        deferred_message_chat_or_channel_name = event.text
        input_deferred_message_chat_or_channel_stamp(bot, event)
    elif deferred_message_chat_or_channel_stamp_boolean:
        deferred_message_chat_or_channel_stamp_boolean = False
        deferred_message_chat_or_channel_stamp = event.text
        add_chat_or_channel_to_deferred_message(bot, event)


# -----------------------------------------
# 2. Check availability of active messages
# -----------------------------------------
def check_availability_of_active_messages(bot):
    """
    The function is needed to notify the user
    about the presence of overdue messages
    """
    global deferred_message_thread_boolean

    deferred_messages = get_messages()

    deferred_message_thread_boolean = False

    if deferred_messages:
        for message in deferred_messages:
            if message[5] == 1:
                # Start the deferred message thread
                deferred_message_thread_boolean = True
                run_deferred_message_thread(bot)
                break


# ------------------------------------------
# 3. Check availability of overdue messages
# ------------------------------------------
def check_availability_of_overdue_messages(bot, event):
    """
    The function is needed to warn the user about overdue messages,
    if there are any
    """
    # get_send_date_and_time()
    deferred_messages = get_messages()

    # Time now
    current_datetime = datetime.now()

    overdue_messages_counter = 0
    overdue_messages_numbers = []

    for message in deferred_messages:

        if message[2] != unspecified:
            send_date = message[2].split(", ")[0]
            send_time = message[2].split(", ")[1]
            if send_date != unspecified and send_time != unspecified:
                to_date_format = datetime.strptime(message[2], "%d-%m-%Y, %H:%M")
                if message[5] == 1 and to_date_format < current_datetime:
                    overdue_messages_counter += 1
                    overdue_messages_numbers.append(str(message[1]))

    if overdue_messages_counter == 0:
        popup_text = "Просроченных сообщений не обнаружено"
        logging.info("При проверке просроченных сообщений не обнаружено")
    else:
        popup_text = "Обнаружены просроченные сообщения"
        logging.info("При проверке обнаружены просроченные сообщения")

        if overdue_messages_counter == 1:
            text = "Сообщение №" + overdue_messages_numbers[0] + " было просрочено\n"
        elif overdue_messages_counter > 1:
            text = "Сообщения : "
            for number in overdue_messages_numbers:
                if overdue_messages_numbers.index(number) == 0:
                    text += "№" + number + ", "
                else:
                    text += ", " + "№" + number
            text += "были просрочены\n"

        text += "Т.е. дата отправки наступила, но сообщение не было отправлено.\n" \
                "Возможные причины:\n" \
                "1. Ошибка работы бота\n" \
                "2. Бот был выключен, когда наступило время отправки"
        send_text(bot, event, text)

    send_popup_window(bot, event, popup_text)


# ---------------------------
# 4. Check number of message
# ---------------------------
def check_deferred_message_number(bot, event, number):
    """
    The function is needed to check the entered message number
    in order to output a correct response
    """
    global \
        deferred_message_id, \
        deferred_message_number_boolean

    # Pattern of number from 1 to infinity
    pattern_of_number = r'[1-9]\d*'

    deferred_message_number_boolean = False

    if re.fullmatch(pattern_of_number, number):
        if (int(number),) not in get_numbers_of_messages():
            message = "Введенное число не соответствует номеру сообщения"
            markup = deferred_messages_menus.ok_menu_to_show_messages
            send_menu(bot, event, message, markup)
        else:
            deferred_message_id = get_message_id(event.text)
            show_deferred_message(bot, event)
    else:
        # Check if the string is a number
        if number.isdigit():
            message = "Введите число, соответствующее номеру сообщения"
            markup = deferred_messages_menus.ok_menu_to_show_messages
            send_menu(bot, event, message, markup)
        else:
            message = "Вы ввели не число"
            markup = deferred_messages_menus.ok_menu_to_show_messages
            send_menu(bot, event, message, markup)


# --------------------------------------
# 5. Checking the_message for readiness
# --------------------------------------
def checking_the_message_for_readiness():
    """
    The function is needed to inform the user what details
    of the message need to be added
    so that the message is ready to be sent
    """
    global \
        deferred_message_send_date, \
        deferred_message_send_time

    get_send_date_and_time()

    if get_text() == unspecified:
        message = "Текст сообщения пуст"
        markup = deferred_messages_menus.add_text_markup
        return message, markup
    elif deferred_message_send_date == unspecified or deferred_message_send_time == unspecified:
        if deferred_message_send_date == unspecified and deferred_message_send_time == unspecified:
            message = "Дата и время отправки не заданы"
            markup = deferred_messages_menus.add_send_date_and_time_markup
            return message, markup
        elif deferred_message_send_date == unspecified:
            message = "Дата отправки не задана"
            markup = deferred_messages_menus.add_send_date_markup
            return message, markup
        elif deferred_message_send_time == unspecified:
            message = "Время отправки не задано"
            markup = deferred_messages_menus.add_send_time_markup
            return message, markup
    elif len(get_chats_and_channels()) == 0:
        message = "Чаты/Каналы для отправки не указаны"
        markup = deferred_messages_menus.empty_chats_and_channels_markup
        return message, markup
    else:
        return True


# ------------------------
# 6. Check message fields
# ------------------------
def check_deferred_message(bot, event):
    """
    The 'Master' function is needed to prompt you
    to enter the missing parameters
    """

    ready_or_not_value = checking_the_message_for_readiness()

    if ready_or_not_value is True:
        message = "Сообщение готово к отправке"
        markup = deferred_messages_menus.check_deferred_message_markup
    else:
        message = ready_or_not_value[0]
        markup = ready_or_not_value[1]

    send_menu(bot, event, message, markup)


# -------------------
# 7. Check send date
# -------------------
def check_send_date(bot, event, date):
    """
    The function is needed to check the entered date,
    including the number of days in the month and leap years
    """
    global \
        deferred_message_send_date_boolean, \
        deferred_message_send_date

    # Pattern of date (DD/MM/YY or DD.MM.YY or DD-MM-YY)
    date_pattern = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1' \
                   r'|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2' \
                   r'))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3' \
                   r'(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|' \
                   r'[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4' \
                   r'(?:(?:1[6-9]|[2-9]\d)?\d{2})$'

    if re.fullmatch(date_pattern, date):
        deferred_message_send_date_boolean = False
        if "/" in date:
            date = date.replace("/", "-")
        elif "." in date:
            date = date.replace(".", "-")

        deferred_message_send_date = date
        set_send_date_and_time(bot, event)
    else:
        deferred_message_send_date_boolean = False
        message = "Введенное время не соответствует шаблонам:\n" \
                  "1. ДД-ММ-ГГ\n" \
                  "2. ДД.ММ.ГГ\n" \
                  "3. ДД/ММ/ГГ\n" \
                  "Или это несуществующая дата"
        markup = deferred_messages_menus.ok_menu_to_show_message
        send_menu(bot, event, message, markup)


# -------------------
# 8. Check send time
# -------------------
def check_send_time(bot, event, send_time):
    """
    The function is needed to check the entered time
    for correctness
    """
    global \
        deferred_message_send_time_boolean, \
        deferred_message_send_time

    deferred_message_send_time_boolean = False

    # Pattern for 00:00 to 19:59 time
    pattern_1 = r'[0-1]\d:[0-5]\d'

    # Pattern for 20:00 to 23:59 time
    pattern_2 = r'2[0-3]:[0-5]\d'

    if re.fullmatch(pattern_1, send_time):
        deferred_message_send_time = send_time
        set_send_date_and_time(bot, event)
    elif re.fullmatch(pattern_2, send_time):
        deferred_message_send_time = send_time
        set_send_date_and_time(bot, event)
    else:
        message = "Введенное время не соответствует шаблону 'ЧЧ:ММ'"
        markup = deferred_messages_menus.ok_menu_to_show_message
        send_menu(bot, event, message, markup)


# --------------------------------------
# 9. Check chat or channel availability
# --------------------------------------
def check_chat_or_channel_availability(bot, event):
    """
    The function is needed so that the message is not sent
    to the same chat/channel several times
    """
    global \
        deferred_message_id, \
        deferred_message_chat_or_channel_stamp

    chats_and_channel_stamps = get_chats_and_channels_stamps()

    if chats_and_channel_stamps:
        stamp = (deferred_message_chat_or_channel_stamp,)

        if stamp in chats_and_channel_stamps:
            popup_text = "Данный чат/канал уже добавлен"
            send_popup_window(bot, event, popup_text)
        else:
            add_chat_or_channel_to_deferred_message(bot, event)
    else:
        add_chat_or_channel_to_deferred_message(bot, event)


# ----------------------------
# 10. Check file availability
# ----------------------------
def check_file_availability(bot, event, file_name, file_id):
    """
    The function is needed so that several identical files
    cannot be attached to one message

    However, files with different extensions will be considered as different.
    For example, 'file.txt ' and 'file.pdf' are two different files
    """
    global \
        deferred_message_id

    if get_attached_file(file_name):
        message = "Файл с таким именем уже прикреплён"
        markup = deferred_messages_menus.ok_menu_to_show_message
        send_menu(bot, event, message, markup)
    else:
        add_attached_file(bot, event, file_name, file_id)


# ----------------------------------------------------------------------------------------------------------------------
#                                                     INPUT  SECTOR
# ----------------------------------------------------------------------------------------------------------------------

# ------------------------
# 1. Input message number
# ------------------------
def input_deferred_message_number(bot, event):
    """
    The function is needed to signal to the bot
    that the next message entered will be number of message
    """
    global deferred_message_number_boolean

    clear_all_booleans()

    deferred_message_number_boolean = True
    popup_text = "Введите номер сообщения"
    text = "Введите номер нужного сообщения ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ----------------------------------------
# 2. Input chat or channel name and stamp
# ----------------------------------------

def input_deferred_message_chat_name(bot, event):
    global chat_channel_type

    chat_channel_type = "chat"
    input_deferred_message_chat_or_channel_name(bot, event)


def input_deferred_message_channel_name(bot, event):
    global chat_channel_type

    chat_channel_type = "channel"
    input_deferred_message_chat_or_channel_name(bot, event)


# -------------------------------
# 2.1 Input chat or channel name
# -------------------------------
def input_deferred_message_chat_or_channel_name(bot, event):
    """
    The function is needed to signal to the bot
    that the next message entered will be chat/channel name
    """
    global deferred_message_chat_or_channel_name_boolean

    clear_all_booleans()

    deferred_message_chat_or_channel_name_boolean = True
    popup_text = "Введите название"
    text = "Введите название чата/канала ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# --------------------------------
# 2.2 Input chat or channel stamp
# --------------------------------
def input_deferred_message_chat_or_channel_stamp(bot, event):
    """
    The function is needed to signal to the bot
    that the next message entered will be chat/channel stamp
    """
    global deferred_message_chat_or_channel_stamp_boolean

    clear_all_booleans()

    deferred_message_chat_or_channel_stamp_boolean = True
    text = "Введите stamp чата/канала ниже:\n\n" \
           "Stamp - завершающая часть ссылки на чат.\n" \
           "Например, у нас есть закрытая группа с ссылкой \n" \
           "httр://myteam.mail.ru/profile/AoLFuNFynm67V2xGFX0.\n" \
           "Её stamp - это AoLFuNFynm67V2xGFX0"

    send_text(bot, event, text)


# ----------------------------
# 3. Input send date and time
# ----------------------------

# --------------------
# 3.1 Input send date
# --------------------
def input_deferred_message_send_date(bot, event):
    """
    The function is needed to signal to the bot
    that the next message entered will be date of sending
    """
    global deferred_message_send_date_boolean

    clear_all_booleans()

    deferred_message_send_date_boolean = True
    popup_text = "Введите дату отправки"
    text = "Введите дату отправки ниже в одном из форматов:\n" \
           "1. ЧЧ.ММ.ГГ\n" \
           "2. ЧЧ-ММ-ГГ\n" \
           "3. ЧЧ/ММ/ГГ\n"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# --------------------
# 3.2 Input send time
# --------------------
def input_deferred_message_send_time(bot, event):
    """
    The function is needed to signal to the bot
    that the next message entered will be time of sending
    """
    global deferred_message_send_time_boolean

    clear_all_booleans()

    deferred_message_send_time_boolean = True
    popup_text = "Введите время отправки"
    text = "Введите время отправки ниже в формате (ЧЧ:ММ) :"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ----------------------
# 4. Input message text
# ----------------------
def input_deferred_message_text(bot, event):
    """
    The function is needed to signal to the bot
    that the next message entered will be text of the message
    """
    global deferred_message_text_boolean

    clear_all_booleans()

    deferred_message_text_boolean = True
    popup_text = "Введите текст сообщения"
    text = "Введите текст сообщения ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# --------------
# 5. Input file
# --------------
def input_deferred_message_file(bot, event):
    """
    This function is needed for:
        1. Sending a message to the user about adding a file.
        2. Give a signal to the bot about adding a file to the file list.
    """
    global deferred_message_file_boolean

    clear_all_booleans()

    deferred_message_file_boolean = True

    popup_text = "Отправьте файл"
    text = "Отправьте любой файл не являющийся медиа.\n" \
           "(Не добавляйте подпись к файлу)\n" \
           "⬇ Для добавления нажмите (+) слева от поля ввода. "

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ----------------------------------------------------------------------------------------------------------------------
#                                   (RUN TIME CHECK THREAD) AND (SEND MESSAGE) SECTOR
# ----------------------------------------------------------------------------------------------------------------------

# --------------
# 1. Run thread
# --------------
def run_deferred_message_thread(bot):
    """
    We run a parallel thread to check the time
    of sending messages at the specified interval.
    """
    global deferred_message_thread_boolean

    class DeferredMessageThread(threading.Thread):
        @classmethod
        def run(cls):
            while deferred_message_thread_boolean:
                check_active_messages(bot)
                time.sleep(10)

    deferred_message_thread = DeferredMessageThread()
    deferred_message_thread.start()
    return deferred_message_thread


# -----------------------------
# 2. Send messages prematurely
# -----------------------------
def send_all_deferred_messages_prematurely(bot, event):
    global deferred_message_id

    deferred_messages = get_messages()

    if len(deferred_messages) == 0:
        popup_text = "Список сообщений пуст"
        send_popup_window(bot, event, popup_text)
        open_deferred_message_menu(bot, event)
    else:
        for message in deferred_messages:
            counter = 0
            if message[5] == 1:
                deferred_message_id = message[0]
                send_deferred_message(bot, True)
                counter += 1

        popup_text = str(counter) + " сообщений из планировщика было отправлено"
        send_popup_window(bot, event, popup_text)
        logging.info(str(counter) + " сообщений было отправлено преждевременно")


# ----------------
# 3. Send message
# ----------------
def send_deferred_message(bot, prematurely=False):
    """
    This function is needed to send a message
    to all selected chats and Channels if there is a message.
    """
    global deferred_message_id

    chats_and_channels = get_chats_and_channels()
    files = get_attached_files()
    text = get_text()

    for chat_or_channel in chats_and_channels:
        chat_or_channel_stamp = chat_or_channel[3]
        bot.send_text(
            chat_id=chat_or_channel_stamp,
            text=text
        )
        for file in files:
            file_id = file[1]
            bot.send_file(
                chat_id=chat_or_channel_stamp,
                file_id=file_id
            )

    if prematurely:
        logging.info("Сообщение с id " + str(deferred_message_id) + " было отправлено преждевременно")
    else:
        logging.info("Сообщение с id " + str(deferred_message_id) + " было отправлено")
    delete_deferred_message(None, None)
    check_availability_of_active_messages(bot)


# -------------------------
# 4. Check active messages
# -------------------------
def check_active_messages(bot):
    """

    :param bot:
    """
    global \
        deferred_message_id, \
        deferred_message_thread_boolean

    deferred_messages = get_messages()

    # Time now at string format
    current_datetime = datetime.now().strftime("%d-%m-%Y, %H:%M")

    for message in deferred_messages:
        if message[5] == 1 and message[2] == current_datetime:
            deferred_message_id = message[0]
            send_deferred_message(bot)


# ----------------------------------------------------------------------------------------------------------------------
#                                                     SHOW  SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                            |
# Functions in this sector show the value of message fields: |
# 1.
# 2. Chats                                                   |
# ------------------------------------------------------------


# -------------------------
# 1. Show deferred message
# -------------------------
def show_deferred_message(bot, event):
    """

    :param bot:
    :param event:
    """
    global \
        deferred_message_id, \
        deferred_message_send_date, \
        deferred_message_send_time

    if deferred_message_id == unspecified:
        go_back(bot, event)
    else:
        clear_all_booleans()
        number_of_chats_and_channels = len(get_chats_and_channels())
        number_of_files = len(get_attached_files())
        message = get_message()

        if message[5] == 1:
            boolean = "Да"
        else:
            boolean = "Нет"

        text = \
            "Сообщение № " + str(message[1]) + \
            "\nЧатов/каналов для отправки: " + str(number_of_chats_and_channels) + \
            "\nПриложенных файлов: " + str(number_of_files) + \
            "\nДата отправки: " + message[2] + \
            "\nДата добавления: " + message[4] + \
            "\nДобавлено в планировщик: " + boolean + \
            "\nТекст: " + message[3]

        if event.type.name == 'CALLBACK_QUERY':
            popup_text = "Сообщение № " + str(message[1])
            send_popup_window(bot, event, popup_text)

        if message[2] == unspecified:
            deferred_message_send_date = unspecified
            deferred_message_send_time = unspecified
        else:
            deferred_message_send_date = message[2].split(", ")[0]
            deferred_message_send_time = message[2].split(", ")[1]

        send_text(bot, event, text)
        check_deferred_message(bot, event)


# --------------------------
# 2. Show deferred messages
# --------------------------
def show_deferred_messages(bot, event):
    """

    :param bot:
    :param event:
    """
    global \
        deferred_message_id

    deferred_message_id = unspecified
    clear_all_booleans()

    messages = get_messages()

    if messages:
        popup_text = "Всего сообщений: " + str(len(messages))
        text = "Список сообщений:\n"
        for message in messages:

            if message[5] == 1:
                boolean = "Да"
            else:
                boolean = "Нет"

            text += \
                "\nСообщение № " + str(message[1]) + \
                "\nДата и время отправки: " + message[2] + \
                "\nДата и время добавления: " + message[4] + \
                "\nДобавлено в планировщик: " + boolean + "\n"

        send_popup_window(bot, event, popup_text)
        message = "Выберите действие"
        markup = deferred_messages_menus.check_deferred_messages_markup
        send_text(bot, event, text)
        send_menu(bot, event, message, markup)
    else:
        popup_text = "Нет запланированных сообщений"
        send_popup_window(bot, event, popup_text)


# ---------------------------
# 3. Show chats and channels
# ---------------------------
def show_deferred_message_chats_and_channels(bot, event):
    """

    :param bot:
    :param event:
    """
    global deferred_message_id

    if deferred_message_id == unspecified:
        go_back(bot, event)
    else:
        chats_and_channels = get_chats_and_channels()

        if len(chats_and_channels) > 0:
            popup_text = "Количество чатов/каналов: " + str(len(chats_and_channels))
            text = "Список чатов/каналов:"
            for chat_or_channel in chats_and_channels:
                text += \
                    "\n\nЧат/канал №" + str(chats_and_channels.index(chat_or_channel) + 1) + \
                    "\nНазвание: " + chat_or_channel[2] + \
                    "\nStamp/id: " + chat_or_channel[3]
            send_text(bot, event, text)
            markup = deferred_messages_menus.chats_and_channels_check_menu
        else:
            popup_text = "Список чатов/каналов пуст"
            markup = deferred_messages_menus.empty_chats_and_channels_markup

        message = "Выберите действие"

        send_popup_window(bot, event, popup_text)
        send_menu(bot, event, message, markup)


# -----------------------
# 4. Show attached files
# -----------------------
def show_deferred_message_attached_files(bot, event):
    """

    :param bot:
    :param event:
    """
    global deferred_message_id

    if deferred_message_id == unspecified:
        go_back(bot, event)
    else:
        message = "Выберите действие"

        if len(get_attached_files()) > 0:
            popup_text = "Приложено файлов: " + str(len(get_attached_files()))
            text = "Список файлов:\n"
            markup = deferred_messages_menus.attached_files_check_menu
            files = get_attached_files()
            send_text(bot, event, text)
            for file in files:
                file_id = file[1]
                bot.send_file(chat_id=event.from_chat,
                              file_id=file_id,
                              caption="Файл №" + str(files.index(file) + 1))

        else:
            popup_text = "Приложенные файлы отсутствуют ( '_' )"
            markup = deferred_messages_menus.attached_files_empty_menu

        send_popup_window(bot, event, popup_text)
        send_menu(bot, event, message, markup)


# ----------------------------------------------------------------------------------------------------------------------
#                                                      ADD SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                                |
# In this sector there are functions for adding data to fields:  |
# 1.  Chats                                                      |
# 2.  Channels                                                   |
# ----------------------------------------------------------------


# ----------------------------------
# 1. Add tables if they don't exist
# ----------------------------------
def create_BotYanao_tables():
    """
    Creates database tables if there are none
    """

    file_path = "BotYanao.db"

    if not os.path.exists(file_path):
        try:
            sqlite_connection = sqlite3.connect('BotYanao.db')
            cursor = sqlite_connection.cursor()

            with open('main_menu\messages\deferred_messages\sqlite_create_tables.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()

            cursor.executescript(sql_script)
            cursor.close()

            logging.info("Таблицы базы данных были созданы")

        except sqlite3.Error as error:
            logging.info("Ошибка при работе с SQLite при создании таблиц: " + str(error))
        finally:
            if sqlite_connection:
                sqlite_connection.close()


# ------------------------
# 2. Add deferred message
# ------------------------
def add_deferred_message(bot, event):
    global \
        is_deferred_message_menu_open

    create_BotYanao_tables()

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_with_param = \
            """
            INSERT INTO messages
            (number, send_date_and_time, text, date_of_addition, activate)
            VALUES (?, 'Не задано', 'Не задано', ?, 0);
            """

        time_of_addition_message = datetime.now()
        time_of_addition_message_string = time_of_addition_message.strftime("%d-%m-%Y, %H:%M:%S")

        if len(get_numbers_of_messages()) == 0:
            new_message_number = 1
        else:
            new_message_number = get_numbers_of_messages()[-1][0] + 1

        data = (new_message_number, time_of_addition_message_string,)

        cursor.execute(sqlite_insert_with_param, data)
        sqlite_connection.commit()
        popup_text = "Новое сообщение успешно создано"
        send_popup_window(bot, event, popup_text)

        if not is_deferred_message_menu_open:
            show_deferred_messages(bot, event)

        cursor.close()

        message_id = get_message_id(get_numbers_of_messages()[-1][0])
        message_author = event.message_author

        logging.info("Пользователь: '" + message_author + "' добавил новое сообщение с id " + str(message_id))

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite в процессе добавления сообщения: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ----------------------------------
# 3. Add and set send date and time
# ----------------------------------

# ------------------
# 3.1 Add send date
# ------------------
def add_deferred_message_send_date(bot, event):
    """

    :param bot:
    :param event:
    """
    global send_date_boolean

    send_date_boolean = True
    popup_text = "Введите дату для отправки"
    text = "Введите дату для отправки ниже в формате (ЧЧ-ММ-ГГ) :"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ------------------
# 3.2 Add send time
# ------------------
def add_deferred_message_send_time(bot, event):
    """

    :param bot:
    :param event:
    """
    global send_time_boolean

    send_time_boolean = True
    popup_text = "Введите время для отправки"
    text = "Введите время для отправки ниже в формате (ЧЧ:ММ) :"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ---------------------------
# 3.3 Set send date and time
# ---------------------------
def set_send_date_and_time(bot, event):
    """

    :param bot:
    :param event:
    """
    global \
        deferred_message_id, \
        deferred_message_send_date, \
        deferred_message_send_time

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        sqlite_update_query = \
            """
            UPDATE messages
            SET send_date_and_time = ?
            WHERE id = ?
            """

        if deferred_message_send_date == unspecified and deferred_message_send_time == unspecified:
            send_date_and_time = unspecified
        else:
            send_date_and_time = deferred_message_send_date + ", " + deferred_message_send_time

        data = (send_date_and_time, deferred_message_id)
        cursor.execute(sqlite_update_query, data)
        sqlite_connection.commit()
        show_deferred_message(bot, event)

        cursor.close()

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время добавления даты и времени отправки: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ------------
# 4. Set text
# ------------
def set_deferred_message_text(bot, event, text):
    """

    :param bot:
    :param event:
    :param text:
    """
    global deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        sqlite_update_query = \
            """
            UPDATE messages
            SET text = ?
            WHERE id = ?
            """

        data = (text, deferred_message_id,)
        cursor.execute(sqlite_update_query, data)
        sqlite_connection.commit()
        show_deferred_message(bot, event)
        cursor.close()

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время добавления текста: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# -----------------------
# 5. Add chat or channel
# -----------------------
def add_chat_or_channel_to_deferred_message(bot, event):
    """

    :param bot:
    :param event:
    """
    global \
        deferred_message_id, \
        chat_channel_type, \
        deferred_message_chat_or_channel_name, \
        deferred_message_chat_or_channel_stamp

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        add_chat_or_channel_query = \
            """
            INSERT INTO chats_and_channels
            (id_message, name, stamp)
            VALUES (?, ?, ?);
            """

        id_message = deferred_message_id
        name = deferred_message_chat_or_channel_name
        stamp = deferred_message_chat_or_channel_stamp

        data = (id_message, name, stamp,)

        cursor.execute(add_chat_or_channel_query, data)
        sqlite_connection.commit()
        cursor.close()

        if event.type.name == 'CALLBACK_QUERY':
            popup_text = "Чат/канал успешно добавлен"
            send_popup_window(bot, event, popup_text)
        else:
            if chat_channel_type == "chat":
                chat_channel_type = unspecified
                message = "Ваш чат успешно добавлен"
                markup = deferred_messages_menus.ok_menu_to_add_chats
            elif chat_channel_type == "channel":
                chat_channel_type = unspecified
                message = "Ваш канал успешно добавлен"
                markup = deferred_messages_menus.ok_menu_to_add_channels
            else:
                message = "Ваш чат/канал успешно добавлен"
                markup = deferred_messages_menus.ok_menu_to_show_message

            send_menu(bot, event, message, markup)

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время добавления чата/канала: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# -------------
# 6. Add chats
# -------------
def add_chats_to_deferred_message(bot, event):
    """
    Just send menu with chats
    """
    popup_text = "Выберите чаты"
    message = 'Выберите, в какие чаты отправить сообщение'
    markup = deferred_messages_menus.chats_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def add_to_deferred_message_all_chats(bot, event):
    """
    Add all chats from chats templates
    """
    for number in range(len(deferred_message_templates.options("chats"))):
        get_chat_or_channel_info(number + 1, "chat")
        check_chat_or_channel_availability(bot, event)


def add_to_deferred_message_chat_1(bot, event):
    get_chat_or_channel_info(1, "chat")
    check_chat_or_channel_availability(bot, event)


def add_to_deferred_message_chat_2(bot, event):
    get_chat_or_channel_info(2, "chat")
    check_chat_or_channel_availability(bot, event)


def add_to_deferred_message_chat_3(bot, event):
    get_chat_or_channel_info(3, "chat")
    check_chat_or_channel_availability(bot, event)


# ----------------
# 7. Add channels
# ----------------
def add_channels_to_deferred_message(bot, event):
    """
    Just send menu with channels
    """
    popup_text = "Выберите каналы"
    message = 'Выберите, в какие каналы отправить сообщение'
    markup = deferred_messages_menus.channels_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def add_to_deferred_message_all_channels(bot, event):
    """
    Add all channels from channels templates
    """
    for number in range(len(deferred_message_templates.options("channels"))):
        get_chat_or_channel_info(number + 1, "channel")
        check_chat_or_channel_availability(bot, event)


def add_to_deferred_message_channel_1(bot, event):
    get_chat_or_channel_info(1, "channel")
    check_chat_or_channel_availability(bot, event)


def add_to_deferred_message_channel_2(bot, event):
    get_chat_or_channel_info(2, "channel")
    check_chat_or_channel_availability(bot, event)


def add_to_deferred_message_channel_3(bot, event):
    get_chat_or_channel_info(3, "channel")
    check_chat_or_channel_availability(bot, event)


# -----------------------------------
# 8. Set activate boolean to message
# -----------------------------------
def set_activate_boolean(bot, event, boolean, set_all=False):
    """
    The function is needed to add or delete a message to the scheduler
    (depending on the received variable)
    """
    global \
        deferred_message_id, \
        deferred_message_thread_boolean

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        activate_message_query = \
            """
            UPDATE messages
            SET activate = ?
            WHERE id = ?
            """

        data = (boolean, deferred_message_id,)
        cursor.execute(activate_message_query, data)
        sqlite_connection.commit()
        cursor.close()

        if boolean == 1:
            popup_text = "Сообщение успешно добавлено в планировщик"
            deferred_message_thread_boolean = True
            run_deferred_message_thread(bot)
            logging.info("Сообщение с id " + str(deferred_message_id) + " было успешно добавлено в планировщик")
        else:
            popup_text = "Сообщение успешно убрано из планировщика"
            logging.info("Сообщение с id " + str(deferred_message_id) + " было успешно убрано из планировщика")

        if not set_all:
            send_popup_window(bot, event, popup_text)
            show_deferred_message(bot, event)

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite во время работы с планировщиком: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def remove_message_from_the_scheduler(bot, event):
    set_activate_boolean(bot, event, 0)


def add_message_to_the_scheduler(bot, event):
    if checking_the_message_for_readiness() is True:
        set_activate_boolean(bot, event, 1)
    else:
        popup_text = "Недостаточно данных для занесения сообщения в планировщик"
        send_popup_window(bot, event, popup_text)


# -------------------------------------
# 9. Add all messages to the scheduler
# -------------------------------------
def add_all_messages_to_the_scheduler(bot, event):
    global deferred_message_id

    deferred_messages = get_messages()
    counter_of_added_messages = 0
    numbers_of_added_messages = []

    for message in deferred_messages:
        deferred_message_id = message[0]
        if checking_the_message_for_readiness() is True and message[5] == 0:
            set_activate_boolean(bot, event, 1, True)
            numbers_of_added_messages.append(str(message[1]))
            counter_of_added_messages += 1

    if counter_of_added_messages == 1:
        popup_text = "Сообщение №" + numbers_of_added_messages[0] + " было добавлено в планировщик"
        show_deferred_messages(bot, event)
    elif counter_of_added_messages > 1:
        popup_text = str(len(numbers_of_added_messages)) + " сообщений было добавлено в планировщик"
        text = "Сообщения : "
        for number in numbers_of_added_messages:
            text += "№" + number + " "
        text += "были добавлены в планировщик"
        send_text(bot, event, text)
        show_deferred_messages(bot, event)
    else:
        popup_text = "Ни одно сообщение не было добавлено в планировщик"

    send_popup_window(bot, event, popup_text)


def remove_all_messages_from_the_scheduler(bot, event):
    global deferred_message_id

    deferred_messages = get_messages()
    counter_of_remove_messages = 0
    numbers_of_remove_messages = []

    for message in deferred_messages:
        deferred_message_id = message[0]
        set_activate_boolean(bot, event, 0)
        numbers_of_remove_messages.append(str(message[1]))
        counter_of_remove_messages += 1

    if counter_of_remove_messages == 1:
        popup_text = "Сообщение №" + numbers_of_remove_messages[0] + " было убрано из планировщика"
        show_deferred_messages(bot, event)
    elif counter_of_remove_messages > 1:
        popup_text = str(len(numbers_of_remove_messages)) + " сообщений было убрано из планировщика"
        text = "Сообщения : "
        for number in numbers_of_remove_messages:
            text += "№" + number + " "
        text += "были убраны из планировщика"
        send_text(bot, event, text)
        show_deferred_messages(bot, event)
    else:
        popup_text = "Ни одно сообщение не было убрано из планировщика"

    send_popup_window(bot, event, popup_text)


# ---------------------
# 10. Add attached file
# ---------------------
def add_attached_file(bot, event, name, file_id):
    """
    Enters data about the attached file into the database
    """
    global \
        deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        add_file_query = \
            """
            INSERT INTO files
            (id_message, name, file_id)
            VALUES (?, ?, ?);
            """

        data = (deferred_message_id, name, file_id)
        cursor.execute(add_file_query, data)
        sqlite_connection.commit()
        cursor.close()

        message = "Файл успешно прикреплен"
        markup = deferred_messages_menus.ok_menu_to_show_message
        send_menu(bot, event, message, markup)

        logging.info("Файл '" + name + "' был добавлен к сообщению с id " + str(deferred_message_id))

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite при добавлении файлов: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def add_file_to_deferred_message_attached_files(bot, event):
    """
    The function is needed to get the file name
    (required for further verification)
    """
    global deferred_message_file_boolean

    if deferred_message_file_boolean:
        deferred_message_file_boolean = False

        file_id = ", ".join([p['payload']['fileId'] for p in event.data['parts']])
        file_info = bot.get_file_info(file_id).json()
        file_name = file_info['filename']

        check_file_availability(bot, event, file_name, file_id)


# ----------------------------------------------------------------------------------------------------------------------
#                                                DELETE AND CLEAR SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                                    |
#  In this sector there are functions for delete or clear            |
#  data from database:                                               |
#                                                                    |
#  1. Chats and channels                                             |
#  2. Channels                                                       |
#  3. Attached files                                                 |
#  4. Message                                                        |
#  5. Booleans                                                       |
# --------------------------------------------------------------------

# ---------------------------------
# 1. Delete all chats and channels
# ---------------------------------
def delete_chats_and_channels(bot, event):
    global deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        delete_chats_and_channels_query = \
            """
            DELETE FROM chats_and_channels
            WHERE id_message = ?
            """

        data = (deferred_message_id,)
        cursor.execute(delete_chats_and_channels_query, data)
        sqlite_connection.commit()
        cursor.close()

        popup_text = ("Чатов/каналов удалено: " + str(cursor.rowcount))
        send_popup_window(bot, event, popup_text)

        message_author = event.message_author

        logging.info("Пользователь: " + message_author +
                     " удалил " + str(cursor.rowcount) +
                     " чатов/каналов у сообщения с id " + str(deferred_message_id))

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite при удалении чатов/каналов: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# -------------------------
# 2. Delete attached files
# -------------------------
def delete_deferred_message_attached_files(bot, event):
    global deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        delete_files_query = \
            """
            DELETE FROM files 
            WHERE id_message = ?
            """

        data = (deferred_message_id,)
        cursor.execute(delete_files_query, data)
        sqlite_connection.commit()
        cursor.close()

        popup_text = "Файлов удалено: " + str(cursor.rowcount)
        send_popup_window(bot, event, popup_text)

        message_author = event.message_author

        logging.info("Пользователь: " + message_author +
                     " удалил " + str(cursor.rowcount) +
                     " файлов у сообщения с id" + str(deferred_message_id))

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite при удалении файлов: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ------------------
# 3. Delete message
# ------------------
def delete_deferred_message(bot, event):
    global deferred_message_id

    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        pragma_on_query = \
            """
            PRAGMA foreign_keys = ON;
            """
        cursor.execute(pragma_on_query)
        sqlite_connection.commit()

        delete_message_query = \
            """
            DELETE FROM messages 
            WHERE id = ?
            """

        data = (deferred_message_id,)
        cursor.execute(delete_message_query, data)
        sqlite_connection.commit()
        cursor.close()

        if bot is not None and event is not None:
            popup_text = "Сообщение удалено"
            send_popup_window(bot, event, popup_text)
            show_deferred_messages(bot, event)
            message_author = event.message_author
            logging.info("Пользователь: '" + message_author + "' удалил сообщение с id " + str(deferred_message_id))

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite при удалении сообщения с id " +
                     str(deferred_message_id) + ": " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# -----------------------
# 4. Delete all messages
# -----------------------
def delete_all_deferred_messages(bot, event):
    try:
        sqlite_connection = sqlite3.connect('BotYanao.db')
        cursor = sqlite_connection.cursor()

        pragma_on_query = \
            """
            PRAGMA foreign_keys = ON;
            """
        cursor.execute(pragma_on_query)
        sqlite_connection.commit()

        delete_all_messages_query = \
            """
            DELETE FROM messages
            """

        cursor.execute(delete_all_messages_query)
        sqlite_connection.commit()
        cursor.close()

        popup_text = "Сообщений удалено: " + str(cursor.rowcount)
        send_popup_window(bot, event, popup_text)
        open_deferred_message_menu(bot, event)

        message_author = event.message_author

        logging.info("Пользователь: '" + message_author + "' удалил все отложенные сообщения")

    except sqlite3.Error as error:
        logging.info("Ошибка при работе с SQLite при удалении всех сообщений: " + str(error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ----------------------
# 5. Clear all booleans
# ----------------------
def clear_all_booleans():
    """
    The function is needed to avoid an error
    when the bot expects to enter a value
    for several parameters at once
    """
    global \
        is_deferred_message_menu_open, \
        deferred_message_number_boolean, \
        deferred_message_text_boolean, \
        deferred_message_send_date_boolean, \
        deferred_message_send_time_boolean, \
        deferred_message_chat_or_channel_name_boolean, \
        deferred_message_chat_or_channel_stamp_boolean, \
        deferred_message_file_boolean

    is_deferred_message_menu_open = False
    deferred_message_number_boolean = False
    deferred_message_text_boolean = False
    deferred_message_send_date_boolean = False
    deferred_message_send_time_boolean = False
    deferred_message_chat_or_channel_name_boolean = False
    deferred_message_chat_or_channel_stamp_boolean = False
    deferred_message_file_boolean = False


# ----------------------------------------------------------------------------------------------------------------------
#                                                      HANDLERS SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                               |
# Event handlers are located in this sector:                    |
# 1. Sending message to the bot                                 |
# 2. Pressing the button                                        |
# ---------------------------------------------------------------


def deferred_messages_handlers(bot):
    """
    Event handlers are located in this sector:
        1. Sending message to the bot
            1.1 Text
            1.2 No media file
        2. Pressing the button
    """
    # --------------------
    # 1. MESSAGE HANDLERS
    # --------------------

    # -----------------
    # 1.1 Text handler
    # -----------------
    bot.dispatcher.add_handler(MessageHandler(
        filters=Filter.text,
        callback=deferred_messages_input_check))

    # --------------------------
    # 1.2 No media file handler
    # --------------------------
    bot.dispatcher.add_handler(MessageHandler(
        filters=Filter.data,
        callback=add_file_to_deferred_message_attached_files))

    # -------------------
    # 2. BUTTON HANDLERS
    # -------------------

    # ----------------------
    # Show message handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_deferred_message,
        filters=Filter.callback_data("show_deferred_message")))

    # ------------------------------
    # Choose message number handler
    # ------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=input_deferred_message_number,
        filters=Filter.callback_data("choose_deferred_message_number")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                INPUT HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # --------------------------------
    # 1. Input message number handler
    # --------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=input_deferred_message_number,
        filters=Filter.callback_data("make_a_deferred_messages_inactive")))

    # -----------------------
    # 2. Input chat handlers
    # -----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=input_deferred_message_chat_name,
        filters=Filter.callback_data("input_deferred_message_chat_name")))

    # -------------------------
    # 3. Input channel handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=input_deferred_message_channel_name,
        filters=Filter.callback_data("input_deferred_message_channel_name")))

    # ---------------------------------------------
    # 4. Input send date and time handlers
    # ---------------------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=input_deferred_message_send_date,
        filters=Filter.callback_data("input_deferred_message_send_date")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=input_deferred_message_send_time,
        filters=Filter.callback_data("input_deferred_message_send_time")))

    # ------------------------------
    # 5. Input message text handler
    # ------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=input_deferred_message_text,
        filters=Filter.callback_data("input_deferred_message_text")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                              RUN SCHEDULE THREAD SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # --------------------------------------
    # Send all messages prematurely handler
    # --------------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=send_all_deferred_messages_prematurely,
        filters=Filter.callback_data("send_all_deferred_messages_prematurely")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                OPEN HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # -----------------------------------
    # Open deferred message menu handler
    # -----------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=open_deferred_message_menu,
        filters=Filter.callback_data("open_deferred_message_menu")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                SHOW HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # ----------------------
    # 1. Show chats handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_deferred_messages,
        filters=Filter.callback_data("show_deferred_messages")))

    # ----------------------
    # 2. Show chats handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_deferred_message_chats_and_channels,
        filters=Filter.callback_data("show_deferred_message_chats_and_channels")))

    # -------------------------------
    # 3. Show attached files handler
    # -------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_deferred_message_attached_files,
        filters=Filter.callback_data("show_deferred_message_attached_files")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                ADD HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------
    # 1. Add message handlers
    # ------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_deferred_message,
        filters=Filter.callback_data("add_deferred_message")))

    # -------------------------
    # 2. Add send time handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_deferred_message_send_time,
        filters=Filter.callback_data("add_deferred_message_send_time")))

    # ----------------------
    # 4. Add chats handlers
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_chats_to_deferred_message,
        filters=Filter.callback_data("add_deferred_message_chats")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_deferred_message_all_chats,
        filters=Filter.callback_data("add_to_deferred_message_all_chats")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_deferred_message_chat_1,
        filters=Filter.callback_data("add_to_deferred_message_chat_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_deferred_message_chat_2,
        filters=Filter.callback_data("add_to_deferred_message_chat_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_deferred_message_chat_3,
        filters=Filter.callback_data("add_to_deferred_message_chat_3")))

    # -------------------------
    # 5. Add channels handlers
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_channels_to_deferred_message,
        filters=Filter.callback_data("add_deferred_message_channels")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_deferred_message_all_channels,
        filters=Filter.callback_data("add_to_deferred_message_all_channels")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_deferred_message_channel_1,
        filters=Filter.callback_data("add_to_deferred_message_channel_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_deferred_message_channel_2,
        filters=Filter.callback_data("add_to_deferred_message_channel_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_deferred_message_channel_3,
        filters=Filter.callback_data("add_to_deferred_message_channel_3")))

    # -----------------------------
    # 6. Add attached file handler
    # -----------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=input_deferred_message_file,
        filters=Filter.callback_data("input_deferred_message_file")))

    # ------------------------------------------
    # 7. Add messages to the scheduler handlers
    # ------------------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_message_to_the_scheduler,
        filters=Filter.callback_data("add_message_to_the_scheduler")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_all_messages_to_the_scheduler,
        filters=Filter.callback_data("add_all_messages_to_the_scheduler")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                              DELETE HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # --------------------------------
    # 1. Clear attached files handler
    # --------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=delete_deferred_message_attached_files,
        filters=Filter.callback_data("delete_deferred_message_attached_files")))

    # ---------------------------------------
    # 2. Clear the message scheduler handler
    # ---------------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=remove_message_from_the_scheduler,
        filters=Filter.callback_data("remove_message_from_the_scheduler")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=remove_all_messages_from_the_scheduler,
        filters=Filter.callback_data("remove_all_messages_from_the_scheduler")))

    # --------------------------
    # 3. Clear message handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=delete_deferred_message,
        filters=Filter.callback_data("delete_deferred_message")))

    # ---------------------------------------
    # 4. Clear all deferred messages handler
    # ---------------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=delete_all_deferred_messages,
        filters=Filter.callback_data("delete_all_deferred_messages")))

    # ------------------------------------------------------------------------------------------------------------------
