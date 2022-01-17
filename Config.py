
import logging

from telegram import Update
from telegram.ext import CallbackContext

from markups import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def log_new_user(update: Update, context: CallbackContext):
    logger.info(f"new user connected: {update.message.from_user.first_name} {update.message.from_user.id}")
    with open("users.txt", "a") as f:
        f.write(f"{update.message.from_user.first_name} {update.message.from_user.id}\n")

def send_start_message(update: Update, context: CallbackContext):
    return update.message.reply_text("Hi " + update.message.from_user.first_name + "!")

def image_location(update: Update, context: CallbackContext):
    return "./out" + str(context.user_data.get('user_id', '0000')) + ".png"

def game_lost(update: Update, context: CallbackContext):
    return update.message.reply_text("You lost!")

def show_main_menu(update: Update, context: CallbackContext):
    menu_msg = context.user_data.get("menu_msg")
    if menu_msg is None:
        menu_msg = update.message.reply_text("Choose an option:", reply_markup=main_menu_markup)
    else:
        menu_msg = menu_msg.edit_text("Choose an option:", reply_markup=main_menu_markup)
    context.user_data["menu_msg"] = menu_msg

# def show_language_menu(update: Update, context: CallbackContext):
#     menu_msg = context.user_data.get("menu_msg")
#     if menu_msg is not None:
#         menu_msg.delete()
#     menu_msg = update.message.reply_text("Choose a language", reply_markup=language_menu_markup)
#     context.user_data["menu_msg"] = menu_msg

def show_language_menu(update: Update, context: CallbackContext):
    menu_msg = context.user_data.get('menu_msg')
    if menu_msg is None:
        menu_msg = update.message.reply_text("Choose your language:", reply_markup=language_menu_markup)
    else:
        menu_msg = menu_msg.edit_text("Choose your language:", reply_markup=language_menu_markup)
    context.user_data["menu_msg"] = menu_msg


"""
    Commands for botfather:
    start - resets the bot
    new - starts a new game
    language - lets you choose another language
    help - shows this help message
"""