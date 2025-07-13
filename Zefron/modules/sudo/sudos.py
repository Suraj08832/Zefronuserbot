from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message
from Zefron.helper.PyroHelpers import get_ub_chats
from Zefron.modules.basic.profile import extract_user, extract_user_and_reason
from Zefron import SUDO_USER
from config import OWNER_ID
from Zefron.modules.help import add_command_help

ok = []
DEVS = int(1669178360)

# Initialize SUDO_USER if it's empty
if not SUDO_USER:
    SUDO_USER = []


@Client.on_message(filters.command("sudolist", ".") & filters.me)
async def sudolist(client: Client, message: Message):
    """Show list of sudo users"""
    try:
        print(f"SUDO_USER: {SUDO_USER}")
        print(f"OWNER_ID: {OWNER_ID}")
        
        if not SUDO_USER:
            await message.edit("**No Sudo Users Found!**\n\n**To add sudo users:**\n• Set SUDO_USERS in config.py\n• Or use `.addsudo` command")
            return
        
        sudo_list = "**🔐 Sudo Users List:**\n\n"
        count = 0
        
        for user_id in SUDO_USER:
            count += 1
            try:
                user = await client.get_users(user_id)
                sudo_list += f"**{count}.** [{user.first_name}](tg://user?id={user_id}) (`{user_id}`)\n"
            except Exception as e:
                sudo_list += f"**{count}.** Unknown User (`{user_id}`) - Error: {e}\n"
        
        sudo_list += f"\n**Total Sudo Users:** {count}"
        await message.edit(sudo_list)
        
    except Exception as e:
        await message.edit(f"**Error showing sudo list:** `{str(e)}`")


@Client.on_message(filters.command("addsudo", ".") & filters.user(OWNER_ID))
async def add_sudo(client: Client, message: Message):
    """Add a user to sudo list (Owner only)"""
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
            await ex.edit("**❌ Please specify a valid user!**\n\n**Usage:**\n• `.addsudo @username`\n• `.addsudo 123456789`\n• Reply to a user with `.addsudo`")
            return
        
        if user.id == client.me.id:
            return await ex.edit("**🤖 You can't add yourself as sudo!**")
        
        if user.id == OWNER_ID:
            return await ex.edit("**👑 Owner is already a sudo user!**")
        
        # Initialize SUDO_USER if it's empty
        if not SUDO_USER:
            SUDO_USER.clear()
        
        if user.id in SUDO_USER:
            return await ex.edit(f"**❌ [{user.first_name}](tg://user?id={user.id}) is already a sudo user!**")
        
        SUDO_USER.append(user.id)
        print(f"Added {user.id} to SUDO_USER: {SUDO_USER}")
        
        await ex.edit(f"**✅ [{user.first_name}](tg://user?id={user.id}) has been added to sudo users!**\n\n**User ID:** `{user.id}`")
        
    except Exception as e:
        await ex.edit(f"**❌ Error adding sudo user:** `{str(e)}`")


@Client.on_message(filters.command("rmsudo", ".") & filters.user(OWNER_ID))
async def remove_sudo(client: Client, message: Message):
    """Remove a user from sudo list (Owner only)"""
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
            await ex.edit("**❌ Please specify a valid user!**\n\n**Usage:**\n• `.rmsudo @username`\n• `.rmsudo 123456789`\n• Reply to a user with `.rmsudo`")
            return
        
        if user.id == client.me.id:
            return await ex.edit("**🤖 You can't remove yourself!**")
        
        if user.id == OWNER_ID:
            return await ex.edit("**👑 Owner cannot be removed from sudo!**")
        
        if user.id not in SUDO_USER:
            return await ex.edit(f"**❌ [{user.first_name}](tg://user?id={user.id}) is not a sudo user!**")
        
        SUDO_USER.remove(user.id)
        print(f"Removed {user.id} from SUDO_USER: {SUDO_USER}")
        
        await ex.edit(f"**✅ [{user.first_name}](tg://user?id={user.id}) has been removed from sudo users!**")
        
    except Exception as e:
        await ex.edit(f"**❌ Error removing sudo user:** `{str(e)}`")


@Client.on_message(filters.command("testsudo", ".") & filters.me)
async def test_sudo(client: Client, message: Message):
    """Test sudo functionality"""
    try:
        current_user_id = message.from_user.id
        is_owner = current_user_id == OWNER_ID
        is_sudo = current_user_id in SUDO_USER
        
        result = "**🔐 Sudo Test Results:**\n\n"
        result += f"**Your ID:** `{current_user_id}`\n"
        result += f"**Owner ID:** `{OWNER_ID}`\n"
        result += f"**Is Owner:** {'✅ Yes' if is_owner else '❌ No'}\n"
        result += f"**Is Sudo:** {'✅ Yes' if is_sudo else '❌ No'}\n"
        result += f"**SUDO_USER List:** `{SUDO_USER}`\n\n"
        
        if is_owner or is_sudo:
            result += "**✅ You can use sudo commands!**\n"
        else:
            result += "**❌ You cannot use sudo commands!**\n"
        
        result += "\n**Available Sudo Commands:**\n"
        result += "• `.sudolist` - Show sudo users\n"
        result += "• `.addsudo` - Add sudo user (Owner only)\n"
        result += "• `.rmsudo` - Remove sudo user (Owner only)\n"
        result += "• `.testsudo` - Test sudo access\n"
        
        await message.edit(result)
        
    except Exception as e:
        await message.edit(f"**❌ Error testing sudo:** `{str(e)}`")


add_command_help(
    "sudos",
    [
        [
            "addsudo <reply/username/userid>",
            "Add any user as Sudo (Owner only).",
        ],
        ["rmsudo <reply/username/userid>", "Remove Sudo access (Owner only)."],
        ["sudolist", "Displays the Sudo List."],
        ["testsudo", "Test sudo functionality."],
    ],
)
