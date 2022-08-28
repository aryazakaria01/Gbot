
import json
import os






# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    #Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 17881110 # integer value, dont use ""
    API_HASH = "41d02175c2858cae93b745ffa4aaed24"
    TOKEN = "5558413169:AAEP69-SWLjh2ftdpj0-v2aG9aN31ANB1Ag"  #This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 5523873067  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "ROWDY_OF_PLUS"
    SUPPORT_CHAT = 't.me/Team_udanpirappu'  #Your own group for support, do not add the @
    UPDATES_CHANNEL = 't.me/Team_udanpirappu' #Your own channel for Updates of bot, Do not add @
    JOIN_LOGGER = 1001351412926  #Prints any new group the bot is added to, prints just the name and ID.
    REM_BG_API_KEY = "http://removebg.com"
    TEMP_DOWNLOAD_DIRECTORY = ""
    EVENT_LOGS = 1001351412926  #Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    SQLALCHEMY_DATABASE_URI = 'postgres://weoqhnsa:djAEOjRGc-S12WNOc5n-OecygFuA3eCi@jelani.db.elephantsql.com/weoqhnsa' #do you hub your old heroku app database_URL then put here, most use 25days ago sql
    LOAD = [] #try to kang this db ur big mothersfuckers i know your noob so only kanging my db
    NO_LOAD = ['rss', 'cleaner', 'connection', 'math']
    WEBHOOK = None
    INFOPIC = True
    JOIN_LOGGER = ""
    OWNER_USERNAME = ""
    ALLOW_CHATS = ""
    SUDO_USERS = ""
    DEV_USERS = ""
    SUPPORT_USERS=""
    WHITELIST_USERS=""
    TIGER_USERS = ""
    URL = None
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"
    BOT_USERNAME = "udanpirappumusic_bot"
    MONGO_DB_URI = "mongodb+srv://logesh:logesh@cluster0.z75dh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    BOT_ID = ""
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  #Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    STRICT_GMUTE = True
    WORKERS = 8  # Number of subthreads to use. Set as number of threads your processor uses
    BAN_STICKER = ''  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    ARQ_API_URL = "https://thearq.tech"
    ARQ_API_KEY = "GKNOHX-UDSREJ-AWTSGO-XFDSCY-ARQ"
    CASH_API_KEY = 'awoo'  # Get your API key from https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = 'awoo'  # Get your API key from https://timezonedb.com/api
    OPENWEATHERMAP_ID = 'awoo'
    WALL_API = 'awoo'  #For wallpapers, get one from https://wall.alphacoders.com/api.php
    AI_API_KEY = 'awoo'  #For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None
    INFOPIC = ""
    GBAN_LOGS = ""
    ERROR_LOGS = ""
    WEBHOOK = ""
    URL = ""
    PORT = ""
    API_ID = ""
    API_HASH = ""
    DATABASE_URL = ""
    DONATION_LINK = ""
    STRICT_GBAN = ""
    BAN_STICKER = ""
    TEMP_DOWNLOAD_DIRECTORY = ""
    LOAD = ""
    NO_LOAD = ""
    CASH_API_KEY = ""
    TIME_API_KEY = ""
    WALL_API = ""
    MONGO_DB_URL = ""
    REDIS_URL = "redis://default:pCLdkE3UCYVQa7DAXhb2jK9mi6ahyR0r@redis-19911.c301.ap-south-1-1.ec2.cloud.redislabs.com:19911:8080/"
    SUPPORT_CHAT = ""
    REM_BG_API_KEY = ""
    OPENWEATHERMAP_ID = ""
    APP_ID = ""
    APP_HASH = ""
    STRING_SESSION = ""
    GENIUS_API_TOKEN = ""
    ALLOW_EXCL = ""
    DEL_CMDS = ""
    BOT_API_URL = ""
    MONGO_DB_URL =""
    MONGO_DB = ""
    HELP_IMG = ""
    GROUP_START_IMG = ""
    REMINDER_LIMIT = ""
    TG_API = ""
    DATABASE_NAME = ""
    BACKUP_PASS = ""


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True

