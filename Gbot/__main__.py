"""
Copyright ( C ) GopiNath  
"""

import contextlib
import html
import json
import importlib
import time
import re
import traceback
import Gbot.modules.sql.users_sql as sql

from sys import argv
from typing import Optional

from Gbot import (
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    TOKEN,
    WEBHOOK,
    SUPPORT_CHAT,
    HELP_IMG,
    GROUP_START_IMG,
    QUEEN_PTB,
    BOT_USERNAME,
    StartTime,
    pgram,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from Gbot.modules import ALL_MODULES
from Gbot.modules.helper_funcs.chat_status import is_user_admin
from Gbot.modules.helper_funcs.misc import paginate_modules
from Gbot.modules.disable import DisableAbleCommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Forbidden,
)
from telegram.ext import (CallbackContext, CallbackContext, filters,
                          CallbackQueryHandler, MessageHandler)

from telegram.helpers import escape_markdown
from pyrogram import idle


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list.pop()}, "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


HELP_MSG = "ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴍᴀɴᴜ ɪɴ ʏᴏᴜʀ ᴘᴍ ✨."
START_MSG = "ɪ'ᴍ ᴀᴡᴀᴋᴇ ᴀʟʀᴇᴀᴅʏ ☺ !\n<b>ʜᴀᴠᴇɴ'ᴛ ꜱʟᴇᴘᴛ ꜱɪɴᴄᴇ🤩:</b> <code>{}</code>"

PM_START_TEXT = """
────「 [{}](https://te.legra.ph/file/d5e4e6a1b6414b0d4444d.mp4) 」────

*ʜᴇʏ ʜɪ ! {},*
───────────────────────
× *I'ᴍ 🇴¤๋͜ғͥғɪᴄͣɪͫ͢ꫝʟ✮͢♔⃟≛⃝🇶 ᴜᴇᴇɴ⋆⏤͟͟❥͢𐏓➳⍣⃟♔ 👸 Gʀᴏᴜᴘ Mᴀɴᴀɢᴇᴍᴇɴᴛ ᴀɴᴅ Vᴄ ᴘʟᴀʏᴇʀ*
× *I'ᴍ Vᴇʀʏ Fᴀꜱᴛ Aɴᴅ Mᴏʀᴇ Eꜰꜰɪᴄɪᴇɴᴛ I Pʀᴏᴠɪᴅᴇ Aᴡᴇꜱᴏᴍᴇ Fᴇᴀᴛᴜʀᴇꜱ!💕* 
────────────────────────
× Hɪᴛ /help  ᴛᴏ ꜱᴇᴇ Mᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ.
× Hɪᴛ /mhelp ᴛᴏ ꜱᴇᴇ Mᴜꜱɪᴄ ᴘʟᴀʏᴇʀ ᴄᴏᴍᴍᴀɴᴅꜱ.
────────────────────────
✪ 3 ɪɴ 1 Bᴏᴛ | Mᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ | ᴍᴜꜱɪᴄ ʙᴏᴛ | ᴜꜱᴇʀ ʙᴏᴛ | ..
✪ ᴄʜᴇᴄᴋ ᴏᴜᴛ ᴀʟʟ ᴛʜᴇ ʙᴏᴛ's ᴄᴏᴍᴍᴀɴᴅs  ᴀɴᴅ ʜᴏᴡ ᴛʜᴇʏ ᴡᴏʀᴋ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ »  ᴄᴏᴍᴍᴀɴᴅs  ʙᴜᴛᴛᴏɴ!.
✪ ᴛʜɪs ɪs ᴀ ʙᴏᴛ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴀɴᴅ ᴠɪᴅᴇᴏ ɪɴ ɢʀᴏᴜᴘs, ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ɴᴇᴡ ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs.
✪ ɪ'ᴍ ᴀ ᴛᴇʟᴇɢʀᴀᴍ strᴇᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴜꜱᴇꜰᴜʟ ꜰᴇᴀᴛᴜʀᴇꜱ. ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ ʟɪᴋᴇ ʏᴏᴜᴛᴜʙᴇ, ꜱᴘᴏᴛɪꜰʏ, ʀᴇꜱꜱᴏ, ᴀᴘᴘʟᴇᴍᴜꜱɪᴄ , ꜱᴏᴜɴᴅᴄʟᴏᴜᴅ ᴇᴛᴄ.
✪ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴀᴅᴅ ᴍᴇ .
───────────────────────
❍ *ᴍʏ ᴜᴘ-ᴛɪᴍᴇ ɪꜱ:* `{}`
❍ `{}` *ᴍᴇᴍʙᴇʀꜱ ᴀʀᴇ ᴜꜱɪɴɢ ᴍᴇ ɪɴ ᴘᴍ , ᴀᴄʀᴏꜱꜱ * `{}` *ᴄʜᴀᴛꜱ*
───────────────────────
× *Pᴏᴡᴇʀᴇᴅ Bʏ: ƬЄ𝗔Μ ƲƉ𝗔ИƤƖЯ𝗔ƤƤƲ 💕!*
───────────────────────
"""

buttons = [
    [
        InlineKeyboardButton(
            text="[✨ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ✨]",
            url=f"https://telegram.dog/udanpirappumusic_bot?startgroup=true")
    ],
    [
        InlineKeyboardButton(text="[✨ ʜᴇʟᴘ ✨]", callback_data="help_back"),
        InlineKeyboardButton(text="[✨ ᴍᴜꜱɪᴄ ✨]", callback_data="help_back"),
        InlineKeyboardButton(text="[✨ ɪɴʟɪɴᴇ ✨]",
                             switch_inline_query_current_chat=""),
    ],
    [
        InlineKeyboardButton(text="[✨ ᴍʏ ɢᴏᴅ ✨]",
                             url="https://telegram.dog/ROWDY_OF_PLUS"),
        InlineKeyboardButton(
            text="[✨  ꜰᴇᴅ   ✨]",
            url="https://telegram.dog/udanpiruppugangsfederal"),
        InlineKeyboardButton(text="[✨ ᴊᴏɪɴ ✨]",
                             url="https://telegram.dog/Team_udanpirappu"),
    ],
    [
        InlineKeyboardButton(text="[✨  ꜱᴜᴘᴘᴏʀᴛ ᴜꜱ  ✨]",
                             url=f"https://telegram.dog/{SUPPORT_CHAT}"),
        InlineKeyboardButton(
            text="[✨  ᴜᴘᴅᴀᴛᴇ ɪɴ  ✨]",
            url="https://telegram.dog/udanpiruppugangsfederal")
    ],
    [
        InlineKeyboardButton(text="[✨  ƬЄ𝗔Μ ƲƉ𝗔ИƤƖЯ𝗔ƤƤƲ  ✨]",
                             url=f"https://telegram.dog/Team_udanpirappu")
    ],
]

HELP_STRINGS = """
*ɪ ʜᴀᴠᴇ ᴍᴏʀᴇ ᴍᴏᴅᴜʟᴇꜱ ꜰᴏʀ ʏᴏᴜʀ ᴜꜱᴇ ʏᴏᴜ ᴄᴀɴ ᴀᴄᴄᴇꜱꜱ ᴡɪᴛʜ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ*: \n
➛ /help: ɪɴ ᴛʜɪꜱ ʏᴏᴜ ᴄᴀɴ ꜱᴇᴇ ᴍᴇ ᴀʟʟ ᴛʜᴇ ᴘᴏꜱꜱɪʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ 🥰.\n
➛ /help <module name>: ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴀɴʏ ꜱᴘᴇᴄɪꜰɪᴄ ᴍᴏᴅᴜʟᴇ ʜᴇʟᴘ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ 💖.\n
➛ /donate: ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ɪɴᴛᴇʀᴇꜱᴛ ʏᴏᴜ ᴄᴀɴ ᴅᴏɴᴀᴛᴇ ᴍᴇ ɪɴ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ 😘 \n
➛ /settings: \n
   ➛ ɪɴ ᴘᴍ: ᴡɪʟʟ ꜱᴇɴᴅ ʏᴏᴜ ʏᴏᴜʀ ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ ᴀʟʟ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇꜱ.\n
   ➛ ɪɴ ᴀ ɢʀᴏᴜᴘ: ᴡɪʟʟ ʀᴇᴅɪʀᴇᴄᴛ ʏᴏᴜ ᴛᴏ ᴘᴍ, ᴡɪᴛʜ ᴀʟʟ ᴛʜᴀᴛ ᴄʜᴀᴛ'ꜱ ꜱᴇᴛᴛɪɴɢꜱ.\n
➛ ɪꜰ ʏᴏᴜ  ꜰᴀᴄᴇ ᴀɴʏ ɪꜱꜱᴜᴇꜱ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ --> [ɢᴏᴘɪ](https://telegram.dog/ROWDY_OF_PLUS)  
"""

DONATE_STRING = """❂ ɪ'ᴍ ꜰʀᴇᴇ ꜰᴏʀ ᴇᴠᴇʀʏ , ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴍᴇ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴄʜᴀʀɢᴇ . ʙᴜᴛ ᴍʏ [ᴏᴡɴᴇʀ](https://telegram.dog/ROWDY_OF_PLUS) ʜᴀꜱ ᴘᴀɪᴅ ꜰᴏʀ ᴍᴇ ʏᴏᴜ ᴄᴀɴ ᴘᴀʏ ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ɪɴᴛᴇʀᴇꜱᴛ ❂"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}
GDPR = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module(f"Gbot.modules.{module_name}")

    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception(
            "ᴄᴀɴ'ᴛ ʜᴀᴠᴇ ᴛᴡᴏ ᴍᴏᴅᴜʟᴇꜱ ᴡɪᴛʜ ᴛʜᴇ ꜱᴀᴍᴇ ɴᴀᴍᴇ! ᴘʟᴇᴀꜱᴇ ᴄʜᴀɴɢᴇ ᴏɴᴇ 📞")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
async def send_help(context: CallbackContext, chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


async def test(update: Update):
    # pLOGGER.debug(eval(str(update)))
    # await update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    await update.effective_message.reply_text("ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ᴇᴅɪᴛᴇᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ")
    LOGGER.debug(update.effective_message)


async def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup([[
                        InlineKeyboardButton(text="[✨ ʙᴀᴄᴋ  ✨]",
                                             callback_data="help_back")
                    ]]),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = await QUEEN_PTB.bot.getChat(match[1])

                if await is_user_admin(update, update.effective_user.id):
                    send_settings(match[1], update.effective_user.id, False)
                else:
                    send_settings(match[1], update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            await update.effective_message.reply_text(
                PM_START_TEXT.format(escape_markdown(context.bot.first_name),
                                     escape_markdown(first_name),
                                     escape_markdown(uptime), sql.num_users(),
                                     sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_animation(
            GROUP_START_IMG,
            caption=
            f"ɪ'ᴍ ᴀᴡᴀᴋᴇ ᴀʟʀᴇᴀᴅʏ ☺ !\n<b>ʜᴀᴠᴇɴ'ᴛ ꜱʟᴇᴘᴛ ꜱɪɴᴄᴇ🤩:</b> <code>{uptime}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text="[✨  ꜱᴜᴘᴘᴏʀᴛ ᴜꜱ  ✨]",
                    url=f"https://telegram.dog/{SUPPORT_CHAT}"),
                InlineKeyboardButton(
                    text="[✨  ᴜᴘᴅᴀᴛᴇ ɪɴ  ✨]",
                    url="https://telegram.dog/udanpiruppugangsfederal")
            ]]),
        )


async def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:",
                 exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error,
                                         context.error.__traceback__)
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = f"An exception was raised while handling an update\n<pre>update = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}</pre>\n\n<pre>{html.escape(tb)}</pre>"

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    await context.bot.send_message(chat_id=OWNER_ID,
                                   text=message,
                                   parse_mode=ParseMode.HTML)


# for test purposes
async def error_callback(_, context: CallbackContext):
    try:
        raise context.error
    except (BadRequest):
        pass
        # remove update.message.chat_id from conversation list
    except TimedOut:
        pass
        # handle slow connection problems
    except NetworkError:
        pass
        # handle other connection problems
    except ChatMigrated:
        pass
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass
        # handle all other telegram related errors


async def help_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    with contextlib.suppress(BadRequest):
        if mod_match:
            module = mod_match[1]
            text = (f"╔═━「 *{HELPABLE[module].__mod_name__}* module: 」\n" +
                    HELPABLE[module].__help__)

            await query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(text="[✨ ʙᴀᴄᴋ  ✨]",
                                         callback_data="help_back"),
                    InlineKeyboardButton(
                        text="[✨  ꜱᴜᴘᴘᴏʀᴛ ᴜꜱ  ✨]",
                        url=f"https://telegram.dog/{SUPPORT_CHAT}"),
                ]]),
            )

        elif prev_match:
            curr_page = int(prev_match[1])
            await query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")),
            )

        elif next_match:
            next_page = int(next_match[1])
            await query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")),
            )

        elif back_match:
            await query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")),
            )

        # ensure no spinny white circle
        await context.bot.answer_callback_query(query.id)
        # await query.message.delete()


async def cutiepii_callback_data(update: Update,
                                 context: CallbackContext) -> None:
    query = update.callback_query
    uptime = get_readable_time((time.time() - StartTime))
    if query.data == "cutiepii_":
        await query.message.edit_text(
            text="""CallBackQueriesData Here""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="[✨ ʙᴀᴄᴋ  ✨]",
                                     callback_data="cutiepii_back")
            ]]),
        )
    elif query.data == "cutiepii_back":
        first_name = update.effective_user.first_name
        await query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(context.bot.first_name),
                                 escape_markdown(first_name),
                                 escape_markdown(uptime), sql.num_users(),
                                 sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


async def get_help(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:

        update.effective_message.reply_photo(
            HELP_IMG,
            HELP_MSG,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text="ᴏᴘᴇɴ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ 🥰",
                    url=f"t.me/{context.bot.username}?start=help",
                )
            ]]),
        )

        return

    if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (f" 〔 *{HELPABLE[module].__mod_name__}* 〕\n" +
                HELPABLE[module].__help__)

        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup([[
                InlineKeyboardButton(text="[► Back ◄]",
                                     callback_data="help_back")
            ]]),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


async def send_settings(context: CallbackContext,
                        chat_id,
                        user_id,
                        user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                f"*{mod.__mod_name__}*:\n{mod.__user_settings__(user_id)}"
                for mod in USER_SETTINGS.values())

            await context.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            await context.bot.send_message(
                user_id,
                "ꜱᴇᴇᴍꜱ ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴜꜱᴇʀ ꜱᴘᴇᴄɪꜰɪᴄ ꜱᴇᴛᴛɪɴɢꜱ ᴀᴠᴀɪʟᴀʙʟᴇ :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    elif CHAT_SETTINGS:
        chat_name = await QUEEN_PTB.bot.getChat(chat_id).title
        await context.bot.send_message(
            user_id,
            text=
            f"ᴡʜɪᴄʜ ᴍᴏᴅᴜʟᴇ ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴄʜᴇᴄᴋ {chat_name}'s ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ?",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)),
        )
    else:
        await context.bot.send_message(
            user_id,
            "ꜱᴇᴇᴍꜱ ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴄʜᴀᴛ ꜱᴇᴛᴛɪɴɢꜱ ᴀᴠᴀɪʟᴀʙʟᴇ :'(\nꜱᴇɴᴅ ᴛʜɪꜱ "
            "ɪɴ ᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ ɪɴ ᴛᴏ ꜰɪɴᴅ ɪᴛꜱ ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ!",
            parse_mode=ParseMode.MARKDOWN,
        )


async def settings_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match[1]
            module = mod_match[2]
            chat = await bot.get_chat(chat_id)
            text = "*{}* ʜᴀꜱ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ ᴛʜᴇ *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            try:
                keyboard = CHAT_SETTINGS[module].__chat_settings_buttons__(
                    chat_id, user.id)
            except AttributeError:
                keyboard = []
            kbrd = InlineKeyboardMarkup(
                InlineKeyboardButton(text="Back",
                                     callback_data=f"stngs_back({chat_id}"))
            keyboard.append(kbrd)
            await query.message.edit_text(text=text,
                                          parse_mode=ParseMode.MARKDOWN,
                                          reply_markup=keyboard)
        elif prev_match:
            chat_id = prev_match[1]
            curr_page = int(prev_match[2])
            chat = await bot.get_chat(chat_id)
            await query.message.reply_text(
                f"ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ Qᴜɪᴛᴇ ᴀ ꜰᴇᴡ ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ {chat.title} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇꜱᴛᴇᴅ ɪɴ.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1,
                                     CHAT_SETTINGS,
                                     "stngs",
                                     chat=chat_id)),
            )

        elif next_match:
            chat_id = next_match[1]
            next_page = int(next_match[2])
            chat = await bot.get_chat(chat_id)
            await query.message.edit_text(
                f"ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ Qᴜɪᴛᴇ ᴀ ꜰᴇᴡ ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ {chat.title} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇꜱᴛᴇᴅ ɪɴ.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1,
                                     CHAT_SETTINGS,
                                     "stngs",
                                     chat=chat_id)),
            )

        elif back_match:
            chat_id = back_match[1]
            chat = await bot.get_chat(chat_id)
            await query.message.edit_text(
                text=
                f"ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ Qᴜɪᴛᴇ ᴀ ꜰᴇᴡ ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ {escape_markdown(chat.title)} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇꜱᴛᴇᴅ ɪɴ.",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)),
            )

        # ensure no spinny white circle
        await bot.answer_callback_query(query.id)
    except BadRequest as excp:
        if excp.message not in [
                "Message is not modified",
                "Query_id_invalid",
                "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s",
                             str(query.data))


async def get_settings(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type == chat.PRIVATE:
        send_settings(chat.id, user.id, True)

    elif await is_user_admin(update, user.id):
        text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ᴛʜɪꜱ ᴄʜᴀᴛ'ꜱ ꜱᴇᴛᴛɪɴɢꜱ, ᴀꜱ ᴡᴇʟʟ ᴀꜱ ʏᴏᴜʀꜱ."
        await msg.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text="ꜱᴇᴛᴛɪɴɢꜱ",
                    url=
                    f"https://telegram.dog/{context.bot.username}?start=stngs_{chat.id}",
                )
            ]]),
        )

    else:
        text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ꜱᴇᴛᴛɪɴɢꜱ. "


async def donate(update: Update, context: CallbackContext) -> None:
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        await update.effective_message.reply_text(
            DONATE_STRING,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)

        if OWNER_ID != 2131857711 and DONATION_LINK:
            await update.effective_message.reply_text(
                f"ʏᴏᴜ ᴄᴀɴ ᴀʟꜱᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴘᴇʀꜱᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ [ʜᴇʀᴇ]({DONATION_LINK})",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        try:
            await bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            await update.effective_message.reply_text(
                text=
                "ɪ'ᴍ ꜰʀᴇᴇ ꜰᴏʀ ᴇᴠᴇʀʏᴏɴᴇ❤️\nᴊᴜꜱᴛ ᴅᴏɴᴀᴛᴇ ʙʏ ꜱᴜʙꜱ ᴄʜᴀɴɴᴇʟ, ᴅᴏɴ'ᴛ ꜰᴏʀɢᴇᴛ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        text="[✨  ꜱᴜᴘᴘᴏʀᴛ ᴜꜱ  ✨]",
                        url=f"https://telegram.dog/{SUPPORT_CHAT}"),
                    InlineKeyboardButton(
                        text="[✨  ᴜᴘᴅᴀᴛᴇ ɪɴ  ✨]",
                        url="https://telegram.dog/udanpiruppugangsfederal")
                ]]),
            )
        except Forbidden:
            await update.effective_message.reply_text(
                "Contact me in PM first to get donation information.")


async def migrate_chats(update: Update):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", old_chat, new_chat)
    for mod in MIGRATEABLE:
        with contextlib.suppress(KeyError, AttributeError):
            mod.__migrate__(old_chat, new_chat)
    LOGGER.info("Successfully migrated!")


def main():
    QUEEN_PTB.add_error_handler(error_callback)
    QUEEN_PTB.add_handler(DisableAbleCommandHandler("test", test, block=False))
    QUEEN_PTB.add_handler(
        DisableAbleCommandHandler("start", start, block=False))

    QUEEN_PTB.add_handler(
        DisableAbleCommandHandler("help", get_help, block=False))
    QUEEN_PTB.add_handler(
        CallbackQueryHandler(help_button, pattern=r"help_.*", block=False))

    QUEEN_PTB.add_handler(
        DisableAbleCommandHandler("settings", get_settings, block=False))
    QUEEN_PTB.add_handler(
        CallbackQueryHandler(settings_button, pattern=r"stngs_", block=False))

    QUEEN_PTB.add_handler(
        CallbackQueryHandler(cutiepii_callback_data,
                             pattern=r"cutiepii_",
                             block=False))
    QUEEN_PTB.add_handler(DisableAbleCommandHandler("donate", donate))
    QUEEN_PTB.add_handler(
        MessageHandler(filters.StatusUpdate.MIGRATE,
                       migrate_chats,
                       block=False))

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        QUEEN_PTB.run_webhook(listen="127.0.0.1", port=PORT, url_path=TOKEN)

    else:
        QUEEN_PTB.run_polling(allowed_updates=Update.ALL_TYPES,
                              stop_signals=None)
        LOGGER.info(
            "Qᴜᴇᴇɴ ʙᴏᴛ started, ᴜꜱɪɴɢ ʟᴏɴɢ ᴘᴏʟʟɪɴɢ. | ʙᴏᴛ: [@ROWDY_OF_PLUS]")


"""
try:
    ubot.start()
except BaseException:
    LOGGER.debug("Userbot Error! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)
"""

if __name__ == "__main__":
    LOGGER.info(f"Successfully loaded modules: {str(ALL_MODULES)}")
    pgram.start()
    main()
    idle()
