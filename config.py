import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")


API_ID = int(getenv("API_ID", "")) #required
API_HASH = getenv("API_HASH", "") #required

# Initialize SUDO_USERS with owner ID if empty
SUDO_USERS_RAW = getenv("SUDO_USERS", "")
if SUDO_USERS_RAW:
    SUDO_USERS = list(map(int, SUDO_USERS_RAW.split()))
else:
    SUDO_USERS = []

OWNER_ID = int(getenv("OWNER_ID", ""))

# Ensure owner is always in sudo users
if OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)

MONGO_URL = getenv("MONGO_URL", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
ALIVE_PIC = getenv("ALIVE_PIC", 'https://telegra.ph/file/9b7e1b820c72a14d90be7.mp4')
ALIVE_TEXT = getenv("ALIVE_TEXT")
PM_LOGGER = getenv("PM_LOGGER", "-1002517933675")
LOG_GROUP = getenv("LOG_GROUP", "-1002543265301")
GIT_TOKEN = getenv("GIT_TOKEN") #personal access token
REPO_URL = getenv("REPO_URL", "https://github.com/Suraj08832/Zefronuserbot")
BRANCH = getenv("BRANCH", "master") #don't change
 
STRING_SESSION1 = getenv("STRING_SESSION1", "")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")
STRING_SESSION4 = getenv("STRING_SESSION4", "")
STRING_SESSION5 = getenv("STRING_SESSION5", "")
STRING_SESSION6 = getenv("STRING_SESSION6", "")
STRING_SESSION7 = getenv("STRING_SESSION7", "")
STRING_SESSION8 = getenv("STRING_SESSION8", "")
STRING_SESSION9 = getenv("STRING_SESSION9", "")
STRING_SESSION10 = getenv("STRING_SESSION10", "")

# Print sudo configuration for debugging
print(f"🔐 Sudo Configuration:")
print(f"   Owner ID: {OWNER_ID}")
print(f"   Sudo Users: {SUDO_USERS}")
