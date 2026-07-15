from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH
import asyncio

async def main():
    bot = Client(
        "bot_session",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
    
    # Handlers initialize karna
    from handlers.authentication import init_auth_handlers
    from handlers.downloader import init_download_handlers
    
    await init_auth_handlers(bot)
    await init_download_handlers(bot)
    
    print("⚡ Bot Started Successfully!")
    await bot.start()
    await asyncio.Event().wait()

if name == "main":
    asyncio.run(main())
