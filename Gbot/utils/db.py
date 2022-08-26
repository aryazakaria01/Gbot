__all__ = ['get_collection']

import asyncio
from Gbot import LOGGER
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection

DB_URL = "mongodb+srv://logesh:logesh@cluster0.rmtzl.mongodb.net/logesh?retryWrites=true&w=majority"

LOGGER.debug("Connecting to Database ...")

_MGCLIENT: AgnosticClient = AsyncIOMotorClient(DB_URL)
_RUN = asyncio.get_event_loop().run_until_complete

if "QueenBot" in _RUN(_MGCLIENT.list_database_names()):
    LOGGER.debug("[LOGI-LAB] Anime  Database Found :) => Now Logging to it...")
else:
    LOGGER.debug("[LOGI-LAB] Anime Database Not Found :( => Creating New Database...")

_DATABASE: AgnosticDatabase = _MGCLIENT["QueenBot"]


def get_collection(name: str) -> AgnosticCollection:
    """ Create or Get Collection from your database """
    return _DATABASE[name]


def _close_db() -> None:
    _MGCLIENT.close()
