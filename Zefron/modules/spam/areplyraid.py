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
from Zefron.modules.help import add_command_help
SUDO_USERS = SUDO_USER
from .replyraid import RAIDS
import random
from .replyraid import RAID



@Client.on_message(
    filters.command(["replyraid"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def replyraid_user(client: Client, message: Message):
    """Activate reply raid on a user"""
    try:
        args = await extract_user(message)
        reply = message.reply_to_message
        ex = await message.edit("**Processing...**")
        
        if args:
            try:
                user = await client.get_users(args)
            except Exception:
                await ex.edit("**❌ Please specify a valid user!**")
                return
        elif reply:
            user_id = reply.from_user.id
            user = await client.get_users(user_id)
        else:
            await ex.edit("**❌ Please specify a valid user!**\n\n**Usage:**\n• `.replyraid @username`\n• `.replyraid 123456789`\n• Reply to a user with `.replyraid`")
            return
        
        if user.id == client.me.id:
            return await ex.edit("**🤖 You can't raid yourself!**")
        
        if user.id in SUDO_USERS:
            return await ex.edit("**❌ Can't raid sudo users!**")
        
        if user.id == DEVS:
            return await ex.edit("**❌ Can't raid developers!**")
        
        # Check if user is already in raid list
        raid_users = await get_rraid_users()
        if user.id in raid_users:
            await ex.edit(f"**⚠️ Replyraid is already activated on [{user.first_name}](tg://user?id={user.id})**")
            return
        
        # Add user to raid database and list
        await rraid_user(user.id)
        if user.id not in RAIDS:
            RAIDS.append(user.id)
        
        print(f"Replyraid activated on user {user.id} - RAIDS list: {RAIDS}")
        
        await ex.edit(f"**✅ Replyraid activated on [{user.first_name}](tg://user?id={user.id})!**\n\n**User ID:** `{user.id}`\n**Status:** Active")
        
    except Exception as e:
        await ex.edit(f"**❌ Error activating replyraid:** `{str(e)}`")


@Client.on_message(
    filters.command(["dreplyraid"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def deactivate_replyraid(client: Client, message: Message):
    """Deactivate reply raid on a user"""
    try:
        args = await extract_user(message)
        reply = message.reply_to_message
        ex = await message.edit("**Processing...**")
        
        if args:
            try:
                user = await client.get_users(args)
            except Exception:
                await ex.edit("**❌ Please specify a valid user!**")
                return
        elif reply:
            user_id = reply.from_user.id
            user = await client.get_users(user_id)
        else:
            await ex.edit("**❌ Please specify a valid user!**\n\n**Usage:**\n• `.dreplyraid @username`\n• `.dreplyraid 123456789`\n• Reply to a user with `.dreplyraid`")
            return
        
        # Check if user is in raid list
        raid_users = await get_rraid_users()
        if user.id not in raid_users:
            await ex.edit(f"**⚠️ Replyraid is not activated on [{user.first_name}](tg://user?id={user.id})**")
            return
        
        # Remove user from raid database and list
        await unrraid_user(user.id)
        if user.id in RAIDS:
            RAIDS.remove(user.id)
        
        print(f"Replyraid deactivated on user {user.id} - RAIDS list: {RAIDS}")
        
        await ex.edit(f"**✅ Replyraid deactivated on [{user.first_name}](tg://user?id={user.id})!**\n\n**User ID:** `{user.id}`\n**Status:** Inactive")
        
    except Exception as e:
        await ex.edit(f"**❌ Error deactivating replyraid:** `{str(e)}`")


@Client.on_message(
    filters.command(["replyraidlist"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def replyraid_list(client: Client, message: Message):
    """Show list of users with active replyraid"""
    try:
        ex = await message.edit("**Processing...**")
        
        raid_users = await get_rraid_users()
        if not raid_users:
            await ex.edit("**📋 No users have active replyraid!**")
            return
        
        raid_list = "**📋 Active Replyraid Users:**\n\n"
        count = 0
        
        for user_id in raid_users:
            count += 1
            try:
                user = await client.get_users(user_id)
                raid_list += f"**{count}.** [{user.first_name}](tg://user?id={user_id}) (`{user_id}`)\n"
            except Exception as e:
                raid_list += f"**{count}.** Unknown User (`{user_id}`) - Error: {e}\n"
        
        raid_list += f"\n**Total Raid Users:** {count}"
        await ex.edit(raid_list)
        
    except Exception as e:
        await ex.edit(f"**❌ Error showing replyraid list:** `{str(e)}`")


@Client.on_message(
    filters.command(["testreplyraid"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def test_replyraid(client: Client, message: Message):
    """Test replyraid functionality"""
    try:
        ex = await message.edit("**Testing Replyraid System...**")
        
        # Get raid users from database
        raid_users = await get_rraid_users()
        
        # Get current RAIDS list
        from .replyraid import RAIDS
        
        result = "**🔧 Replyraid Test Results:**\n\n"
        result += f"**Database Raid Users:** {len(raid_users)}\n"
        result += f"**Memory RAIDS List:** {len(RAIDS)}\n"
        result += f"**RAIDS List:** `{RAIDS}`\n\n"
        
        # Test RAID messages
        try:
            raid_message = random.choice(RAID)
            result += f"**RAID Message Test:** ✅ Working\n"
            result += f"**Sample Message:** `{raid_message[:50]}...`\n\n"
        except Exception as e:
            result += f"**RAID Message Test:** ❌ Error: {e}\n\n"
        
        if raid_users:
            result += "**Database Users:**\n"
            for user_id in raid_users[:5]:  # Show first 5
                result += f"• `{user_id}`\n"
            if len(raid_users) > 5:
                result += f"• ... and {len(raid_users) - 5} more\n"
        
        result += f"\n**Test Commands:**\n"
        result += f"• `.replyraid @username` - Activate raid\n"
        result += f"• `.dreplyraid @username` - Deactivate raid\n"
        result += f"• `.replyraidlist` - Show raid users\n"
        result += f"• `.sendraid` - Send test raid message\n"
        result += f"• Send a message from raided user to test\n"
        
        await ex.edit(result)
        
    except Exception as e:
        await ex.edit(f"**❌ Error testing replyraid:** `{str(e)}`")


@Client.on_message(
    filters.command(["sendraid"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def send_test_raid(client: Client, message: Message):
    """Send a test raid message"""
    try:
        ex = await message.edit("**Sending test raid message...**")
        
        # Get a random raid message
        raid_message = random.choice(RAID)
        
        # Send the raid message
        await message.reply_text(raid_message)
        
        await ex.edit(f"**✅ Test raid message sent!**\n\n**Message:** `{raid_message[:100]}...`")
        
    except Exception as e:
        await ex.edit(f"**❌ Error sending test raid message:** `{str(e)}`")


@Client.on_message(
    filters.command(["triggerraid"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def trigger_raid(client: Client, message: Message):
    """Manually trigger raid on a user"""
    try:
        args = await extract_user(message)
        reply = message.reply_to_message
        ex = await message.edit("**Triggering raid...**")
        
        if args:
            try:
                user = await client.get_users(args)
            except Exception:
                await ex.edit("**❌ Please specify a valid user!**")
                return
        elif reply:
            user_id = reply.from_user.id
            user = await client.get_users(user_id)
        else:
            await ex.edit("**❌ Please specify a valid user!**\n\n**Usage:**\n• `.triggerraid @username`\n• `.triggerraid 123456789`\n• Reply to a user with `.triggerraid`")
            return
        
        # Check if user is in raid list
        raid_users = await get_rraid_users()
        if user.id not in raid_users:
            await ex.edit(f"**⚠️ [{user.first_name}](tg://user?id={user.id}) is not in raid list!**\n\n**Use `.replyraid @{user.username or user.id}` first**")
            return
        
        # Send raid message
        try:
            raid_message = random.choice(RAID)
            await client.send_message(user.id, raid_message)
            await ex.edit(f"**✅ Raid message sent to [{user.first_name}](tg://user?id={user.id})!**\n\n**Message:** `{raid_message[:100]}...`")
        except Exception as e:
            await ex.edit(f"**❌ Error sending raid message:** `{str(e)}`")
        
    except Exception as e:
        await ex.edit(f"**❌ Error triggering raid:** `{str(e)}`")


@Client.on_message(
    filters.command(["syncraids"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def sync_raids(client: Client, message: Message):
    """Manually sync raids list with database"""
    try:
        ex = await message.edit("**Syncing raids list...**")
        
        # Get raid users from database
        raid_users = await get_rraid_users()
        
        # Sync with RAIDS list
        from .replyraid import RAIDS
        RAIDS.clear()
        RAIDS.extend(raid_users)
        
        result = "**🔄 Raids List Synced!**\n\n"
        result += f"**Database Users:** {len(raid_users)}\n"
        result += f"**Memory RAIDS List:** {len(RAIDS)}\n"
        result += f"**RAIDS List:** `{RAIDS}`\n\n"
        
        if raid_users:
            result += "**Active Raid Users:**\n"
            for user_id in raid_users[:5]:  # Show first 5
                try:
                    user = await client.get_users(user_id)
                    result += f"• [{user.first_name}](tg://user?id={user_id}) (`{user_id}`)\n"
                except:
                    result += f"• Unknown User (`{user_id}`)\n"
            if len(raid_users) > 5:
                result += f"• ... and {len(raid_users) - 5} more\n"
        
        await ex.edit(result)
        
    except Exception as e:
        await ex.edit(f"**❌ Error syncing raids:** `{str(e)}`")


add_command_help(
    "replyraid",
    [
        [".replyraid <reply/username/userid>", "Activate replyraid on a user."],
        [".dreplyraid <reply/username/userid>", "Deactivate replyraid on a user."],
        [".replyraidlist", "Show list of users with active replyraid."],
        [".testreplyraid", "Test replyraid functionality."],
        [".sendraid", "Send a test raid message."],
        [".triggerraid <reply/username/userid>", "Manually trigger raid on a user."],
        [".syncraids", "Sync raids list with database."],
    ],
)
