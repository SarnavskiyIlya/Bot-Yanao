# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
#                                                    MASTER`S  MENUS
# ----------------------------------------------------------------------------------------------------------------------
#                                                      |
# These menus are sent by the 'master'                 |
# depending on whether the fields are filled in or not |
#                                                      |
# ------------------------------------------------------

deferred_message_menu = \
    [
        [
            {"text": "Добавить сообщение", "callbackData": "add_deferred_message"},
            {"text": "Список сообщений", "callbackData": "show_deferred_messages"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

check_deferred_messages_markup = \
    [
        [
            {"text": "Посмотреть детали сообщения", "callbackData": "choose_deferred_message_number"}
        ],
        [
            {"text": "Добавить сообщение", "callbackData": "add_deferred_message"}
        ],
        [
            {"text": "Отправить все преждевременно", "callbackData": "send_all_deferred_messages_prematurely"}
        ],
        [
            {"text": "Подтвердить отправку у всех сообщений", "callbackData": "add_all_messages_to_the_scheduler"}
        ],
        [
            {"text": "Отменить отправку у всех сообщений", "callbackData": "remove_all_messages_from_the_scheduler"}
        ],
        [
            {"text": "🗑 Удалить все сообщения", "callbackData": "delete_all_deferred_messages"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_deferred_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

check_deferred_message_markup = \
    [
        [
            {"text": "Посмотреть чаты/каналы", "callbackData": "show_deferred_message_chats_and_channels"}
        ],
        [
            {"text": "Посмотреть приложенные файлы", "callbackData": "show_deferred_message_attached_files"}
        ],
        [
            {"text": "Изменить текст", "callbackData": "input_deferred_message_text"}
        ],
        [
            {"text": "Изменить время", "callbackData": "input_deferred_message_send_time"},
            {"text": "Изменить дату", "callbackData": "input_deferred_message_send_date"}
        ],
        [
            {"text": "Отменить отправку", "callbackData": "remove_message_from_the_scheduler"},
            {"text": "Подтвердить отправку", "callbackData": "add_message_to_the_scheduler"}
        ],
        [
            {"text": "🗑 Удалить сообщение", "callbackData": "delete_deferred_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_messages"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

add_text_markup = \
    [
        [
            {"text": "Добавить текст сообщения", "callbackData": "input_deferred_message_text"}
        ],
        [
            {"text": "Удалить сообщение", "callbackData": "delete_deferred_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_messages"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

add_send_date_and_time_markup = \
    [
        [
            {"text": "Установить дату отправки", "callbackData": "input_deferred_message_send_date"}
        ],
        [
            {"text": "Установить время отправки", "callbackData": "input_deferred_message_send_time"}
        ],
        [
            {"text": "🗑 Удалить сообщение", "callbackData": "delete_deferred_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_messages"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

add_send_date_markup = \
    [
        [
            {"text": "Установить дату отправки", "callbackData": "input_deferred_message_send_date"}
        ],
        [
            {"text": "🗑 Удалить сообщение", "callbackData": "delete_deferred_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_messages"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

add_send_time_markup = \
    [
        [
            {"text": "Установить время отправки", "callbackData": "input_deferred_message_send_time"}
        ],
        [
            {"text": "🗑 Удалить сообщение", "callbackData": "delete_deferred_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_messages"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

empty_chats_and_channels_markup = \
    [
        [
            {"text": "Указать чаты для отправки", "callbackData": "add_deferred_message_chats"}
        ],
        [
            {"text": "Указать каналы для отправки", "callbackData": "add_deferred_message_channels"}
        ],
        [
            {"text": "Изменить время", "callbackData": "input_deferred_message_send_time"},
            {"text": "Изменить дату", "callbackData": "input_deferred_message_send_date"}
        ],
        [
            {"text": "🗑 Удалить сообщение", "callbackData": "delete_deferred_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_messages"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

chats_and_channels_check_menu = \
    [
        [
            {"text": "Добавить чаты", "callbackData": "add_deferred_message_chats"},
            {"text": "Добавить каналы", "callbackData": "add_deferred_message_channels"}
        ],
        [
            {"text": "Оставить", "callbackData": "show_deferred_message"}
        ],
        [
            {"text": "🗑 Удалить чаты/каналы", "callbackData": "delete_chats_and_channels"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# ----------------------------------------------------------------------------------------------------------------------
#                                               MENUS FOR  MANUAL EDITING
# ----------------------------------------------------------------------------------------------------------------------

chats_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_deferred_message_chats"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

attached_files_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "input_deferred_message_file"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
attached_files_check_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "input_deferred_message_file"},
            {"text": "Оставить", "callbackData": "show_deferred_message"},
            {"text": "🗑 Удалить файлы", "callbackData": "delete_deferred_message_attached_files"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

ok_menu_to_show_messages = \
    [
        [
            {"text": "OK", "callbackData": "show_deferred_messages"}
        ]
    ]

ok_menu_to_show_message = \
    [
        [
            {"text": "OK", "callbackData": "show_deferred_message"}
        ]
    ]

ok_menu_to_add_chats = \
    [
        [
            {"text": "OK", "callbackData": "add_deferred_message_chats"}
        ]
    ]

ok_menu_to_add_channels = \
    [
        [
            {"text": "OK", "callbackData": "add_deferred_message_channels"}
        ]
    ]

ok_menu_to_show_attached_files = \
    [
        [
            {"text": "OK", "callbackData": "show_deferred_message_attached_files"}
        ]
    ]

# ----------------------------------------------------------------------------------------------------------------------
#                                            MENUS WITH A SELECTION OF ITEMS
# ----------------------------------------------------------------------------------------------------------------------

chats_menu = \
    [

        [{"text": "Чат 1", "callbackData": "add_to_deferred_message_chat_1"}],
        [{"text": "Чат 2", "callbackData": "add_to_deferred_message_chat_2"}],
        [{"text": "Чат 3", "callbackData": "add_to_deferred_message_chat_3"}],
        [{"text": "Добавить все чаты", "callbackData": "add_to_deferred_message_all_chats"}],
        [{"text": "✍ Добавить вручную", "callbackData": "input_deferred_message_chat_name"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

channels_menu = \
    [

        [{"text": "Канал 1", "callbackData": "add_to_deferred_message_channel_1"}],
        [{"text": "Канал 2", "callbackData": "add_to_deferred_message_channel_2"}],
        [{"text": "Канал 3", "callbackData": "add_to_deferred_message_channel_3"}],
        [{"text": "Добавить все каналы", "callbackData": "add_to_deferred_message_all_channels"}],
        [{"text": "✍ Добавить вручную", "callbackData": "input_deferred_message_channel_name"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "show_deferred_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]
