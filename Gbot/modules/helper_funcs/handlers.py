"""
Copyright ( C ) GopiNath  
"""

import Gbot.modules.sql.blacklistusers_sql as sql

from Gbot import ALLOW_EXCL
from Gbot import DEV_USERS, SUDO_USERS, SUPPORT_USERS, TIGER_USERS, WHITELIST_USERS, QUEEN_PTB

from telegram import Update
import telegram.ext as tg
from pyrate_limiter import (
    Duration,
    RequestRate,
    Limiter,
    MemoryListBucket,
)

CMD_STARTERS = ("/", "?", ".", "~", "+") if ALLOW_EXCL else ("/", "?", ".", "+")


class AntiSpam:
    def __init__(self):
        self.whitelist = (
            (DEV_USERS or [])
            + (SUDO_USERS or [])
            + (WHITELIST_USERS or [])
            + (SUPPORT_USERS or [])
            + (TIGER_USERS or [])
        )
        # Values are HIGHLY experimental, its recommended you pay attention to our commits as we will be adjusting the values over time with what suits best.
        Duration.CUSTOM = 15  # Custom duration, 15 seconds
        self.sec_limit = RequestRate(6, Duration.CUSTOM)  # 6 / Per 15 Seconds
        self.min_limit = RequestRate(20, Duration.MINUTE)  # 20 / Per minute
        self.hour_limit = RequestRate(100, Duration.HOUR)  # 100 / Per hour
        self.daily_limit = RequestRate(1000, Duration.DAY)  # 1000 / Per day
        self.limiter = Limiter(
            self.sec_limit,
            self.min_limit,
            self.hour_limit,
            self.daily_limit,
            bucket_class=MemoryListBucket,
        )

    @staticmethod
    def check_user(self, user):
        """
        Return True if user is to be ignored else False
        """
        return bool(sql.is_user_blacklisted(user))

SpamChecker = AntiSpam()
MessageHandlerChecker = AntiSpam()


class CustomCommandHandler(tg.CommandHandler):
    def __init__(self, command, callback, block=False, **kwargs):
        if "admin_ok" in kwargs:
            del kwargs["admin_ok"]
        super().__init__(command, callback, **kwargs)

    def check_update(self, update):
        if not isinstance(update, Update) or not update.effective_message:
            return
        message = update.effective_message

        try:
            user_id = update.effective_user.id
        except Exception:
            user_id = None

        if message.text and len(message.text) > 1:
            fst_word = message.text.split(None, 1)[0]
            if len(fst_word) > 1 and any(
                fst_word.startswith(start) for start in CMD_STARTERS
            ):
                args = message.text.split()[1:]
                command = fst_word[1:].split("@")
                command.append(
                    message._bot.username
                )  # in case the command was sent without a username

                if not (
                    frozenset({command[0].lower()}) in self.commands
                    and command[1].lower() == message._bot.username.lower()
                ):
                    return None

                if SpamChecker.check_user(user_id):
                    return None

                if filter_result := self.filters.check_update(update):
                    return args, filter_result
                return False


    def collect_additional_context(self, context, update, QUEEN_PTB, check_result):
        if isinstance(check_result, bool):
            context.args = update.effective_message.text.split()[1:]
        else:
            context.args = check_result[0]
            if isinstance(check_result[1], dict):
                context.update(check_result[1])


