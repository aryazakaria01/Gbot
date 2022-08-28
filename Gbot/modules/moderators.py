"""
Copyright ( C ) GopiNath  
"""

import html
import contextlib
import Gbot.modules.sql.moderators_sql as sql

from Gbot import QUEEN_PTB
from Gbot.modules.disable import DisableAbleCommandHandler
from Gbot.modules.helper_funcs.anonymous import user_admin
from Gbot.modules.helper_funcs.extraction import extract_user
from Gbot.modules.log_channel import loggable
from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.helpers import mention_html


@loggable
@user_admin
async def mod(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        await message.reply_text(
            "I don't know who you're talking about, you're going to need to specify a user!"
        )
        return ""
    with contextlib.suppress(BadRequest):
        member = await chat.get_member(user_id)

    if member.status in ("administrator", "creator"):
        await message.reply_text("No need to Modertor an Admin!")
        return ""
    if sql.is_modd(message.chat_id, user_id):
        await message.reply_text(
            f"[{member.user['first_name']}](tg://user?id={member.user['id']}) is already moderator in {chat_title}",
            parse_mode=ParseMode.MARKDOWN,
        )
        return ""
    sql.mod(message.chat_id, user_id)
    await message.reply_text(
        f"[{member.user['first_name']}](tg://user?id={member.user['id']}) has been moderator in {chat_title}",
        parse_mode=ParseMode.MARKDOWN,
    )
    return f"<b>{html.escape(chat.title)}:</b>\n#MODERATOR\n<b>Admin:</b> {mention_html(user.id, user.first_name)}\n<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"


@loggable
@user_admin
async def dismod(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        await message.reply_text(
            "I don't know who you're talking about, you're going to need to specify a user!"
        )
        return ""
    try:
        member = await chat.get_member(user_id)
    except BadRequest:
        return ""
    if member.status in ("administrator", "creator"):
        await update.effective_message.reply_text("This Is User Admin")
        return ""
    if not sql.is_modd(message.chat_id, user_id):
        await message.reply_text(
            f"{member.user['first_name']} isn't moderator yet!")
        return ""
    sql.dismod(message.chat_id, user_id)
    await message.reply_text(
        f"{member.user['first_name']} is no longer moderator in {chat_title}.")
    return f"<b>{html.escape(chat.title)}:</b>\n#UNMODERTOR\n<b>Admin:</b> {mention_html(user.id, user.first_name)}\n<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"


@user_admin
async def modd(update: Update):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    msg = "The following users are Moderator.\n"
    modd_users = sql.list_modd(message.chat_id)
    for i in modd_users:
        member = chat.get_member(int(i.user_id))
        msg += f"{member.user['first_name']}\n"
    if msg.endswith("moderator.\n"):
        await message.reply_text(f"No users are Moderator in {chat_title}.")
        return ""
    await message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


async def modr(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    user_id = extract_user(message, args)
    member = await chat.get_member(user_id)
    if not user_id:
        await message.reply_text(
            "I don't know who you're talking about, you're going to need to specify a user!"
        )
        return ""
    if sql.is_modd(message.chat_id, user_id):
        await message.reply_text(
            f"{member.user['first_name']} is an moderator user.")
    else:
        await message.reply_text(
            f"{member.user['first_name']} is not an moderator user.")


__mod_name__ = "[✨ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ ✨]"

QUEEN_PTB.add_handler(DisableAbleCommandHandler("addmod", mod, block=False))
QUEEN_PTB.add_handler(DisableAbleCommandHandler("rmmod", dismod, block=False))
QUEEN_PTB.add_handler(DisableAbleCommandHandler("modlist", modd, block=False))
QUEEN_PTB.add_handler(DisableAbleCommandHandler("modcheck", modr, block=False))

__command_list__ = [
    "addmod",
    "rmmod",
    "modlist",
    "modcheck",
]
