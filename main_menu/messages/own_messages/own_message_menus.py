# ----------------------------------------------------------------------------------------------------------------------
#                                                    MASTER`S  MENUS
# ----------------------------------------------------------------------------------------------------------------------
#                                                      |
# These menus are sent by the 'master'                 |
# depending on whether the fields are filled in or not |
#                                                      |
# ------------------------------------------------------

#
text_empty_markup = \
    [
        [
            {"text": "Добавить текст", "callbackData": "add_own_message_text"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
chats_and_channels_empty_markup = \
    [
        [
            {"text": "Добавить чаты для отправки", "callbackData": "add_own_message_chats"},
            {"text": "Добавить каналы для отправки", "callbackData": "add_own_message_channels"}
        ],
        [
            {"text": "Изменить текст", "callbackData": "set_own_message_text"}
        ],
        [
            {"text": "Очистить", "callbackData": "clear_own_message"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
message_ready_markup = \
    [
        [
            {"text": "Чаты для отправки", "callbackData": "show_own_message_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_own_message_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_own_message_attached_files"}
        ],
        [
            {"text": "Изменить текст", "callbackData": "set_own_message_text"}
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "send_own_message"},
            {"text": "Очистить", "callbackData": "clear_own_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

chats_empty_markup = \
    [
        [
            {"text": "Добавить", "callbackData": "add_own_message_chats"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_own_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

chats_check_markup = \
    [
        [
            {"text": "Оставить", "callbackData": "check_own_message"},
            {"text": "Очистить", "callbackData": "clear_own_message_chats"},
            {"text": "Добавить", "callbackData": "add_own_message_chats"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_own_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

channels_empty_markup = \
    [
        [
            {"text": "Добавить", "callbackData": "add_own_message_channels"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_own_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

channels_check_markup = \
    [
        [
            {"text": "Оставить", "callbackData": "check_own_message"},
            {"text": "Очистить", "callbackData": "clear_own_message_channels"},
            {"text": "Добавить", "callbackData": "add_own_message_channels"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_own_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

attached_files_empty_markup = \
    [
        [
            {"text": "Добавить", "callbackData": "add_own_message_attached_file"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_own_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
attached_files_check_markup = \
    [
        [
            {"text": "Оставить", "callbackData": "check_own_message"},
            {"text": "Очистить", "callbackData": "clear_own_attached_files"},
            {"text": "Добавить", "callbackData": "add_own_message_attached_file"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_own_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

menu_ok = \
    [
        [
            {"text": "ok", "callbackData": "check_own_message"},
        ],
    ]

# ----------------------------------------------------------------------------------------------------------------------
chats_menu = \
    [
        [{"text": "Чат 1", "callbackData": "add_to_own_message_chats_chat_1"}],
        [{"text": "Чат 2", "callbackData": "add_to_own_message_chats_chat_2"}],
        [{"text": "Чат 3", "callbackData": "add_to_own_message_chats_chat_3"}],
        [{"text": "Добавить все чаты", "callbackData": "add_to_own_message_chats_all_chats"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_own_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

channels_menu = \
    [
        [{"text": "Канал 1", "callbackData": "add_to_own_message_channels_channel_1"}],
        [{"text": "Канал 2", "callbackData": "add_to_own_message_channels_channel_2"}],
        [{"text": "Канал 3", "callbackData": "add_to_own_message_channels_channel_3"}],
        [{"text": "Добавить все каналы", "callbackData": "add_to_own_message_channels_all_channels"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_own_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]