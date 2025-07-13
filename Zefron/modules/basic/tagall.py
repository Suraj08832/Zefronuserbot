from asyncio import sleep

from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired, FloodWait

from Zefron.helper.parser import mention_html
from Zefron.modules.help import add_command_help

spam_chats = []


def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

@Client.on_message(filters.command("tagall", ".") & filters.me)
async def mentionall(client: Client, message: Message):
    chat_id = message.chat.id
    direp = message.reply_to_message
    args = get_arg(message)
    
    if not direp and not args:
        return await message.edit("**Send me a message or reply to a message!**")
    
    # Check if user is admin in the chat
    try:
        member = await client.get_chat_member(chat_id, client.me.id)
        if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return await message.edit("**I need to be admin to tag all members!**")
    except Exception as e:
        return await message.edit(f"**Error checking permissions: {str(e)}**")
    
    await message.delete()
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    
    try:
        # Use the same approach as the everyone command
        kek = client.get_chat_members(chat_id)
        async for usr in kek:
            if not chat_id in spam_chats:
                break
            # Skip bots
            if usr.user.is_bot:
                continue
            usrnum += 1
            usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
            if usrnum == 5:
                if args:
                    txt = f"{args}\n\n{usrtxt}"
                    await client.send_message(chat_id, txt)
                elif direp:
                    await direp.reply(usrtxt)
                await sleep(2)
                usrnum = 0
                usrtxt = ""
    except ChatAdminRequired:
        await message.reply_text("**I need to be admin to tag all members!**")
    except FloodWait as e:
        await message.reply_text(f"**Flood wait: {e.value} seconds**")
    except Exception as e:
        await message.reply_text(f"**Error: {str(e)}**")
    finally:
        try:
            spam_chats.remove(chat_id)
        except:
            pass


@Client.on_message(filters.command("cancel", ".") & filters.me)
async def cancel_spam(client: Client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.edit("**It seems there is no tagall here.**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("**Cancelled.**")


add_command_help(
    "tagall",
    [
        [
            "tagall [text/reply ke chat]",
            "Tag all the members one by one",
        ],
        [
            "cancel",
            f"to stop .tagall",
        ],
    ],
)
