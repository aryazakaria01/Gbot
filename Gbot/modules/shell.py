"""
Copyright ( C ) GopiNath  
"""

import subprocess

from Gbot import LOGGER, QUEEN_PTB
from Gbot.modules.helper_funcs.chat_status import dev_plus
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler


@dev_plus
async def shell(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    cmd = await message.text.split(" ", 1)
    if len(cmd) == 1:
        await update.effective_message.reply_text(
            "No command to execute was given.")
        return
    cmd = cmd[1]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    stdout, stderr = process.communicate()
    reply = ""
    stderr = stderr.decode()
    if stdout := stdout.decode():
        reply += f"*Stdout*\n`{stdout}`\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    if stderr:
        reply += f"*Stderr*\n`{stderr}`\n"
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open("shell_output.txt", "w") as file:
            file.write(reply)
        with open("shell_output.txt", "rb") as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id,
            )
    else:
        await message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


QUEEN_PTB.add_handler(CommandHandler(["sh"], shell, block=False))

__mod_name__ = "[✨ ꜱʜᴇʟʟ ✨]"
__command_list__ = ["sh"]
