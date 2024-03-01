import logging

from bot.bot import Bot

from main_menu.main_menu_open import main_menu_handlers
from main_menu.messages.message_menu_open import message_handlers
from main_menu.messages.crash.crash_message import crash_handlers
from main_menu.messages.planned_works.planned_works_message import planned_works_handlers
from main_menu.messages.deferred_messages.deferred_message import deferred_messages_handlers
from main_menu.messages.deferred_messages.deferred_message import check_availability_of_active_messages
from main_menu.messages.own_messages.own_message import own_message_handlers
from main_menu.info.info import info_handlers


NAME = "Superbot"
VERSION = "1.0.0"
# TOKEN = "001.0207247169.3537649363:1000000012"  # ExampleBot
TOKEN = "001.3869140736.3690680165:1000000011"  # Superbot
OWNER = "iasarnavskiy@yanao.ru"
TEST_CHAT = ""
TEST_USER = ""
API_URL = "https://api.vkteams.yanao.ru/bot/v1"


def create_logger():
    logging.basicConfig(
        level=logging.INFO,
        filename="mylog.log",
        encoding='utf-8',
        format="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
        datefmt='%H:%M:%S',
    )


def main():
    bot = Bot(token=TOKEN, api_url_base=API_URL)
    create_logger()
    main_menu_handlers(bot)
    message_handlers(bot)
    crash_handlers(bot)
    planned_works_handlers(bot)
    deferred_messages_handlers(bot)
    own_message_handlers(bot)
    check_availability_of_active_messages(bot)
    info_handlers(bot)

    bot.start_polling()


if __name__ == '__main__':
    main()
