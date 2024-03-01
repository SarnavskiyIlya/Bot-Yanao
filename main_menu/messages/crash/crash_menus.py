# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
#                                                    MASTER`S  MENUS
# ----------------------------------------------------------------------------------------------------------------------
#                                                      |
# These menus are sent by the 'master'                 |
# depending on whether the fields are filled in or not |
#                                                      |
# ------------------------------------------------------

# If the chats to send are not specified, the bot sends this menu
chats_and_channels_empty_markup = \
    [
        [
            {"text": "Добавить чаты для отправки", "callbackData": "add_crash_chats"},
            {"text": "Добавить каналы для отправки", "callbackData": "add_crash_channels"}
        ],
        [
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the type of crash is not specified, the bot sends this menu
type_empty_markup = \
    [
        [
            {"text": "Добавить тип аварии", "callbackData": "add_crash_type"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_crash_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_crash_attached_files"},
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If who reported the crash is not specified, the bot sends this menu
reporter_empty_markup = \
    [
        [
            {"text": "Добавить 'Кто доложил'", "callbackData": "add_crash_reporter"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_crash_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_crash_attached_files"},
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If location of crash is not specified, the bot sends this menu
location_empty_markup = \
    [
        [
            {"text": "Добавить 'Локацию'", "callbackData": "add_crash_location"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_crash_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_crash_attached_files"},
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the affected services are not specified, the bot sends this menu
affected_services_empty_markup = \
    [
        [
            {"text": "Добавить 'Затронутые сервисы'", "callbackData": "add_crash_affected_services"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_crash_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_crash_attached_files"},
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the reason of crash is not specified, the bot sends this menu
reason_empty_markup = \
    [
        [
            {"text": "Добавить 'Причину аварии'", "callbackData": "add_crash_reason"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_crash_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_crash_attached_files"},
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the measures taken are not specified, the bot sends this menu
measures_taken_empty_markup = \
    [
        [
            {"text": "Добавить 'Принятые меры'", "callbackData": "add_crash_measures_taken"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_crash_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_crash_attached_files"},
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the group members are not specified, the bot sends this menu
group_empty_markup = \
    [
        [
            {"text": "Добавить 'Состав аварийной группы'", "callbackData": "add_members_to_crash_group"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_crash_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_crash_attached_files"},
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the begin date is not specified, the bot sends this menu
begin_date_empty_markup = \
    [
        [
            {"text": "Добавить время начала аварии", "callbackData": "add_crash_begin_date"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_crash_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_crash_attached_files"},
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the end date of crash is not specified, the bot sends this menu
end_date_empty_markup = \
    [
        [
            {"text": "Добавить время конца аварии", "callbackData": "add_crash_end_date"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_crash_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_crash_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_crash_attached_files"},
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить", "callbackData": "clear_crash_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the user clicks on the "Редактировать сообщение вручную" button, the bot sends this menu
form_menu = \
    [
        [{"text": "💬 Чаты для отправки", "callbackData": "show_crash_chats"}],
        [{"text": "📢 Каналы для отправки", "callbackData": "show_crash_channels"}],
        [{"text": "1. Тип аварии", "callbackData": "show_crash_type"}],
        [{"text": "2. Доложивший об аварии", "callbackData": "show_crash_reporter"}],
        [{"text": "3. Место возникновения", "callbackData": "show_crash_location"}],
        [{"text": "4. Затронутые сервисы", "callbackData": "show_crash_affected_services"}],
        [{"text": "5. Причина аварии", "callbackData": "show_crash_reason"}],
        [{"text": "6. Предпринимаемые меры", "callbackData": "show_crash_measures_taken"}],
        [{"text": "7. Состав, контакты аварийно-восстановительной бригады", "callbackData": "show_crash_group"}],
        [{"text": "8. Время начала аварии", "callbackData": "show_crash_begin_date"}],
        [{"text": "9. Время окончания аварии", "callbackData": "show_crash_end_date"}],
        [{"text": "📁 Приложенные файлы", "callbackData": "show_crash_attached_files"}],
        [{"text": "✍ Написать сообщение вручную", "callbackData": "add_crash_handwrite_message"}],
        [{"text": "Посмотреть получившееся сообщение", "style": "primary", "callbackData": "check_crash_message"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# OK menu =)
menu_ok = \
    [
        [
            {"text": "ok", "callbackData": "check_crash_message"},
        ],
    ]

# ----------------------------------------------------------------------------------------------------------------------
#                                           CHECK VALUES OF FIELD`S MENUS
# ----------------------------------------------------------------------------------------------------------------------
#                                         |
# These menus are shown when              |
# the user checks the value of the field  |
#                                         |
# -----------------------------------------

# If chats are not specified, the bot sends this menu
chats_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_chats"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are specified, the bot show the chats and send this menu
chats_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_chats"},
            {"text": "Добавить", "callbackData": "add_crash_chats"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If channels are not specified, the bot sends this menu
channels_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_channels"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If channels are specified, the bot show the chats and send this menu
channels_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_channels"},
            {"text": "Добавить", "callbackData": "add_crash_channels"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are not specified, the bot sends this menu
type_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_type"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are specified, the bot show the chats and send this menu
type_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_type"},
            {"text": "Добавить", "callbackData": "add_crash_type"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are not specified, the bot sends this menu
reporter_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_reporter"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are specified, the bot show the chats and send this menu
reporter_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_reporter"},
            {"text": "Добавить", "callbackData": "add_crash_reporter"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are not specified, the bot sends this menu
location_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_location"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "style": "primary", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are specified, the bot show the chats and send this menu
location_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_location"},
            {"text": "Добавить", "callbackData": "add_crash_location"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "style": "primary", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are not specified, the bot sends this menu
affected_services_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_affected_services"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are specified, the bot show the chats and send this menu
affected_services_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Добавить", "callbackData": "add_crash_affected_services"},
            {"text": "Очистить", "callbackData": "clear_crash_affected_services"},
            {"text": "Добавить", "callbackData": "add_crash_affected_services"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are not specified, the bot sends this menu
reason_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_reason"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are specified, the bot show the chats and send this menu
reason_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_reason"},
            {"text": "Добавить", "callbackData": "add_crash_reason"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are not specified, the bot sends this menu
measure_taken_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_measures_taken"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are specified, the bot show the chats and send this menu
measure_taken_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_measures_taken"},
            {"text": "Добавить", "callbackData": "add_crash_measures_taken"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are not specified, the bot sends this menu
group_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_members_to_crash_group"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are specified, the bot show the chats and send this menu
group_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Добавить", "callbackData": "add_members_to_crash_group"},
            {"text": "Очистить", "callbackData": "clear_crash_group"},
            {"text": "Добавить", "callbackData": "add_members_to_crash_group"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If chats are not specified, the bot sends this menu
begin_date_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_begin_date"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If crash end date are specified, the bot show the chats and send this menu
begin_date_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_begin_date"},
            {"text": "Добавить", "callbackData": "add_crash_begin_date"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If crash end date is not specified, the bot sends this menu
end_date_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_end_date"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If crash end date is specified, the bot show the end date and send this menu
end_date_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_end_date"},
            {"text": "Добавить", "callbackData": "add_crash_end_date"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
attached_files_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_crash_attached_file"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
attached_files_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Очистить", "callbackData": "clear_crash_attached_files"},
            {"text": "Добавить", "callbackData": "add_crash_attached_file"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If all fields are specified, the bot send this menu
check_crash_message_menu = \
    [
        [
            {"text": "Отправить", "style": "primary", "callbackData": "crash_message_send"},
            {"text": "Очистить письмо", "callbackData": "clear_crash_message"},
            {"text": "Посмотреть чаты", "callbackData": "show_crash_chats"},
            {"text": "Посмотреть каналы", "callbackData": "show_crash_channels"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# ----------------------------------------------------------------------------------------------------------------------
#                                            MENUS WITH A SELECTION OF ITEMS
# ----------------------------------------------------------------------------------------------------------------------

# If the user clicks on the "Добавить чаты для отправки" button, the bot sends this menu
chats_menu = \
    [
        [{"text": "Чат 1", "callbackData": "add_to_crash_chats_chat_1"}],
        [{"text": "Чат 2", "callbackData": "add_to_crash_chats_chat_2"}],
        [{"text": "Чат 3", "callbackData": "add_to_crash_chats_chat_3"}],
        [{"text": "✍ Добавить вручную", "callbackData": "add_to_crash_chats_chat_handwrite"}],
        [{"text": "Добавить все чаты", "callbackData": "add_to_crash_chats_all_chats"}],
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Проверить", "callbackData": "show_crash_chats"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the user clicks on the "Добавить каналы для отправки" button, the bot sends this menu
channels_menu = \
    [
        [{"text": "Канал 1", "callbackData": "add_to_crash_channels_channel_1"}],
        [{"text": "Канал 2", "callbackData": "add_to_crash_channels_channel_2"}],
        [{"text": "Канал 3", "callbackData": "add_to_crash_channels_channel_3"}],
        [{"text": "✍ Добавить вручную", "callbackData": "add_to_crash_chats_chat_handwrite"}],
        [{"text": "Добавить все каналы", "callbackData": "add_to_crash_channels_all_channels"}],
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Проверить", "callbackData": "show_crash_channels"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the user clicks on the "Добавить тип аварии" button, the bot sends this menu
types_menu = \
    [
        [{"text": "1. Региональный центр обработки данных ЯНАО", "callbackData": "add_crash_type_1"}],
        [{"text": "2. Магистральная транспортная сеть", "callbackData": "add_crash_type_2"}],
        [{"text": "3. Оборудование РМТКС", "callbackData": "add_crash_type_3"}],
        [{"text": "4. Единый каталог пользователей", "callbackData": "add_crash_type_4"}],
        [{"text": "5. Единый почтовый домен", "callbackData": "add_crash_type_5"}],
        [{"text": "6. РСЭД Тезис", "callbackData": "add_crash_type_6"}],
        [{"text": "✍ Добавить вручную", "style": "primary", "callbackData": "add_crash_type_handwrite"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the user clicks on the "Добавить 'Кто доложил'" button, the bot sends this menu
reporters_menu = \
    [
        [{"text": "1. Инженер ГКУ 'Ресурсы Ямала'", "callbackData": "add_crash_reporter_1"}],
        [{"text": "2. Call-центр", "callbackData": "add_crash_reporter_2"}],
        [{"text": "3. Дергачев Д.В.", "callbackData": "add_crash_reporter_3"}],
        [{"text": "4. Овчинников А.Ю.", "callbackData": "add_crash_reporter_4"}],
        [{"text": "5. Михайлюк Е.В.", "callbackData": "add_crash_reporter_5"}],
        [{"text": "✍ Добавить вручную", "style": "primary", "callbackData": "add_crash_reporter_handwrite"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the user clicks on the "Добавить 'Локацию'" button, the bot sends this menu
locations_menu = \
    [
        [{"text": "ул. Матросова, зд. 29", "callbackData": "add_crash_location_1"}],
        [{"text": "пр. Молодёжи, зд. 9", "callbackData": "add_crash_location_2"}],
        [{"text": "ул. Республики, д. 72", "callbackData": "add_crash_location_3"}],
        [{"text": "ул. Республики, д. 73", "callbackData": "add_crash_location_4"}],
        [{"text": "прочий узел РМТКС", "callbackData": "add_crash_location_5"}],
        [{"text": "✍ Добавить вручную", "style": "primary", "callbackData": "add_crash_location_handwrite"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the user clicks on the "Добавить 'Затронутые сервисы'" button, the bot sends this menu
services_menu = \
    [
        [{"text": "1. Почта", "callbackData": "add_crash_affected_service_1"}],
        [{"text": "2. Виртуализация", "callbackData": "add_crash_affected_service_2"}],
        [{"text": "3. Доступ в сеть Интернет", "callbackData": "add_crash_affected_service_3"}],
        [{"text": "4. Информационная система", "callbackData": "add_crash_affected_service_4"}],
        [{"text": "5. Прочая инфраструктура", "callbackData": "add_crash_affected_service_5"}],
        [{"text": "✍ Добавить вручную", "style": "primary", "callbackData": "add_crash_affected_service_handwrite"}],
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Проверить", "callbackData": "show_crash_affected_services"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# If the user clicks on the "Добавить 'Состав аварийной группы'" button, the bot sends this menu
group_members_menu = \
    [
        [{"text": "Ананьев Е.С.", "callbackData": "add_to_crash_group_member_1"}],
        [{"text": "Владимиров А.К.", "callbackData": "add_to_crash_group_member_2"}],
        [{"text": "Дергачев Д.В.", "callbackData": "add_to_crash_group_member_3"}],
        [{"text": "Михайлюк Е.В.", "callbackData": "add_to_crash_group_member_4"}],
        [{"text": "Овчинников А.Ю.", "callbackData": "add_to_crash_group_member_5"}],
        [{"text": "Райлеску О.П.", "callbackData": "add_to_crash_group_member_6"}],
        [{"text": "✍ Добавить вручную", "style": "primary", "callbackData": "add_to_crash_group_member_handwrite"}],
        [
            {"text": "Оставить", "callbackData": "check_crash_message"},
            {"text": "Проверить", "callbackData": "show_crash_group"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_crash_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]
