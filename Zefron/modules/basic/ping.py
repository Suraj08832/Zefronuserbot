import time
from datetime import datetime

import speedtest
from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from Zefron import StartTime, app, SUDO_USER
from Zefron.helper.PyroHelpers import SpeedConvert
from Zefron.modules.bot.inline import get_readable_time

from Zefron.modules.help import add_command_help

class WWW:
    SpeedTest = (
        "Speedtest started at `{start}`\n\n"
        "Ping:\n{ping} ms\n\n"
        "Download:\n{download}\n\n"
        "Upload:\n{upload}\n\n"
        "ISP:\n__{isp}__"
    )

    NearestDC = "Country: `{}`\n" "Nearest Datacenter: `{}`\n" "This Datacenter: `{}`"

@Client.on_message(
    filters.command(["speedtest"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def speed_test(client: Client, message: Message):
    new_msg = await message.reply_text("`Running speed test . . .`")
    try:
       await message.delete()
    except:
       pass
    spd = speedtest.Speedtest()

    try:
        new_msg = await new_msg.edit(
            f"`{new_msg.text}`\n" "`Getting best server based on ping . . .`"
        )
    except:
        pass
    spd.get_best_server()

    try:
        new_msg = await new_msg.edit(f"`{new_msg.text}`\n" "`Testing download speed . . .`")
    except:
        pass
    spd.download()

    try:
        new_msg = await new_msg.edit(f"`{new_msg.text}`\n" "`Testing upload speed . . .`")
    except:
        pass
    spd.upload()

    try:
        new_msg = await new_msg.edit(
            f"`{new_msg.text}`\n" "`Getting results and preparing formatting . . .`"
        )
    except:
        pass
    results = spd.results.dict()

    try:
        await new_msg.edit(
            WWW.SpeedTest.format(
                start=results["timestamp"],
                ping=results["ping"],
                download=SpeedConvert(results["download"]),
                upload=SpeedConvert(results["upload"]),
                isp=results["client"]["isp"],
            )
        )
    except Exception as e:
        # If editing fails, send a new message
        await message.reply_text(
            WWW.SpeedTest.format(
                start=results["timestamp"],
                ping=results["ping"],
                download=SpeedConvert(results["download"]),
                upload=SpeedConvert(results["upload"]),
                isp=results["client"]["isp"],
            )
        )



@Client.on_message(
    filters.command(["ping"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def pingme(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    xx = await message.reply_text("**0% ▒▒▒▒▒▒▒▒▒▒**")
    try:
       await message.delete()
    except:
       pass
    
    # Add error handling for message editing
    try:
        await xx.edit("**20% ██▒▒▒▒▒▒▒▒**")
    except:
        pass
    try:
        await xx.edit("**40% ████▒▒▒▒▒▒**")
    except:
        pass
    try:
        await xx.edit("**60% ██████▒▒▒▒**")
    except:
        pass
    try:
        await xx.edit("**80% ████████▒▒**")
    except:
        pass
    try:
        await xx.edit("**100% ██████████**")
    except:
        pass
    
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    
    try:
        await xx.edit(
            f"❏ **╰☞ 𝗣𝗢𝗡𝗚™╮**\n"
            f"├• **╰☞** - `%sms`\n"
            f"├• **╰☞ -** `{uptime}` \n"
            f"└• **╰☞:** {client.me.mention}" % (duration)
        )
    except Exception as e:
        # If editing fails, send a new message
        await message.reply_text(
            f"❏ **╰☞ 𝗣𝗢𝗡𝗚™╮**\n"
            f"├• **╰☞** - `%sms`\n"
            f"├• **╰☞ -** `{uptime}` \n"
            f"└• **╰☞:** {client.me.mention}" % (duration)
        )


add_command_help(
    "ping",
    [
        ["ping", "Check bot alive or not."],
    ],
)
