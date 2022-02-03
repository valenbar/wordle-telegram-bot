from PIL import Image
import json

from telegram.ext import CallbackContext
from telegram import Update

import globals
from markups import *

def monti_on(update: Update, context: CallbackContext) -> (None):
    try:
        with open("./res/montimontimonti.webp", "rb") as f:
            monti = f.read()
        update.message.reply_sticker(sticker=monti)
        context.user_data["flip"] = True
        context.user_data["flips"] = 0
        context.bot.send_message(globals.LOG_CHANNEL, f"{update.message.from_user.mention_markdown_v2()} called *MONTI*", parse_mode='MarkdownV2')
        return
    except Exception as e:
        print(e)
        pass

def monti_off(context: CallbackContext) -> (None):
    context.user_data["flip"] = False

def flip_image(context: CallbackContext, img: Image) -> (Image):
    try:
        if context.user_data.get('flip', False):
            rotate = context.user_data.get('flips', 0) % 5
            context.user_data['flips'] = rotate + 1
            return img.transpose(rotate)
        else:
            return img
    except Exception as e:
        print(e)
        pass

def log_new_user(update: Update, context: CallbackContext):
    with open("users.txt", "a") as f:
        f.write(f"{update.message.from_user.first_name} {update.message.from_user.id}\n")
    new_user = {
                    "name": update.message.from_user.first_name,
                    "id": update.message.from_user.id
                }
    try:
        with open("unique_users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []
    if new_user not in users:
        users.append(new_user)
        globals.logger.info(f"new user connected: {new_user['name']} {new_user['id']}")
        context.bot.send_message(globals.LOG_CHANNEL, f"new user: {update.message.from_user.mention_markdown_v2()} \nID: `{update.message.from_user.id}`\nTotal uniqe users: `{len(users)}`", parse_mode='MarkdownV2')
        with open("unique_users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

def image_location(context: CallbackContext):
    return "./out" + str(context.user_data.get('user_id', '0000')) + ".png"

def show_main_menu(update: Update, context: CallbackContext):
    menu_msg = context.user_data.get("menu_msg")
    if menu_msg is None:
        menu_msg = update.message.reply_text("Choose an option:", reply_markup=main_menu_markup)
    else:
        menu_msg = menu_msg.edit_text("Choose an option:", reply_markup=main_menu_markup)
    context.user_data["menu_msg"] = menu_msg

def show_language_menu(update: Update, context: CallbackContext):
    menu_msg = context.user_data.get('menu_msg')
    if menu_msg is None:
        try:
            menu_msg = update.message.reply_text("Choose your language:", reply_markup=language_menu_markup)
        except:
            menu_msg = update.callback_query.message.reply_text("Choose your language:", reply_markup=language_menu_markup)
    else:
        try:
            menu_msg = menu_msg.edit_text("Choose your language:", reply_markup=language_menu_markup)
        except:
            globals.logger.info("could not edit menu message, too much time passed")
            menu_msg = update.message.reply_text("Choose your language:", reply_markup=language_menu_markup)
            pass
    context.user_data["menu_msg"] = menu_msg