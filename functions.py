import json

from PIL import Image
from telegram.ext import CallbackContext
from telegram import Update

import globals
from markups import *
from loggingFunctions import *

def monti_on(update: Update, context: CallbackContext) -> (None):
    try:
        with open("./assets/montimontimonti.webp", "rb") as f:
            monti = f.read()
        update.message.reply_sticker(sticker=monti)
        context.user_data["flip"] = True
        context.user_data["flips"] = 0
        log_user_monti(context, update.message.from_user)
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

def handle_new_user(update: Update, context: CallbackContext):
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
        log_new_user(update, context, new_user["name"], new_user["id"], len(users))
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
        except Exception as e:
            print(e)
            menu_msg = update.callback_query.message.reply_text("Choose your language:", reply_markup=language_menu_markup)
    else:
        try:
            menu_msg = menu_msg.edit_text("Choose your language:", reply_markup=language_menu_markup)
        except Exception as e:
            print(e)
            menu_msg = update.message.reply_text("Choose your language:", reply_markup=language_menu_markup)
            pass
    context.user_data["menu_msg"] = menu_msg