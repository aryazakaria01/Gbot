"""
Copyright ( C ) GopiNath  
"""

import requests
from telegram.constants import ParseMode

from Gbot.events import register as bot


@bot(pattern="[/!]waifu")
async def ok(event):
    url = "https://api.waifu.pics/sfw/waifu"
    r = requests.get(url)
    e = r.json()
    await event.reply(
        "**A waifu appeared!** \nAdd them to your harem by sending /protecc character name",
        parse_mode=ParseMode.MARKDOWN,
        file=e["url"])


@bot(pattern="[/!]protecc")
async def ok(event):
    await event.reply(
        "OwO you protecc'd A Waifu This waifu has been added to your harem.")


@bot(pattern="[/!]harem")
async def ok(event):
    await event.reply("You haven't protecc'd any waifu yet...")
