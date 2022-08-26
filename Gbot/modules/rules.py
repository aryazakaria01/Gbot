"""
Copyright ( C ) GopiNath  
"""

import Gbot.modules.sql.rules_sql as sql

from typing import Optional
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import filters, CommandHandler
from telegram.helpers import escape_markdown
from Gbot import QUEEN_PTB
from Gbot.modules.helper_funcs.string_handling import markdown_parser
from Gbot.modules.helper_funcs.admin_status import (
    user_admin_check,
    AdminPerms,
)


def get_rules(update: Update):
    chat_id = update.effective_chat.id
    send_rules(update, chat_id)


# Do not async - not from a handler
async def send_rules(update, chat_id, from_pm=False):
    bot = QUEEN_PTB.bot
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message
    try:
        chat = await bot.get_chat(chat_id)
    except BadRequest as excp:
        if excp.message != "Chat not found" or not from_pm:
            raise

        await bot.send_message(
            user.id,
            "The rules shortcut for this chat hasn't been set properly! Ask admins to "
            "fix this.\nMaybe they forgot the hyphen in ID",
        )
        return
    rules = sql.get_rules(chat_id)
    text = f"The rules for *{escape_markdown(chat.title)}* are:\n\n{rules}"

    if from_pm and rules:
        await bot.send_message(user.id,
                               text,
                               parse_mode=ParseMode.MARKDOWN,
                               disable_web_page_preview=True)
    elif from_pm:
        await bot.send_message(
            user.id,
            "The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!",
        )
    elif rules:
        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton(text="Rules",
                                 url=f"t.me/{bot.username}?start={chat_id}")
        ]])
        txt = "Please click the button below to see the rules."
        if not message.reply_to_message:
            await message.reply_text(txt, reply_markup=btn)

        if message.reply_to_message:
            message.reply_to_message.reply_text(txt, reply_markup=btn)
    else:
        await update.effective_message.reply_text(
            "The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!")


@user_admin_check(AdminPerms.CAN_CHANGE_INFO)
async def set_rules(update: Update):
    chat_id = update.effective_chat.id
    msg = update.effective_message  # type: Optional[Message]

    raw_text = msg.text
    args = raw_text.split(None,
                          1)  # use python's maxsplit to separate cmd and args
    if len(args) == 2:
        txt = args[1]
        offset = len(txt) - len(
            raw_text)  # set correct offset relative to command
        markdown_rules = markdown_parser(txt,
                                         entities=msg.parse_entities(),
                                         offset=offset)

        sql.set_rules(chat_id, markdown_rules)
        await update.effective_message.reply_text(
            "Successfully set rules for this group.")


@user_admin_check(AdminPerms.CAN_CHANGE_INFO)
async def clear_rules(update: Update):
    chat_id = update.effective_chat.id
    chat = update.effective_chat  # type: Optional[Chat]

    sql.set_rules(chat_id, "")
    await update.effective_message.reply_text(
        f"Rules for {chat.title} were successfully cleared!")


def __stats__():
    return f"➛ {sql.num_chats()} chats have rules set."


def __import_data__(chat_id, data):
    # set chat rules
    rules = data.get("info", {}).get("rules", "")
    sql.set_rules(chat_id, rules)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id):
    return f"This chat has had it's rules set: `{bool(sql.get_rules(chat_id))}`"


__mod_name__ = "Rules"

QUEEN_PTB.add_handler(
    CommandHandler("rules",
                   get_rules,
                   filters=filters.ChatType.GROUPS,
                   block=False))
QUEEN_PTB.add_handler(
    CommandHandler("setrules",
                   set_rules,
                   filters=filters.ChatType.GROUPS,
                   block=False))
QUEEN_PTB.add_handler(
    CommandHandler("clearrules",
                   clear_rules,
                   filters=filters.ChatType.GROUPS,
                   block=False))
