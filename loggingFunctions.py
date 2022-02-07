
from telegram import Update, User
from telegram.ext import CallbackContext

import globals

def log_new_user(update: Update, context: CallbackContext, name: str, id: int, total_users: int) -> None:
    globals.logger.info(f"new user connected: {name} {id}")
    if globals.LOG_CHANNEL:
        msg = context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"new user: {update.message.from_user.mention_markdown_v2()} \nID: `{update.message.from_user.id}`\nTotal uniqe users: `{total_users}`",
        context.bot.pin_chat_message(globals.LOG_CHANNEL, msg.message_id, disable_notification=True)

def log_language_change(context: CallbackContext, user: User, language: str) -> None:
    globals.logger.info(f"{user.first_name} changed language to {language}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} changed language to _{language}_",
            parse_mode='MarkdownV2')

def log_new_game(context: CallbackContext, user: User, target_word: str) -> None:
    hardmode = context.user_data.get('hardmode', False)
    globals.logger.info(f"{user.first_name} started a new game, word: {target_word}, hardmode: {hardmode}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} started a new game, word: *_{target_word}_*\n" \
                f"language: *{context.user_data.get('language')}*\n" \
                f"hardmode: *{hardmode}*",
            parse_mode='MarkdownV2')

def log_user_guess(context: CallbackContext, user: User, word: str) -> None:
    globals.logger.info(f"{user.first_name} guessed {word}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} guessed: _{word}_",
            parse_mode='MarkdownV2')

def log_user_won(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} won the game")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} won the game",
            parse_mode='MarkdownV2')

def log_user_lost(context: CallbackContext, user: User, target_word: str) -> None:
    globals.logger.info(f"{user.first_name} lost the game, word: {target_word}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} lost the game, word: *_{target_word}_*",
            parse_mode='MarkdownV2')

def log_user_give_up(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} gave up")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} gave up",
            parse_mode='MarkdownV2')

def log_user_command_start(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} executed /start")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} executed /start",
            parse_mode='MarkdownV2')

def log_user_command_help(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} executed /help")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} executed /help",
            parse_mode='MarkdownV2')

def log_user_toggle_hardmode(context: CallbackContext, user: User) -> None:
    hardmode = context.user_data.get('hardmode', False)
    globals.logger.info(f"{user.first_name} toggled hardmode: {hardmode}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} toggled hardmode: *{hardmode}*",
            parse_mode='MarkdownV2')

def log_user_monti(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} typed MONTI")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} called *MONTI*",
            parse_mode='MarkdownV2')