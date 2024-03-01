from bot.filter import Filter
# from bot.handler import MessageHandler
from bot.handler import BotButtonCommandHandler

# from main_menu import admins
# from main_menu import menus
from main_menu.main_menu_open import sender


message_menu = \
    [
        [{"text": "🚨 Сообщение об аварии", "style": "attention", "callbackData": "check_crash_message"}],
        [{"text": "🗓 Плановые работы", "callbackData": "check_planned_works_message"}],
        [{"text": "🕑 Написать отложенное сообщение", "callbackData": "open_deferred_message_menu"}],
        [{"text": "✍ Свое сообщение", "callbackData": "check_own_message"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_main_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}

        ]
    ]


def open_message_menu(bot, event):
    sender(bot, chat_id=event.from_chat,
           message='|                       Отправка сообщений                |',
           markup=message_menu
           )

    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text="Переход в меню отправки сообщений",
    )


def message_handlers(bot):
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=open_message_menu,
        filters=Filter.callback_data("open_message_menu")))
