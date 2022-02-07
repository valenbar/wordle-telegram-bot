#!/usr/bin/env python

from telegram import Update, ForceReply, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, PicklePersistence, CallbackQueryHandler

from WordlePlugin import Wordle, GameState
from markups import *
import Config as config
import globals
from functions import *
from loggingFunctions import *

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    handle_new_user(update, context)

    context.user_data["name"] = update.message.from_user.first_name
    context.user_data["user_id"] = update.message.from_user.id
    context.user_data["language"] = "english"
    context.user_data["board_size"] = "5x6"
    context.user_data["hardmode"] = False

    update.message.reply_text(text=config.help_text)
    update.message.reply_text(text=f"Current language: _{context.user_data.get('language')}_", parse_mode='MarkdownV2')
    context.user_data['menu_msg'] = update.message.reply_text("What do you want to do now?", reply_markup=get_main_menu_markup(context))
    log_user_command_start(context, update.message.from_user)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(text=config.help_text)
    update.message.reply_text(text=f"Current language: _{context.user_data.get('language')}_", parse_mode='MarkdownV2')
    context.user_data['menu_msg'] = update.message.reply_text("What do you want to do now?", reply_markup=get_main_menu_markup(context))
    log_user_command_help(context, update.message.from_user)


def set_language(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /set_language is issued."""
    query = update.callback_query
    lan = query.data.split(":")[1]
    if lan == context.user_data.get("language"):
        query.answer()
    else:
        query.answer()
        context.user_data["language"] = lan
        log_language_change(context, query.from_user, lan)
    show_main_menu(update, context)


def start_game(update: Update, context: CallbackContext) -> None:
    """Starts a new game"""
    query = update.callback_query
    update_backup = update
    if query != None:
        query.answer()
        update = query

    menu_msg = context.user_data.get("menu_msg")
    if menu_msg != None:
        try:
            menu_msg.delete()
        except Exception as e:
            print(e)
            pass
    wordle = Wordle(context.user_data.get("language", "english"))
    context.user_data["wordle"] = wordle
    board_size = context.user_data.get("board_size", "5x6").split("x")
    img = wordle.new_game(
        x=int(board_size[0]),
        y=int(board_size[1]),
        hardmode=context.user_data.get("hardmode", False))
    img.save(image_location(context))

    if context.user_data.get("hardmode", False): hardmode = "On"
    else: hardmode = "Off"
    with open(image_location(context), "rb") as img:
        img_msg = update.message.reply_photo(
            photo=img,
            caption=f"language: _{context.user_data.get('language', 'not sure')}_, hardmode: _{hardmode}_, *Good luck\!*",
            parse_mode='MarkdownV2',
            reply_markup=give_up_markup)
    context.user_data["img_msg"] = img_msg

    if query == None:
        update = update_backup.message
    log_new_game(context, update.from_user, wordle.target_word)


def check_word(update: Update, context: CallbackContext) -> None:
    context.user_data['name'] = update.message.from_user.first_name

    # remove message with forbidden chars
    if any(c not in globals.alphabet for c in update.message.text):
        img_msg = context.user_data.get("img_msg")
        try: img_msg.edit_caption(caption=config.bad_word_text, reply_markup=give_up_markup)
        except: pass
        update.message.delete()
        return

    # easteregg
    if update.message.text.upper() == "MONTI":
        monti_on(update, context)
        start_game(update, context)
        return

    log_user_guess(context, update.message.from_user, update.message.text)
    wordle = context.user_data.get("wordle", None)
    if wordle == None:
        start(update, context)
        return

    if wordle.state == GameState.WON or wordle.state == GameState.LOST or wordle.state == GameState.INIT or wordle is None:
        show_main_menu(update, context)
        return

    img = wordle.try_word(update.message.text)
    if img is not None:

        # easteregg
        img = flip_image(context, img)

        img.save(image_location(context))
        img = open(image_location(context), "rb")

        context.user_data.get("img_msg").delete()

        if wordle.state == GameState.WON:
            log_user_won(context, update.message.from_user)
            img_msg = update.message.reply_photo(
                photo=img,
                caption=f"You won, the word was: __*_{wordle.target_word}_*__",
                parse_mode='MarkdownV2')
            context.user_data["menu_msg"] = update.message.reply_text("What do you want to do now?", reply_markup=get_main_menu_markup(context))
        elif wordle.state == GameState.LOST:
            log_user_lost(context, update.message.from_user, wordle.target_word)
            img_msg = update.message.reply_photo(
                photo=img,
                caption=f"You lost, the word was: __*_{wordle.target_word}_*__",
                parse_mode='MarkdownV2')
            context.user_data["menu_msg"] = update.message.reply_text(
                text="What do you want to do now?",
                reply_markup=get_main_menu_markup(context))
        elif wordle.state == GameState.PLAYING:
            context.user_data["img_msg"] = update.message.reply_photo(
                photo=img,
                caption=config.good_word_text,
                reply_markup=give_up_markup)
        img.close()
    else:
        if wordle.state == GameState.PLAYING:
            img_msg = context.user_data["img_msg"]
            if img_msg is None:
                print("message not found")
            elif len(update.message.text) < len(wordle.target_word):
                try: img_msg.edit_caption(caption=config.short_word_text, reply_markup=give_up_markup)
                except: pass
            elif len(update.message.text) > len(wordle.target_word):
                try: img_msg.edit_caption(caption=config.long_word_text, reply_markup=give_up_markup)
                except: pass
            elif len(update.message.text) == len(wordle.target_word):
                try: img_msg.edit_caption(caption=config.bad_word_text, reply_markup=give_up_markup)
                except: pass
            update.message.delete()


def give_up(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /give_up is issued."""
    if context.user_data.get('flip', False): monti_off(context)
    query = update.callback_query
    query.answer()
    wordle = context.user_data.get("wordle", None)
    if wordle == None:
        start_game(update, context)
        return
    img_msg = context.user_data.get("img_msg")
    img_msg.edit_caption(
        caption=f"You gave up, the word was: __*_{wordle.target_word}_*__",
        parse_mode='MarkdownV2')
    context.user_data["menu_msg"] = query.message.reply_text("What do you want to do now?", reply_markup=get_main_menu_markup(context))
    wordle.state = GameState.INIT
    log_user_give_up(context, update.callback_query.from_user)


def language_select(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /language is issued."""
    query = update.callback_query
    query.answer()
    show_language_menu(update, context)


def toggle_hardmode(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    hardmode = context.user_data.get('hardmode', False)
    context.user_data['hardmode'] = not hardmode
    log_user_toggle_hardmode(context=context, user=update.callback_query.from_user)
    if query.message != None:
        query.message.edit_reply_markup(reply_markup=get_main_menu_markup(context))
    else:
        context.user_data["menu_msg"] = query.message.reply_text(text="What do you want to do now?", reply_markup=get_main_menu_markup(context))


def main() -> None:
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
    dispatcher.add_handler(CallbackQueryHandler(toggle_hardmode, pattern="hardmode"))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_word))

    if globals.LOG_CHANNEL:
        updater.bot.send_message(globals.LOG_CHANNEL, "Wordle Bot starting...")
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
