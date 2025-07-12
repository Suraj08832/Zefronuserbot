from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import Telegraph, exceptions, upload_file
import os
from typing import Optional

from Zefron.modules.help import *
from Zefron.helper.PyroHelpers import convert_to_image

telegraph = Telegraph()
# Remove the account creation during import to avoid network issues
# r = telegraph.create_account(short_name="telegram")
# auth_url = r["auth_url"]

# Global variable to store the account info
_telegraph_account = None

def get_telegraph_account():
    """Get or create telegraph account lazily"""
    global _telegraph_account
    if _telegraph_account is None:
        try:
            _telegraph_account = telegraph.create_account(short_name="telegram")
        except Exception as e:
            print(f"Failed to create telegraph account: {e}")
            _telegraph_account = None
    return _telegraph_account

def get_text(message: Message) -> Optional[str]:
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

@Client.on_message(filters.command(["tg", "telegraph", "tm", "tgt"], ".") & filters.me)
async def uptotelegraph(client: Client, message: Message):
    tex = await message.edit_text("`Processing . . .`")
    
    # Get telegraph account when needed
    account = get_telegraph_account()
    if not account:
        await tex.edit("**Failed to initialize Telegraph account. Please try again later.**")
        return
    
    if not message.reply_to_message:
        await tex.edit(
            "**Reply to an Image or text.**"
        )
        return
    if message.reply_to_message.media:
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await tex.edit(f"**ERROR:** `{exc}`")
            os.remove(m_d)
            return
        U_done = (
            f"**Uploaded on ** [Telegraph](https://telegra.ph/{media_url[0]})"
        )
        await tex.edit(U_done)
        os.remove(m_d)
    elif message.reply_to_message.text:
        page_title = get_text(message) if get_text(message) else client.me.first_name
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await tex.edit(f"**ERROR:** `{exc}`")
            return
        wow_graph = f"**Uploaded as** [Telegraph](https://telegra.ph/{response['path']})"
        await tex.edit(wow_graph)


add_command_help(
    "telegraph",
    [
        [
            f"telegraph `or` .tg",
            "To upload on telegraph.",
        ],
    ],
)
