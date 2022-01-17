
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

settings_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Change language", callback_data="set_lan"),
            InlineKeyboardButton("Change Word Length (placeholder)", callback_data="set_word_length"),
            InlineKeyboardButton("Change Word Count (placeholder)", callback_data="set_word_count"),
            InlineKeyboardButton("Change difficulty (placeholder)", callback_data="set_difficulty")
        ]
    ])

game_settings_markup = ReplyKeyboardMarkup(
    [
        #
    ])

language_menu_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("German", callback_data="set_lan:german"),
            InlineKeyboardButton("English", callback_data="set_lan:english")
        ]
    ])

give_up_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Give up", callback_data="give_up")
        ]
    ])

main_menu_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("New Game", callback_data="new_game"),
            InlineKeyboardButton("Change language", callback_data="change_language")
        ]
    ])

