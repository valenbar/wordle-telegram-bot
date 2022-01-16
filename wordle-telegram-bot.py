#!/usr/bin/env python

import logging
from dotenv import load_dotenv
import os

from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, PicklePersistence, CallbackQueryHandler

from WordlePlugin import Wordle, GameState
# from ImageExport import ImageExport


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> (None):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Hi {update.message.from_user.first_name}!')
    context.user_data["name"] = update.message.from_user.first_name
    help_command(update, context)

def change_language(update: Update, context: CallbackContext) -> (None):
    """show buttons to choose a language"""
    query = update.callback_query
    InlineKeyboard = [
        [InlineKeyboardButton("German", callback_data="set_lan:german")],
        [InlineKeyboardButton("English", callback_data="set_lan:english")]
    ]
    if query == None:
        msg_out = f"Choose a language, current language is: " + context.user_data.get("language", "german")
        update.message.reply_text(text=msg_out, reply_markup=InlineKeyboardMarkup(InlineKeyboard))
    elif query.data.split(":")[1] == context.user_data.get("language"):
        query.answer()
    else:
        query.answer()
        context.user_data["language"] = query.data.split(":")[1]
        logging.info("%s changed language to %s", context.user_data.get('name'), query.data.split(':')[1])
        msg_out = f"Choose a language, current language is: " + context.user_data.get("language", "german")
        query.edit_message_text(text=msg_out + "\nstart a new game with /new", reply_markup=InlineKeyboardMarkup(InlineKeyboard))


def start_game(update: Update, context: CallbackContext) -> (None):
    """Starts a new game"""
    wordle = Wordle(context.user_data.get("language", "german"))
    context.user_data["wordle"] = wordle
    img = wordle.new_game(x=5, y=6)
    img.save("out.png")
    img = open("./out.png", "rb")
#     update.message.reply_text(wordle.target_word)
    board_img_msg = update.message.reply_photo(img)
    board_desc_msg = update.message.reply_text("Good luck!")

    context.user_data["board_img_msg"] = board_img_msg.message_id
    context.user_data["board_desc_msg"] = board_desc_msg
    logger.info(f"{update.message.from_user.first_name} started a new game word: " + wordle.target_word)


def check_word(update: Update, context: CallbackContext) -> (None):
    logger.info(f"{update.message.from_user.first_name} guessed {update.message.text}")
    wordle = context.user_data["wordle"]

    if wordle is None:
        update.message.repyl_text("You need to start a game first! you can use /new")
        return
    if wordle.state == GameState.LOST:
        update.message.reply_text("You lost the game! Start a new one with /new")
        return
    if wordle.state == GameState.WON:
        update.message.reply_text("You won the game! Start a new one with /new")
        return

    img = wordle.try_word(update.message.text)
    if img is not None:
        img.save("out.png")
        img = open("./out.png", "rb")
        context.bot.delete_message(message_id=context.user_data["board_img_msg"], chat_id=update.message.chat_id)
        context.user_data.get("board_desc_msg").delete()
        # context.bot.delete_message(message_id=context.user_data["board_desc_msg"].message_id, chat_id=update.message.chat_id)
        context.user_data["board_img_msg"] = update.message.reply_photo(img).message_id
        context.user_data["board_desc_msg"] = update.message.reply_text("That looks good!")
        # update.edit_message_media(chat_id=update.message.chat_id, message_id=context.user_data["board_img_msg"], media=img)
        # context.user_data["board_img_msg"].
    # else:
    if wordle.state == GameState.LOST:
        logger.info(f"{update.message.from_user.first_name} lost the game")
        context.user_data.get("board_img_msg").edit_text(f"You lost, the word was: {wordle.target_word}\nStart a new one with /new")
        # update.message.reply_text(f"You lost, the word was: {wordle.target_word}\nStart a new one with /new")
    if wordle.state == GameState.WON:
        logger.info(f"{update.message.from_user.first_name} won the game")
        context.user_data.get("board_desc_msg").edit_text(f"You won, the word was: {wordle.target_word}\nStart a new one with /new")
        # update.message.reply_text("You won the game! Start a new one with /new")
    if wordle.state == GameState.PLAYING and img is None:
        # update.message.reply_text("Try another word")
        context.user_data.get("board_desc_msg").edit_text("Try another word")
    if wordle.state == GameState.INIT:
        update.message.reply_text("You need to start a game first! you can use /new")

def help_command(update: Update, context: CallbackContext) -> (None):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Commands:\n /start - resets the bot\n /new - starts a new game\n /language - lets you choose another language\n /help - shows this help message')


def main() -> (None):
    """Start the bot."""
    load_dotenv()
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ.get("API_TOKEN"), persistence=PicklePersistence(filename="wordle_bot_data"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("new", start_game))
    dispatcher.add_handler(CommandHandler("language", change_language))
    dispatcher.add_handler(CallbackQueryHandler(change_language, pattern="set_lan:.*"))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_word))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
