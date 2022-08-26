"""
Copyright ( C ) GopiNath  
"""

import os
import requests

from pyrogram import filters
from json import JSONDecodeError

from Gbot.utils.pluginhelpers import admins_only, edit_or_reply, fetch_audio
from Gbot import pgram, SUPPORT_CHAT, QUEEN_PTB


@pgram.on_message(
    filters.command(["identify", "shazam", "shazam@Gbot"]))
@admins_only
async def shazamm(client: Client, message: Message):
    kek = await edit_or_reply(message, "`Shazaming In Progress!`")
    if not message.reply_to_message:
        await kek.edit("Reply To The Audio.")
        return
    if os.path.exists("friday.mp3"):
        os.remove("friday.mp3")
    kkk = await fetch_audio(client, message)
    downloaded_file_name = kkk
    f = {"file": (downloaded_file_name, open(downloaded_file_name, "rb"))}
    await kek.edit(
        "**Searching For This Song In Qᴜᴇᴇɴ ʙᴏᴛ 愛's DataBase.**")
    r = requests.post("https://starkapi.herokuapp.com/shazam/", files=f)
    try:
        xo = r.json()
    except JSONDecodeError:
        await kek.edit(
            "`Seems Like Our Server Has Some Issues, Please Try Again Later!`")
        return
    if xo.get("success") is False:
        await kek.edit("`Song Not Found In Database. Please Try Again.`")
        os.remove(downloaded_file_name)
        return
    xoo = xo.get("response")
    zz = xoo[1]
    zzz = zz.get("track")
    zzz.get("sections")[3]
    nt = zzz.get("images")
    image = nt.get("coverarthq")
    by = zzz.get("subtitle")
    title = zzz.get("title")
    messageo = f"""<b>Song Shazamed.</b>
<b>Song Name : </b>{title}
<b>Song By : </b>{by}
<u><b>Identified Using @Gbot - Join our support @{SUPPORT_CHAT}</b></u>
<i>Powered by @rowdy_of_blus</i>
"""
    await client.send_photo(message.chat.id,
                            image,
                            messageo,
                            parse_mode="HTML")
    os.remove(downloaded_file_name)
    await kek.delete()
