"""
Copyright ( C ) GopiNath  
"""

import time
import requests

from typing import List
from telegram import Update
from telegram.constants import ParseMode

from Gbot import StartTime, QUEEN_PTB
from Gbot.modules.helper_funcs.chat_status import sudo_plus
from Gbot.modules.disable import DisableAbleCommandHandler

sites_list = {
    "Telegram": "https://api.telegram.org",
    "Kaizoku": "https://animekaizoku.com",
    "Kayo": "https://animekayo.com",
    "Jikan": "https://api.jikan.moe/v3",
    "Kuki Chatbot": "https://www.kukiapi.xyz/",
}


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


def ping_func(to_ping: List[str]) -> List[str]:
    ping_result = []

    for each_ping in to_ping:

        start_time = time.time()
        site_to_ping = sites_list[each_ping]
        r = requests.get(site_to_ping)
        end_time = time.time()
        ping_time = f"{str(round((end_time - start_time), 2))}s"

        pinged_site = f"<b>{each_ping}</b>"

        if each_ping in ("Kaizoku", "Kayo"):
            pinged_site = f"<a href='{sites_list[each_ping]}'>{each_ping}</a>"
            ping_time = f"<code>{ping_time} (Status: {r.status_code})</code>"

        ping_text = f"{pinged_site}: <code>{ping_time}</code>"
        ping_result.append(ping_text)

    return ping_result


@sudo_plus
async def ping(update: Update):
    msg = update.effective_message

    start_time = time.time()
    message = await msg.reply_text("Pinging...")
    end_time = time.time()
    telegram_ping = f"{str(round((end_time - start_time) * 1000, 3))} ms"
    uptime = get_readable_time((time.time() - StartTime))

    await message.edit_text(
        f"PONG!!\n<b>Time Taken:</b> <code>{telegram_ping}</code>\n<b>Service uptime:</b> <code>{uptime}</code>",
        parse_mode=ParseMode.HTML,
    )


@sudo_plus
async def pingall(update: Update):
    to_ping = ["Kaizoku", "Kayo", "Telegram", "Jikan", "Kuki Chatbot"]
    pinged_list = ping_func(to_ping)
    pinged_list.insert(2, "")
    uptime = get_readable_time((time.time() - StartTime))

    reply_msg = "⏱Ping results are:\n" + "\n".join(pinged_list)
    reply_msg += f"\n<b>Service uptime:</b> <code>{uptime}</code>"

    await update.effective_message.reply_text(
        reply_msg,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


QUEEN_PTB.add_handler(DisableAbleCommandHandler("ping", ping, block=False))
QUEEN_PTB.add_handler(DisableAbleCommandHandler("pingall", pingall, block=False))

__command_list__ = ["ping", "pingall"]
