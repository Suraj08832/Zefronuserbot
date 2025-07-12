import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")


API_ID = int(getenv("API_ID", "23533031")) #optional
API_HASH = getenv("API_HASH", "912addd0288cdc2e1b0a463df9deeb8c") #optional

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
OWNER_ID = int(getenv("OWNER_ID", "8115787127"))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://sandeep:fpA5BAT3VqCq0THj@cluster0.bege5a8.mongodb.net/destinymusic?retryWrites=true&w=majority&appName=Cluster0")
BOT_TOKEN = getenv("BOT_TOKEN", "7691210897:AAHCRIkp6qWt171xyjX4oxHDPXkLmFJMZKs")
ALIVE_PIC = getenv("ALIVE_PIC", 'https://telegra.ph/file/9b7e1b820c72a14d90be7.mp4')
ALIVE_TEXT = getenv("ALIVE_TEXT")
PM_LOGGER = getenv("PM_LOGGER", "-1002517933675")
LOG_GROUP = getenv("LOG_GROUP", "-1002517933675")
GIT_TOKEN = getenv("GIT_TOKEN") #personal access token
REPO_URL = getenv("REPO_URL", "https://github.com/ITZ-Zefron/Zefron-USERBOT")
BRANCH = getenv("BRANCH", "master") #don't change
 
STRING_SESSION1 = getenv("STRING_SESSION1", "BQFnFecAHomh24LIWFmPBSCnhhr1ZSMgraY5LlH9zHLSmZ6GENsI-wczWHIYhJQCzfAHYKfGcyx5tXAU6lbFbe6F3L1F05v4g6gDsvLFgWA5Jcu1IPt8GvHbDne6sBdF1liV_c8mWq3Pd7fpnpjAIBAkHe_N2AntaenIEeM74VqFnLXFAu9q-T3tosxftJMXJOWGOh9u8CAGKCbJTwSbx7fj3zaQJnC4wayKlIxTkLp8BWIov1emzOg0iiNR1Qdz9JUa-W4KskUhtlILKMvMNSneLSGaoViKfravE2IN6jJtX_6Ijb46cs_OxHKa5gPlWAjUHOHksUVFQoIRdAhYFE9bqN7H4gAAAAHjvRV3AA")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")
STRING_SESSION4 = getenv("STRING_SESSION4", "")
STRING_SESSION5 = getenv("STRING_SESSION5", "")
STRING_SESSION6 = getenv("STRING_SESSION6", "")
STRING_SESSION7 = getenv("STRING_SESSION7", "")
STRING_SESSION8 = getenv("STRING_SESSION8", "")
STRING_SESSION9 = getenv("STRING_SESSION9", "")
STRING_SESSION10 = getenv("STRING_SESSION10", "")
