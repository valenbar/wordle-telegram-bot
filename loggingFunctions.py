
from telegram import Update, User
from telegram.ext import CallbackContext

import globals

def log_new_user(update: Update, context: CallbackContext, name: str, id: int, total_users: int) -> None:
    globals.logger.info(f"new user connected: {name} {id}")
    if globals.LOG_CHANNEL:
        msg = context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"new user: {update.message.from_user.mention_markdown_v2()} \nID: `{update.message.from_user.id}`\nTotal uniqe users: `{total_users}`",
            parse_mode='MarkdownV2',
            disable_notification=False
        )
        context.bot.pin_chat_message(globals.LOG_CHANNEL, msg.message_id, disable_notification=True)

def log_language_change(context: CallbackContext, user: User, language: str) -> None:
    globals.logger.info(f"{user.first_name} changed language to {language}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} changed language to _{language}_",
            parse_mode='MarkdownV2',
            disable_notification=True
        )

def log_new_game(context: CallbackContext, user: User, target_word: str) -> None:
    hardmode = context.user_data.get('hardmode', False)
    globals.logger.info(f"{user.first_name} started a new game, word: {target_word}, hardmode: {hardmode}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} started a new game, word: *_{target_word}_*\n" \
                f"language: *{context.user_data.get('language')}*\n" \
                f"hardmode: *{hardmode}*, board size: *{context.user_data.get('board_size')}*",
            parse_mode='MarkdownV2',
            disable_notification=False
            )

def log_user_guess(context: CallbackContext, user: User, word: str, board: str) -> None:
    globals.logger.info(f"{user.first_name} guessed {word}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} guessed: _{word}_\n{board}",
            parse_mode='MarkdownV2',
            disable_notification=True
        )

def log_user_invalid_guess(context: CallbackContext, user: User, word: str) -> None:
    globals.logger.info(f"{user.first_name} wrote {word}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} wrote: _{word}_",
            parse_mode='MarkdownV2',
            disable_notification=True
        )

def log_user_won(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} won the game")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} won the game",
            parse_mode='MarkdownV2',
            disable_notification=True
        )

def log_user_lost(context: CallbackContext, user: User, target_word: str) -> None:
    globals.logger.info(f"{user.first_name} lost the game, word: {target_word}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} lost the game, word: *_{target_word}_*",
            parse_mode='MarkdownV2',
            disable_notification=True
        )

def log_user_give_up(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} gave up")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} gave up",
            parse_mode='MarkdownV2',
            disable_notification=True
            )

def log_user_command_start(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} executed /start")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} executed /start",
            parse_mode='MarkdownV2',
            disable_notification=True
        )

def log_user_command_help(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} executed /help")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} executed /help",
            parse_mode='MarkdownV2',
            disable_notification=True
        )

def log_user_toggle_hardmode(context: CallbackContext, user: User) -> None:
    hardmode = context.user_data.get('hardmode', False)
    globals.logger.info(f"{user.first_name} toggled hardmode: {hardmode}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} toggled hardmode: *{hardmode}*",
            parse_mode='MarkdownV2',
            disable_notification=True
        )

def log_board_size_set(context: CallbackContext, user: User, board_size: str) -> None:
    globals.logger.info(f"{user.first_name} set board size to: {board_size}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} set board size to: *{board_size}*",
            parse_mode='MarkdownV2',
            disable_notification=True
        )

def log_feedback(context: CallbackContext, user: User, feedback: str) -> None:
    globals.logger.info(f"{user.first_name} submitted feedback: {feedback}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.first_name} submitted feedback:\n{feedback}",
            disable_notification=False
        )

def log_hint(context: CallbackContext, user: User, hint: str) -> None:
    globals.logger.info(f"{user.first_name} used hint: {hint}")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.first_name} used hint:\n{hint}",
            disable_notification=True
        )

def log_user_monti(context: CallbackContext, user: User) -> None:
    globals.logger.info(f"{user.first_name} typed MONTI")
    if globals.LOG_CHANNEL:
        context.bot.send_message(
            chat_id=globals.LOG_CHANNEL,
            text=f"{user.mention_markdown_v2()} called *MONTI*",
            parse_mode='MarkdownV2',
            disable_notification=False
            )