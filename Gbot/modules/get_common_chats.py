"""
Copyright ( C ) GopiNath  
"""

import os

from time import sleep
from Gbot import QUEEN_PTB
from Gbot.modules.helper_funcs.chat_status import dev_plus
from Gbot.modules.helper_funcs.extraction import extract_user
from Gbot.modules.sql.users_sql import get_user_com_chats

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import BadRequest, RetryAfter, Forbidden
from telegram.ext import CallbackContext, CommandHandler


@dev_plus
async def get_user_common_chats(update: Update,
                                context: CallbackContext) -> None:
    bot, args = context.bot, context.args
    msg = update.effective_message
    user = extract_user(msg, args)
    if not user:
        await msg.reply_text("I share no common chats with the void.")
        return
    common_list = get_user_com_chats(user)
    if not common_list:
        await msg.reply_text("No common chats with this user!")
        return
    name = await bot.get_chat(user).first_name
    text = f"<b>Common chats with {name}</b>\n"
    for chat in common_list:
        try:
            chat_name = await bot.get_chat(chat).title
            sleep(0.3)
            text += f"➛ <code>{chat_name}</code>\n"
        except (BadRequest, Forbidden):
            pass
        except RetryAfter as e:
            sleep(e.retry_after)

    if len(text) < 4096:
        await msg.reply_text(text, parse_mode=ParseMode.HTML)
    else:
        with open("common_chats.txt", "w") as f:
            f.write(text)
        with open("common_chats.txt", "rb") as f:
            msg.reply_document(f)
        os.remove("common_chats.txt")


QUEEN_PTB.add_handler(CommandHandler("getchats", get_user_common_chats, block=False))
