
from telegram import Update, User
from telegram.ext import CallbackContext

import globals

def log_new_user(update: Update, context: CallbackContext, name: str, id: int, total_users: int) -> (None):
    globals.logger.info(f"new user connected: {name} {id}")
    context.bot.send_message(
        chat_id=globals.LOG_CHANNEL,
        text=f"new user: {update.message.from_user.mention_markdown_v2()} \nID: `{update.message.from_user.id}`\nTotal uniqe users: `{total_users}`",
        parse_mode='MarkdownV2')

def log_language_change(context: CallbackContext, user: User, language: str) -> (None):
    globals.logger.info(f"{user.first_name} changed language to {language}")
    context.bot.send_message(
        chat_id=globals.LOG_CHANNEL,
        text=f"{user.mention_markdown_v2()} changed language to _{language}_",
        parse_mode='MarkdownV2')

def log_new_game(context: CallbackContext, user: User, target_word: str) -> (None):
    globals.logger.info(f"{user.first_name} started a new game, word: {target_word}")
    context.bot.send_message(
        chat_id=globals.LOG_CHANNEL,
        text=f"{user.mention_markdown_v2()} started a new game, word: *_{target_word}_*\n",
        parse_mode='MarkdownV2')

def log_user_guess(context: CallbackContext, user: User, word: str) -> (None):
    globals.logger.info(f"{user.first_name} guessed {word}")
    context.bot.send_message(
        chat_id=globals.LOG_CHANNEL,
        text=f"{user.mention_markdown_v2()} guessed: _{word}_",
        parse_mode='MarkdownV2')

def log_user_won(context: CallbackContext, user: User) -> (None):
    globals.logger.info(f"{user.first_name} won the game")
    context.bot.send_message(
        chat_id=globals.LOG_CHANNEL,
        text=f"{user.mention_markdown_v2()} won the game",
        parse_mode='MarkdownV2')

def log_user_lost(context: CallbackContext, user: User, target_word: str) -> (None):
    globals.logger.info(f"{user.first_name} lost the game, word: {target_word}")
    context.bot.send_message(
        chat_id=globals.LOG_CHANNEL,
        text=f"{user.mention_markdown_v2()} lost the game, word: *_{target_word}_*",
        parse_mode='MarkdownV2')

def log_user_give_up(context: CallbackContext, user: User) -> (None):
    globals.logger.info(f"{user.first_name} gave up")
    context.bot.send_message(
        chat_id=globals.LOG_CHANNEL,
        text=f"{user.mention_markdown_v2()} gave up",
        parse_mode='MarkdownV2')

def log_user_monti(context: CallbackContext, user: User) -> (None):
    globals.logger.info(f"{user.first_name} typed MONTI")
    context.bot.send_message(
        chat_id=globals.LOG_CHANNEL,
        text=f"{user.mention_markdown_v2()} called *MONTI*",
        parse_mode='MarkdownV2')