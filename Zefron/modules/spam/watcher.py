import random
import asyncio
from pyrogram import filters, Client
from Zefron.modules.help import *
from Zefron.helper.utility import get_arg
from pyrogram.types import *
from pyrogram import __version__
import os
import sys
import asyncio
import re
from random import choice
from pyrogram import Client, filters
from pyrogram.types import Message
from cache.data import *
from Zefron.database.rraid import *
from Zefron import SUDO_USER
from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message
DEVS = int(1669178360)
from Zefron.helper.PyroHelpers import get_ub_chats
from Zefron.modules.basic.profile import extract_user, extract_user_and_reason
SUDO_USERS = SUDO_USER
from .replyraid import RAIDS


# Initialize RAIDS list if empty
if not RAIDS:
    RAIDS = []

# Always clear RAIDS list on startup to prevent any user from being raided after restart
RAIDS.clear()

print(f"🔧 Watcher initialized - RAIDS: {RAIDS}")
print(f"🔧 RAID messages available: {len(RAID) if 'RAID' in globals() else 'Not found'}")


async def sync_raids_list():
    """Sync RAIDS list with database"""
    try:
        raid_users = await get_rraid_users()
        RAIDS.clear()
        RAIDS.extend(raid_users)
        print(f"🔄 Synced RAIDS list with database: {RAIDS}")
    except Exception as e:
        print(f"❌ Error syncing RAIDS list: {e}")


@Client.on_message(filters.incoming & ~filters.me & ~filters.bot)
async def check_and_replyraid(app: Client, message: Message):
    """Check if user has active replyraid and send raid message"""
    try:
        # Removed: await sync_raids_list()
        
        # Skip if no raids are active
        if not RAIDS:
            return
        
        # Skip if user is not in raid list
        if message.from_user.id not in RAIDS:
            return
        
        # Skip if user is sudo or dev
        if message.from_user.id in SUDO_USERS or message.from_user.id == DEVS:
            return
        
        print(f"🚨 Replyraid triggered for user {message.from_user.id} in {message.chat.type}")
        
        # Get raid message from database
        raid_users = await get_rraid_users()
        if message.from_user.id in raid_users:
            # Send random raid message
            try:
                raid_message = random.choice(RAID)
                await message.reply_text(raid_message)
                print(f"✅ Raid message sent to user {message.from_user.id}: {raid_message[:50]}...")
            except Exception as e:
                print(f"❌ Error sending raid message: {e}")
                # Try sending a simple message as fallback
                try:
                    await message.reply_text("MADARCHOD TERI MAA KI CHUT ME GHUTKA KHAAKE THOOK DUNGA 🤣🤣")
                    print(f"✅ Fallback raid message sent to user {message.from_user.id}")
                except Exception as e2:
                    print(f"❌ Error sending fallback raid message: {e2}")
        
    except Exception as e:
        print(f"❌ Error in replyraid watcher: {e}")
