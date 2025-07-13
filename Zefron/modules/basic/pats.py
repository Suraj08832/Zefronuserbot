import asyncio

import aiohttp
from pyrogram import filters, Client
from pyrogram.types import Message


from Zefron.helper.PyroHelpers import GetChatID, ReplyCheck
from Zefron.modules.help import add_command_help


@Client.on_message(filters.command(["pat", "pats"], ".") & filters.me)
async def give_pats(bot: Client, message: Message):
    # Updated to use a working API
    URL = "https://api.waifu.pics/sfw/pat"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as request:
                if request.status == 404:
                    return await message.edit("`no Pats for you :c`")
                result = await request.json()
                url = result.get("url", None)
                if not url:
                    return await message.edit("`Failed to get pat gif`")
                await asyncio.gather(
                    message.delete(),
                    bot.send_video(
                        GetChatID(message), url, reply_to_message_id=ReplyCheck(message)
                    ),
                )
    except Exception as e:
        await message.edit(f"`Error: {str(e)}`")


add_command_help(
    "pats",
    [
        [".pat | .pats", "Give pats."],
    ],
)
