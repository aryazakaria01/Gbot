"""
Copyright ( C ) GopiNath  
"""

import time
import requests
import datetime
import platform
import git
import Gbot.modules.sql.users_sql as sql

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, __version__ as ptbver
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.helpers import escape_markdown

from Gbot import StartTime, QUEEN_PTB
from Gbot.__main__ import STATS
from Gbot.modules.sql import SESSION
from Gbot.modules.helper_funcs.chat_status import sudo_plus
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version


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


@sudo_plus
async def stats(update: Update):
    message = update.effective_message
    db_size = SESSION.execute(
        "SELECT pg_size_pretty(pg_database_size(current_database()))"
    ).scalar_one_or_none()
    uptime = datetime.datetime.fromtimestamp(
        boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    botuptime = get_readable_time((time.time() - StartTime))
    status = "*╔═━「 System statistics: 」*\n\n"
    status += f"*➛ System Start time:* {str(uptime)}" + "\n"
    uname = platform.uname()
    status += f"*➛ System:* {str(uname.system)}" + "\n"
    status += f"*➛ Node name:* {escape_markdown(str(uname.node))}" + "\n"
    status += f"*➛ Release:* {escape_markdown(str(uname.release))}" + "\n"
    status += f"*➛ Machine:* {escape_markdown(str(uname.machine))}" + "\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += f"*➛ CPU:* {str(cpu)}" + " %\n"
    status += f"*➛ RAM:* {str(mem[2])}" + " %\n"
    status += f"*➛ Storage:* {str(disk[3])}" + " %\n\n"
    status += f"*➛ Python version:* {python_version()}" + "\n"
    status += f"*➛ python-telegram-bot:* {str(ptbver)}" + "\n"
    status += f"*➛ Uptime:* {str(botuptime)}" + "\n"
    status += f"*➛ Database size:* {str(db_size)}" + "\n"
    kb = [[InlineKeyboardButton("Ping", callback_data="pingCB")]]
    try:
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        status += f"*➛ Commit*: `{sha[:9]}`\n"
    except Exception as e:
        status += f"*➛ Commit*: `{str(e)}`\\n"
    try:
        await message.reply_text(
            status + "\n*╔═━「 Bot statistics*: 」\n" +
            "\n".join([mod.__stats__() for mod in STATS]) +
            "\n\n✦ [Support](https://t.me/gangs_for_udanpirappu) | ✦ [Updates](https://t.me/gangs_for_udanpirappu)\n\n"
            + "╘═━「 by [LOGI-LAB](https://github.com/logi-lab) 」\n",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(kb),
            disable_web_page_preview=True,
            allow_sending_without_reply=True)
    except BaseException:
        await message.reply_text(
            ((("\n*╔═━「 Bot statistics*: 」\n" + "\n".join(mod.__stats__()
                                                          for mod in STATS)) +
              "\n\n✦ [Support](https://t.me/gangs_for_udanpirappu) | ✦ [Updates](https://t.me/gangs_for_udanpirappu)\n\n"
              ) + "╘═━「 by [LOGI-LAB](https://github.com/LOGI-LAB) 」\n"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(kb),
            disable_web_page_preview=True,
            allow_sending_without_reply=True,
        )


async def ping(update: Update, _):
    msg = update.effective_message
    start_time = time.time()
    message = await msg.reply_text("Pinging...")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    await message.edit_text(f"*Pong!!!*\n`{ping_time}ms`",
                            parse_mode=ParseMode.MARKDOWN)


async def pingCallback(update: Update):
    query = update.callback_query
    start_time = time.time()
    requests.get("https://api.telegram.org")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    await query.answer(f'Pong! {ping_time}ms')


QUEEN_PTB.add_handler(CommandHandler(["stats", "statistics"], stats, block=False))
QUEEN_PTB.add_handler(CallbackQueryHandler(pingCallback, pattern=r"pingCB", block=False))

__mod_name__ = "[✨ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ ✨]"
