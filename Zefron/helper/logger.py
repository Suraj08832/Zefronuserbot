import asyncio
from pyrogram import Client, enums
from config import LOG_GROUP, PM_LOGGER


async def validate_logger_group(client: Client, logger_id: str) -> bool:
    """Validate if the logger group exists and userbot has access"""
    if not logger_id or logger_id == "None":
        return False
    
    try:
        # Convert string to int if needed
        if isinstance(logger_id, str):
            logger_id = int(logger_id)
        
        # Try to get chat information
        chat = await client.get_chat(logger_id)
        print(f"Logger group validation successful: {chat.title} ({chat.id})")
        return True
    except Exception as e:
        print(f"Logger group validation failed for {logger_id}: {e}")
        return False


async def send_to_logger(client: Client, message: str, logger_id: str, parse_mode=enums.ParseMode.MARKDOWN):
    """Send message to logger with proper error handling"""
    if not logger_id or logger_id == "None":
        print(f"Logger Error: Invalid logger_id - {logger_id}")
        return False
    
    try:
        # Convert string to int if needed
        if isinstance(logger_id, str):
            logger_id = int(logger_id)
        
        print(f"Attempting to send message to logger: {logger_id}")
        
        # Validate the logger group first
        if not await validate_logger_group(client, logger_id):
            print(f"Logger group {logger_id} is not accessible")
            return False
        
        await client.send_message(
            chat_id=logger_id,
            text=message,
            parse_mode=parse_mode,
            disable_web_page_preview=True
        )
        print(f"Successfully sent message to logger: {logger_id}")
        return True
    except Exception as e:
        print(f"Logger Error for {logger_id}: {e}")
        return False


async def log_pm(client: Client, message, user_mention: str = None, is_approved: bool = None):
    """Log PM messages to PM_LOGGER"""
    print(f"PM_LOGGER value: {PM_LOGGER}")
    
    if not PM_LOGGER or PM_LOGGER == "None":
        print("PM_LOGGER not set or invalid")
        return False
    
    if not user_mention:
        user_mention = message.from_user.mention
    
    # Create log message with approval status
    log_message = f"**📨 PM from {user_mention}:**\n"
    log_message += f"**User ID:** `{message.from_user.id}`\n"
    log_message += f"**Username:** @{message.from_user.username or 'None'}\n"
    
    # Add approval status if provided
    if is_approved is not None:
        status_emoji = "✅" if is_approved else "❌"
        status_text = "Approved" if is_approved else "Not Approved"
        log_message += f"**Status:** {status_emoji} {status_text}\n"
    
    log_message += f"**Message:** {message.text or 'No text'}"
    
    print(f"Logging PM message to {PM_LOGGER}")
    return await send_to_logger(client, log_message, PM_LOGGER)


async def log_tag(client: Client, message, group_title: str = None):
    """Log tag mentions to LOG_GROUP"""
    print(f"LOG_GROUP value: {LOG_GROUP}")
    
    if not LOG_GROUP or LOG_GROUP == "None":
        print("LOG_GROUP not set or invalid")
        return False
    
    if not group_title:
        group_title = message.chat.title
    
    result = f"<b>📨 #TAGS #MESSAGE</b>\n<b> • User : </b>{message.from_user.mention}"
    result += f"\n<b> • Group : </b>{group_title}"
    result += f"\n<b> • 👀 </b><a href = '{message.link}'>Lihat Pesan</a>"
    result += f"\n<b> • Message : </b><code>{message.text}</code>"
    
    print(f"Logging tag message to {LOG_GROUP}")
    return await send_to_logger(client, result, LOG_GROUP, enums.ParseMode.HTML)


async def log_action(client: Client, action: str, details: str, logger_id: str = None):
    """Log general actions to specified logger or LOG_GROUP"""
    if not logger_id:
        logger_id = LOG_GROUP
    
    log_message = f"**🔔 {action}**\n{details}"
    
    return await send_to_logger(client, log_message, logger_id)


async def log_error(client: Client, error: str, context: str = "", logger_id: str = None):
    """Log errors to specified logger or LOG_GROUP"""
    if not logger_id:
        logger_id = LOG_GROUP
    
    log_message = f"**❌ ERROR**\n**Context:** {context}\n**Error:** `{error}`"
    
    return await send_to_logger(client, log_message, logger_id) 