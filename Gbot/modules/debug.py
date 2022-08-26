"""
Copyright ( C ) GopiNath  
"""

import os
import datetime

from telethon import events
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from Gbot import telethn, QUEEN_PTB, LOGGER
from Gbot.modules.helper_funcs.chat_status import dev_plus

DEBUG_MODE = False


@dev_plus
async def debug(update: Update):
    global DEBUG_MODE
    message = update.effective_message
    args = message.text.split(" " or None, 1)
    LOGGER.debug(DEBUG_MODE)
    if len(args) > 1:
        if args[1] in ("yes", "on"):
            DEBUG_MODE = True
            await update.effective_message.reply_text("Debug mode is now on.")
        elif args[1] in ("no", "off"):
            DEBUG_MODE = False
            await update.effective_message.reply_text("Debug mode is now off.")
    elif DEBUG_MODE:
        await update.effective_message.reply_text("Debug mode is currently on."
                                                  )
    else:
        await update.effective_message.reply_text(
            "Debug mode is currently off.")


@telethn.on(events.NewMessage(pattern="[/!].*"))
async def i_do_nothing_yes(event):
    if DEBUG_MODE:
        LOGGER.debug(f"-{event.sender_id} ({event.chat_id}) : {event.text}")
        if os.path.exists("updates.txt"):
            with open("updates.txt", "r") as f:
                text = f.read()
            with open("updates.txt", "w+") as f:
                f.write(
                    f"{text}\n-{event.sender_id} ({event.chat_id}) : {event.text}"
                )
        else:
            with open("updates.txt", "w+") as f:
                f.write(
                    f"- {event.sender_id} ({event.chat_id}) : {event.text} | {datetime.datetime.now()}",
                )


support_chat = os.getenv("SUPPORT_CHAT")


@dev_plus
def logs(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    with open("log.txt", "rb") as f:
        context.bot.send_document(document=f, filename=f.name, chat_id=user.id)


QUEEN_PTB.add_handler(CommandHandler("logs", logs, block=False))
QUEEN_PTB.add_handler(CommandHandler("debug", debug, block=False))

__mod_name__ = "[✨ ᴅᴇʙᴜɢ ✨]"

__command_list__ = ["debug"]
