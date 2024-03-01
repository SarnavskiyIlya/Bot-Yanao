from bot.filter import Filter
from bot.handler import MessageHandler, BotButtonCommandHandler


def show_info(bot, event):
    popup_text = "Над ботом работал Сарнавский И.А."

    text = "Бот был сделан на основе VK Teams Bot API \n" \
           "https://myteam.mail.ru/botapi/"

    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=popup_text
    )

    bot.send_text(
        chat_id=event.from_chat,
        text=text
    )


def input_check(bot, event):
    if event.text == "/info":
        show_info(bot, event)


def info_handlers(bot):
    bot.dispatcher.add_handler(MessageHandler(callback=input_check))

    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=show_info,
        filters=Filter.callback_data("show_info")))
