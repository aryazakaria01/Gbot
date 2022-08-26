"""
Copyright ( C ) GopiNath  
"""
from enum import Enum
import functools

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram.constants import ParseMode

from Gbot import DEV_USERS, SUDO_USERS, QUEEN_PTB


class AdminPerms(Enum):
    CAN_RESTRICT_MEMBERS = "can_restrict_members"
    CAN_PROMOTE_MEMBERS = "can_promote_members"
    CAN_INVITE_USERS = "can_invite_users"
    CAN_DELETE_MESSAGES = "can_delete_messages"
    CAN_CHANGE_INFO = "can_change_info"
    CAN_PIN_MESSAGES = "can_pin_messages"


class ChatStatus(Enum):
    OWNER = "creator"
    ADMINISTRATOR = "administrator"


anon_callbacks = {}
anon_callback_messages = {}


def user_admin(permission: AdminPerms):
    def wrapper(func):
        @functools.wraps(func)
        async def awrapper(update: Update, context: CallbackContext, *args, **kwargs):
            nonlocal permission
            if update.effective_chat.type == "private":
                return func(update, context, *args, **kwargs)
            message = update.effective_message
            if is_anon := update.effective_message.sender_chat:
                callback_id = (
                    f"anoncb/{message.chat.id}/{message.message_id}/{permission.value}"
                )
                anon_callbacks[(message.chat.id, message.message_id)] = (
                    (update, context),
                    func,
                )
                anon_callback_messages[(message.chat.id, message.message_id)] = (
                    await message.reply_text(
                        "Seems like you're anonymous, click the button below to prove your identity",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="Prove identity", callback_data=callback_id
                                    )
                                ]
                            ]
                        ),
                    )
                ).message_id
            else:
                user_id = message.from_user.id
                chat_id = message.chat.id
                mem = await context.bot.get_chat_member(
                    chat_id=chat_id, user_id=user_id
                )
                if (
                    getattr(mem, permission.value) is True
                    or mem.status == "creator"
                    or user_id in SUDO_USERS
                ):
                    return func(update, context, *args, **kwargs)
                else:
                    return await message.reply_text(
                        f"You lack the permission: `{permission.name}`",
                        parse_mode=ParseMode.MARKDOWN,
                    )

        return awrapper

    return wrapper


async def anon_callback_handler1(upd: Update):
    callback = upd.callback_query
    perm = callback.data.split("/")[3]
    chat_id = int(callback.data.split("/")[1])
    message_id = int(callback.data.split("/")[2])
    try:
        mem = upd.effective_chat.get_member(user_id=callback.from_user.id)
    except BaseException as e:
        callback.answer(f"Error: {e}", show_alert=True)
        return
    if mem.status not in [ChatStatus.ADMINISTRATOR.value, ChatStatus.OWNER.value]:
        callback.answer("You're aren't admin.")
        await QUEEN_PTB.bot.delete_message(
            chat_id, anon_callback_messages.pop((chat_id, message_id), None)
        )
        await QUEEN_PTB.bot.send_message(
            chat_id, "You lack the permissions required for this command"
        )
    elif (
        getattr(mem, perm) is True
        or mem.status == "creator"
        or mem.user.id in DEV_USERS
    ):
        if cb := anon_callbacks.pop((chat_id, message_id), None):
            message_id = anon_callback_messages.pop((chat_id, message_id), None)
            if message_id is not None:
                await QUEEN_PTB.bot.delete_message(chat_id, message_id)
            return cb[1](cb[0][0], cb[0][1])
    else:
        callback.answer("This isn't for ya")

QUEEN_PTB.add_handler(CallbackQueryHandler(anon_callback_handler1, pattern=r"anoncb", block=False))