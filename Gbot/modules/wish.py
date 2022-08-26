"""
Copyright ( C ) GopiNath  
"""
import random

from Gbot import OWNER_ID, telethn

from telethon import events, Button
from telegram.constants import ParseMode

BUTTON = [[
    Button.url("✨ Owner ✨", "https://t.me/ROWDY_OF_PLUS")
]]
COMET = "https://telegra.ph/file/713fbfbdde25cc1726866.mp4"
STAR = "https://telegra.ph/file/ad90b44c551cec31df76b.mp4"
WISH = """
**You can use** `/wish` **as a general Wishing Well of sorts**
**For example:**
`/wish I could date you 😍,` **or**
`/wish that sushi was 🍣 in /emojify, or
/wish I had someone to /cuddle at night...`
"""


@telethn.on(events.NewMessage(pattern="/wish ?(.*)"))
async def wish(e):
    quew = e.pattern_match.group(1)
    if e.sender_id != OWNER_ID and not quew:
        (await e.reply(WISH,
                       parse_mode=ParseMode.MARKDOWN,
                       buttons=BUTTON,
                       file=STAR), )
        return
    if not e.is_reply:
        mm = random.randint(1, 100)
        DREAM = f"**Your wish has been cast.✨**\n\n__chance of success {mm}%__"
        await e.reply(DREAM, buttons=BUTTON, file=COMET)
