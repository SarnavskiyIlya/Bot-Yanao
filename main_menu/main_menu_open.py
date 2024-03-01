import json

from bot.filter import Filter
from bot.handler import MessageHandler
from bot.handler import BotButtonCommandHandler
from main_menu import admins


main_menu = \
    [
        [{"text": "📃 Отправить сообщение", "callbackData": "open_message_menu"}],
        [{"text": "ℹ Информация", "callbackData": "show_info"}],
        [{"text": "✉ Почта", "style": "primary", "url": "https://email.yanao.ru"}]
    ]


def sender(bot, chat_id=None, query_id=None, markup=None, message='', text='',
           alert=False, url='', separate_message=''):
    if separate_message:
        bot.send_text(chat_id=chat_id,
                      text=separate_message)
    if markup:
        bot.send_text(chat_id=chat_id,
                      text=message,
                      inline_keyboard_markup=json.dumps(markup))
    if query_id:
        bot.answer_callback_query(
            query_id=query_id,
            text=text,
            show_alert=alert,
            url=url)


def main_menu_input_check(bot, event):
    if event.from_chat in admins.logins and event.text == "меню":

        open_main_menu(bot, event)


def open_main_menu(bot, event):
    sender(bot, chat_id=event.from_chat,
           message='|                   Главное меню          |',
           markup=main_menu
           )

    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text="Переход в главное меню",
    )


def in_development(bot, event):
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text="В разработке",
    )


def main_menu_handlers(bot):
    bot.dispatcher.add_handler(MessageHandler(callback=main_menu_input_check))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=main_menu_input_check,
        filters=Filter.callback_data("main_menu_input_check")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=open_main_menu,
        filters=Filter.callback_data("open_main_menu")))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=in_development,
        filters=Filter.callback_data("in_development")))
