import logging

from telegram import Update
from telegram.ext import CallbackContext

from markups import *

# logging.basicConfig(
#     filename='logfile.log', filemode='a', encoding='utf-8', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# clogger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='myapp.log',
                    filemode='a')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
# logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

good_word_text: str = "Good guess, keep trying!"
short_word_text: str = "The word is too short!"
long_word_text: str = "The word is too long!"
bad_word_text: str = "That word is not in the dictionary!"

help_text = "Game rules:\n" \
            "1. You need to guess a 5 letter word.\n" \
            "2. A yellow letter means that the letter is in the word, but in the wrong position.\n" \
            "3. A green letter means that the letter is in the word, and in the right position.\n" \
            "4. You have 6 guesses.\n\n" \
            "Commands:\n" \
            "/start - Resets the bot\n" \
            "/help - Shows this message"

def log_new_user(update: Update, context: CallbackContext):
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
        try:
            menu_msg = menu_msg.edit_text("Choose your language:", reply_markup=language_menu_markup)
        except:
            logger.info("could not edit menu message, too much time passed")
            menu_msg = update.message.reply_text("Choose your language:", reply_markup=language_menu_markup)
            pass
    context.user_data["menu_msg"] = menu_msg


"""
    Commands for botfather:
    start - resets the bot
    new - starts a new game
    language - lets you choose another language
    help - shows this help message
"""