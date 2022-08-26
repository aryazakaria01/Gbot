"""
Copyright ( C ) GopiNath  
"""

import time

from requests import get
from pyrogram import filters
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup

from Gbot import pgram


def call_back_in_filter(data):
    return filters.create(lambda flt, _, query: flt.data in query.data,
                          data=data)


def latest():

    url = 'https://subsplease.org/api/?f=schedule&h=true&tz=Japan'
    res = get(url).json()

    k = None
    for x in res['schedule']:
        title = x['title']
        time = x['time']
        try:
            aired = bool(x['aired'])
            title = (
                f"**~~[{title}](https://subsplease.org/shows/{x['page']})~~**"
                if aired else
                f"**[{title}](https://subsplease.org/shows/{x['page']})**")

        except (KeyError, IndexError):
            title = f"**[{title}](https://subsplease.org/shows/{x['page']})**"
        data = f"{title} - {time}"

        k = f"{k}\n{data}" if k else data
    return k


@pgram.on_message(filters.command('latest'))
def lates(_, message):
    mm = latest()
    message.reply_text(f"Today's Schedule:\nTZ: Japan\n{mm}",
                       reply_markup=InlineKeyboardMarkup([[
                           InlineKeyboardButton("Refresh", callback_data="fk")
                       ]]))


@pgram.on_callback_query(call_back_in_filter("fk"))
def callbackk(_, query):

    if query.data == "fk":
        mm = latest()

        try:
            query.message.edit(f"Today\'s Schedule:\nTZ: Japan\n{mm}",
                               reply_markup=InlineKeyboardMarkup([[
                                   InlineKeyboardButton("Refresh",
                                                        callback_data="fk")
                               ]]))
            query.answer("Refreshed!")

        except:
            query.answer("Refreshed!")
