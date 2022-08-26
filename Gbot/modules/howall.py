"""
Copyright ( C ) GopiNath  
"""
import random
from .. import telethn as asst
from telethon import Button, events

BUTTON = [[
    Button.url("❓ What Is This", "https://t.me/Black_Knights_Union/195")
]]
HOT = "https://telegra.ph/file/daad931db960ea40c0fca.gif"
SMEXY = "https://telegra.ph/file/a23e9fd851fb6bc771686.gif"
LEZBIAN = "https://telegra.ph/file/5609b87f0bd461fc36acb.gif"
BIGBALL = "https://i.gifer.com/8ZUg.gif"
LANG = "https://telegra.ph/file/423414459345bf18310f5.gif"
CUTIE = "https://64.media.tumblr.com/d701f53eb5681e87a957a547980371d2/tumblr_nbjmdrQyje1qa94xto1_500.gif"


@asst.on(events.NewMessage(pattern="/horny ?(.*)"))
async def horny(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    HORNY = f"**🔥** {mention} **Is** {mm}**% Horny!**"
    await e.reply(HORNY, buttons=BUTTON, file=HOT)


@asst.on(events.NewMessage(pattern="/gay ?(.*)"))
async def gay(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    GAY = f"**🏳‍🌈** {mention} **Is** {mm}**% Gay!**"
    await e.reply(GAY, buttons=BUTTON, file=SMEXY)


@asst.on(events.NewMessage(pattern="/lezbian ?(.*)"))
async def lezbian(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    FEK = f"**💜** {mention} **Is** {mm}**% Lezbian!**"
    await e.reply(FEK, buttons=BUTTON, file=LEZBIAN)


@asst.on(events.NewMessage(pattern="/boobs ?(.*)"))
async def boobs(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    BOOBS = f"**🍒** {mention}**'s Boobs Size Is** {mm}**!**"
    await e.reply(BOOBS, buttons=BUTTON, file=BIGBALL)


@asst.on(events.NewMessage(pattern="/cock ?(.*)"))
async def cock(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    COCK = f"**🍆** {mention}**'s Cock Size Is** {mm}**cm**"
    await e.reply(COCK, buttons=BUTTON, file=LANG)


@asst.on(events.NewMessage(pattern="/cute ?(.*)"))
async def cute(e):
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    CUTE = f"**🍑** {mention} {mm}**% Cute**"
    await e.reply(CUTE, buttons=BUTTON, file=CUTIE)


__help__ = """
➛ /horny - Check Your Current Hornyess 
➛ /gay - Check Your Current Gayness 
➛ /lezbian - Check Your Current Lezbianess 
➛ /boobs - Check Your Current Boobs Size 
➛ /cock - Check Your Current Cock Size 
➛ /cute - Check Your Current Cuteness 

Note :- This Module Inspired By @HowAllBot We Just Make It For Fun Don't Take It Serious
"""

__mod_name__ = "How-All"
