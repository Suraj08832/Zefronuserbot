import os
import sys
from pyrogram import Client



def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Zefron"])

async def join(client):
    try:
        await client.join_chat("bots_update_all")
    except BaseException:
        pass
