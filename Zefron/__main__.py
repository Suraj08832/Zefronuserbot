import asyncio
import importlib
from pyrogram import Client, idle
from Zefron.helper import join
from Zefron.modules import ALL_MODULES
from Zefron import clients, app, ids
# Import sync_raids_list for replyraid system
from Zefron.modules.spam.watcher import sync_raids_list

async def start_bot():
    await app.start()
    print("LOG: Founded Bot token Booting..")
    for all_module in ALL_MODULES:
        importlib.import_module("Zefron.modules" + all_module)
        print(f"Successfully Imported {all_module} 💥")
    # Sync replyraid list on startup
    await sync_raids_list()
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            await join(cli)
            print(f"Started {ex.first_name} 🔥")
            ids.append(ex.id)
        except Exception as e:
            print(f"{e}")
    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
