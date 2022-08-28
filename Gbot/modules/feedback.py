"""
Copyright ( C ) GopiNath  
"""

import random

from telegram.constants import ParseMode
from telethon import Button

from Gbot import OWNER_ID, SUPPORT_CHAT
from Gbot import telethn as tbot

from ..events import register


@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    HOTTIE = (
        "https://telegra.ph/file/5a03a79acba8d3c407056.jpg",
        "https://telegra.ph//file/15ab1c01c8ed09a7ffc95.jpg",
        "https://telegra.ph/file/b4af1ee5c4179e8833d6d.jpg",
        "https://telegra.ph/file/15f2fb8f2ff8c0bf2bd06.jpg",
        "https://telegra.ph//file/5a3ec69041389b4fbcc2a.jpg",
        "https://telegra.ph/file/979500203d6fcf1924130.jpg",
        "https://telegra.ph/file/6b09f8642d1890e4d67c8.jpg",
        "https://telegra.ph/file/abf580ada4818ab99f9c0.jpg",
        "https://telegra.ph/file/ab410f256673c3001307b.jpg",
        "https://telegra.ph/file/398e8cb58bff53c59ee19.jpg",
    )
    FEED = ("https://telegra.ph/file/7739e801954a16bcb130f.jpg", )
    BUTTON = [[
        Button.url("Go To Support Group", f"https://t.me/{SUPPORT_CHAT}")
    ]]
    TEXT = "Thanks For Your Feedback, I Hope You Happy With Our Service"
    logger_text = f"""
**New Feedback**
**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if user_id == 1926801217:
        await e.reply("**Sry I Can't Identify ur Info**",
                      parse_mode=ParseMode.MARKDOWN)
        return

    if user_id == 1087968824:
        await e.reply("**Turn Off Ur Anonymous Mode And Try**",
                      parse_mode=ParseMode.MARKDOWN)
        return

    if e.sender_id != OWNER_ID and not quew:
        GIVE = "Give Some Text For Feedback ✨"
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=random.choice(FEED),
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(HOTTIE),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(HOTTIE), buttons=BUTTON)
