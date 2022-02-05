
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


language_menu_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("German", callback_data="set_lan:german"),
            InlineKeyboardButton("English", callback_data="set_lan:english"),
            InlineKeyboardButton("Swedish", callback_data="set_lan:swedish")
        ]
    ])

give_up_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Give up", callback_data="give_up")
        ]
    ])

def get_main_menu_markup(context: CallbackContext) -> (InlineKeyboardMarkup):
    """Get the main menu markup"""
    if context.user_data.get("hardmode", False):
        state = "On"
    else:
        state = "Off"
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("New Game", callback_data="new_game"),
                InlineKeyboardButton("Change language", callback_data="change_language"),
                InlineKeyboardButton(f"Hardmode: {state}", callback_data="hardmode")
            ]
        ])

