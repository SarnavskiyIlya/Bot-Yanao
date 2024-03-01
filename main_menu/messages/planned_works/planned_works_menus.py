# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
#                                                    MASTER`S  MENUS
# ----------------------------------------------------------------------------------------------------------------------
#                                                      |
# These menus are sent by the 'master'                 |
# depending on whether the fields are filled in or not |
#                                                      |
# ------------------------------------------------------

#
chats_and_channels_empty_markup = \
    [
        [
            {"text": "Добавить чаты для отправки", "callbackData": "add_planned_works_chats"},
            {"text": "Добавить каналы для отправки", "callbackData": "add_planned_works_channels"}
        ],
        [
            {"text": "Редактировать сообщение вручную", "callbackData": "open_planned_works_form_menu"}
        ],
        [
            {"text": "Очистить", "callbackData": "clear_planned_works_message"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
type_empty_markup = \
    [
        [
            {"text": "Установить тип плановых работ", "callbackData": "add_planned_works_type"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_planned_works_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_planned_works_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_planned_works_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_planned_works_attached_files"}
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "send_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
ES_type_empty_markup = \
    [
        [
            {"text": "Установить тип ЭС", "callbackData": "add_planned_works_ES_type"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_planned_works_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_planned_works_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_planned_works_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_planned_works_attached_files"}
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "send_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
content_empty_markup = \
    [
        [
            {"text": "Ввести Содержание работ", "callbackData": "add_planned_works_content"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_planned_works_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_planned_works_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_planned_works_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_planned_works_attached_files"}
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "send_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
group_empty_markup = \
    [
        [
            {"text": "Ввести состав группы плановых работ", "callbackData": "add_members_to_planned_works_group"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_planned_works_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_planned_works_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_planned_works_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_planned_works_attached_files"}
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "send_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
begin_date_empty_markup = \
    [
        [
            {"text": "Ввести время начала плановых работ", "callbackData": "add_planned_works_begin_date"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_planned_works_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_planned_works_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_planned_works_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_planned_works_attached_files"}
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "send_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
end_date_empty_markup = \
    [
        [
            {"text": "Ввести время окончания плановых работ", "callbackData": "add_planned_works_end_date"},
            {"text": "Редактировать сообщение вручную", "callbackData": "open_planned_works_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_planned_works_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_planned_works_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_planned_works_attached_files"}
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "send_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
send_check_planned_works_message = \
    [
        [
            {"text": "Редактировать сообщение вручную", "callbackData": "open_planned_works_form_menu"}
        ],
        [
            {"text": "Чаты для отправки", "callbackData": "show_planned_works_chats"},
            {"text": "Каналы для отправки", "callbackData": "show_planned_works_channels"}
        ],
        [
            {"text": "Приложенные файлы", "callbackData": "show_planned_works_attached_files"}
        ],
        [
            {"text": "Отправить", "style": "primary", "callbackData": "send_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_message"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_message_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# ----------------------------------------------------------------------------------------------------------------------
#                                               MENUS FOR MANUAL EDITING
# ----------------------------------------------------------------------------------------------------------------------

form_menu = \
    [
        [{"text": "💬 Чаты для отправки", "callbackData": "show_planned_works_chats"}],
        [{"text": "📢 Каналы для отправки", "callbackData": "show_planned_works_channels"}],
        [{"text": "1. Тип работ", "callbackData": "show_planned_works_type"}],
        [{"text": "2. Тип ЭС", "callbackData": "show_planned_works_ES_type"}],
        [{"text": "3. Содержание работ", "callbackData": "show_planned_works_content"}],
        [{"text": "4. Состав и контакты бригады", "callbackData": "show_planned_works_group"}],
        [{"text": "5. Начало проведения работ", "callbackData": "show_planned_works_begin_date"}],
        [{"text": "6. Окончание проведения работ", "callbackData": "show_planned_works_end_date"}],
        [{"text": "📁 Приложенные файлы", "callbackData": "show_planned_works_attached_files"}],
        [{"text": "✍ Написать сообщение вручную", "callbackData": "add_planned_works_handwrite_message"}],
        [{"text": "Посмотреть получившееся сообщение", "callbackData": "check_planned_works_message"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

chats_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_planned_works_chats"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

chats_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_chats"},
            {"text": "Добавить", "callbackData": "add_planned_works_chats"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

channels_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_planned_works_channels"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

channels_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_channels"},
            {"text": "Добавить", "callbackData": "add_planned_works_channels"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

type_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_planned_works_type"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

type_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_type"},
            {"text": "Добавить", "callbackData": "open_planned_works_choose_type_menu"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

ES_type_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_planned_works_ES_type"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

ES_type_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_ES_type"},
            {"text": "Добавить", "callbackData": "add_begin_date"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

content_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_planned_works_content"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

content_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_content"},
            {"text": "Добавить", "callbackData": "add_title"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

group_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_members_to_planned_works_group"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

group_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_group"},
            {"text": "Добавить", "callbackData": "add_reporter"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

begin_date_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_planned_works_begin_date"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "style": "primary", "callbackData": "open_main_menu"}
        ]
    ]

begin_date_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_begin_date"},
            {"text": "Добавить", "callbackData": "set_planned_works_end_date"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "style": "primary", "callbackData": "open_main_menu"}
        ]
    ]

end_date_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_planned_works_end_date"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

end_date_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_end_date"},
            {"text": "Добавить", "callbackData": "set_planned_works_begin_date"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
attached_files_empty_menu = \
    [
        [
            {"text": "Добавить", "callbackData": "add_planned_works_attached_file"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

#
attached_files_check_menu = \
    [
        [
            {"text": "Оставить", "callbackData": "check_planned_works_message"},
            {"text": "Очистить", "callbackData": "clear_planned_works_attached_files"},
            {"text": "Добавить", "callbackData": "add_planned_works_attached_file"},
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

check_planned_works_message_menu = \
    [
        [
            {"text": "Отправить", "style": "primary", "callbackData": "send_planned_works_message"},
            {"text": "Очистить письмо", "callbackData": "clear_planned_works_message"}
        ],
        [
            {"text": "Посмотреть чаты", "callbackData": "show_planned_works_chats"},
            {"text": "Посмотреть каналы", "callbackData": "show_planned_works_channels"}
        ],
        [
            {"text": "Назад", "style": "attention", "callbackData": "open_planned_works_menu"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

menu_ok = \
    [
        [
            {"text": "ok", "callbackData": "check_planned_works_message"},
        ],
    ]

# ----------------------------------------------------------------------------------------------------------------------
#                                            MENUS WITH A SELECTION OF ITEMS
# ----------------------------------------------------------------------------------------------------------------------

chats_menu = \
    [
        [{"text": "Чат 1", "callbackData": "add_to_planned_works_chats_chat_1"}],
        [{"text": "Чат 2", "callbackData": "add_to_planned_works_chats_chat_2"}],
        [{"text": "Чат 3", "callbackData": "add_to_planned_works_chats_chat_3"}],
        [{"text": "✍ Добавить вручную", "callbackData": "add_to_planned_works_chats_chat_handwrite"}],
        [{"text": "Добавить все чаты", "callbackData": "add_to_planned_works_chats_all_chats"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

channels_menu = \
    [
        [{"text": "Канал 1", "callbackData": "add_to_planned_works_channels_channel_1"}],
        [{"text": "Канал 2", "callbackData": "add_to_planned_works_channels_channel_2"}],
        [{"text": "Канал 3", "callbackData": "add_to_planned_works_channels_channel_3"}],
        [{"text": "✍ Добавить вручную", "callbackData": "add_to_planned_works_channels_channel_handwrite"}],
        [{"text": "Добавить все каналы", "callbackData": "add_to_planned_works_channels_all_channels"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

types_menu = \
    [
        [{"text": "Плановые", "callbackData": "add_planned_works_type_1"}],
        [{"text": "Неплановые", "callbackData": "add_planned_works_type_2"}],
        [{"text": "Аварийно-восстановительные", "callbackData": "add_planned_works_type_3"}],
        # [{"text": "Тип работ 4", "callbackData": "set_planned_works_type_4"}],
        # [{"text": "Тип работ 5", "callbackData": "set_planned_works_type_5"}],
        [{"text": "✍ Добавить вручную", "callbackData": "set_planned_works_type_handwrite"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

ES_types_menu = \
    [
        [{"text": "Региональный центр обработки данных ЯНАО", "callbackData": "add_planned_works_ES_type_1"}],
        [{"text": "Магистральная транспортная сеть", "callbackData": "add_planned_works_ES_type_2"}],
        [{"text": "Оборудование РМТКС", "callbackData": "add_planned_works_ES_type_3"}],
        [{"text": "Единый каталог пользователей", "callbackData": "add_planned_works_ES_type_4"}],
        [{"text": "Единый почтовый домен", "callbackData": "add_planned_works_ES_type_5"}],
        [{"text": "РСЭД Тезис", "callbackData": "add_planned_works_ES_type_6"}],
        [{"text": "✍ Добавить вручную", "callbackData": "add_planned_works_ES_type_handwrite"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

group_members_menu = \
    [
        [{"text": "Ананьев Е.С.", "callbackData": "add_to_planned_works_group_member_1"}],
        [{"text": "Владимиров А.К.", "callbackData": "add_to_planned_works_group_member_2"}],
        [{"text": "Дергачев Д.В.", "callbackData": "add_to_planned_works_group_member_3"}],
        [{"text": "Михайлюк Е.В.", "callbackData": "add_to_planned_works_group_member_4"}],
        [{"text": "Овчинников А.Ю.", "callbackData": "add_to_planned_works_group_member_5"}],
        [{"text": "Райлеску О.П.", "callbackData": "add_to_planned_works_group_member_6"}],
        [{"text": "✍ Добавить вручную", "callbackData": "add_to_planned_works_group_member_handwrite"}],
        [
            {"text": "Назад", "style": "attention", "callbackData": "check_planned_works_message"},
            {"text": "На главную", "callbackData": "open_main_menu"}
        ]
    ]

# ----------------------------------------------------------------------------------------------------------------------
