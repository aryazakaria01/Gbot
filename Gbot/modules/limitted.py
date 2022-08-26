"""
Copyright ( C ) GopiNath  
"""

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from Gbot.events import register
from Gbot import ubot


@register(pattern="^/limited ?(.*)")
async def _(event):
    chat = "@SpamBot"
    msg = await event.reply("Checking If You Are Limited...")
    async with ubot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=178220800))
            await conv.send_message("/start")
            response = await response
            await ubot.send_read_acknowledge(chat)
        except YouBlockedUserError:
            await msg.edit("Boss! Please Unblock @SpamBot ")
            return
        await msg.edit(f"~ {response.message.message}")
