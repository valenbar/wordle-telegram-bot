#!/usr/bin/env python
from PIL import Image

from telegram import Update, ForceReply, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, PicklePersistence, CallbackQueryHandler

from WordlePlugin import Wordle, GameState
from markups import *
import Config as config
import globals
from functions import monti_on, monti_off, flip_image

def start(update: Update, context: CallbackContext) -> (None):
    """Send a message when the command /start is issued."""
    config.log_new_user(update, context)

    context.user_data["name"] = update.message.from_user.first_name
    context.user_data["user_id"] = update.message.from_user.id
    context.user_data["language"] = "english"
    context.user_data["board_size"] = "5x6"

    help_command(update, context)


def help_command(update: Update, context: CallbackContext) -> (None):
    """Send a message when the command /help is issued."""
    update.message.reply_text(text=config.help_text)
    update.message.reply_text(text=f"Current language: _{context.user_data.get('language')}_", parse_mode='MarkdownV2')
    context.user_data['menu_msg'] = update.message.reply_text("What do you want to do now?", reply_markup=main_menu_markup)



def set_language(update: Update, context: CallbackContext) -> (None):
    """Send a message when the command /set_language is issued."""
    query = update.callback_query
    lan = query.data.split(":")[1]
    if lan == context.user_data.get("language"):
        query.answer()
    else:
        query.answer()
        context.user_data["language"] = lan
        globals.logger.info(f"{query.from_user.first_name} changed language to {lan}")
        context.bot.send_message(globals.LOG_CHANNEL, f"{query.from_user.mention_markdown_v2()} changed language to _{lan}_", parse_mode='MarkdownV2')
    config.show_main_menu(update, context)


def start_game(update: Update, context: CallbackContext) -> (None):
    """Starts a new game"""
    query = update.callback_query
    if query != None:
        query.answer()
        update = query

    menu_msg = context.user_data.get("menu_msg")
    if menu_msg != None:
        try:
            menu_msg.delete()
        except:
            globals.logger.info("could not delete menu message, too much time passed")
            pass
    wordle = Wordle(context.user_data.get("language", "english"))
    context.user_data["wordle"] = wordle
    board_size = context.user_data.get("board_size", "5x6").split("x")
    img = wordle.new_game(int(board_size[0]), int(board_size[1]))
    img.save(config.image_location(update, context))

    with open(config.image_location(update, context), "rb") as img:
        img_msg = update.message.reply_photo(img, reply_markup=give_up_markup)

    board_desc_msg = update.message.reply_text(f"language: _{context.user_data.get('language', 'not sure')}_, *Good luck\!*", parse_mode='MarkdownV2')

    context.user_data["img_msg"] = img_msg
    context.user_data["board_desc_msg"] = board_desc_msg
    globals.logger.info(f"{update.message.from_user.first_name} started a new game, word: {wordle.target_word}")
    context.bot.send_message(globals.LOG_CHANNEL, f"{update.message.from_user.mention_markdown_v2()} started a new game, word: *_{wordle.target_word}_*\n", parse_mode='MarkdownV2')


def check_word(update: Update, context: CallbackContext) -> (None):
    context.user_data['name'] = update.message.from_user.first_name

    # remove message with forbidden chars
    if any(c not in globals.alphabet for c in update.message.text):
        desc_msg = context.user_data.get("board_desc_msg")
        try: desc_msg.edit_text(text=config.bad_word_text)
        except: pass
        update.message.delete()
        return

    # easteregg
    if update.message.text.upper() == "MONTI":
        monti_on(update, context)
        start_game(update, context)
        return

    globals.logger.info(f"{update.message.from_user.first_name} guessed {update.message.text}")
    context.bot.send_message(globals.LOG_CHANNEL, f"{update.message.from_user.mention_markdown_v2()} guessed: _{update.message.text}_", parse_mode='MarkdownV2')
    wordle = context.user_data.get("wordle", None)
    if wordle == None:
        start(update, context)
        return

    if wordle.state == GameState.WON or wordle.state == GameState.LOST or wordle.state == GameState.INIT or wordle is None:
        config.show_main_menu(update, context)
        return

    img = wordle.try_word(update.message.text)
    if img is not None:

        # easteregg
        img = flip_image(context, img)

        img.save(config.image_location(update, context))
        img = open(config.image_location(update, context), "rb")

        context.user_data.get("img_msg").delete()
        context.user_data.get("board_desc_msg").delete()

        if wordle.state == GameState.WON:
            globals.logger.info(f"{update.message.from_user.first_name} won the game")
            context.bot.send_message(globals.LOG_CHANNEL, f"{update.message.from_user.mention_markdown_v2()} won the game", parse_mode='MarkdownV2')
            img_msg = update.message.reply_photo(photo=img)
            update.message.reply_text(f"You won, the word was: __*_{wordle.target_word}_*__", parse_mode='MarkdownV2')
            context.user_data["menu_msg"] = update.message.reply_text("What do you want to do now?", reply_markup=main_menu_markup)
        elif wordle.state == GameState.LOST:
            globals.logger.info(f"{update.message.from_user.first_name} lost the game")
            context.bot.send_message(globals.LOG_CHANNEL, f"{update.message.from_user.mention_markdown_v2()} lost the game", parse_mode='MarkdownV2')
            img_msg = update.message.reply_photo(photo=img)
            update.message.reply_text(f"You lost, the word was: __*_{wordle.target_word}_*__", parse_mode='MarkdownV2')
            context.user_data["menu_msg"] = update.message.reply_text("What do you want to do now?", reply_markup=main_menu_markup)
        else:
            img_msg = update.message.reply_photo(photo=img, reply_markup=give_up_markup)
        if wordle.state == GameState.PLAYING:
            try: context.user_data["board_desc_msg"] = update.message.reply_text(text=config.good_word_text)
            except: pass
        context.user_data["img_msg"] = img_msg

        img.close()
    else:
        if wordle.state == GameState.PLAYING:
            desc_msg = context.user_data["board_desc_msg"]
            if desc_msg is None:
                print("message not found")
            elif len(update.message.text) < len(wordle.target_word):
                try: desc_msg.edit_text(text=config.short_word_text)
                except: pass
            elif len(update.message.text) > len(wordle.target_word):
                try: desc_msg.edit_text(text=config.long_word_text)
                except: pass
            elif len(update.message.text) == len(wordle.target_word):
                try: desc_msg.edit_text(text=config.bad_word_text)
                except: pass
            update.message.delete()


def give_up(update: Update, context: CallbackContext) -> (None):
    """Send a message when the command /give_up is issued."""
    if context.user_data.get('flip', False): monti_off(context)
    query = update.callback_query
    query.answer()
    wordle = context.user_data.get("wordle", None)
    if wordle == None:
        start_game(update, context)
        return
    img_msg = context.user_data.get("img_msg")
    img_msg.delete()
    with open(config.image_location(update, context), "rb") as img:
        query.message.reply_photo(img)
    context.user_data.get("board_desc_msg").delete()
    context.user_data['board_desc_msg'] = query.message.reply_text(fr"You gave up, the word was: __*_{wordle.target_word}_*__", parse_mode='MarkdownV2')
    context.user_data["menu_msg"] = query.message.reply_text("What do you want to do now?", reply_markup=main_menu_markup)
    wordle.state = GameState.INIT
    globals.logger.info(f"{query.from_user.first_name} gave up")
    context.bot.send_message(globals.LOG_CHANNEL, f"{query.from_user.mention_markdown_v2()} gave up", parse_mode='MarkdownV2')


def language_select(update: Update, context: CallbackContext) -> (None):
    """Send a message when the command /language is issued."""
    query = update.callback_query
    query.answer()
    config.show_language_menu(update, context)


def main() -> (None):
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(globals.API_TOKEN, persistence=PicklePersistence(filename="wordle_bot_data"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("new", start_game))
    dispatcher.add_handler(CallbackQueryHandler(set_language, pattern="set_lan:.*"))
    dispatcher.add_handler(CallbackQueryHandler(give_up, pattern="give_up"))
    dispatcher.add_handler(CallbackQueryHandler(start_game, pattern="new_game"))
    dispatcher.add_handler(CallbackQueryHandler(language_select, pattern="change_language"))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_word))

    updater.bot.send_message(globals.LOG_CHANNEL, "Wordle Bot restarting...")
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    globals.initialize()
    globals.logger.info("Starting bot")
    main()
