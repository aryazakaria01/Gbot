"""
Copyright ( C ) GopiNath  
"""

import traceback
import html
import random

from Gbot.modules.helper_funcs.misc import upload_text
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler
from psycopg2 import errors as sqlerrors

from Gbot import TOKEN, QUEEN_PTB, DEV_USERS, OWNER_ID, LOGGER


class ErrorsDict(dict):
    "A custom dict to store errors and their count"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __contains__(self, error):
        error.identifier = "".join(
            random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5))
        for e in self:
            if type(e) is type(error) and e.args == error.args:
                self[e] += 1
                return True
        self[error] = 0
        return False


errors = ErrorsDict()


async def error_callback(update: Update, context: CallbackContext) -> None:
    if not update:
        return

    e = html.escape(f"{context.error}")
    if e.find(TOKEN) != -1:
        e = e.replace(TOKEN, "TOKEN")

    if update.effective_chat.type != "channel":
        try:
            await context.bot.send_message(
                update.effective_chat.id,
                f"<b>Sorry I ran into an error!</b>\n<b>Error</b>: <code>{e}</code>\n<i>This incident has been logged. No further action is required.</i>",
                parse_mode=ParseMode.HTML)
        except BaseException as e:
            LOGGER.exception(e)

    if context.error in errors:
        return
    tb_list = traceback.format_exception(None, context.error,
                                         context.error.__traceback__)
    tb = "".join(tb_list)
    pretty_message = (
        "An exception was raised while handling an update\n"
        "User: {}\n"
        "Chat: {} {}\n"
        "Callback data: {}\n"
        "Message: {}\n\n"
        "Full Traceback: {}").format(
            update.effective_user.id,
            update.effective_chat.title if update.effective_chat else "",
            update.effective_chat.id if update.effective_chat else "",
            update.callback_query.data if update.callback_query else "None",
            update.effective_message.text
            if update.effective_message else "No message",
            tb,
        )
    paste_url = upload_text(pretty_message)

    if not paste_url:
        with open("Queen_error.txt", "w+") as f:
            f.write(pretty_message)
        await context.bot.send_document(
            OWNER_ID,
            open("Queen_error.txt", "rb"),
            caption=
            f"#{context.error.identifier}\n<b>Your sugar mommy got an error for you, you cute guy:</b>\n<code>{e}</code>",
            parse_mode=ParseMode.HTML,
        )
        return
    await context.bot.send_message(
        OWNER_ID,
        text=
        f"#{context.error.identifier}\n<b>Your sugar mommy got an error for you, you cute guy:</b>\n<code>{e}</code>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("PrivateBin", url=paste_url)]]),
        parse_mode=ParseMode.HTML,
    )


"""
async def list_errors(update: Update,
                      context: CallbackContext) -> None:
    if update.effective_user.id not in DEV_USERS:
        return
    e = dict(sorted(errors.items(), key=lambda item: item[1], reverse=True))
    msg = "<b>Errors List:</b>\n"
    for x, value in e.items():
        msg += f"➛ <code>{x}:</code> <b>{e[x]}</b> #{x.identifier}\n"

    msg += f"{len(errors)} have occurred since startup."
    if len(msg) > 4096:
        with open("Queen_errors_msg.txt", "w+") as f:
            f.write(msg)
        await context.bot.send_document(
            update.effective_chat.id,
            open("Queen_errors_msg.txt", "rb"),
            caption='Too many errors have occured..',
            parse_mode=ParseMode.HTML,
        )

        return
    await update.effective_message.reply_text(msg, parse_mode=ParseMode.HTML)
"""

QUEEN_PTB.add_error_handler(error_callback)

# QUEEN_PTB.add_handler(CommandHandler("errors", list_errors, block=False))
