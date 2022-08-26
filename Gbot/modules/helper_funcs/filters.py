"""
Copyright ( C ) GopiNath  
"""

from telegram import Message
from telegram.ext.filters import MessageFilter

    class _IsAnonChannel(MessageFilter):
        def filter(self, message: Message):
            return bool((message.from_user and message.from_user.id == 136817688 ))

    is_anon_channel = _IsAnonChannel()
