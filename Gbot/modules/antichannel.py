"""
Copyright ( C ) GopiNath  
"""
import html
from telegram import Update
from telegram.ext import filters, CallbackContext

from Gbot import QUEEN_PTB
from Gbot.modules.disable import DisableAbleCommandHandler
from Gbot.modules.helper_funcs.anonymous import user_admin
from Gbot.modules.sql.antichannel_sql import antichannel_status, disable_antichannel, enable_antichannel


@user_admin
async def set_antichannel(update: Update,
                          context: CallbackContext) -> None:
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            await message.reply_html(
                f"Enabled antichannel in {html.escape(chat.title)}")
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            await message.reply_html(
                f"Disabled antichannel in {html.escape(chat.title)}")
        else:
            await update.effective_message.reply_text(
                f"Unrecognized arguments {s}")
        return
    await message.reply_html(
        f"Antichannel setting is currently {antichannel_status(chat.id)} in {html.escape(chat.title)}"
    )


async def eliminate_channel(update: Update,
                            context: CallbackContext) -> None:
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    if message.sender_chat and message.sender_chat.type == "channel" and not message.is_automatic_forward:
        await message.delete()
        sender_chat = message.sender_chat
        await bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id,
                                       chat_id=chat.id)


QUEEN_PTB.add_handler(
    DisableAbleCommandHandler("antichannel",
                              set_antichannel,
                              filters=filters.ChatType.GROUPS, block=False))
