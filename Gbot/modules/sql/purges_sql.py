"""
Copyright ( C ) GopiNath  
"""
#Purges_SQL for /purgefrom & /purgeto

import threading

from Gbot.modules.sql import BASE, SESSION
from sqlalchemy import (Column, Integer, String)


class Purges(BASE):
    __tablename__ = "purges"
    chat_id = Column(String(14), primary_key=True)
    message_from = Column(Integer, primary_key=True)


    def __init__(self, chat_id, message_from):
        self.chat_id = str(chat_id)  # ensure string
        self.message_from = message_from


    def __repr__(self):
        return f"<Purges {self.chat_id}>"


Purges.__table__.create(checkfirst=True)

PURGES_INSERTION_LOCK = threading.RLock()

def purgefrom(chat_id, message_from):
    with PURGES_INSERTION_LOCK:
        note = Purges(str(chat_id), message_from)
        SESSION.add(note)
        SESSION.commit()

def is_purgefrom(chat_id, message_from):
    try:
        return SESSION.query(Purges).get((str(chat_id), message_from))
    finally:
        SESSION.close()

def clear_purgefrom(chat_id, message_from):
    with PURGES_INSERTION_LOCK:
        if note := SESSION.query(Purges).get((str(chat_id), message_from)):
            SESSION.delete(note)
            SESSION.commit()
            return True
        SESSION.close()
        return False

def show_purgefrom(chat_id):
    try:
        return SESSION.query(Purges).filter(Purges.chat_id == str(chat_id)).order_by(Purges.message_from.asc()).all()
    finally:
        SESSION.close()
