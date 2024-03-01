# ----------------------------------------------------------------------------------------------------
#                                             OWN MESSAGE                                            |
# ----------------------------------------------------------------------------------------------------
#                                                                                                    |
#  This module is needed if you need to make a newsletter.                                           |
#  You can also attach files with various formats to the message (word, pdf, txt...)                 |                                                                                          |
#                                                                                                    |
#  Almost every function in this module has a (1. bot), (2. event) in its input data.                |
#  1. bot - Is a unique instance of a bot with its own properties, which we set in Start.py          |
#  2. event - The type of event and its inherent properties. Each type of event has its own handler. |
#                                                                                                    |
#  There are 9 event types in total, but we use only 2:                                              |
#  1. event = NEW_MESSAGE; eventHandler = MessageHandler                                             |
#       1.1 Sending text                                                                             |
#       1.2 Sending no media file                                                                    |
#  2. event = CALLBACK_QUERY; eventHandler = CommandHandler                                          |
#                                                                                                    |
# All global constants from this module are in own_message_config.py                                 |
# All templates from this module are in own_message_templates.ini                                    |
#                                                                                                    |
# ----------------------------------------------------------------------------------------------------

import configparser
import logging

from bot.filter import Filter
from bot.handler import MessageHandler, BotButtonCommandHandler

from main_menu.main_menu_open import sender
from main_menu.messages.own_messages import own_message_menus
from main_menu.messages.own_messages.own_message_config import *

try:
    # Creating a parser templates object
    own_message_templates = configparser.ConfigParser()

    path_to_templates = "main_menu/messages/own_messages/own_message_templates.ini"

    # Read file with templates
    own_message_templates.read(path_to_templates, encoding="utf-8")

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
                   All menus are in own_message_menus.py

    """
    sender(bot,
           chat_id=event.from_chat,
           message=message,  # Title of menu
           markup=markup  # Template of menu from (own_message_menus.py)
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


# --------------------------------------------------------------------
#                            CHECK MESSAGE                           |
# --------------------------------------------------------------------
#                                                                    |
# This function is needed for monitoring of the message.             |
#                                                                    |
# Checks whether the data for sending the message is filled in.      |
# By default, every field has the value "unspecified" ('Не задано'). |
#                                                                    |
# --------------------------------------------------------------------
def check_own_message(bot, event):
    """
    This function is needed to constantly
    check how the message looks now
    """
    global own_message_text

    text = "Текст сообщения:\n" + own_message_text

    if own_message_text == unspecified:
        popup_text = "Текст не задан"
        markup = own_message_menus.text_empty_markup
    elif len(own_message_chats) == 0 and len(own_message_channels) == 0:
        popup_text = "Не указаны чаты/каналы для отправки"
        markup = own_message_menus.chats_and_channels_empty_markup
    else:
        popup_text = "Сообщение готово к отправке"
        markup = own_message_menus.message_ready_markup

    message = popup_text

    send_text(bot, event, text)
    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# --------------------------------------------------------------------
#                             INPUT CHECK                            |
# --------------------------------------------------------------------
#                                                                    |
# Any text you enter goes through this function.                     |
#                                                                    |
# Depending on the boolean variables,                                |
# it assigns the entered text to one or another field                |
#                                                                    |
# --------------------------------------------------------------------
def input_own_message_check(bot, event):
    """
    This function reads any text that the user has entered into the chat.
    It is needed in order to record values manually.
    """
    global \
        own_message_text, \
        own_message_text_boolean, \
        own_message_handwrite_chat_name_boolean, \
        own_message_handwrite_chat_stamp_boolean, \
        own_message_handwrite_channel_name_boolean, \
        own_message_handwrite_channel_stamp_boolean

    message = ""

    if own_message_text_boolean:
        own_message_text_boolean = False
        own_message_text = event.text
        message = "Текст успешно изменен"

    if message:
        markup = own_message_menus.menu_ok
        send_menu(bot, event, message, markup)


# --------------------------------------------------------------------
#                             SEND message                           |
# --------------------------------------------------------------------
#                                                                    |
# The function sends messages to all the chats that you have added   |
#                                                                    |
# --------------------------------------------------------------------
def send_own_message(bot, event):
    """
    This function is needed to send a message
    to all selected chats if there is a message.
    """
    global own_message_text

    if own_message_text == unspecified or (len(own_message_chats) == 0 and len(own_message_channels) == 0):
        popup_text = "Сообщение не готово к отправке"
        check_own_message(bot, event)
    else:
        if len(own_message_chats) > 0:
            text = own_message_text

            for chat in own_message_chats:
                chat_id = chat[1]
                bot.send_text(
                    chat_id=chat_id,
                    text=text
                )
                for file in own_message_files:
                    file_id = file[1]
                    bot.send_file(
                        chat_id=chat_id,
                        file_id=file_id
                    )

        if len(own_message_channels) > 0:
            for channel in own_message_channels:
                channel_id = channel[1]
                bot.send_text(
                    chat_id=channel_id,
                    text=text
                )
                for file in own_message_files:
                    file_id = file[1]
                    bot.send_file(
                        chat_id=channel_id,
                        file_id=file_id
                    )

        popup_text = "Сообщение отправлено"
        message_author = event.message_author
        logging.info("Пользователь: '" + message_author + "' отправил свое сообщение")

        send_popup_window(bot, event, popup_text)
        clear_own_message(bot, event)
        check_own_message(bot, event)

    send_popup_window(bot, event, popup_text)


# ----------------------------------------------------------------------------------------------------------------------
#                                                     SHOW  SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                            |
# Functions in this sector show the value of message fields: |
# 1. Chats                                                   |
# 2. Channels                                                |
# 3. Attached files                                          |
# ------------------------------------------------------------


# --------------
# 1. Show chats
# --------------
def show_own_message_chats(bot, event):
    """
    The function is needed to take data about chats from the list
    and output them in an understandable form
    """

    if len(own_message_chats) == 0:
        popup_text = "Список чатов пуст"
        markup = own_message_menus.chats_empty_markup
    else:
        popup_text = "Количество чатов: " + str(len(own_message_chats))
        text = "Значение сейчас:"
        for chat in own_message_chats:
            text += "\n\nЧат № " + str(own_message_chats.index(chat) + 1) + \
                    "\nНазвание: " + chat[0] + \
                    "\nStamp: " + chat[1]

        markup = own_message_menus.chats_check_markup
        send_text(bot, event, text)

    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -----------------
# 2. Show channels
# -----------------
def show_own_message_channels(bot, event):
    """
    The function is needed to take data about channels from the list
    and output them in an understandable form
    """

    if len(own_message_channels) == 0:
        popup_text = "Список каналов пуст"
        markup = own_message_menus.channels_empty_markup
    else:
        popup_text = "Количество каналов: " + str(len(own_message_channels))
        text = "Значение сейчас:"
        for channel in own_message_channels:
            text += "\n\nКанал №" + str(own_message_channels.index(channel) + 1) + \
                    "\nНазвание: " + channel[0] + \
                    "\nStamp: " + channel[1]

        markup = own_message_menus.channels_check_markup
        send_text(bot, event, text)

    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -----------------------
# 3. Show attached files
# -----------------------
def show_own_message_attached_files(bot, event):
    """
    The function is needed to take data about attached files
    from the list and output them in an understandable form
    """
    message = 'Выберите действие'

    if len(own_message_files) == 0:
        popup_text = "Приложенные файлы отсутствуют"
        markup = own_message_menus.attached_files_empty_markup
    else:
        popup_text = "Приложено файлов: " + str(len(own_message_files))
        text = "Приложенные файлы: "
        send_text(bot, event, text)
        markup = own_message_menus.attached_files_check_markup

        for file in own_message_files:
            file_id = file[1]
            bot.send_file(chat_id=event.from_chat,
                          file_id=file_id,
                          caption="Файл №" + str(own_message_files.index(file) + 1))

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# ----------------------------------------------------------------------------------------------------------------------
#                                                      ADD SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                                |
# In this sector there are functions for adding data to fields:  |
# 1.  Text                                                       |
# 2.  Chats                                                      |
# 3.  Channels                                                   |
# 4.  Attached files                                             |
# ----------------------------------------------------------------

# ------------
# 1. Add text
# ------------
def add_own_message_text(bot, event):
    global own_message_text_boolean

    own_message_text_boolean = True
    popup_text = "Введите текст"
    text = 'Введите текст сообщения ниже:'

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# -------------
# 2. Add chats
# -------------
def add_own_message_chats(bot, event):
    popup_text = "Выберите чаты"
    message = 'Выберите, в какие чаты отправить сообщение'
    markup = own_message_menus.chats_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def add_to_own_message_chats_chat(bot, event, number):
    """
    This function is needed to add a chat from templates to the general chat list.
    It does this by dividing the separation of the string by the character '; '.
    _______
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param number: Number of chat`s template from (own_message_templates.ini)
    """

    name_and_stamp = own_message_templates['chats']['chat_' + str(number)].split('; ')

    chat_name = name_and_stamp[0]
    chat_stamp = name_and_stamp[1]

    chat = [chat_name, chat_stamp]

    if chat in own_message_chats:
        popup_text = "Данный чат уже добавлен",
    else:
        own_message_chats.append(chat)

        popup_text = chat_name + ": добавлен в список чатов для отправки"

    send_popup_window(bot, event, popup_text)


def add_to_own_message_chats_chat_1(bot, event):
    add_to_own_message_chats_chat(bot, event, 1)


def add_to_own_message_chats_chat_2(bot, event):
    add_to_own_message_chats_chat(bot, event, 2)


def add_to_own_message_chats_chat_3(bot, event):
    add_to_own_message_chats_chat(bot, event, 3)


# ----------------
# 3. Add channels
# ----------------
def add_own_message_channels(bot, event):
    popup_text = "Выберите каналы"
    message = 'Выберите, в какие каналы отправить сообщение'
    markup = own_message_menus.channels_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def add_to_own_message_channels_channel(bot, event, number):
    """
    This function is needed to add a channel from templates to the general channel list.
    It does this by dividing the separation of the string by the character '; '.
    _______
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param number: Number of channel`s template from (own_message_templates.ini)
    """

    name_and_stamp = own_message_templates['channels']['channel_' + str(number)].split('; ')

    channel_name = name_and_stamp[0]
    channel_stamp = name_and_stamp[1]

    channel = [channel_name, channel_stamp]

    if channel in own_message_channels:
        popup_text = "Данный канал уже добавлен",
    else:
        own_message_channels.append(channel)

        popup_text = channel_name + ": добавлен в список каналов для отправки"

    send_popup_window(bot, event, popup_text)


def add_to_own_message_channels_channel_1(bot, event):
    add_to_own_message_channels_channel(bot, event, 1)


def add_to_own_message_channels_channel_2(bot, event):
    add_to_own_message_channels_channel(bot, event, 2)


def add_to_own_message_channels_channel_3(bot, event):
    add_to_own_message_channels_channel(bot, event, 3)


# ---------------------
# 4. Add attached file
# ---------------------
def add_own_message_attached_file(bot, event):
    """
    This function is needed for
    1. Sending a message to the user about adding a file.
    2. Give a signal to the bot about adding a file to the file list.

    """
    global \
        own_message_files_boolean

    own_message_files_boolean = True

    popup_text = "Отправьте файл"
    text = "Отправьте любой файл не являющийся медиа.\n" \
           "(Не добавляйте подпись к файлу)\n" \
           "⬇ Для добавления файла нажмите (+) слева от поля ввода. "

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_file_to_own_message_attached_files(bot, event):
    """
    This function is needed for adding a file to the file list.
    """
    global own_message_files_boolean

    if own_message_files_boolean:
        own_message_files_boolean = None

        file_id = ", ".join([p['payload']['fileId'] for p in event.data['parts']])
        file_info = bot.get_file_info(file_id).json()
        file_name = file_info['filename']

        file = [file_name, file_id]

        file_names = []

        for file in own_message_files:
            file_names.append(file[0])

        if file_name in file_names:
            message = "Файл с таким именем уже добавлен"
            markup = own_message_menus.menu_ok
        else:
            own_message_files.append(file)
            message = "Файл успешно добавлен"
            markup = own_message_menus.menu_ok

        send_menu(bot, event, message, markup)


# ----------------------------------------------------------------------------------------------------------------------
#                                                      CLEAR SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                                 |
# In this sector there are functions for delete data from fields: |
# 1. Chats                                                        |
# 2. Channels                                                     |
# 3. Attached files                                               |
# 4. Message                                                     |
# -----------------------------------------------------------------

# ---------------
# 1. Clear chats
# ---------------
def clear_own_message_chats(bot, event):
    """
    This function is needed to delete information
    about chats
    """
    own_message_chats.clear()
    popup_text = "Список чатов очищен"
    send_popup_window(bot, event, popup_text)


# ------------------
# 2. Clear channels
# ------------------
def clear_own_message_channels(bot, event):
    """
    This function is needed to delete information
    about channels
    """
    own_message_channels.clear()
    popup_text = "Список чатов очищен"
    send_popup_window(bot, event, popup_text)


# ------------------------
# 3. Clear attached files
# ------------------------
def clear_own_message_attached_files(bot, event):
    """
    This function is needed to delete information
    about the attached files.
    """
    global \
        own_message_files, \
        own_message_files_boolean

    own_message_files.clear()
    own_message_files_boolean = None

    popup_text = "Список с файлами очищен"
    send_popup_window(bot, event, popup_text)


# -----------------
# 4. Clear message
# -----------------
def clear_own_message(bot, event):
    """
    This function is needed to completely clear the message
    and all its fields.
    """
    global \
        own_message_text, \
        own_message_text_boolean, \
        own_message_files_boolean

    popup_text = "Сообщение было успешно удалено"
    send_popup_window(bot, event, popup_text)

    own_message_text = unspecified
    own_message_text_boolean = False
    own_message_files_boolean = False
    own_message_chats.clear()
    own_message_channels.clear()

# ----------------------------------------------------------------------------------------------------------------------
#                                                      HANDLERS SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                               |
# Event handlers are located in this sector:                    |
# 1. Sending message to the bot                                 |
# 2. Pressing the button                                        |
# ---------------------------------------------------------------


def own_message_handlers(bot):
    # 1. MESSAGE HANDLERS

    # Handler for simple text message without media content
    bot.dispatcher.add_handler(MessageHandler(
        filters=Filter.text,
        callback=input_own_message_check))

    # Handler for no media file. For example, text file
    bot.dispatcher.add_handler(MessageHandler(
        filters=Filter.data,
        callback=add_file_to_own_message_attached_files))

    # 2. BUTTON HANDLERS

    # --------------
    # Check message
    # --------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=check_own_message,
        filters=Filter.callback_data("check_own_message")))

    # -------------
    # Send message
    # -------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=send_own_message,
        filters=Filter.callback_data("send_own_message")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                SHOW HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # ----------------------
    # 1. Show chats handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_own_message_chats,
        filters=Filter.callback_data("show_own_message_chats")))

    # -------------------------
    # 2. Show channels handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_own_message_channels,
        filters=Filter.callback_data("show_own_message_channels")))

    # -------------------------------
    # 3. Show attached files handler
    # -------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_own_message_attached_files,
        filters=Filter.callback_data("show_own_message_attached_files")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                ADD HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # ----------------------
    # 1. Add chats handlers
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_own_message_text,
        filters=Filter.callback_data("add_own_message_text")))

    # ----------------------
    # 2. Add chats handlers
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_own_message_chats,
        filters=Filter.callback_data("add_own_message_chats")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_own_message_chats_chat_1,
        filters=Filter.callback_data("add_to_own_message_chats_chat_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_own_message_chats_chat_2,
        filters=Filter.callback_data("add_to_own_message_chats_chat_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_own_message_chats_chat_3,
        filters=Filter.callback_data("add_to_own_message_chats_chat_3")))

    # -------------------------
    # 3. Add channels handlers
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_own_message_channels,
        filters=Filter.callback_data("add_own_message_channels")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_own_message_channels_channel_1,
        filters=Filter.callback_data("add_to_own_message_channels_channel_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_own_message_channels_channel_2,
        filters=Filter.callback_data("add_to_own_message_channels_channel_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_own_message_channels_channel_3,
        filters=Filter.callback_data("add_to_own_message_channels_channel_3")))

    # -----------------------------
    # 4. Add attached file handler
    # -----------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_own_message_attached_file,
        filters=Filter.callback_data("add_own_message_attached_file")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                               CLEAR HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # -----------------------
    # 1. Clear chats handler
    # -----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_own_message_chats,
        filters=Filter.callback_data("clear_own_message_chats")))

    # --------------------------
    # 2. Clear channels handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_own_message_channels,
        filters=Filter.callback_data("clear_own_message_channels")))

    # --------------------------------
    # 9. Clear attached files handler
    # --------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_own_message_attached_files,
        filters=Filter.callback_data("clear_own_message_attached_files")))

    # --------------------------
    # 10. Clear message handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_own_message,
        filters=Filter.callback_data("clear_own_message")))

    # ------------------------------------------------------------------------------------------------------------------
