import asyncio
from pyrogram import Client, enums, filters 
from pyrogram.types import Message 
from config import LOG_GROUP
from Zefron.modules.help import add_command_help
from Zefron.helper.logger import log_tag

log = []


@Client.on_message(filters.command("tagalert on", ".") & filters.me)
async def set_no_log_p_m(client: Client, message: Message):
    if LOG_GROUP and LOG_GROUP != "-100":
        if not message.chat.id in log:
            log.append(message.chat.id)
            await message.edit("**Tag alert Activated Successfully**")
        else:
            await message.edit("**Tag alert is already active in this chat**")
    else:
        await message.edit("**Please set LOG_GROUP in config to use tag alert**")


@Client.on_message(filters.command("tagalert off", ".") & filters.me)
async def set_no_log_p_m(client: Client, message: Message):
    if message.chat.id in log:
        log.remove(message.chat.id)
        await message.edit("**Tag alert Deactivated Successfully**")
    else:
        await message.edit("**Tag alert is not active in this chat**")


if log:
 @Client.on_message(filters.group & filters.mentioned & filters.incoming)
 async def log_tagged_messages(client: Client, message: Message):
    if message.chat.id not in log:
        return
        
    await asyncio.sleep(0.5)
    await log_tag(client, message)


add_command_help(
    "tagalert",
    [
        [
            "tagalert on/off",
            "To activate or deactivate the group tag, which will go to the log group.",
        ],
    ],
)
