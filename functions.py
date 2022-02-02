from PIL import Image
import time

from telegram.ext import CallbackContext
from telegram import Update

import globals

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