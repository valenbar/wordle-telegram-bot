
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


language_menu_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("German", callback_data="set_lan:german"),
            InlineKeyboardButton("English", callback_data="set_lan:english"),
            InlineKeyboardButton("Swedish", callback_data="set_lan:swedish"),
        ],
        [
            InlineKeyboardButton("Back", callback_data="back")
        ]
    ])

give_up_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Give up", callback_data="give_up")
        ]
    ])

def get_settings_menu_markup(context: CallbackContext) -> (InlineKeyboardMarkup):
    """Get the game menu markup"""
    if context.user_data.get("hardmode", False):
        state = "On"
    else:
        state = "Off"
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Change language", callback_data="change_language"),
                InlineKeyboardButton(f"Hardmode: {state}", callback_data="hardmode"),
            ],
            [
                InlineKeyboardButton("Word length", callback_data="board_size_menu"),
                InlineKeyboardButton("Back", callback_data="back")
            ]
        ])

board_size_menu_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("3", callback_data="set_board:3x7"),
            InlineKeyboardButton("4", callback_data="set_board:4x6"),
            InlineKeyboardButton("5", callback_data="set_board:5x6"),
        ],
        [
            InlineKeyboardButton("6", callback_data="set_board:6x6"),
            InlineKeyboardButton("7", callback_data="set_board:7x6"),
            InlineKeyboardButton("Back", callback_data="back")
        ]
    ]
)

main_menu_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Settings", callback_data="settings_menu"),
            InlineKeyboardButton("Feedback", callback_data="feedback")
        ],
        [
            InlineKeyboardButton("New Game", callback_data="new_game")
        ]
    ])

feedback_menu_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Cancel", callback_data="cancel")
        ]
    ]
)

