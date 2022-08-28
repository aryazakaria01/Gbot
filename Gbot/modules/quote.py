"""
Copyright ( C ) GopiNath  
"""

from io import BytesIO
from traceback import format_exc

from pyrogram import filters
from pyrogram.types import Message

from Gbot.utils.errors import capture_err
from Gbot import arq, pgram, LOGGER

Queen_PYRO_Q = filters.command(["quote", "q"])


async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(message: Message) -> str:
    return message.text.strip().split(None, 1)[1].strip()


def isArgInt(message: Message) -> list:
    count = getArg(message)
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]


@pgram.on_message(Queen_PYRO_Q & ~filters.forwarded & ~filters.bot)
@pgram.on_edited_message(Queen_PYRO_Q)
@capture_err
async def quote(client, message: Message):
    await message.delete()
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to quote it.")
    if not message.reply_to_message.text:
        return await message.reply_text(
            "Replied message has no text, can't quote it.")
    m = await message.reply_text("Quoting Messages Please wait....")
    if len(message.command) < 2:
        messages = [message.reply_to_message]
    elif len(message.command) == 2:
        arg = isArgInt(message)
        if arg[0]:
            if arg[1] < 2 or arg[1] > 10:
                return await m.edit("Argument must be between 2-10.")
            count = arg[1]
            messages = [
                i for i in await client.get_messages(
                    message.chat.id,
                    range(message.reply_to_message.id,
                          message.reply_to_message.id + (count + 5)),
                    replies=0) if not i.empty and not i.media
            ]
            messages = messages[:count]
        else:
            if getArg(message) != "r":
                return await m.edit(
                    "Incorrect Argument, Pass **'r'** or **'INT'**, **EX:** __/q 2__"
                )
            reply_message = await client.get_messages(
                message.chat.id,
                message.reply_to_message.id,
                replies=1,
            )
            messages = [reply_message]
    else:
        return await m.edit(
            "Incorrect argument, check quotly module in help section.")
    try:
        if not message:
            return await m.edit("Something went wrong.")
        sticker = await quotify(messages)
        if not sticker[0]:
            await message.reply_text(sticker[1])
            return await m.delete()
        sticker = sticker[1]
        await message.reply_sticker(sticker)
        await m.delete()
        sticker.close()
    except Exception as e:
        await m.edit("Something went wrong while quoting messages," +
                     " This error usually happens when there's a " +
                     " message containing something other than text," +
                     " or one of the messages in-between are deleted.")
        e = format_exc()
        LOGGER.debug(e)


__mod_name__ = "[✨ Qᴜᴏᴛʟʏ ✨]"
