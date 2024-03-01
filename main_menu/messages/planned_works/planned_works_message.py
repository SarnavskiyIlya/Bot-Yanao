# ----------------------------------------------------------------------------------------------------
#                                       PLANNED WORKS MESSAGE                                        |
# ----------------------------------------------------------------------------------------------------
#                                                                                                    |
#  This module is needed to compile a message about planned work                                     |
#  with the ability to both fill in data using templates and fill them out by hand.                  |
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
# All global constants from this module are in planned_works_config.py                               |
# All templates from this module are in planned_works_templates.ini                                  |
#                                                                                                    |
# ----------------------------------------------------------------------------------------------------

import configparser

from bot.filter import Filter
from bot.handler import MessageHandler, BotButtonCommandHandler

from main_menu.main_menu_open import sender
from main_menu.messages.planned_works import planned_works_menus
from main_menu.messages.planned_works.planned_works_config import *

# Creating a parser object
config = configparser.ConfigParser()

# Read config
config.read("main_menu\messages\planned_works\planned_works_templates.ini", encoding="utf-8")


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
                   All menus are in planned_works_menus.py

    """
    sender(bot,
           chat_id=event.from_chat,
           message=message,  # Title of menu
           markup=markup  # Template of menu from (planned_works_menus.py)
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
def check_planned_works_message(bot, event):
    """
    This function is needed to constantly check how the message looks now

    After each message change, this function is called,
    and the bot sends the resulting message to the chat
    """
    global planned_works_message

    # You need to check whether the message is handwritten.
    # In order not to perform unnecessary filling actions.
    if planned_works_handwrite_message_boolean:
        planned_works_message = planned_works_message
        popup_text = "Письмо готово к отправке"
        markup = planned_works_menus.send_check_planned_works_message
    else:
        planned_works_group_string = unspecified

        if len(planned_works_group) != 0:
            # We translate the list with the group members into a line
            # so that it is more convenient to insert this value
            # into the form below ("Состав и контакты бригады: ")
            planned_works_group_string = ""
            for i in range(len(planned_works_group)):
                planned_works_group_string += \
                    "\n\n" + \
                    "Имя: " + planned_works_group[i][0] + "\n" + \
                    "Контакты: " + planned_works_group[i][1]

        planned_works_message = \
            "Тип работ: " + planned_works_type + "\n\n" + \
            "Тип ЭС: " + planned_works_ES_type + "\n\n" + \
            "Содержание работ: " + planned_works_content + "\n\n" + \
            "Состав и контакты бригады: " + planned_works_group_string + "\n\n" + \
            "Начало проведения работ: " + planned_works_begin_date + "\n\n" + \
            "Окончание проведения работ: " + planned_works_end_date + "\n\n"

        # Depending on which fields are filled in,
        # need to send the appropriate menu
        if len(planned_works_chats) == 0 and len(planned_works_channels) == 0:
            popup_text = "Чаты/Каналы для отправки не указаны"
            markup = planned_works_menus.chats_and_channels_empty_markup
        elif planned_works_type == unspecified:
            popup_text = "Тип работ не указан"
            markup = planned_works_menus.type_empty_markup
        elif planned_works_ES_type == unspecified:
            popup_text = "Тип ЭС не указан"
            markup = planned_works_menus.ES_type_empty_markup
        elif planned_works_content == unspecified:
            popup_text = "Содержание работ не указано"
            markup = planned_works_menus.content_empty_markup
        elif len(planned_works_group) == 0:
            popup_text = "Состав бригады не указан"
            markup = planned_works_menus.group_empty_markup
        elif planned_works_begin_date == unspecified:
            popup_text = "Время начала работ не установлено"
            markup = planned_works_menus.begin_date_empty_markup
        elif planned_works_end_date == unspecified:
            popup_text = "Время окончания работ не установлено"
            markup = planned_works_menus.end_date_empty_markup
        else:
            popup_text = "Форма заполнена"
            markup = planned_works_menus.send_check_planned_works_message

    message = popup_text

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, planned_works_message_head + planned_works_message)
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
def input_planned_works_check(bot, event):
    """
    This function reads any text that the user has entered into the chat.
    It is needed in order to record values manually.
    """
    global \
        planned_works_message, \
        planned_works_handwrite_chat_name_boolean, \
        planned_works_handwrite_chat_stamp_boolean, \
        planned_works_handwrite_channel_name_boolean, \
        planned_works_handwrite_channel_stamp_boolean, \
        planned_works_type, \
        planned_works_type_boolean, \
        planned_works_ES_type, \
        planned_works_ES_type_boolean, \
        planned_works_content, \
        planned_works_content_boolean, \
        planned_works_group, \
        planned_works_handwrite_group_members, \
        planned_works_handwrite_group_member_name_boolean, \
        planned_works_handwrite_group_member_contacts_boolean, \
        planned_works_begin_date, \
        planned_works_begin_date_boolean, \
        planned_works_end_date, \
        planned_works_end_date_boolean

    message = ""

    if planned_works_handwrite_message_boolean:
        planned_works_message = event.text
        message = "Ваше письмо успешно добавлено"
    else:
        if planned_works_handwrite_chat_name_boolean:
            planned_works_handwrite_chat_names.append(event.text)
            planned_works_handwrite_chat_name_boolean = None
            add_chat_stamp_to_planned_works_handwrite_chat(bot, event)
        elif planned_works_handwrite_chat_stamp_boolean:
            planned_works_handwrite_chat_stamps.append(event.text)
            handwrite_chat = \
                [
                    planned_works_handwrite_chat_names[-1],
                    planned_works_handwrite_chat_stamps[-1]
                ]
            planned_works_chats.append(handwrite_chat)
            planned_works_handwrite_chat_stamp_boolean = None
            message = "Чат успешно добавлен"
        if planned_works_handwrite_channel_name_boolean:
            planned_works_handwrite_channel_names.append(event.text)
            planned_works_handwrite_channel_name_boolean = None
            add_channel_stamp_to_planned_works_handwrite_channel(bot, event)
        elif planned_works_handwrite_channel_stamp_boolean:
            planned_works_handwrite_channel_stamps.append(event.text)
            handwrite_channel = \
                [
                    planned_works_handwrite_channel_names[-1],
                    planned_works_handwrite_channel_stamps[-1]
                ]
            planned_works_channels.append(handwrite_channel)
            planned_works_handwrite_channel_stamp_boolean = None
            message = "Канал успешно добавлен"
        elif planned_works_type_boolean:
            planned_works_type = event.text
            planned_works_type_boolean = None
            message = "Тип работ успешно установлен"
        elif planned_works_ES_type_boolean:
            planned_works_ES_type = event.text
            planned_works_ES_type_boolean = None
            message = "Тип ЕС успешно установлен"
        elif planned_works_content_boolean:
            planned_works_content = event.text
            planned_works_content_boolean = None
            message = "Данные о содержании работ успешно внесены"
        elif planned_works_handwrite_group_member_name_boolean:
            planned_works_handwrite_group_members_names.append(event.text)
            message = "Данные об участнике успешно внесены"
            planned_works_handwrite_group_member_name_boolean = None
            add_to_planned_works_handwrite_group_members_contacts(bot, event)
        elif planned_works_handwrite_group_member_contacts_boolean:
            planned_works_handwrite_group_members_contacts.append(event.text)
            handwrite_group_members = \
                [
                    planned_works_handwrite_group_members_names[-1],
                    planned_works_handwrite_group_members_contacts[-1]
                ]
            planned_works_group.append(handwrite_group_members)
            planned_works_handwrite_group_member_contacts_boolean = None
            message = "Данные об участнике успешно внесены"
        elif planned_works_begin_date_boolean:
            planned_works_begin_date = event.text
            planned_works_begin_date_boolean = None
            message = "Дата начала работ успешно назначена"
        elif planned_works_end_date_boolean:
            planned_works_end_date = event.text
            planned_works_end_date_boolean = None
            message = "Дата окончания работ успешно назначена"

    if message:
        markup = planned_works_menus.menu_ok
        send_menu(bot, event, message, markup)


# --------------------------------------------------------------------
#                             SEND message                           |
# --------------------------------------------------------------------
#                                                                    |
# The function sends messages to all the chats that you have added   |
#                                                                    |
# --------------------------------------------------------------------
def send_planned_works_message(bot, event):
    """
    This function is needed to send a message
    to all selected chats if there is a message.
    """
    global planned_works_message

    # If all fields are omitted, the message should be considered empty

    #
    fields_not_filled_in = ""
    if \
            planned_works_type == unspecified \
            and planned_works_ES_type == unspecified \
            and planned_works_content == unspecified \
            and len(planned_works_group) == 0 \
            and planned_works_begin_date == unspecified:
        if planned_works_type == unspecified:
            fields_not_filled_in += "Тип работ. "
        if planned_works_ES_type == unspecified:
            fields_not_filled_in += "Тип ЕС. "
        if planned_works_content == unspecified:
            fields_not_filled_in += "Содержание. "
        if len(planned_works_group) == 0:
            fields_not_filled_in += "Группа. "
        if planned_works_begin_date == unspecified:
            fields_not_filled_in += "Дата начала. "
        popup_text = "Не все обязательные поля заполнены: " + fields_not_filled_in
    else:

        if len(planned_works_chats) == 0 and len(planned_works_channels) == 0:
            popup_text = "Чаты/Каналы для отправки не указаны"
            markup = planned_works_menus.chats_empty_menu
            message = popup_text

            send_menu(bot, event, message, markup)
        else:
            text = planned_works_message_head + planned_works_message

            for i in range(len(planned_works_chats)):
                chat = planned_works_chats[i][1]
                bot.send_text(
                    chat_id=chat,
                    text=text
                )
                for file_id in planned_works_files:
                    bot.send_file(
                        chat_id=chat,
                        file_id=file_id
                    )
            for i in range(len(planned_works_channels)):
                channel = planned_works_channels[i][1]
                bot.send_text(
                    chat_id=channel,
                    text=text
                )
                for file_id in planned_works_files:
                    bot.send_file(
                        chat_id=channel,
                        file_id=file_id
                    )

            popup_text = "Сообщение отправлено"

            send_popup_window(bot, event, popup_text)
            clear_planned_works_message(bot, event)
            check_planned_works_message(bot, event)

    send_popup_window(bot, event, popup_text)


# ----------------------------------------------------------------------------------------------------------------------
#                                                     OPEN MENU SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                              |
# The functions to open menus  |
#                              |
# ------------------------------


def open_planned_works_form_menu(bot, event):
    """
    This function is needed to display the message form
    if the user wants to change the message manually.
    """
    message = '|Меню плановых работ|'
    markup = planned_works_menus.form_menu
    popup_text = 'Переход в меню плановых работ'

    send_menu(bot, event, message, markup)
    send_popup_window(bot, event, popup_text)


# ----------------------------------------------------------------------------------------------------------------------
#                                                     SHOW  SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                            |
# Functions in this sector show the value of message fields: |
# 1. Chats                                                   |
# 2. Channels                                                |
# 3. Type                                                    |
# 4. ES Type                                                 |
# 5. Content                                                 |
# 6. Group and contacts                                      |
# 7. Begin date                                              |
# 8. End date                                                |
# 9. Attached files                                          |
# ------------------------------------------------------------


# --------------
# 1. Show chats
# --------------
def show_planned_works_chats(bot, event):
    """
    The function is needed to take data about chats from the list
    and output them in an understandable form
    """

    if len(planned_works_chats) == 0:
        popup_text = "Список чатов пуст"
        markup = planned_works_menus.chats_empty_menu
    else:
        popup_text = "Количество чатов: " + str(len(planned_works_chats))
        text = "Значение сейчас:"
        for i in range(len(planned_works_chats)):
            text += "\n\nЧат №" + str(i + 1) + "\n" + \
                    "Название: " + planned_works_chats[i][0] + "\n" + \
                    "Stamp: " + planned_works_chats[i][1]

        markup = planned_works_menus.chats_check_menu
        send_text(bot, event, text)

    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -----------------
# 2. Show channels
# -----------------
def show_planned_works_channels(bot, event):
    """
    The function is needed to take data about channels from the list
    and output them in an understandable form
    """

    if len(planned_works_channels) == 0:
        popup_text = "Список каналов пуст"
        markup = planned_works_menus.channels_empty_menu
    else:
        popup_text = "Количество каналов: " + str(len(planned_works_channels))
        text = "Значение сейчас:"
        for i in range(len(planned_works_channels)):
            text += "\n\nКанал №" + str(i + 1) + "\n" + \
                    "Название: " + planned_works_channels[i][0] + "\n" + \
                    "Stamp: " + planned_works_channels[i][1]

        markup = planned_works_menus.channels_check_menu
        send_text(bot, event, text)

    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -------------
# 3. Show type
# -------------
def show_planned_works_type(bot, event):
    if planned_works_type == unspecified:
        markup = planned_works_menus.type_empty_menu
    else:
        markup = planned_works_menus.type_check_menu

    popup_text = planned_works_type
    text = "Тип работ: " + planned_works_type
    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)
    send_menu(bot, event, message, markup)


# ----------------
# 4. Show ES type
# ----------------
def show_planned_works_ES_type(bot, event):
    if planned_works_ES_type == unspecified:
        markup = planned_works_menus.ES_type_empty_menu
    else:
        markup = planned_works_menus.ES_type_check_menu

    popup_text = planned_works_type
    text = "Тип ЕС: " + planned_works_ES_type
    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)
    send_menu(bot, event, message, markup)


# ----------------
# 5. Show content
# ----------------
def show_planned_works_content(bot, event):
    if planned_works_content == unspecified:
        markup = planned_works_menus.content_empty_menu
    else:
        markup = planned_works_menus.content_check_menu

    popup_text = planned_works_type
    text = "Содержание работ: " + planned_works_content
    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)
    send_menu(bot, event, message, markup)


# --------------
# 6. Show group
# --------------
def show_planned_works_group(bot, event):
    """
    The function is needed to take data
    about the composition of the group from the list
    and output them in an understandable form
    """
    if len(planned_works_group) == 0:
        popup_text = "Состав группы не указан"
        markup = planned_works_menus.group_empty_menu
    else:
        planned_works_group_string = "Состав и контакты бригады:"
        for i in range(len(planned_works_group)):
            planned_works_group_string += \
                "\n\n" + \
                "Имя: " + planned_works_group[i][0] + \
                "\nКонтакты: " + planned_works_group[i][1]

        popup_text = "Человек в группе: " + str(len(planned_works_group))
        send_text(bot, event, planned_works_group_string)
        markup = planned_works_menus.group_check_menu

    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -------------------
# 7. Show begin date
# -------------------
def show_planned_works_begin_date(bot, event):
    if planned_works_begin_date == unspecified:
        markup = planned_works_menus.begin_date_empty_menu
    else:
        markup = planned_works_menus.begin_date_check_menu

    popup_text = planned_works_begin_date
    text = "Начало проведения работ: " + planned_works_begin_date
    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)
    send_menu(bot, event, message, markup)


# -----------------
# 8. Show end date
# -----------------
def show_planned_works_end_date(bot, event):
    if planned_works_end_date == unspecified:
        markup = planned_works_menus.end_date_empty_menu
    else:
        markup = planned_works_menus.end_date_check_menu

    popup_text = planned_works_type
    text = "Окончание проведения работ: " + planned_works_end_date
    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)
    send_menu(bot, event, message, markup)


# -----------------------
# 9. Show attached files
# -----------------------
def show_planned_works_attached_files(bot, event):
    message = 'Выберите действие'

    if len(planned_works_files) == 0:
        popup_text = "Приложенные файлы отсутствуют"
        markup = planned_works_menus.attached_files_empty_menu
    else:
        popup_text = "Приложено файлов: " + str(len(planned_works_files))
        text = "Приложенные файлы: "
        send_text(bot, event, text)
        markup = planned_works_menus.attached_files_check_menu

        for file_id in planned_works_files:
            bot.send_file(chat_id=event.from_chat,
                          file_id=file_id,
                          caption="Файл №" + str(planned_works_files.index(file_id) + 1))

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# ----------------------------------------------------------------------------------------------------------------------
#                                                      ADD SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                                |
# In this sector there are functions for adding data to fields:  |
# 1.  Chats                                                      |
# 2.  Channels                                                   |
# 3.  Type                                                       |
# 4.  ES Type                                                    |
# 5.  Content                                                    |
# 6.  Group and contacts                                         |
# 7.  Begin date                                                 |
# 8.  End date                                                   |
# 9.  Attached files                                             |
# 10. Handwrite message                                          |
# ----------------------------------------------------------------


# -------------
# 1. Add chats
# -------------
def add_planned_works_chats(bot, event):
    popup_text = "Выберите чаты"
    message = 'Выберите, в какие чаты отправить сообщение'
    markup = planned_works_menus.chats_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def add_to_planned_works_chats_chat(bot, event, number):
    """
    This function is needed to add a chat from templates to the general chat list.
    It does this by dividing the separation of the string by the character '; '.
    _______
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param number: Number of chat`s template from (planned_works_templates.ini)
    """
    planned_works_chat = []

    for i in range(len((config['chats']['chat_' + str(number)]).split('; '))):
        planned_works_chat.append((config['chats']['chat_' + str(number)]).split('; ')[i])
    if planned_works_chat in planned_works_chats:
        popup_text = "Данный чат уже добавлен",
    else:
        planned_works_chats.append(planned_works_chat)

        popup_text = (config['chats']['chat_' + str(number)]).split('; ')[0] + ": добавлен в список чатов для отправки"

    send_popup_window(bot, event, popup_text)


def add_chat_name_to_planned_works_handwrite_chat(bot, event):
    """
    A function to indicate that the next text sent to the bot
    will be the name of the chat
    """
    global planned_works_handwrite_chat_name_boolean

    planned_works_handwrite_chat_name_boolean = True
    text = "Введите название чата ниже:"

    send_text(bot, event, text)


def add_chat_stamp_to_planned_works_handwrite_chat(bot, event):
    """
    A function to indicate that the next text sent to the bot
    will be the stamp of the chat
    """
    global planned_works_handwrite_chat_stamp_boolean

    planned_works_handwrite_chat_stamp_boolean = True
    text = "Введите stamp чата ниже:\n\n" \
           "Stamp - завершающая часть ссылки на чат.\n" \
           "Например, у нас есть закрытая группа с ссылкой \n" \
           "httр://myteam.mail.ru/profile/AoLFuNFynm67V2xGFX0.\n" \
           "Её stamp - это AoLFuNFynm67V2xGFX0"

    send_text(bot, event, text)


def add_to_planned_works_chats_chat_handwrite(bot, event):
    """
    The function is needed to enter chat data manually by the user.
    First he will have to enter the chat name, then the chat stamp.
    At the same time, the chat name is needed for convenience,
    in fact, only the chat stamp is needed to send.
    """
    add_chat_name_to_planned_works_handwrite_chat(bot, event)


def add_to_planned_works_chats_chat_1(bot, event):
    add_to_planned_works_chats_chat(bot, event, 1)


def add_to_planned_works_chats_chat_2(bot, event):
    add_to_planned_works_chats_chat(bot, event, 2)


def add_to_planned_works_chats_chat_3(bot, event):
    add_to_planned_works_chats_chat(bot, event, 3)


# ----------------
# 2. Add channels
# ----------------
def add_planned_works_channels(bot, event):
    popup_text = "Выберите каналы"
    message = 'Выберите, в какие каналы отправить сообщение'
    markup = planned_works_menus.channels_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def add_to_planned_works_channels_channel(bot, event, number):
    """
    This function is needed to add a channel from templates to the general channel list.
    It does this by dividing the separation of the string by the character '; '.
    _______
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param number: Number of channel`s template from (planned_works_templates.ini)
    """
    planned_works_channel = []

    for i in range(len((config['channels']['channel_' + str(number)]).split('; '))):
        planned_works_channel.append((config['channels']['channel_' + str(number)]).split('; ')[i])
    if planned_works_channel in planned_works_channels:
        popup_text = "Данный канал уже добавлен",
    else:
        planned_works_channels.append(planned_works_channel)

        popup_text = \
            (config['channels']['channel_' + str(number)]).split('; ')[0] + \
            ": добавлен в список каналов для отправки"

    send_popup_window(bot, event, popup_text)


def add_channel_name_to_planned_works_handwrite_channel(bot, event):
    """
    A function to indicate that the next text sent to the bot
    will be the name of the channel
    """
    global planned_works_handwrite_channel_name_boolean

    planned_works_handwrite_channel_name_boolean = True
    text = "Введите название канала ниже:"

    send_text(bot, event, text)


def add_channel_stamp_to_planned_works_handwrite_channel(bot, event):
    """
    A function to indicate that the next text sent to the bot
    will be the stamp of the channel
    """
    global planned_works_handwrite_channel_stamp_boolean

    planned_works_handwrite_channel_stamp_boolean = True
    text = "Введите stamp чата ниже:\n\n" \
           "Stamp - завершающая часть ссылки на чат.\n" \
           "Например, у нас есть закрытая группа с ссылкой \n" \
           "httр://myteam.mail.ru/profile/AoLFuNFynm67V2xGFX0.\n" \
           "Её stamp - это AoLFuNFynm67V2xGFX0"

    send_text(bot, event, text)


def add_to_planned_works_channels_channel_handwrite(bot, event):
    """
    The function is needed to enter channel data manually by the user.
    First he will have to enter the channel name, then the channel stamp.
    At the same time, the channel name is needed for convenience,
    in fact, only the channel stamp is needed to send.
    """
    add_channel_name_to_planned_works_handwrite_channel(bot, event)


def add_to_planned_works_channels_channel_1(bot, event):
    add_to_planned_works_channels_channel(bot, event, 1)


def add_to_planned_works_channels_channel_2(bot, event):
    add_to_planned_works_channels_channel(bot, event, 2)


def add_to_planned_works_channels_channel_3(bot, event):
    add_to_planned_works_channels_channel(bot, event, 3)


# ------------
# 3. Add type
# ------------
def add_planned_works_type(bot, event):
    popup_text = "Выберите тип работ"
    message = 'Типы работ'
    markup = planned_works_menus.types_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def set_planned_works_type(bot, event, number):
    """
    This function is needed to add a type from templates
    _______
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param number: Number of type template from (planned_works_templates.ini)

    """
    global planned_works_type

    planned_works_type = config['types']['type_' + str(number)]
    popup_text = "Выбран тип работ: " + config['types']['type_' + str(number)]

    send_popup_window(bot, event, popup_text)
    check_planned_works_message(bot, event)


def add_planned_works_type_handwrite(bot, event):
    """
    The function is needed to enter an indication
    that the next text sent to the bot
    will be the type of planned works
    """
    global planned_works_type_boolean

    planned_works_type_boolean = True
    popup_text = "Напишите тип работ"
    text = "Напишите тип работ ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_planned_works_type_1(bot, event):
    set_planned_works_type(bot, event, 1)


def add_planned_works_type_2(bot, event):
    set_planned_works_type(bot, event, 2)


def add_planned_works_type_3(bot, event):
    set_planned_works_type(bot, event, 3)


def add_planned_works_type_4(bot, event):
    set_planned_works_type(bot, event, 4)


def add_planned_works_type_5(bot, event):
    set_planned_works_type(bot, event, 5)


# ---------------
# 4. Add ES type
# ---------------
def add_planned_works_ES_type(bot, event):
    popup_text = "Выберите тип ЭС"
    message = 'Типы ЭС'
    markup = planned_works_menus.ES_types_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def set_planned_works_ES_type(bot, event, number):
    """
    This function is needed to add es type from templates
    _______
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param number: Number of ES type template from (planned_works_templates.ini)
    """
    global planned_works_ES_type

    planned_works_ES_type = config['ES_types']['type_' + str(number)]
    popup_text = "Выбран тип ЭС: " + config['ES_types']['type_' + str(number)]

    send_popup_window(bot, event, popup_text)
    check_planned_works_message(bot, event)


def add_planned_works_ES_type_handwrite(bot, event):
    """
    The function is needed to enter an indication
    that the next text sent to the bot
    will be the es type of planned works
    """
    global planned_works_ES_type_boolean

    planned_works_ES_type_boolean = True
    popup_text = "Напишите тип ЭС"
    text = "Напишите тип ЭС ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_planned_works_ES_type_1(bot, event):
    set_planned_works_ES_type(bot, event, 1)


def add_planned_works_ES_type_2(bot, event):
    set_planned_works_ES_type(bot, event, 2)


def add_planned_works_ES_type_3(bot, event):
    set_planned_works_ES_type(bot, event, 3)


def add_planned_works_ES_type_4(bot, event):
    set_planned_works_ES_type(bot, event, 4)


def add_planned_works_ES_type_5(bot, event):
    set_planned_works_ES_type(bot, event, 5)


def add_planned_works_ES_type_6(bot, event):
    set_planned_works_ES_type(bot, event, 6)


# ---------------
# 5. Add content
# ---------------
def add_planned_works_content(bot, event):
    """
    The function is needed to enter an indication
    that the next text sent to the bot
    will be the content of planned works

    """
    global planned_works_content_boolean

    planned_works_content_boolean = True
    popup_text = "Напишите содержание работ"
    text = "Напишите содержание работ ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ---------------------
# 6. Add group members
# ---------------------
def add_members_to_planned_works_group(bot, event):
    """
    This function sends a menu in chat
    with a selection of group members to the chat

    """
    popup_text = "Выберите членов группы"
    message = 'Выберите, кого добавить в аварийную группу'
    markup = planned_works_menus.group_members_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def add_member_to_planned_works_group(bot, event, number):
    """
    This function is needed to take data about the
    desired member from the templates from the list
    and add this member to the group
    :param bot: Read the description at the beginning of the file
    :param event: Read the description at the beginning of the file
    :param number: Number of member`s template from (planned_works_templates.ini)

    """
    global planned_works_group

    group_member = []

    for i in range(len((config['group_members']['group_member_' + str(number)]).split('; '))):
        group_member.append((config['group_members']['group_member_' + str(number)]).split('; ')[i])
    if group_member in planned_works_group:
        popup_text = "Данный участник уже добавлен",
    else:
        planned_works_group.append(group_member)

        popup_text = (config['group_members']['group_member_' + str(number)]).split('; ')[0] + ": добавлен(а) в группу"

    send_popup_window(bot, event, popup_text)


def add_to_planned_works_handwrite_group_members_names(bot, event):
    """
    This function indicates that the next text sent to the bot
    will be the name of the member

    """
    global planned_works_handwrite_group_member_name_boolean

    planned_works_handwrite_group_member_name_boolean = True
    text = "Введите имя сотрудника ниже:"

    send_text(bot, event, text)


def add_to_planned_works_handwrite_group_members_contacts(bot, event):
    """
    This function indicates that the next text sent to the bot
    will be the contacts of the member

    """
    global planned_works_handwrite_group_member_contacts_boolean

    planned_works_handwrite_group_member_contacts_boolean = True
    text = "Введите контакты сотрудника ниже:"

    send_text(bot, event, text)


def add_to_planned_works_group_member_handwrite(bot, event):
    """
    This function specifies that the user must enter
    the member's name and contacts manually.

    Then the list with this data: ['Name', 'Contacts']
    will be added to the group of members:
    group = \
    [
        ['Some name', 'Some contacts']
        ['Name', 'Contacts']
    ]

    """

    add_to_planned_works_handwrite_group_members_names(bot, event)


def add_to_planned_works_group_member_1(bot, event):
    add_member_to_planned_works_group(bot, event, 1)


def add_to_planned_works_group_member_2(bot, event):
    add_member_to_planned_works_group(bot, event, 2)


def add_to_planned_works_group_member_3(bot, event):
    add_member_to_planned_works_group(bot, event, 3)


def add_to_planned_works_group_member_4(bot, event):
    add_member_to_planned_works_group(bot, event, 4)


def add_to_planned_works_group_member_5(bot, event):
    add_member_to_planned_works_group(bot, event, 5)


def add_to_planned_works_group_member_6(bot, event):
    add_member_to_planned_works_group(bot, event, 6)


# ------------------
# 7. Add begin date
# ------------------
def add_planned_works_begin_date(bot, event):
    """
    The function is needed to enter an indication
    that the next text sent to the bot
    will be the begin date of planned works

    """
    global planned_works_begin_date_boolean

    popup_text = "Введите время начала работ"
    text = "Введите время начала работ ниже:"
    planned_works_begin_date_boolean = True

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ----------------
# 8. Add end date
# ----------------
def add_planned_works_end_date(bot, event):
    """
    The function is needed to enter an indication
    that the next text sent to the bot
    will be the end date of planned works

    """
    global planned_works_end_date_boolean

    popup_text = "Введите время окончания работ"
    text = "Введите время окончания работ ниже:"
    planned_works_end_date_boolean = True

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ---------------------
# 9. Add attached file
# ---------------------
def add_planned_works_attached_file(bot, event):
    """
    This function is needed for
    1. Sending a message to the user about adding a file.
    2. Give a signal to the bot about adding a file to the file list.

    """
    global \
        planned_works_files_boolean

    planned_works_files_boolean = True

    popup_text = "Отправьте файл"
    text = "Отправьте любой файл не являющийся медиа.\n" \
           "(Не добавляйте подпись к файлу)\n" \
           "⬇ Для добавления файла нажмите (+) слева от поля ввода. "

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_file_to_planned_works_attached_files(bot, event):
    """
    This function is needed for adding a file to the file list.

    """
    global \
        planned_works_files, \
        planned_works_files_boolean

    if planned_works_files_boolean:
        planned_works_files_boolean = None
        file_id = ", ".join([p['payload']['fileId'] for p in event.data['parts']])
        planned_works_files.append(file_id)

        message = "Файл успешно добавлен"
        markup = planned_works_menus.menu_ok
        send_menu(bot, event, message, markup)


# --------------------------
# 10. Add handwrite message
# --------------------------

def add_planned_works_handwrite_message(bot, event):
    """
    The function is needed to enter an indication
    that the next text sent to the bot will be a handwritten message

    """
    global planned_works_handwrite_message_boolean

    popup_text = "Введите свое сообщение:"
    text = "Введите свое сообщение ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)

    planned_works_handwrite_message_boolean = True


# ----------------------------------------------------------------------------------------------------------------------
#                                                      CLEAR SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                                 |
# In this sector there are functions for delete data from fields: |
# 1. Chats                                                        |
# 2. Channels                                                     |
# 3. Type                                                         |
# 4. ES type                                                      |
# 5. Content                                                      |
# 6. Group (members and contacts)                                 |
# 7. Begin date                                                   |
# 8. End date                                                     |
# 9. Attached files                                               |
# 10. Message                                                     |
# -----------------------------------------------------------------

# ---------------
# 1. Clear chats
# ---------------
def clear_planned_works_chats(bot, event):
    """
    This function is needed to clear all lists
    with information about chats
    """
    global \
        planned_works_handwrite_chat_names, \
        planned_works_handwrite_chat_stamps, \
        planned_works_handwrite_chat_name_boolean, \
        planned_works_handwrite_chat_stamp_boolean

    planned_works_chats.clear()
    planned_works_handwrite_chat_names.clear()
    planned_works_handwrite_chat_name_boolean = None
    planned_works_handwrite_chat_stamps.clear()
    planned_works_handwrite_chat_stamp_boolean = None

    popup_text = "Список чатов очищен"

    send_popup_window(bot, event, popup_text)


# ------------------
# 2. Clear channels
# ------------------
def clear_planned_works_channels(bot, event):
    """
    This function is needed to clear all lists
    with information about channels
    """
    global \
        planned_works_handwrite_channel_names, \
        planned_works_handwrite_channel_stamps, \
        planned_works_handwrite_channel_name_boolean, \
        planned_works_handwrite_channel_stamp_boolean

    planned_works_channels.clear()
    planned_works_handwrite_channel_names.clear()
    planned_works_handwrite_channel_name_boolean = None
    planned_works_handwrite_channel_stamps.clear()
    planned_works_handwrite_channel_stamp_boolean = None

    popup_text = "Список чатов очищен"

    send_popup_window(bot, event, popup_text)


# --------------
# 3. Clear type
# --------------
def clear_planned_works_type(bot, event):
    """
    This function is needed to change
    the value of planned works type to default
    """
    global \
        planned_works_type, \
        planned_works_type_boolean

    planned_works_type = unspecified
    planned_works_type_boolean = None

    popup_text = "Тип работ удален"

    send_popup_window(bot, event, popup_text)


# -----------------
# 4. Clear ES type
# -----------------
def clear_planned_works_ES_type(bot, event):
    """
    This function is needed to change
    the value of planned works es type to default
    """
    global \
        planned_works_ES_type, \
        planned_works_ES_type_boolean

    planned_works_ES_type = unspecified
    planned_works_ES_type_boolean = None

    popup_text = "Тип Ес удален"

    send_popup_window(bot, event, popup_text)


# -----------------
# 5. Clear content
# -----------------
def clear_planned_works_content(bot, event):
    """
    This function is needed to change
    the value of planned works content to default
    """
    global \
        planned_works_content, \
        planned_works_content_boolean

    planned_works_content = unspecified
    planned_works_content_boolean = None

    popup_text = "Содержание работ удалено"

    send_popup_window(bot, event, popup_text)


# ---------------
# 6. Clear group
# ---------------
def clear_planned_works_group(bot, event):
    """
    This function is needed to clear all lists
    that contain information about group members
    and their contacts
    """
    global \
        planned_works_group, \
        planned_works_handwrite_group_members_names, \
        planned_works_handwrite_group_member_name_boolean, \
        planned_works_handwrite_group_members_contacts, \
        planned_works_handwrite_group_member_contacts_boolean

    planned_works_group.clear()
    planned_works_handwrite_group_members_names.clear()
    planned_works_handwrite_group_member_name_boolean = None
    planned_works_handwrite_group_members_contacts.clear()
    planned_works_handwrite_group_member_contacts_boolean = None

    popup_text = "Состав группы очищен"

    send_popup_window(bot, event, popup_text)


# --------------------
# 7. Clear begin date
# --------------------
def clear_planned_works_begin_date(bot, event):
    """
    This function is needed to change
    the value of planned works begin date to default

    """
    global \
        planned_works_begin_date, \
        planned_works_begin_date_boolean

    planned_works_begin_date = unspecified
    planned_works_begin_date_boolean = None

    popup_text = "Дата начала работ удалена"

    send_popup_window(bot, event, popup_text)


# ------------------
# 8. Clear end date
# ------------------
def clear_planned_works_end_date(bot, event):
    """
    This function is needed to change
    the value of planned works end date to default

    """
    global \
        planned_works_end_date, \
        planned_works_end_date_boolean

    planned_works_end_date = unspecified
    planned_works_end_date_boolean = None

    popup_text = "Дата окончания работ удалена"

    send_popup_window(bot, event, popup_text)


# -------------------------
# 9. Clear attached files
# -------------------------
def clear_planned_works_attached_files(bot, event):
    """
    This function is needed to clear the list
    with information about the attached files.

    """
    global \
        planned_works_files,\
        planned_works_files_boolean

    planned_works_files.clear()
    planned_works_files_boolean = None

    popup_text = "Список с файлами очищен"
    send_popup_window(bot, event, popup_text)


# -----------------
# 10. Clear message
# -----------------
def clear_planned_works_message(bot, event):
    """
    This function is needed to completely clear the message
    and all its fields.

    """
    global \
        planned_works_message, \
        planned_works_handwrite_message_boolean

    popup_text = "Сообщение было успешно удалено"
    send_popup_window(bot, event, popup_text)

    planned_works_message = ""
    planned_works_handwrite_message_boolean = None
    clear_planned_works_chats(bot, event)
    clear_planned_works_channels(bot, event)
    clear_planned_works_type(bot, event)
    clear_planned_works_ES_type(bot, event)
    clear_planned_works_content(bot, event)
    clear_planned_works_group(bot, event)
    clear_planned_works_begin_date(bot, event)
    clear_planned_works_end_date(bot, event)
    clear_planned_works_attached_files(bot, event)

    check_planned_works_message(bot, event)

# ----------------------------------------------------------------------------------------------------------------------
#                                                      HANDLERS SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                               |
# Event handlers are located in this sector:                    |
# 1. Sending message to the bot                                 |
# 2. Pressing the button                                        |
# ---------------------------------------------------------------


def planned_works_handlers(bot):

    # 1. MESSAGE HANDLERS

    # Handler for simple text message without media content
    bot.dispatcher.add_handler(MessageHandler(
        filters=Filter.text,
        callback=input_planned_works_check))

    # Handler for no media file. For example, text file
    bot.dispatcher.add_handler(MessageHandler(
        filters=Filter.data,
        callback=add_file_to_planned_works_attached_files))

    # 2. BUTTON HANDLERS

    # --------------
    # Check message
    # --------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=check_planned_works_message,
        filters=Filter.callback_data("check_planned_works_message")))

    # -------------
    # Send message
    # -------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=send_planned_works_message,
        filters=Filter.callback_data("send_planned_works_message")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                OPEN HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # -------------------------------------
    # Open planned works form menu handler
    # -------------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=open_planned_works_form_menu,
        filters=Filter.callback_data("open_planned_works_form_menu")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                SHOW HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # ----------------------
    # 1. Show chats handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_planned_works_chats,
        filters=Filter.callback_data("show_planned_works_chats")))

    # -------------------------
    # 2. Show channels handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_planned_works_channels,
        filters=Filter.callback_data("show_planned_works_channels")))

    # ---------------------
    # 3. Show type handler
    # ---------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_planned_works_type,
        filters=Filter.callback_data("show_planned_works_type")))

    # ------------------------
    # 4. Show ES type handler
    # ------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_planned_works_ES_type,
        filters=Filter.callback_data("show_planned_works_ES_type")))

    # ------------------------
    # 5. Show content handler
    # ------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_planned_works_content,
        filters=Filter.callback_data("show_planned_works_content")))

    # ----------------------
    # 6. Show group handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_planned_works_group,
        filters=Filter.callback_data("show_planned_works_group")))

    # ---------------------------
    # 7. Show begin date handler
    # ---------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_planned_works_begin_date,
        filters=Filter.callback_data("show_planned_works_begin_date")))

    # -------------------------
    # 8. Show end date handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_planned_works_end_date,
        filters=Filter.callback_data("show_planned_works_end_date")))

    # -------------------------------
    # 9. Show attached files handler
    # -------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_planned_works_attached_files,
        filters=Filter.callback_data("show_planned_works_attached_files")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                ADD HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # ----------------------
    # 1. Add chats handlers
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_chats,
        filters=Filter.callback_data("add_planned_works_chats")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_chats_chat_handwrite,
        filters=Filter.callback_data("add_to_planned_works_chats_chat_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_chats_chat_1,
        filters=Filter.callback_data("add_to_planned_works_chats_chat_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_chats_chat_2,
        filters=Filter.callback_data("add_to_planned_works_chats_chat_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_chats_chat_3,
        filters=Filter.callback_data("add_to_planned_works_chats_chat_3")))

    # -------------------------
    # 2. Add channels handlers
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_channels,
        filters=Filter.callback_data("add_planned_works_channels")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_channels_channel_handwrite,
        filters=Filter.callback_data("add_to_planned_works_channels_channel_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_channels_channel_1,
        filters=Filter.callback_data("add_to_planned_works_channels_channel_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_channels_channel_2,
        filters=Filter.callback_data("add_to_planned_works_channels_channel_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_channels_channel_3,
        filters=Filter.callback_data("add_to_planned_works_channels_channel_3")))

    # ---------------------
    # 3. Add type handlers
    # ---------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_type,
        filters=Filter.callback_data("add_planned_works_type")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_type_handwrite,
        filters=Filter.callback_data("add_planned_works_type_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_type_1,
        filters=Filter.callback_data("add_planned_works_type_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_type_2,
        filters=Filter.callback_data("add_planned_works_type_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_type_3,
        filters=Filter.callback_data("add_planned_works_type_3")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_type_4,
        filters=Filter.callback_data("add_planned_works_type_4")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_type_5,
        filters=Filter.callback_data("add_planned_works_type_5")))

    # ------------------------
    # 4. Add ES type handlers
    # ------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_ES_type,
        filters=Filter.callback_data("add_planned_works_ES_type")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_ES_type_handwrite,
        filters=Filter.callback_data("add_planned_works_ES_type_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_ES_type_1,
        filters=Filter.callback_data("add_planned_works_ES_type_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_ES_type_2,
        filters=Filter.callback_data("add_planned_works_ES_type_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_ES_type_3,
        filters=Filter.callback_data("add_planned_works_ES_type_3")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_ES_type_4,
        filters=Filter.callback_data("add_planned_works_ES_type_4")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_ES_type_5,
        filters=Filter.callback_data("add_planned_works_ES_type_5")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_ES_type_6,
        filters=Filter.callback_data("add_planned_works_ES_type_6")))

    # -------------------------
    # 5. Add to group handlers
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_members_to_planned_works_group,
        filters=Filter.callback_data("add_members_to_planned_works_group")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_handwrite_group_members_names,
        filters=Filter.callback_data("add_to_planned_works_handwrite_group_members_names")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_group_member_1,
        filters=Filter.callback_data("add_to_planned_works_group_member_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_group_member_2,
        filters=Filter.callback_data("add_to_planned_works_group_member_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_group_member_3,
        filters=Filter.callback_data("add_to_planned_works_group_member_3")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_group_member_4,
        filters=Filter.callback_data("add_to_planned_works_group_member_4")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_group_member_5,
        filters=Filter.callback_data("add_to_planned_works_group_member_5")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_planned_works_group_member_6,
        filters=Filter.callback_data("add_to_planned_works_group_member_6")))

    # -----------------------
    # 6. Add content handler
    # -----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_content,
        filters=Filter.callback_data("add_planned_works_content")))

    # --------------------------
    # 7. Add begin date handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_begin_date,
        filters=Filter.callback_data("add_planned_works_begin_date")))

    # ------------------------
    # 8. Add end date handler
    # ------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_end_date,
        filters=Filter.callback_data("add_planned_works_end_date")))

    # -----------------------------
    # 9. Add attached file handler
    # -----------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_attached_file,
        filters=Filter.callback_data("add_planned_works_attached_file")))

    # ---------------------------------
    # 10. Add handwrite message handler
    # ---------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_planned_works_handwrite_message,
        filters=Filter.callback_data("add_planned_works_handwrite_message")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                               CLEAR HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # -----------------------
    # 1. Clear chats handler
    # -----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_chats,
        filters=Filter.callback_data("clear_planned_works_chats")))

    # --------------------------
    # 2. Clear channels handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_channels,
        filters=Filter.callback_data("clear_planned_works_channels")))

    # ----------------------
    # 3. Clear type handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_type,
        filters=Filter.callback_data("clear_planned_works_type")))

    # -------------------------
    # 4. Clear ES type handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_ES_type,
        filters=Filter.callback_data("clear_planned_works_ES_type")))

    # -------------------------
    # 5. Clear content handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_content,
        filters=Filter.callback_data("clear_planned_works_content")))

    # -----------------------
    # 6. Clear group handler
    # -----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_group,
        filters=Filter.callback_data("clear_planned_works_group")))

    # ----------------------------
    # 7. Clear begin date handler
    # ----------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_begin_date,
        filters=Filter.callback_data("clear_planned_works_begin_date")))

    # --------------------------
    # 8. Clear end date handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_end_date,
        filters=Filter.callback_data("clear_planned_works_end_date")))

    # --------------------------------
    # 9. Clear attached files handler
    # --------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_attached_files,
        filters=Filter.callback_data("clear_planned_works_attached_files")))

    # --------------------------
    # 10. Clear message handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_planned_works_message,
        filters=Filter.callback_data("clear_planned_works_message")))

    # ------------------------------------------------------------------------------------------------------------------
