"""
Copyright ( C ) GopiNath  
"""

from requests import get
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import BadRequest
from Gbot import QUEEN_PTB
from Gbot.modules.disable import DisableAbleCommandHandler


async def ud(update: Update, context: CallbackContext) -> None:
    msg = update.effective_message
    args = context.args
    text = " ".join(args).lower()
    if not text:
        await msg.reply_text("Please enter keywords to search on ud!")
        return
    if text == "Queen":
        await msg.reply_text(
            "Queen is my owner so if you search him on urban dictionary you can't find the meaning because he is my husband and only me who know what's the meaning of!"
        )
        return
    try:
        results = get(
            f"http://api.urbandictionary.com/v0/define?term={text}").json()
        reply_text = f'Word: {text}\n\nDefinition: \n{results["list"][0]["definition"]}'
        reply_text += f'\n\nExample: \n{results["list"][0]["example"]}'
    except IndexError:
        reply_text = (
            f"Word: {text}\n\nResults: Sorry could not find any matching results!"
        )
    ignore_chars = "[]"
    reply = reply_text
    for chars in ignore_chars:
        reply = reply.replace(chars, "")
    if len(reply) >= 4096:
        reply = reply[:4096]  # max msg lenth of tg.
    try:
        await msg.reply_text(reply)
    except BadRequest as err:
        await msg.reply_text(f"Error! {err.message}")


QUEEN_PTB.add_handler(DisableAbleCommandHandler(["ud"], ud, block=False))

__command_list__ = ["ud"]
