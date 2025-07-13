from pyrogram import filters, Client
import asyncio
from pyrogram.types import Message 

from pyrogram.methods import messages
from Zefron.database.pmpermitdb import get_approved_users, pm_guard
import Zefron.database.pmpermitdb as Zefron
from config import LOG_GROUP, PM_LOGGER
from Zefron.modules.help import add_command_help
from Zefron.helper.logger import log_pm

FLOOD_CTRL = 0
USERS_AND_WARNS = {}

def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


# Single PM guard handler that catches ALL private messages
@Client.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def pm_guard_handler(app: Client, message):
    """Main PM guard handler"""
    global FLOOD_CTRL
    
    try:
        # Check if PM guard is enabled
        pm_enabled = await pm_guard()
        if not pm_enabled:
            # Log PM if logger is enabled
            if PM_LOGGER:
                approved_users = await get_approved_users()
                is_approved = message.chat.id in approved_users
                await log_pm(app, message, message.from_user.mention, is_approved)
            return  # PM guard is disabled, allow all messages
        
        user_id = message.chat.id
        print(f"🚨 PM Guard checking user {user_id}")
        
        # Get approved users
        approved_users = await get_approved_users()
        
        # Check if user is approved
        if user_id in approved_users:
            # User is approved, just log the PM
            if PM_LOGGER:
                await log_pm(app, message, message.from_user.mention, True)
            return  # User is approved, allow message
        
        # User is NOT approved - handle PM guard
        print(f"🚫 User {user_id} is NOT approved - triggering PM guard")
        
        # Log the PM first
        if PM_LOGGER:
            await log_pm(app, message, message.from_user.mention, False)
        
        # Get PM settings
        pm_settings = await Zefron.get_pm_settings()
        if pm_settings is False:
            # Initialize default settings
            await Zefron.set_pm(True)
            pmpermit, pm_message, limit, block_message = True, Zefron.PMPERMIT_MESSAGE, Zefron.LIMIT, Zefron.BLOCKED
        else:
            pmpermit, pm_message, limit, block_message = pm_settings
        
        # Get user's current warning count
        user_warns = USERS_AND_WARNS.get(user_id, 0)
        print(f"⚠️ User {user_id} has {user_warns} warnings, limit is {limit}")
        
        # Check if user is within warning limit
        if user_warns <= limit - 2:
            user_warns += 1
            USERS_AND_WARNS[user_id] = user_warns
            print(f"📈 User {user_id} now has {user_warns} warnings")
            
            # Flood control
            if not FLOOD_CTRL > 0:
                FLOOD_CTRL += 1
            else:
                FLOOD_CTRL = 0
                print(f"🚫 Flood control active for user {user_id}")
                return
            
            # Delete previous PM permit messages
            try:
                async for msg in app.search_messages(
                    chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
                ):
                    await msg.delete()
            except Exception as e:
                print(f"❌ Error deleting previous messages: {e}")
            
            # Send warning message
            print(f"📤 Sending warning message to user {user_id}")
            try:
                await message.reply(pm_message, disable_web_page_preview=True)
                print(f"✅ Warning message sent successfully to user {user_id}")
            except Exception as e:
                print(f"❌ Error sending warning message: {e}")
            return
        
        # User exceeded limit, block them
        print(f"🚫 User {user_id} exceeded limit, blocking")
        try:
            await message.reply(block_message, disable_web_page_preview=True)
            print(f"✅ Block message sent to user {user_id}")
        except Exception as e:
            print(f"❌ Error sending block message: {e}")
        
        try:
            await app.block_user(message.chat.id)
            print(f"✅ Successfully blocked user {user_id}")
        except Exception as e:
            print(f"❌ Failed to block user {user_id}: {e}")
        
        # Reset user warnings
        USERS_AND_WARNS[user_id] = 0
        
    except Exception as e:
        print(f"❌ Error in PM guard handler: {e}")


@Client.on_message(filters.command("pmguard", ["."]) & filters.me)
async def pmguard_toggle(client, message):
    arg = get_arg(message)
    if arg == "on":
        await Zefron.set_pm(True)
        await message.edit("**PM Guard is now ON**")
    elif arg == "off":
        await Zefron.set_pm(False)
        await message.edit("**PM Guard is now OFF**")
    else:
        status = await pm_guard()
        status_text = "ON" if status else "OFF"
        await message.edit(f"**PM Guard is currently {status_text}**\n\nUse `.pmguard on` to enable\nUse `.pmguard off` to disable")


@Client.on_message(filters.command("setlimit", ["."]) & filters.me)
async def pmguard_limit(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Set limit to what?**")
        return
    try:
        limit = int(arg)
        await Zefron.set_limit(limit)
        await message.edit(f"**Limit set to {arg}**")
    except ValueError:
        await message.edit("**Please provide a valid number for limit**")


@Client.on_message(filters.command("setblockmsg", ["."]) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**What message to set**")
        return
    if arg == "default":
        await Zefron.set_block_message(Zefron.BLOCKED)
        await message.edit("**Block message set to default**.")
        return
    await Zefron.set_block_message(f"`{arg}`")
    await message.edit("**Custom block message set**")


@Client.on_message(filters.command("setpmmsg", ["."]) & filters.me)
async def setpmpermitmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**What message to set**")
        return
    if arg == "default":
        await Zefron.set_permit_message(Zefron.PMPERMIT_MESSAGE)
        await message.edit("**PM permit message set to default**.")
        return
    await Zefron.set_permit_message(f"`{arg}`")
    await message.edit("**Custom PM permit message set**")


@Client.on_message(filters.command(["allow", "ap", "approve", "a"], ["."]) & filters.me & filters.private)
async def allow(client, message):
    chat_id = message.chat.id
    await Zefron.allow_user(chat_id)
    await message.edit(f"**I have allowed [you](tg://user?id={chat_id}) to PM me.**")
    USERS_AND_WARNS.update({chat_id: 0})


@Client.on_message(filters.command(["deny", "dap", "disapprove", "dapp"], ["."]) & filters.me & filters.private)
async def deny(client, message):
    chat_id = message.chat.id
    await Zefron.deny_user(chat_id)
    await message.edit(f"**I have denied [you](tg://user?id={chat_id}) to PM me.**")


@Client.on_message(filters.command("testpmguard", ["."]) & filters.me)
async def test_pm_guard(client, message):
    """Test PM guard functionality"""
    await message.edit("**Testing PM Guard...**")
    
    try:
        pm_enabled = await pm_guard()
        approved_users = await get_approved_users()
        current_user_id = message.chat.id
        is_approved = current_user_id in approved_users
        
        result = f"**PM Guard Test:**\n\n"
        result += f"**Status:** {'✅ ON' if pm_enabled else '❌ OFF'}\n"
        result += f"**Approved Users:** {len(approved_users)}\n"
        result += f"**Current User:** {'✅ Approved' if is_approved else '❌ Not Approved'}\n\n"
        
        if is_approved:
            result += "**To test warnings, use `.deny` first**\n"
        else:
            result += "**Send a message to test warnings**\n"
        
        await message.edit(result)
        
    except Exception as e:
        await message.edit(f"**Error:** `{str(e)}`")


add_command_help(
    "pmguard",
    [
        [".pmguard", "Check PM Guard status"],
        [".pmguard on", "Enable PM Guard"],
        [".pmguard off", "Disable PM Guard"],
        [".setlimit <number>", "Set warning limit (default: 5)"],
        [".setblockmsg <text>", "Set custom block message"],
        [".setpmmsg <text>", "Set custom PM permit message"],
        [".allow", "Allow user to PM (use in PM)"],
        [".deny", "Deny user from PM (use in PM)"],
        [".testpmguard", "Test PM Guard functionality"],
    ],
)
