import asyncio
import datetime
from datetime import datetime
from telethon import Button, __version__ as tlhver
from Gbot.events import register
from Gbot import telethn
from platform import python_version
from pyrogram import __version__ as pyrover

edit_time = 5
""" =======================Hottie====================== """
file1 = "https://telegra.ph/file/11cfb0be7163d32c51259.jpg"
file2 = "https://telegra.ph/file/444028d9b3daccc947a2d.jpg"
file3 = "https://telegra.ph/file/fdf47498b208bc63000b4.jpg"
file4 = "https://telegra.ph/file/e8f3310b943b8b8699dcd.jpg"
file5 = "https://telegra.ph/file/401cb7f6216764ebab161.jpg"
""" =======================Hottie====================== """

BUTTON = [[
    Button.url("【► HELP ◄】", "https://t.me/Gbot?start=help"),
    Button.url("【► SUPPORT ◄】", "https://t.me/Black_Knights_Union_Support"),
]]

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)


@register(pattern=("/alive"))
async def hmm(yes):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    pm_caption = f"** ♡ Hey [{yes.sender.first_name}](tg://user?id={yes.sender.id}) I,m Queen 愛 **\n\n"
    pm_caption += f"**♡ My Uptime :** `{uptime}`\n\n"
    pm_caption += f"**♡ Python Version :** `{python_version}`\n\n"
    pm_caption += f"**♡ Telethon Version :** `{tlhver}`\n\n"
    pm_caption += f"**♡ Pyrogram Version :** `{pyrover}`\n\n"
    pm_caption += "**♡ My Master :** [Rajkumar](https://t.me/Awesome_RJ_official) "
    BUTTON = [[
        Button.url("【► Help ◄】", "https://t.me/Gbot?start=help"),
        Button.url("【► Support ◄】",
                   "https://t.me/Black_Knights_Union_Support"),
    ]]
    on = await telethn.send_file(yes.chat_id,
                                 file=file1,
                                 caption=pm_caption,
                                 buttons=BUTTON,
                                 reply_to=yes)

    await asyncio.sleep(edit_time)
    ok = await telethn.edit_message(yes.chat_id,
                                    on,
                                    file=file2,
                                    buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok2 = await telethn.edit_message(yes.chat_id,
                                     ok,
                                     file=file3,
                                     buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok3 = await telethn.edit_message(yes.chat_id,
                                     ok2,
                                     file=file4,
                                     buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok4 = await telethn.edit_message(yes.chat_id,
                                     ok3,
                                     file=file5,
                                     buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok5 = await telethn.edit_message(yes.chat_id,
                                     ok4,
                                     file=file1,
                                     buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok6 = await telethn.edit_message(yes.chat_id,
                                     ok5,
                                     file=file2,
                                     buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok7 = await telethn.edit_message(yes.chat_id,
                                     ok6,
                                     file=file3,
                                     buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok8 = await telethn.edit_message(yes.chat_id,
                                     ok7,
                                     file=file4,
                                     buttons=BUTTON)

    await asyncio.sleep(edit_time)
    ok9 = await telethn.edit_message(yes.chat_id,
                                     ok8,
                                     file=file5,
                                     buttons=BUTTON)
