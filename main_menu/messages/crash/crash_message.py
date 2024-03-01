import configparser
import logging

from bot.filter import Filter
from bot.handler import MessageHandler, BotButtonCommandHandler

from main_menu.main_menu_open import sender
from main_menu.messages.crash import crash_menus
from main_menu.messages.crash.crash_config import *

# создаём объекта парсера
crash_templates = configparser.ConfigParser()

# читаем конфиг
crash_templates.read("main_menu\messages\crash\crash_templates.ini", encoding="utf-8")


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
    :param bot:
    :param event:
    :param message: Text above the buttons
    :param markup: The template of the menu that will be sent.
                   All menus are in planned_works_menus.py

    """
    sender(bot,
           chat_id=event.from_chat,
           message=message,
           markup=markup
           )


def send_popup_window(bot, event, popup_text):
    """
    This function is needed for send popup window to necessary chat
    :param bot:
    :param event:
    :param popup_text: The text that will be in the pop-up window
    """
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=popup_text
    )


def send_text(bot, event, text):
    """
    This function is needed for send text to necessary chat
    :param bot:
    :param event:
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
def check_crash_message(bot, event):
    """
    This function is needed to constantly check how the message looks now

    After each message change, this function is called,
    and the bot sends the resulting message to the chat
    """
    global \
        crash_message, \
        crash_handwrite_message_boolean

    if crash_handwrite_message_boolean:
        crash_message = crash_message
        popup_text = "Ваше сообщение готово к отправке"
        markup = crash_menus.check_crash_message_menu
    else:
        # This loop converts the list of affected services into string
        #
        # from this: ['Service 1', 'Service 2']
        #
        # to this:
        # Сервис №1: Service 1
        # Сервис №2: Service 2

        # string form of affected services list
        crash_affected_services_string = unspecified

        if len(crash_affected_services) != 0:
            crash_affected_services_string = ""
            for i in range(len(crash_affected_services)):
                crash_affected_services_string += \
                    "\n\n" + \
                    "Сервис №" + str(i + 1) + " :" + crash_affected_services[i]

        # This loop converts the list of group into string
        #
        # from this: [
        #               ['Name 1', 'Contacts 1']
        #               ['Name 2', 'Contacts 2']
        #            ]
        #
        # to this:
        # Имя: Name 1
        # Контакты: Contacts 1
        #
        # Имя: Name 2
        # Контакты: Contacts 2

        crash_group_string = unspecified  # string form of group list

        if len(crash_group) != 0:
            crash_group_string = ""
            for i in range(len(crash_group)):
                crash_group_string += \
                    "\n\n" + \
                    "Имя: " + crash_group[i][0] + "\n" + \
                    "Контакты: " + crash_group[i][1]

        # The text of the message changes depending on the value of the fields

        if crash_handwrite_message_boolean:
            crash_message = crash_message
        else:
            crash_message = \
                "Тип аварии: " + crash_type + "\n\n" + \
                "Кто доложил: " + crash_reporter + "\n\n" + \
                "Место возникновения: " + crash_location + "\n\n" + \
                "Затронутые сервисы: " + crash_affected_services_string + "\n\n" + \
                "Причина аварии: " + crash_reason + "\n\n" + \
                "Предпринимаемые меры: " + crash_measures_taken + "\n\n" + \
                "Состав и контакты бригады: " + crash_group_string + "\n\n" + \
                "Время начала аварии: " + crash_begin_date + "\n\n" + \
                "Время конца аварии: " + crash_end_date

        # Checking which fields are not set.
        # If the field is not specified, the bot will send the correct menu.

        if len(crash_chats) == 0 and len(crash_channels) == 0:
            popup_text = "Чаты/Каналы для отправки не указаны"
            markup = crash_menus.chats_and_channels_empty_markup
        elif crash_type == unspecified:
            popup_text = "Тип аварии не указан"
            markup = crash_menus.type_empty_markup
        elif crash_reporter == unspecified:
            popup_text = "'Кто доложил' не указан"
            markup = crash_menus.reporter_empty_markup
        elif crash_location == unspecified:
            popup_text = "Место аварии не указано"
            markup = crash_menus.location_empty_markup
        elif crash_affected_services_string == unspecified:
            popup_text = "Затронутые сервисы не указаны"
            markup = crash_menus.affected_services_empty_markup
        elif crash_reason == unspecified:
            popup_text = "Причина не указана"
            markup = crash_menus.reason_empty_markup
        elif crash_measures_taken == unspecified:
            popup_text = "Принятые меры не указаны"
            markup = crash_menus.measures_taken_empty_markup
        elif crash_group_string == unspecified:
            popup_text = "Состав 'аварийной бригады' не указан"
            markup = crash_menus.group_empty_markup
        elif crash_begin_date == unspecified:
            popup_text = "Дата начала аварии не указана"
            markup = crash_menus.begin_date_empty_markup
        elif crash_end_date == unspecified:
            popup_text = "Дата окончания аварии не указана"
            markup = crash_menus.end_date_empty_markup
        else:
            popup_text = "Форма заполнена"
            markup = crash_menus.check_crash_message_menu

    message = popup_text

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, crash_message_head + crash_message)
    send_menu(bot, event, message, markup)


# --------------------------------------------------------------------
#                             INPUT CHECK                            |
# -------------------------------------------------------------------|
#                                                                    |
# Any text you enter goes through this function.                     |
#                                                                    |
# Depending on the boolean variables,                                |
# it assigns the entered text to one or another field                |
#                                                                    |
# --------------------------------------------------------------------

def crashes_input_check(bot, event):
    """
    This function reads any text that the user has entered into the chat.
    It is needed in order to record values manually.
    """
    global \
        crash_handwrite_crash_message_boolean, \
        crash_handwrite_chat_name_boolean, \
        crash_handwrite_chat_stamp_boolean, \
        crash_handwrite_channel_name_boolean, \
        crash_handwrite_channel_stamp_boolean, \
        crash_type, \
        crash_type_handwrite_boolean, \
        crash_reporter, \
        crash_reporter_handwrite_boolean, \
        crash_location, \
        crash_location_handwrite_boolean, \
        crash_affected_services_handwrite_boolean, \
        crash_reason, \
        crash_reason_boolean, \
        crash_measures_taken, \
        crash_measures_taken_boolean, \
        crash_group, \
        crash_handwrite_group_member_name_boolean, \
        crash_handwrite_group_member_contacts_boolean, \
        crash_begin_date, \
        crash_begin_date_boolean, \
        crash_end_date, \
        crash_end_date_boolean, \
        crash_message

    message = ""

    if crash_handwrite_message_boolean:
        crash_message = event.text
        message = "Ваше письмо успешно добавлено"
    else:
        if crash_handwrite_chat_name_boolean:
            crash_handwrite_chat_names.append(event.text)
            crash_handwrite_chat_name_boolean = None
            add_chat_stamp_to_crash_handwrite_chat(bot, event)
        elif crash_handwrite_chat_stamp_boolean:
            crash_handwrite_chat_stamps.append(event.text)
            crash_handwrite_chat_stamp_boolean = None
            handwrite_chat = \
                [
                    crash_handwrite_chat_names[-1],
                    crash_handwrite_chat_stamps[-1]
                ]
            crash_chats.append(handwrite_chat)
            message = "Ваш чат успешно добавлен"
        if crash_handwrite_channel_name_boolean:
            crash_handwrite_channel_names.append(event.text)
            crash_handwrite_channel_name_boolean = None
            add_channel_stamp_to_crash_handwrite_channel(bot, event)
        elif crash_handwrite_channel_stamp_boolean:
            crash_handwrite_channel_stamps.append(event.text)
            crash_handwrite_channel_stamp_boolean = None
            handwrite_channel = \
                [
                    crash_handwrite_channel_names[-1],
                    crash_handwrite_channel_stamps[-1]
                ]
            crash_channels.append(handwrite_channel)
            message = "Ваш канал успешно добавлен"
        elif crash_type_handwrite_boolean:
            crash_type = event.text
            crash_type_handwrite_boolean = None
            message = "Тип аварии успешно изменен"
        elif crash_reporter_handwrite_boolean:
            crash_reporter = event.text
            crash_reporter_handwrite_boolean = None
            message = "Доложившее лицо успешно установлено"
        elif crash_location_handwrite_boolean:
            crash_location = event.text
            crash_location_handwrite_boolean = None
            message = "Локация успешно установлена"
        elif crash_affected_services_handwrite_boolean:
            for i in range(len(event.text.split(';'))):  # split handwrite services by template ';'
                crash_affected_services.append(event.text.split(';')[i])
            crash_affected_services_handwrite_boolean = None
            message = "Задетые сервисы успешно добавлены"
        elif crash_reason_boolean:
            crash_reason = event.text
            crash_reason_boolean = None
            message = "Причина аварии успешно добавлена"
        elif crash_measures_taken_boolean:
            crash_measures_taken = event.text
            crash_measures_taken_boolean = None
            message = "Принятые меры успешно добавлены"
        elif crash_handwrite_group_member_name_boolean:
            crash_handwrite_group_members_names.append(event.text)
            crash_handwrite_group_member_name_boolean = None
            add_to_crash_handwrite_group_members_contacts(bot, event)
        elif crash_handwrite_group_member_contacts_boolean:
            crash_handwrite_group_members_contacts.append(event.text)
            handwrite_group_members = \
                [
                    crash_handwrite_group_members_names[-1],
                    crash_handwrite_group_members_contacts[-1]
                ]
            crash_group.append(handwrite_group_members)
            crash_handwrite_group_member_contacts_boolean = None
            message = "Данные об участнике успешно внесены"
        elif crash_begin_date_boolean:
            crash_begin_date = event.text
            crash_begin_date_boolean = None
            message = "Дата начала аварии успешно установлена"
        elif crash_end_date_boolean:
            crash_end_date = event.text
            crash_end_date_boolean = None
            message = "Дата окончания аварии успешно добавлена"

    if message:
        markup = crash_menus.menu_ok
        send_menu(bot, event, message, markup)


# --------------------------------------------------------------------
#                             SEND message                           |
# -------------------------------------------------------------------|
#                                                                    |
# The function sends messages to all the chats that you have added   |
#                                                                    |
# --------------------------------------------------------------------

def crash_message_send(bot, event):
    """
    This function is needed to send a message
    to all selected chats if there is a message.
    """
    global crash_message

    if crash_message:

        if len(crash_chats) == 0 and len(crash_channels) == 0:
            popup_text = "Чаты/Каналы для отправки не указаны"
            markup = crash_menus.chats_and_channels_empty_markup
            message = popup_text

            send_menu(bot, event, message, markup)
        else:
            text = crash_message_head + crash_message

            for i in range(len(crash_chats)):
                chat = crash_chats[i][1]
                bot.send_text(
                    chat_id=chat,
                    text=text
                )
                for file_id in crash_files:
                    bot.send_file(
                        chat_id=chat,
                        file_id=file_id
                    )
            for i in range(len(crash_channels)):
                channel = crash_channels[i][1]
                bot.send_text(
                    chat_id=channel,
                    text=text
                )
                for file_id in crash_files:
                    bot.send_file(
                        chat_id=channel,
                        file_id=file_id
                    )

            popup_text = "Сообщение отправлено"
            message_author = event.message_author
            logging.info("Пользователь: '" + message_author + "' отправил сообщение об аварии")

            send_popup_window(bot, event, popup_text)
            clear_crash_message(bot, event)
            check_crash_message(bot, event)
    else:
        popup_text = "Сообщение отсутствует, " \
                     "или уже было отправлено"

    send_popup_window(bot, event, popup_text)


# ----------------------------------------------------------------------------------------------------------------------
#                                                     OPEN MENU SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                              |
# The functions to open menus  |
#                              |
# ------------------------------


def open_crash_form_menu(bot, event):
    """
    This function is needed to display the message form
    if the user wants to change the message manually.
    """
    message = 'Меню параметров аварии'
    markup = crash_menus.form_menu
    popup_text = "Пункты для заполнения"

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# ----------------------------------------------------------------------------------------------------------------------
#                                                     SHOW  SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                             |
# Functions in this sector show the value of message fields:  |
# 1.  Chats                                                   |
# 2.  Channels                                                |
# 3.  Type                                                    |
# 4.  Reporter                                                |
# 5.  Location                                                |
# 6.  Affected services                                       |
# 7.  Reason                                                  |
# 8.  Measures taken                                          |
# 9.  Group and contacts                                      |
# 10.  Begin date                                             |
# 11. End date                                                |
# 12. Attached files                                          |
# -------------------------------------------------------------


# --------------
# 1. Show chats
# --------------
def show_crash_chats(bot, event):
    """
    The function is needed to take data about chats from the list
    and output them in an understandable form
    """

    if len(crash_chats) == 0:
        popup_text = "Список чатов пуст"
        markup = crash_menus.chats_empty_menu
    else:
        popup_text = "Количество чатов: " + str(len(crash_chats))
        text = "Значение сейчас:"
        for i in range(len(crash_chats)):
            text += "\n\nЧат №" + str(i + 1) + "\n" + \
                    "Название: " + crash_chats[i][0] + "\n" + \
                    "Stamp: " + crash_chats[i][1]

        markup = crash_menus.chats_check_menu
        send_text(bot, event, text)

    message = 'Выберите действие'

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -----------------
# 2. Show channels
# -----------------
def show_crash_channels(bot, event):
    """
    The function is needed to take data about channels from the list
    and output them in an understandable form
    """

    if len(crash_channels) == 0:
        popup_text = "Список каналов пуст"
        markup = crash_menus.channels_empty_menu
    else:
        popup_text = "Количество каналов: " + str(len(crash_channels))
        text = "Значение сейчас:"
        for i in range(len(crash_channels)):
            text += "\n\nКанал №" + str(i + 1) + "\n" + \
                    "Название: " + crash_channels[i][0] + "\n" + \
                    "Stamp: " + crash_channels[i][1]

        markup = crash_menus.channels_check_menu
        send_text(bot, event, text)

    message = 'Выберите действие'

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -------------
# 3. Show type
# -------------
def show_crash_type(bot, event):
    message = 'Выберите действие'

    if crash_type == unspecified:
        popup_text = "Тип аварии отсутствует"
        markup = crash_menus.type_empty_menu
    else:
        popup_text = "Тип аварии добавлен"
        text = "Значение сейчас: " + crash_type
        send_text(bot, event, text)
        markup = crash_menus.type_check_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -----------------
# 4. Show reporter
# -----------------
def show_crash_reporter(bot, event):
    message = 'Выберите действие'

    if crash_reporter == "" or crash_reporter == unspecified:
        popup_text = "Нет данных о лице подавшем заявку"
        markup = crash_menus.reporter_empty_menu
    else:
        popup_text = "Заявку подал: " + crash_reporter
        text = "Значение сейчас: " + crash_reporter
        send_text(bot, event, text)
        markup = crash_menus.reporter_check_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -----------------
# 5. Show location
# -----------------
def show_crash_location(bot, event):
    message = 'Выберите действие'

    if crash_location == "" or crash_location == unspecified:
        popup_text = "Нет данных о локации"
        markup = crash_menus.location_empty_menu
    else:
        popup_text = "Локация: " + crash_location
        text = "Значение сейчас: " + crash_location
        send_text(bot, event, text)
        markup = crash_menus.location_check_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# --------------------------
# 6. Show affected services
# --------------------------
def show_crash_affected_services(bot, event):
    message = 'Выберите действие'

    if len(crash_affected_services) == 0:
        popup_text = "Нет данных о задетых сервисах"
        markup = crash_menus.affected_services_empty_menu
    else:
        text = "Значение сейчас: \n"
        for i in range(len(crash_affected_services)):
            text += str(i + 1) + ". " + crash_affected_services[i] + ".\n"
        popup_text = "Затронуто cервисов: " + str(len(crash_affected_services))
        send_text(bot, event, text)
        markup = crash_menus.affected_services_check_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# ---------------
# 7. Show reason
# ---------------
def show_crash_reason(bot, event):
    message = 'Выберите действие'

    if crash_reason == "" or crash_reason == unspecified:
        popup_text = "Нет данных о причине"
        markup = crash_menus.reason_empty_menu
    else:
        popup_text = "Есть данные о причине"
        text = "Значение сейчас: " + crash_reason
        send_text(bot, event, text)
        markup = crash_menus.reason_check_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# -----------------------
# 8. Show measures taken
# -----------------------
def show_crash_measures_taken(bot, event):
    message = 'Выберите действие'

    if crash_measures_taken == "" or crash_measures_taken == unspecified:
        popup_text = "Нет данных о принятых мерах"
        markup = crash_menus.measure_taken_empty_menu
    else:
        popup_text = "Есть данные о принятых мерах"
        text = "Значение сейчас: " + crash_measures_taken
        send_text(bot, event, text)
        markup = crash_menus.measure_taken_check_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# --------------
# 9. Show group
# --------------
def show_crash_group(bot, event):
    """
    The function is needed to take data
    about the composition of the group from the list
    and output them in an understandable form
    """
    if len(crash_group) == 0:
        popup_text = "Состав группы не указан"
        markup = crash_menus.group_empty_menu
    else:
        crash_group_string = "Состав и контакты бригады:"
        for i in range(len(crash_group)):
            crash_group_string += \
                "\n\n" + \
                "Имя: " + crash_group[i][0] + \
                "\nКонтакты: " + crash_group[i][1]

        popup_text = "Человек в группе: " + str(len(crash_group))
        send_text(bot, event, crash_group_string)
        markup = crash_menus.group_check_menu

    message = "Выберите действие"

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# --------------------
# 10. Show begin date
# --------------------
def show_crash_begin_date(bot, event):
    if crash_begin_date == unspecified:
        markup = crash_menus.begin_date_empty_menu
    else:
        markup = crash_menus.begin_date_check_menu

    popup_text = crash_begin_date
    text = "Начало аварии: " + crash_begin_date
    message = 'Выберите действие'

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)
    send_menu(bot, event, message, markup)


# ------------------
# 11. Show end date
# ------------------
def show_crash_end_date(bot, event):
    if crash_end_date == unspecified:
        markup = crash_menus.end_date_empty_menu
    else:
        markup = crash_menus.end_date_check_menu

    popup_text = crash_end_date
    text = "Конец аварии: " + crash_end_date
    message = 'Выберите действие'

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)
    send_menu(bot, event, message, markup)


# ------------------------
# 12. Show attached files
# ------------------------
def show_crash_attached_files(bot, event):
    message = 'Выберите действие'

    if len(crash_files) == 0:
        popup_text = "Приложенные файлы отсутствуют"
        markup = crash_menus.attached_files_empty_menu
    else:
        popup_text = "Приложено файлов: " + str(len(crash_files))
        text = "Приложенные файлы: "
        send_text(bot, event, text)
        markup = crash_menus.attached_files_check_menu

        for file_id in crash_files:
            bot.send_file(chat_id=event.from_chat,
                          file_id=file_id,
                          caption="Файл №" + str(crash_files.index(file_id) + 1))

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


# ----------------------------------------------------------------------------------------------------------------------
#                                                      ADD SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                               |
# In this sector there are functions for adding data to fields: |
# 1.  Chats                                                     |
# 2.  Channels                                                  |
# 3.  Type                                                      |
# 4.  Reporter                                                  |
# 5.  Location                                                  |
# 6.  Affected services                                         |
# 7.  Reason                                                    |
# 8.  Measures taken                                            |
# 9.  Members and contacts                                      |
# 10.  Begin date                                               |
# 11. End date                                                  |
# 12. Attached files                                            |
# 13. Handwrite message                                         |
# ---------------------------------------------------------------


# -------------
# 1. Add chats
# -------------
def add_crash_chats(bot, event):
    popup_text = "Выберите чаты"
    message = 'Выберите, в какие чаты отправить сообщение'
    markup = crash_menus.chats_menu

    send_menu(bot, event, message, markup)
    send_popup_window(bot, event, popup_text)


def add_to_crash_chats_chat(bot, event, chat):
    chat_value = crash_templates.get('chats', chat)
    chat_name = chat_value.split('; ')[0]
    chat_stamp = chat_value.split('; ')[1]

    chat = []
    chat.extend([chat_name, chat_stamp])

    if chat in crash_chats:
        popup_text = "Данный чат уже добавлен",
    else:
        crash_chats.append(chat)
        popup_text = chat_name + ": добавлен в список чатов для отправки"

    send_popup_window(bot, event, popup_text)


def add_to_crash_chats_handwrite_chat(bot, event):
    crash_chat = []

    if (len(crash_handwrite_chat_stamps) > 0) and (crash_handwrite_chat_stamps[-1] in crash_handwrite_chat_stamps):
        send_text(bot, event, "Чат с таким Stamp уже был добавлен")
    else:
        crash_chat.append(crash_handwrite_chat_names[-1])
        crash_chat.append(crash_handwrite_chat_stamps[-1])

        crash_chats.append(crash_chat)

        send_text(bot, event, "Чат добавлен")

    check_crash_message(bot, event)


def add_chat_name_to_crash_handwrite_chat(bot, event):
    global crash_handwrite_chat_name_boolean

    crash_handwrite_chat_name_boolean = True
    popup_text = "Введите название"
    text = "Введите название вашего чата:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_chat_stamp_to_crash_handwrite_chat(bot, event):
    global crash_handwrite_chat_stamp_boolean

    crash_handwrite_chat_stamp_boolean = True
    # popup_text = "Введите Stamp"
    text = "Теперь введите stamp вашего чата:\n\n" \
           "Stamp - завершающая часть ссылки на чат.\n" \
           "Например, у нас есть закрытая группа с ссылкой \n" \
           "httр://myteam.mail.ru/profile/AoLFuNFynm67V2xGFX0.\n" \
           "Её stamp - это AoLFuNFynm67V2xGFX0"

    # send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_to_crash_chats_chat_handwrite(bot, event):
    add_chat_name_to_crash_handwrite_chat(bot, event)


def add_to_crash_chats_all_chats(bot, event):
    chats_counter = 0
    for name, value in crash_templates.items('chats'):

        chat_name = value.split('; ')[0]
        chat_stamp = value.split('; ')[1]

        chat = []
        chat.extend([chat_name, chat_stamp])

        if chat not in crash_chats:
            crash_chats.append(chat)
            chats_counter += 1
    if chats_counter == 0:
        popup_text = "Все чаты уже добавлены"
    else:
        popup_text = str(chats_counter) + " чатов было добавлено"
    send_popup_window(bot, event, popup_text)


def add_to_crash_chats_chat_1(bot, event):
    add_to_crash_chats_chat(bot, event, 'chat_1')


def add_to_crash_chats_chat_2(bot, event):
    add_to_crash_chats_chat(bot, event, 'chat_2')


def add_to_crash_chats_chat_3(bot, event):
    add_to_crash_chats_chat(bot, event, 'chat_3')


# ----------------
# 2. Add channels
# ----------------
def add_crash_channels(bot, event):
    popup_text = "Выберите каналы"
    message = 'Выберите, в какие каналы отправить сообщение'
    markup = crash_menus.channels_menu

    send_menu(bot, event, message, markup)
    send_popup_window(bot, event, popup_text)


def add_to_crash_channels_channel(bot, event, channel):
    channel_value = crash_templates.get('channels', channel)
    channel_name = channel_value.split('; ')[0]
    channel_stamp = channel_value.split('; ')[1]

    channel = []
    channel.extend([channel_name, channel_stamp])

    if channel in crash_channels:
        popup_text = "Данный канал уже добавлен",
    else:
        crash_channels.append(channel)
        popup_text = channel_name + ": добавлен в список каналов для отправки"

    send_popup_window(bot, event, popup_text)


def add_to_crash_channels_handwrite_channel(bot, event):
    crash_channel = []

    if (len(crash_handwrite_channel_stamps) > 0) \
            and (crash_handwrite_channel_stamps[-1] in crash_handwrite_channel_stamps):
        send_text(bot, event, "Канал с таким Stamp уже был добавлен")
    else:
        crash_channel.append(crash_handwrite_channel_names[-1])
        crash_channel.append(crash_handwrite_channel_stamps[-1])

        crash_channels.append(crash_channel)

        send_text(bot, event, "Канал добавлен")

    check_crash_message(bot, event)


def add_channel_name_to_crash_handwrite_channel(bot, event):
    global crash_handwrite_chat_name_boolean

    crash_handwrite_chat_name_boolean = True
    popup_text = "Введите название"
    text = "Введите название вашего канала:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_channel_stamp_to_crash_handwrite_channel(bot, event):
    global crash_handwrite_chat_stamp_boolean

    crash_handwrite_chat_stamp_boolean = True
    text = "Теперь введите stamp вашего чата:\n\n" \
           "Stamp - завершающая часть ссылки на чат.\n" \
           "Например, у нас есть закрытая группа с ссылкой \n" \
           "httр://myteam.mail.ru/profile/AoLFuNFynm67V2xGFX0.\n" \
           "Её stamp - это AoLFuNFynm67V2xGFX0"

    send_text(bot, event, text)


def add_to_crash_channels_channel_handwrite(bot, event):
    add_channel_name_to_crash_handwrite_channel(bot, event)


def add_to_crash_channels_all_channels(bot, event):
    channels_counter = 0

    for name, value in crash_templates.items('channels'):

        channel_name = value.split('; ')[0]
        channel_stamp = value.split('; ')[1]

        channel = []
        channel.extend([channel_name, channel_stamp])

        if channel not in crash_channels:
            crash_channels.append(channel)
            channels_counter += 1
    if channels_counter == 0:
        popup_text = "Все каналы уже добавлены"
    else:
        popup_text = str(channels_counter) + " каналов было добавлено"
    send_popup_window(bot, event, popup_text)


def add_to_crash_channels_channel_1(bot, event):
    add_to_crash_channels_channel(bot, event, 'channel_1')


def add_to_crash_channels_channel_2(bot, event):
    add_to_crash_channels_channel(bot, event, 'channel_2')


def add_to_crash_channels_channel_3(bot, event):
    add_to_crash_channels_channel(bot, event, 'channel_3')


# ------------
# 3. Add type
# ------------
def add_crash_type(bot, event):
    popup_text = "Выберите тип аварии"
    message = 'Типы аварий'
    markup = crash_menus.types_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def set_crash_type(bot, event, type_template):
    global crash_type

    crash_type = crash_templates['types'][type_template]
    popup_text = "Тип аварии установлен"

    send_popup_window(bot, event, popup_text)
    check_crash_message(bot, event)


def add_crash_type_handwrite(bot, event):
    global crash_type_handwrite_boolean

    crash_type_handwrite_boolean = True
    popup_text = "Введите тип аварии"
    text = "Введите тип аварии ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_crash_type_1(bot, event):
    set_crash_type(bot, event, 'type_1')


def add_crash_type_2(bot, event):
    set_crash_type(bot, event, 'type_2')


def add_crash_type_3(bot, event):
    set_crash_type(bot, event, 'type_3')


def add_crash_type_4(bot, event):
    set_crash_type(bot, event, 'type_4')


def add_crash_type_5(bot, event):
    set_crash_type(bot, event, 'type_5')


def add_crash_type_6(bot, event):
    set_crash_type(bot, event, 'type_6')


# ----------------
# 4. Add reporter
# ----------------
def add_crash_reporter(bot, event):
    popup_text = "Выберите предприятие"
    message = "Выберите предприятие из списка"
    markup = crash_menus.reporters_menu

    send_menu(bot, event, message, markup)
    send_popup_window(bot, event, popup_text)


def set_crash_reporter(bot, event, reporter):
    global crash_reporter

    crash_reporter = crash_templates['reporters'][reporter]
    popup_text = "Доложивший выбран"

    send_popup_window(bot, event, popup_text)
    check_crash_message(bot, event)


def add_crash_reporter_handwrite(bot, event):
    global crash_reporter_handwrite_boolean

    crash_reporter_handwrite_boolean = True
    popup_text = "Введите 'Кто доложил'"
    text = "Введите, кто доложил об аварии ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_crash_reporter_1(bot, event):
    set_crash_reporter(bot, event, 'reporter_1')


def add_crash_reporter_2(bot, event):
    set_crash_reporter(bot, event, 'reporter_2')


def add_crash_reporter_3(bot, event):
    set_crash_reporter(bot, event, 'reporter_3')


def add_crash_reporter_4(bot, event):
    set_crash_reporter(bot, event, 'reporter_4')


def add_crash_reporter_5(bot, event):
    set_crash_reporter(bot, event, 'reporter_5')


# ----------------
# 5. Add location
# ----------------
def add_crash_location(bot, event):
    popup_text = "Выберите локацию"
    message = "Выберите локацию из списка"
    markup = crash_menus.locations_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def set_crash_location(bot, event, template):
    global crash_location

    crash_location = crash_templates['locations'][template]
    popup_text = "Место аварии выбрано"

    send_popup_window(bot, event, popup_text)
    check_crash_message(bot, event)


def add_crash_location_handwrite(bot, event, location):
    global \
        crash_location, \
        crash_location_handwrite_boolean

    if location:
        crash_location_handwrite_boolean = False
        crash_location = location
        popup_text = "Место аварии введено"

        send_popup_window(bot, event, popup_text)
        check_crash_message(bot, event)
    else:
        crash_location_handwrite_boolean = True
        popup_text = "Введите место аварии"
        text = "Введите место аварии ниже:"

        send_popup_window(bot, event, popup_text)
        send_text(bot, event, text)


def add_crash_location_1(bot, event):
    set_crash_location(bot, event, 'location_1')


def add_crash_location_2(bot, event):
    set_crash_location(bot, event, 'location_2')


def add_crash_location_3(bot, event):
    set_crash_location(bot, event, 'location_3')


def add_crash_location_4(bot, event):
    set_crash_location(bot, event, 'location_4')


def add_crash_location_5(bot, event):
    set_crash_location(bot, event, 'location_5')


# ----------------------------
# 6. Add members and contacts
# ----------------------------
def add_members_to_crash_group(bot, event):
    popup_text = "Выберите членов группы"
    message = 'Выберите, кого добавить в аварийную группу'
    markup = crash_menus.group_members_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def add_member_to_crash_group(bot, event, template):
    global crash_group

    group_member_value = crash_templates.get('group_members', template)
    group_member_name = group_member_value.split("; ")[0]
    group_member_contacts = group_member_value.split("; ")[1]

    group_member = []
    group_member.extend([group_member_name, group_member_contacts])

    if group_member_value in crash_group:
        popup_text = "Данный участник уже добавлен",
    else:
        crash_group.append(group_member)

        popup_text = group_member_name + ": добавлен(а) в группу"

    send_popup_window(bot, event, popup_text)


def add_to_crash_handwrite_group_members_names(bot, event):
    global crash_handwrite_group_member_name_boolean

    crash_handwrite_group_member_name_boolean = True
    text = "Введите имя сотрудника ниже:"

    send_text(bot, event, text)


def add_to_crash_handwrite_group_members_contacts(bot, event):
    global crash_handwrite_group_member_contacts_boolean

    crash_handwrite_group_member_contacts_boolean = True
    text = "Введите контакты сотрудника ниже:"

    send_text(bot, event, text)


def add_to_crash_group_member_handwrite(bot, event):
    add_to_crash_handwrite_group_members_names(bot, event)


def add_to_crash_group_member_1(bot, event):
    add_member_to_crash_group(bot, event, 1)


def add_to_crash_group_member_2(bot, event):
    add_member_to_crash_group(bot, event, 2)


def add_to_crash_group_member_3(bot, event):
    add_member_to_crash_group(bot, event, 3)


def add_to_crash_group_member_4(bot, event):
    add_member_to_crash_group(bot, event, 4)


def add_to_crash_group_member_5(bot, event):
    add_member_to_crash_group(bot, event, 5)


def add_to_crash_group_member_6(bot, event):
    add_member_to_crash_group(bot, event, 6)


# -------------------------
# 7. Add affected services
# -------------------------
def add_crash_affected_services(bot, event):
    popup_text = "Выберите сервисы"
    message = 'Выберите затронутые сервисы'
    markup = crash_menus.services_menu

    send_popup_window(bot, event, popup_text)
    send_menu(bot, event, message, markup)


def add_crash_affected_service(bot, event, number):
    if crash_templates['services']['service_' + str(number)] in crash_affected_services:
        popup_text = "Данный сервис уже добавлен"
    else:
        crash_affected_services.append(crash_templates['services']['service_' + str(number)])
        popup_text = "Добавлен сервис: " + crash_templates['services']['service_' + str(number)]

    send_popup_window(bot, event, popup_text)


def add_crash_affected_service_handwrite(bot, event):
    global crash_affected_services_handwrite_boolean

    crash_affected_services_handwrite_boolean = True
    popup_text = "Введите задетые сервисы"
    text = "Введите задетые сервисы ниже (Разделяйте их точкой с запятой ';'):"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_crash_affected_service_1(bot, event):
    add_crash_affected_service(bot, event, 1)


def add_crash_affected_service_2(bot, event):
    add_crash_affected_service(bot, event, 2)


def add_crash_affected_service_3(bot, event):
    add_crash_affected_service(bot, event, 3)


def add_crash_affected_service_4(bot, event):
    add_crash_affected_service(bot, event, 4)


def add_crash_affected_service_5(bot, event):
    add_crash_affected_service(bot, event, 5)


# --------------
# 8. Add reason
# --------------
def add_crash_reason(bot, event):
    global crash_reason_boolean

    crash_reason_boolean = True
    popup_text = "Введите причину аварии"
    text = "Введите причину аварии ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ----------------------
# 9. Add measures taken
# ----------------------
def add_crash_measures_taken(bot, event):
    global crash_measures_taken_boolean

    popup_text = "Напишите принятые меры"
    text = "Напишите принятые меры ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)

    crash_measures_taken_boolean = 1


# -------------------
# 10. Add begin date
# -------------------
def add_crash_begin_date(bot, event):
    global crash_begin_date_boolean

    crash_begin_date_boolean = True
    popup_text = "Напишите дату и время начала аварии"
    text = "Напишите дату и время начала аварии ниже: "

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# -----------------
# 11. Add end date
# -----------------
def add_crash_end_date(bot, event):
    global crash_end_date_boolean

    crash_end_date_boolean = True
    popup_text = "Напишите дату и время окончания аварии"
    text = "Напишите дату и время окончания аварии ниже: "

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


# ----------------------
# 12. Add attached file
# ----------------------
def add_crash_attached_file(bot, event):
    global \
        crash_files_boolean

    crash_files_boolean = True

    popup_text = "Отправьте файл"
    text = "Отправьте любой файл не являющийся медиа.\n" \
           "(Не добавляйте подпись к файлу)\n" \
           "⬇ Для добавления файла нажмите (+) слева от поля ввода. "

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)


def add_file_to_crash_attached_files(bot, event):
    global \
        crash_files, \
        crash_files_boolean

    if crash_files_boolean:
        crash_files_boolean = None
        file_id = ", ".join([p['payload']['fileId'] for p in event.data['parts']])
        crash_files.append(file_id)

        message = "Файл успешно добавлен"
        markup = crash_menus.menu_ok
        send_menu(bot, event, message, markup)


# -------------------------
# 13. Add handwrite message
# -------------------------
def add_crash_handwrite_message(bot, event):
    global crash_handwrite_message_boolean

    popup_text = "Введите свое сообщение:"
    text = "Введите свое сообщение ниже:"

    send_popup_window(bot, event, popup_text)
    send_text(bot, event, text)

    crash_handwrite_message_boolean = True


# ----------------------------------------------------------------------------------------------------------------------
#                                                      CLEAR SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                                 |
# In this sector there are functions for delete data from fields: |
# 1.  Chats                                                       |
# 2.  Channels                                                    |
# 3.  Type                                                        |
# 4.  Reporter                                                    |
# 5.  Location                                                    |
# 6.  Affected services                                           |
# 7.  Reason                                                      |
# 8.  Measures taken                                              |
# 9.  Members and contacts                                        |
# 10.  Begin date                                                 |
# 11. End date                                                    |
# 12. Attached files                                              |
# 13. Message                                                     |
# -----------------------------------------------------------------


# ---------------
# 1. Clear chats
# ---------------
def clear_crash_chats(bot, event):
    """
    This function is needed to clear all lists
    with information about chats

    """
    global \
        crash_handwrite_chat_name_boolean, \
        crash_handwrite_chat_stamp_boolean

    crash_chats.clear()
    crash_handwrite_chat_names.clear()
    crash_handwrite_chat_name_boolean = None
    crash_handwrite_chat_stamps.clear()
    crash_handwrite_chat_stamp_boolean = None

    popup_text = "Список чатов очищен"
    send_popup_window(bot, event, popup_text)


# ------------------
# 2. Clear channels
# ------------------
def clear_crash_channels(bot, event):
    """
    This function is needed to clear all lists
    with information about channels

    """
    global \
        crash_handwrite_channel_name_boolean, \
        crash_handwrite_channel_stamp_boolean

    crash_channels.clear()
    crash_handwrite_channel_names.clear()
    crash_handwrite_channel_name_boolean = None
    crash_handwrite_channel_stamps.clear()
    crash_handwrite_channel_stamp_boolean = None

    popup_text = "Список каналов очищен"
    send_popup_window(bot, event, popup_text)


# ---------------
# 3. Clear type
# ---------------
def clear_crash_type(bot, event):
    """
    This function is needed to change
    the value of crash type to default

    """
    global \
        crash_type, \
        crash_type_handwrite_boolean

    crash_type = unspecified
    crash_type_handwrite_boolean = None

    popup_text = "Тип аварии удалён"
    send_popup_window(bot, event, popup_text)


# ------------------
# 4. Clear reporter
# ------------------
def clear_crash_reporter(bot, event):
    """
    This function is needed to change
    the value of crash reporter to default

    """
    global \
        crash_reporter, \
        crash_reporter_boolean, \
        crash_reporter_handwrite_boolean

    crash_reporter = unspecified
    crash_reporter_boolean = None
    crash_reporter_handwrite_boolean = None

    popup_text = "Доложившее лицо удалено"
    send_popup_window(bot, event, popup_text)


# ------------------
# 5. Clear location
# ------------------
def clear_crash_location(bot, event):
    """
    This function is needed to change
    the value of crash location to default

    """
    global \
        crash_location, \
        crash_location_boolean, \
        crash_location_handwrite_boolean

    crash_location = unspecified
    crash_location_boolean = None
    crash_location_handwrite_boolean = None

    popup_text = "Локация удалена"
    send_popup_window(bot, event, popup_text)


# ---------------------------
# 6. Clear affected services
# ---------------------------
def clear_crash_affected_services(bot, event):
    """
    This function is needed to change
    the value of crash affected services to default

    """
    global \
        crash_affected_services, \
        crash_affected_services_boolean, \
        crash_affected_services_handwrite_boolean

    crash_affected_services.clear()
    crash_affected_services_boolean = None
    crash_affected_services_handwrite_boolean = None

    popup_text = "Затронутые сервисы удалены"
    send_popup_window(bot, event, popup_text)


# ----------------
# 7. Clear reason
# ----------------
def clear_crash_reason(bot, event):
    """
    This function is needed to change
    the value of crash reason to default

    """
    global \
        crash_reason, \
        crash_reason_boolean

    crash_reason = unspecified
    crash_reason_boolean = None

    popup_text = "Причина удалена"
    send_popup_window(bot, event, popup_text)


# ------------------------
# 8. Clear measures taken
# ------------------------
def clear_crash_measures_taken(bot, event):
    """
    This function is needed to change
    the value of crash measures taken to default

    """
    global \
        crash_measures_taken, \
        crash_measures_taken_boolean

    crash_measures_taken = unspecified
    crash_measures_taken_boolean = None

    popup_text = "Предпринятые меры удалены"
    send_popup_window(bot, event, popup_text)


# ---------------
# 9. Clear group
# ---------------
def clear_crash_group(bot, event):
    """
    This function is needed to clear all lists
    that contain information about group members
    and their contacts

    """
    global \
        crash_handwrite_group_member_name_boolean, \
        crash_handwrite_group_member_contacts_boolean

    crash_group.clear()
    crash_handwrite_group_members_names.clear()
    crash_handwrite_group_member_name_boolean = None
    crash_handwrite_group_members_contacts.clear()
    crash_handwrite_group_member_contacts_boolean = None

    popup_text = "Данные об аварийной группе удалены"
    send_popup_window(bot, event, popup_text)


# ---------------------
# 10. Clear begin date
# ---------------------
def clear_crash_begin_date(bot, event):
    """
    This function is needed to change
    the value of crash begin date to default

    """
    global \
        crash_begin_date, \
        crash_begin_date_boolean

    crash_begin_date = unspecified
    crash_begin_date_boolean = None

    popup_text = "Время начала аварии удалено"
    send_popup_window(bot, event, popup_text)


# -------------------
# 11. Clear end date
# -------------------
def clear_crash_end_date(bot, event):
    """
    This function is needed to change
    the value of crash end date to default

    """
    global \
        crash_end_date, \
        crash_end_date_boolean

    crash_end_date = unspecified
    crash_end_date_boolean = None

    popup_text = "Время начала аварии удалено"
    send_popup_window(bot, event, popup_text)


# -------------------------
# 12. Clear attached files
# -------------------------
def clear_crash_attached_files(bot, event):
    """
    This function is needed to clear the list
    with information about the attached files.

    """
    global \
        crash_files, \
        crash_files_boolean

    crash_files.clear()
    crash_files_boolean = None

    popup_text = "Список с файлами очищен"
    send_popup_window(bot, event, popup_text)


# ------------------
# 13. Clear message
# ------------------
def clear_crash_message(bot, event):
    """
    This function is needed to completely clear the message
    and all its fields.

    """
    global \
        crash_message, \
        crash_handwrite_message_boolean

    popup_text = "Сообщение было успешно удалено"
    send_popup_window(bot, event, popup_text)

    crash_message = ""
    crash_handwrite_message_boolean = None
    clear_crash_chats(bot, event)
    clear_crash_channels(bot, event)
    clear_crash_type(bot, event)
    clear_crash_reporter(bot, event)
    clear_crash_location(bot, event)
    clear_crash_affected_services(bot, event)
    clear_crash_reason(bot, event)
    clear_crash_measures_taken(bot, event)
    clear_crash_group(bot, event)
    clear_crash_begin_date(bot, event)
    clear_crash_end_date(bot, event)
    clear_crash_attached_files(bot, event)

    check_crash_message(bot, event)


# ----------------------------------------------------------------------------------------------------------------------
#                                                      HANDLERS SECTOR
# ----------------------------------------------------------------------------------------------------------------------
#                                                               |
# Event handlers are located in this sector:                    |
# 1. Sending message to the bot                                 |
# 2. Pressing the button                                        |
# ---------------------------------------------------------------


def crash_handlers(bot):
    # 1. MESSAGE HANDLERS

    # Handler for simple text message without media content
    bot.dispatcher.add_handler(MessageHandler(
        filters=Filter.text,
        callback=crashes_input_check))

    # Handler for no media file. For example, text file
    bot.dispatcher.add_handler(MessageHandler(
        filters=Filter.data,
        callback=add_file_to_crash_attached_files))

    # 2. BUTTON HANDLERS

    # ----------------------
    # Check message handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=check_crash_message,
        filters=Filter.callback_data("check_crash_message")))

    # ---------------------
    # Send message handler
    # ---------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=crash_message_send,
        filters=Filter.callback_data("crash_message_send")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                OPEN HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # -----------------------------
    # Open crash form menu handler
    # -----------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=open_crash_form_menu,
        filters=Filter.callback_data("open_crash_form_menu")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                SHOW HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # ----------------------
    # 1. Show chats handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_chats,
        filters=Filter.callback_data("show_crash_chats")))

    # -------------------------
    # 2. Show channels handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_channels,
        filters=Filter.callback_data("show_crash_channels")))

    # ---------------------
    # 3. Show type handler
    # ---------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_type,
        filters=Filter.callback_data("show_crash_type")))

    # -------------------------
    # 4. Show reporter handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_reporter,
        filters=Filter.callback_data("show_crash_reporter")))

    # -------------------------
    # 5. Show location handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_location,
        filters=Filter.callback_data("show_crash_location")))

    # ----------------------------------
    # 6. Show affected services handler
    # ----------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_affected_services,
        filters=Filter.callback_data("show_crash_affected_services")))

    # -----------------------
    # 7. Show reason handler
    # -----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_reason,
        filters=Filter.callback_data("show_crash_reason")))

    # -------------------------------
    # 8. Show measures taken handler
    # -------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_measures_taken,
        filters=Filter.callback_data("show_crash_measures_taken")))

    # ----------------------
    # 9. Show group handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_group,
        filters=Filter.callback_data("show_crash_group")))

    # ----------------------------
    # 10. Show begin date handler
    # ----------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_begin_date,
        filters=Filter.callback_data("show_crash_begin_date")))

    # --------------------------
    # 11. Show end date handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_end_date,
        filters=Filter.callback_data("show_crash_end_date")))

    # --------------------------------
    # 12. Show attached files handler
    # --------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_crash_attached_files,
        filters=Filter.callback_data("show_crash_attached_files")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                                ADD HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # ----------------------
    # 1. Add chats handlers
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_chats,
        filters=Filter.callback_data("add_crash_chats")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_chats_chat_handwrite,
        filters=Filter.callback_data("add_to_crash_chats_chat_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_chats_all_chats,
        filters=Filter.callback_data("add_to_crash_chats_all_chats")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_chats_chat_1,
        filters=Filter.callback_data("add_to_crash_chats_chat_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_chats_chat_2,
        filters=Filter.callback_data("add_to_crash_chats_chat_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_chats_chat_3,
        filters=Filter.callback_data("add_to_crash_chats_chat_3")))

    # ----------------------
    # 2. Add channels handlers
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_channels,
        filters=Filter.callback_data("add_crash_channels")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_channels_channel_handwrite,
        filters=Filter.callback_data("add_to_crash_channels_channel_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_channels_all_channels,
        filters=Filter.callback_data("add_to_crash_channels_all_channels")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_channels_channel_1,
        filters=Filter.callback_data("add_to_crash_channels_channel_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_channels_channel_2,
        filters=Filter.callback_data("add_to_crash_channels_channel_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_channels_channel_3,
        filters=Filter.callback_data("add_to_crash_channels_channel_3")))

    # ---------------------
    # 3. Add type handlers
    # ---------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_type,
        filters=Filter.callback_data("add_crash_type")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_type_handwrite,
        filters=Filter.callback_data("add_crash_type_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_type_1,
        filters=Filter.callback_data("add_crash_type_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_type_2,
        filters=Filter.callback_data("add_crash_type_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_type_3,
        filters=Filter.callback_data("add_crash_type_3")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_type_4,
        filters=Filter.callback_data("add_crash_type_4")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_type_5,
        filters=Filter.callback_data("add_crash_type_5")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_type_6,
        filters=Filter.callback_data("add_crash_type_6")))

    # -------------------------
    # 4. Add reporter handlers
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_reporter,
        filters=Filter.callback_data("add_crash_reporter")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_reporter_handwrite,
        filters=Filter.callback_data("add_crash_reporter_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_reporter_1,
        filters=Filter.callback_data("add_crash_reporter_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_reporter_2,
        filters=Filter.callback_data("add_crash_reporter_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_reporter_3,
        filters=Filter.callback_data("add_crash_reporter_3")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_reporter_4,
        filters=Filter.callback_data("add_crash_reporter_4")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_reporter_5,
        filters=Filter.callback_data("add_crash_reporter_5")))

    # -------------------------
    # 5. Add location handlers
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_location,
        filters=Filter.callback_data("add_crash_location")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_location_handwrite,
        filters=Filter.callback_data("add_crash_location_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_location_1,
        filters=Filter.callback_data("add_crash_location_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_location_2,
        filters=Filter.callback_data("add_crash_location_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_location_3,
        filters=Filter.callback_data("add_crash_location_3")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_location_4,
        filters=Filter.callback_data("add_crash_location_4")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_location_5,
        filters=Filter.callback_data("add_crash_location_5")))

    # ----------------------------------
    # 6. Add affected services handlers
    # ----------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_affected_services,
        filters=Filter.callback_data("add_crash_affected_services")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_affected_service_handwrite,
        filters=Filter.callback_data("add_crash_affected_service_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_affected_service_1,
        filters=Filter.callback_data("add_crash_affected_service_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_affected_service_2,
        filters=Filter.callback_data("add_crash_affected_service_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_affected_service_3,
        filters=Filter.callback_data("add_crash_affected_service_3")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_affected_service_4,
        filters=Filter.callback_data("add_crash_affected_service_4")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_affected_service_5,
        filters=Filter.callback_data("add_crash_affected_service_5")))

    # ----------------------
    # 7. Add reason handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_reason,
        filters=Filter.callback_data("add_crash_reason")))

    # ------------------------------
    # 8. Add measures taken handler
    # ------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_measures_taken,
        filters=Filter.callback_data("add_crash_measures_taken")))

    # -------------------------
    # 9. Add to group handlers
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_members_to_crash_group,
        filters=Filter.callback_data("add_members_to_crash_group")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_group_member_handwrite,
        filters=Filter.callback_data("add_to_crash_group_member_handwrite")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_group_member_1,
        filters=Filter.callback_data("add_to_crash_group_member_1")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_group_member_2,
        filters=Filter.callback_data("add_to_crash_group_member_2")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_group_member_3,
        filters=Filter.callback_data("add_to_crash_group_member_3")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_group_member_4,
        filters=Filter.callback_data("add_to_crash_group_member_4")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_group_member_5,
        filters=Filter.callback_data("add_to_crash_group_member_5")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_to_crash_group_member_6,
        filters=Filter.callback_data("add_to_crash_group_member_6")))

    # ---------------------------
    # 10. Add begin date handler
    # ---------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_begin_date,
        filters=Filter.callback_data("add_crash_begin_date")))

    # -------------------------
    # 11. Add end date handler
    # -------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_end_date,
        filters=Filter.callback_data("add_crash_end_date")))

    # ------------------------------
    # 12. Add attached file handler
    # ------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_attached_file,
        filters=Filter.callback_data("add_crash_attached_file")))

    # ----------------------------------
    # 13. Add handwrite message handler
    # ----------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=add_crash_handwrite_message,
        filters=Filter.callback_data("add_crash_handwrite_message")))

    # ------------------------------------------------------------------------------------------------------------------
    #                                               CLEAR HANDLERS SECTOR
    # ------------------------------------------------------------------------------------------------------------------

    # -----------------------
    # 1. Clear chats handler
    # -----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_chats,
        filters=Filter.callback_data("clear_crash_chats")))

    # --------------------------
    # 2. Clear channels handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_channels,
        filters=Filter.callback_data("clear_crash_channels")))

    # ----------------------
    # 3. Clear type handler
    # ----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_type,
        filters=Filter.callback_data("clear_crash_type")))

    # --------------------------
    # 4. Clear reporter handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_reporter,
        filters=Filter.callback_data("clear_crash_reporter")))

    # --------------------------
    # 5. Clear location handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_location,
        filters=Filter.callback_data("clear_crash_location")))

    # -----------------------------------
    # 6. Clear affected services handler
    # -----------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_affected_services,
        filters=Filter.callback_data("clear_crash_affected_services")))

    # ------------------------
    # 7. Clear reason handler
    # ------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_reason,
        filters=Filter.callback_data("clear_crash_reason")))

    # --------------------------------
    # 8. Clear measures taken handler
    # --------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_measures_taken,
        filters=Filter.callback_data("clear_crash_measures_taken")))

    # -----------------------
    # 9. Clear chats handler
    # -----------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_group,
        filters=Filter.callback_data("clear_crash_group")))

    # -----------------------------
    # 10. Clear begin date handler
    # -----------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_begin_date,
        filters=Filter.callback_data("clear_crash_begin_date")))

    # ---------------------------
    # 11. Clear end date handler
    # ---------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_end_date,
        filters=Filter.callback_data("clear_crash_end_date")))

    # ---------------------------------
    # 12. Clear attached files handler
    # ---------------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_attached_files,
        filters=Filter.callback_data("clear_crash_attached_files")))

    # --------------------------
    # 13. Clear message handler
    # --------------------------
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=clear_crash_message,
        filters=Filter.callback_data("clear_crash_message")))

    # ------------------------------------------------------------------------------------------------------------------
