"""
Copyright ( C ) GopiNath  
"""
from functools import wraps
from telegram import error


async def send_message(message, *args, **kwargs):
    try:
        return await message.reply_text(*args, **kwargs)
    except error.BadRequest as err:
        if str(err) == "Reply message not found":
            return await message.reply_text(quote=False, *args, **kwargs)


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):

        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, action=action)
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator
