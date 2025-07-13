import asyncio
from datetime import datetime
from platform import python_version
import os
import sys

from pyrogram import __version__, filters, Client
from pyrogram.types import Message
from config import ALIVE_PIC, ALIVE_TEXT, PM_LOGGER, LOG_GROUP
from Zefron import START_TIME
from Zefron import SUDO_USER
from Zefron.helper.PyroHelpers import ReplyCheck
from Zefron.modules.help import add_command_help
from Zefron.modules.bot.inline import get_readable_time
from Zefron.helper.logger import log_action

alive_logo = ALIVE_PIC or "https://telegra.ph/file/cc0890d0876bc18c19e05.jpg"

if ALIVE_TEXT:
   txt = ALIVE_TEXT
else:
    txt = (
        f"** ✘ zefron υѕєявσт ✘**\n\n"
        f"❏ **νєяѕισи**: `2.1`\n"
        f"├• **υρтιмє**: `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f"├• **ρутнσи**: `{python_version()}`\n"
        f"├• **ρуяσgяαм**: `{__version__}`\n"
        f"├• **ѕυρρσят**: [Click](t.me/bots_update_all)\n"
        f"├• **¢нαииєℓ**: [Click](t.me/bots_update_all)\n"
        f"└• **яєρσ**: [Click](https://github.com/Suraj08832/Zefronuserbot)"        
    )

@Client.on_message(
    filters.command(["alive", "awake"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def alive(client: Client, message: Message):
    xx = await message.reply_text("⚡️")
    try:
       await message.delete()
    except:
       pass
    send = client.send_video if alive_logo.endswith(".mp4") else client.send_photo
    xd = (f"{txt}")
    try:
        await asyncio.gather(
            xx.delete(),
            send(
                message.chat.id,
                alive_logo,
                caption=xd,
                reply_to_message_id=ReplyCheck(message),
            ),
        )
    except BaseException:
        await xx.edit(xd, disable_web_page_preview=True)

@Client.on_message(filters.command("repo", ".") & filters.me)
async def repo(bot: Client, message: Message):
    await message.edit("⚡")
    await asyncio.sleep(1)
    await message.edit("Fetching Source Code.....")
    await asyncio.sleep(1)
    await message.edit("Here is repo: \n\n\nhttps://github.com/Suraj08832/Zefronuserbot\nFork & Give an ⭐")


@Client.on_message(filters.command("creator", ".") & filters.me)
async def creator(bot: Client, message: Message):
    await message.edit("https://gitHub.com/itz-Zefron")


@Client.on_message(filters.command(["uptime", "up"], ".") & filters.me)
async def uptime(bot: Client, message: Message):
    now = datetime.now()
    current_uptime = now - START_TIME
    await message.edit(f"Uptime ⚡\n" f"```{str(current_uptime).split('.')[0]}```")


@Client.on_message(filters.command("id", ".") & filters.me)
async def get_id(bot: Client, message: Message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message

        if rep.audio:
            file_id = f"**File ID**: `{rep.audio.file_id}`"
            file_id += "**File Type**: `audio`"

        elif rep.document:
            file_id = f"**File ID**: `{rep.document.file_id}`"
            file_id += f"**File Type**: `{rep.document.mime_type}`"

        elif rep.photo:
            file_id = f"**File ID**: `{rep.photo.file_id}`"
            file_id += "**File Type**: `photo`"

        elif rep.sticker:
            file_id = f"**Sicker ID**: `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"**Sticker Set**: `{rep.sticker.set_name}`\n"
                file_id += f"**Sticker Emoji**: `{rep.sticker.emoji}`\n"
                if rep.sticker.is_animated:
                    file_id += f"**Animated Sticker**: `{rep.sticker.is_animated}`\n"
                else:
                    file_id += "**Animated Sticker**: `False`\n"
            else:
                file_id += "**Sticker Set**: __None__\n"
                file_id += "**Sticker Emoji**: __None__"

        elif rep.video:
            file_id = f"**File ID**: `{rep.video.file_id}`\n"
            file_id += "**File Type**: `video`"

        elif rep.animation:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `GIF`"

        elif rep.voice:
            file_id = f"**File ID**: `{rep.voice.file_id}`\n"
            file_id += "**File Type**: `Voice Note`"

        elif rep.video_note:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `Video Note`"

        elif rep.location:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.location.latitude}`"

        elif rep.venue:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.venue.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.venue.location.latitude}`\n\n"
            file_id += "**Address**:\n"
            file_id += f"**title**: `{rep.venue.title}`\n"
            file_id += f"**detailed**: `{rep.venue.address}`\n\n"

        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.id}`"
        await message.edit(user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.id}`\n\n"
        user_detail += file_id
        await message.edit(user_detail)

    else:
        await message.edit(f"**Chat ID**: `{message.chat.id}`")


@Client.on_message(filters.command("restart", ".") & filters.me)
async def restart_bot(client: Client, message: Message):
    await message.edit("**Restarting Zefron Userbot...**")
    try:
        # Import the restart function
        from Zefron.helper import restart
        restart()
    except Exception as e:
        await message.edit(f"**Error restarting:** `{str(e)}`")


@Client.on_message(filters.command("testlogger", ".") & filters.me)
async def test_logger(client: Client, message: Message):
    await message.edit("**Testing logger functionality...**")
    
    result = f"**Logger Test Results:**\n\n"
    
    # Test PM Logger
    if PM_LOGGER:
        try:
            # First validate the group
            from Zefron.helper.logger import validate_logger_group
            is_valid = await validate_logger_group(client, PM_LOGGER)
            
            if is_valid:
                await log_action(client, "TEST", f"PM Logger test from {message.chat.title}", PM_LOGGER)
                pm_status = "✅ PM Logger working"
            else:
                pm_status = f"❌ PM Logger group not accessible\n**Group ID:** `{PM_LOGGER}`\n**Issue:** Group doesn't exist or userbot not a member"
        except Exception as e:
            pm_status = f"❌ PM Logger failed: {str(e)}"
    else:
        pm_status = "❌ PM_LOGGER not set"
    
    # Test General Logger
    if LOG_GROUP:
        try:
            # First validate the group
            from Zefron.helper.logger import validate_logger_group
            is_valid = await validate_logger_group(client, LOG_GROUP)
            
            if is_valid:
                await log_action(client, "TEST", f"General Logger test from {message.chat.title}", LOG_GROUP)
                general_status = "✅ General Logger working"
            else:
                general_status = f"❌ General Logger group not accessible\n**Group ID:** `{LOG_GROUP}`\n**Issue:** Group doesn't exist or userbot not a member"
        except Exception as e:
            general_status = f"❌ General Logger failed: {str(e)}"
    else:
        general_status = "❌ LOG_GROUP not set"
    
    result += f"**PM Logger ({PM_LOGGER}):** {pm_status}\n\n"
    result += f"**General Logger ({LOG_GROUP}):** {general_status}\n\n"
    result += f"**Current Chat:** {message.chat.title} (`{message.chat.id}`)\n\n"
    
    # Add troubleshooting tips
    result += "**🔧 Troubleshooting Tips:**\n"
    result += "• Make sure the group ID is correct\n"
    result += "• Ensure your userbot is a member of the logger group\n"
    result += "• Check if the group is a supergroup (not a regular group)\n"
    result += "• Verify the group hasn't been deleted\n"
    result += "• Try adding your userbot to the group again"
    
    await message.edit(result)


@Client.on_message(filters.command("pmstatus", ".") & filters.me)
async def check_pm_status(client: Client, message: Message):
    await message.edit("**Checking PM Guard status...**")
    
    try:
        from Zefron.database.pmpermitdb import get_pm_settings, get_approved_users, pm_guard
        
        # Check PM guard status
        pm_enabled = await pm_guard()
        pm_status = "✅ ON" if pm_enabled else "❌ OFF"
        
        # Get PM settings
        pm_settings = await get_pm_settings()
        if pm_settings is False:
            settings_status = "❌ Not initialized"
            limit = "5 (default)"
            block_msg = "Default"
            permit_msg = "Default"
        else:
            pmpermit, permit_msg, limit, block_msg = pm_settings
            settings_status = "✅ Initialized"
        
        # Get approved users
        approved_users = await get_approved_users()
        approved_count = len(approved_users)
        
        result = f"**PM Guard Status:**\n\n"
        result += f"**Guard Status:** {pm_status}\n"
        result += f"**Settings:** {settings_status}\n"
        result += f"**Warning Limit:** {limit}\n"
        result += f"**Approved Users:** {approved_count}\n\n"
        
        if approved_users:
            result += "**Approved User IDs:**\n"
            for user_id in approved_users[:5]:  # Show first 5
                result += f"• `{user_id}`\n"
            if len(approved_users) > 5:
                result += f"• ... and {len(approved_users) - 5} more\n"
        
        result += f"\n**Commands:**\n"
        result += f"• `.pmguard on` - Enable PM guard\n"
        result += f"• `.pmguard off` - Disable PM guard\n"
        result += f"• `.setlimit <number>` - Set warning limit\n"
        result += f"• `.allow` - Allow user (use in PM)\n"
        result += f"• `.deny` - Deny user (use in PM)"
        
        await message.edit(result)
        
    except Exception as e:
        await message.edit(f"**Error checking PM status:** `{str(e)}`")


@Client.on_message(filters.command("testpmguard", ".") & filters.me)
async def test_pm_guard(client: Client, message: Message):
    await message.edit("**Testing PM Guard functionality...**")
    
    try:
        from Zefron.database.pmpermitdb import get_pm_settings, get_approved_users, pm_guard
        from Zefron.modules.private.pmguard import denied_users, USERS_AND_WARNS
        
        result = f"**PM Guard Test Results:**\n\n"
        
        # Test PM guard status
        pm_enabled = await pm_guard()
        result += f"**PM Guard Enabled:** {'✅ Yes' if pm_enabled else '❌ No'}\n"
        
        # Test PM settings
        pm_settings = await get_pm_settings()
        if pm_settings is False:
            result += f"**PM Settings:** ❌ Not initialized\n"
        else:
            pmpermit, permit_msg, limit, block_msg = pm_settings
            result += f"**PM Settings:** ✅ Initialized\n"
            result += f"**Warning Limit:** {limit}\n"
        
        # Test approved users
        approved_users = await get_approved_users()
        result += f"**Approved Users:** {len(approved_users)}\n"
        
        # Test current user status
        current_user_id = message.chat.id
        is_approved = current_user_id in approved_users
        result += f"**Current User Approved:** {'✅ Yes' if is_approved else '❌ No'}\n"
        
        # Test denied_users filter
        try:
            # Create a mock message for testing
            class MockMessage:
                def __init__(self, chat_id):
                    self.chat = type('Chat', (), {'id': chat_id})()
            
            mock_msg = MockMessage(current_user_id)
            should_deny = await denied_users(None, client, mock_msg)
            result += f"**Filter Test:** {'🚫 Would deny' if should_deny else '✅ Would allow'}\n"
        except Exception as e:
            result += f"**Filter Test:** ❌ Error: {str(e)}\n"
        
        # Show warning counts
        result += f"\n**Current Warning Counts:**\n"
        if USERS_AND_WARNS:
            for user_id, warns in list(USERS_AND_WARNS.items())[:5]:
                result += f"• User {user_id}: {warns} warnings\n"
        else:
            result += "• No users have warnings\n"
        
        result += f"\n**Current Chat:** {message.chat.title} (`{message.chat.id}`)\n"
        
        # Add troubleshooting tips
        result += f"\n**🔧 Troubleshooting:**\n"
        if not pm_enabled:
            result += "• PM Guard is disabled - use `.pmguard on`\n"
        if pm_settings is False:
            result += "• PM settings not initialized - use `.pmguard on`\n"
        if is_approved:
            result += "• Current user is approved - won't trigger warnings\n"
        else:
            result += "• Current user is not approved - should trigger warnings\n"
        
        await message.edit(result)
        
    except Exception as e:
        await message.edit(f"**Error testing PM guard:** `{str(e)}`")


add_command_help(
    "start",
    [
        [".alive", "Check if the bot is alive or not."],
        [".repo", "Display the repo of this userbot."],
        [".creator", "Show the creator of this userbot."],
        [".id", "Send id of what you replied to."],
        [".up `or` .uptime", "Check bot's current uptime."],
    ],
)

add_command_help(
    "restart",
    [
        [".restart", "Restart the Zefron Userbot."],
    ],
)

add_command_help(
    "logger",
    [
        [".testlogger", "Test logger functionality."],
        [".pmstatus", "Check PM Guard status and settings."],
        [".testpmguard", "Test PM Guard functionality and debug issues."],
    ],
)
