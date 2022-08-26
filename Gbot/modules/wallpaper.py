"""
Copyright ( C ) GopiNath  
"""

import requests as r

from random import randint
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from Gbot import SUPPORT_CHAT, WALL_API, QUEEN_PTB
from Gbot.modules.disable import DisableAbleCommandHandler
from Gbot.modules.helper_funcs.alternate import send_action

# Wallpaper module powered by wall.alphacoders.com


@send_action(ChatAction.UPLOAD_PHOTO)
async def wall(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    msg = update.effective_message
    args = context.args
    msg_id = update.effective_message.message_id
    bot = context.bot
    query = " ".join(args)
    if not query:
        await msg.reply_text("Please enter a query!")
        return
    term = await query.replace(" ", "%20")
    json_rep = r.get(
        f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}"
    ).json()
    if not json_rep.get("success"):
        await msg.reply_text(f"An error occurred! Report this @{SUPPORT_CHAT}")
    else:
        wallpapers = json_rep.get("wallpapers")
        if not wallpapers:
            await msg.reply_text("No results found! Refine your search.")
            return
        index = randint(0, len(wallpapers) - 1)  # Choose random index
        wallpaper = wallpapers[index]
        wallpaper = wallpaper.get("url_image")
        wallpaper = wallpaper.replace("\\", "")
        await bot.send_photo(
            chat_id,
            photo=wallpaper,
            caption="Preview",
            reply_to_message_id=msg_id,
            timeout=60,
        )
        caption = query
        await bot.send_document(
            chat_id,
            document=wallpaper,
            filename="wallpaper",
            caption=caption,
            reply_to_message_id=msg_id,
            timeout=60,
        )

QUEEN_PTB.add_handler(DisableAbleCommandHandler("wall", wall, block=False))