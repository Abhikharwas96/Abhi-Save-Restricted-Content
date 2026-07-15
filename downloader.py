import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from config import user_sessions

# Ek waqt mein maximum 3 downloads chalenge takki account ban ya limit na ho
DOWNLOAD_SEMAPHORE = asyncio.Semaphore(3)

def parse_tg_link(link: str):
    parts = link.strip().split('/')
    msg_id = int(parts[-1])
    chat_id = parts[-2]
    if chat_id.isdigit():
        chat_id = int(f"-100{chat_id}")
    return chat_id, msg_id

# Safe downloader function jo speed handle karta hai
async def safe_download_upload(bot: Client, user_client: Client, chat_id: int, msg_id: int, user_id: int):
    async with DOWNLOAD_SEMAPHORE: # Sirf 3 tasks ek sath chalenge, baki queue mein rahenge
        file_path = None
        try:
            msg = await user_client.get_messages(chat_id, msg_id)
            if not msg or msg.empty:
                return

            if msg.media:
                # Downloader speed badhane ke liye chunk size Pyrogram internally manage karta hai
                file_path = await user_client.download_media(
                    msg,
                    block=True # Background process block na ho
                )
                
                # Fast upload directly back to the user
                await bot.send_document(chat_id=user_id, document=file_path)
                
                # Space bachane ke liye download hone ke baad file delete karna
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
            elif msg.text:
                await bot.send_message(chat_id=user_id, text=msg.text)

        except FloodWait as e:
            # Agar Telegram block kare, to ye automatically wait karega aur phir resume karega
            print(f"⚠️ Rate limit hit! Sleeping for {e.value} seconds...")
            await asyncio.sleep(e.value)
            await safe_download_upload(bot, user_client, chat_id, msg_id, user_id) # Retry
        except Exception as e:
            print(f"❌ Error processing message {msg_id}: {str(e)}")
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

async def init_download_handlers(bot: Client):

    @bot.on_message(filters.command("start") & filters.private)
    async def start(client, message: Message):
        await message.reply_text(
            "⚡ Super Fast Restricted Downloader Bot ⚡\n\n"
            "1. /login - Pehle apna account login karein.\n"
            "2. Send Single Link - Direct download start ho jayega.\n"
            "3. /batch start_link end_link - Fast parallel batch downloading ke liye."
        )

    # Single Link (Fast Queue)
    @bot.on_message(filters.regex(r"https://t\.me/") & filters.private)
    async def single_link_downloader(client, message: Message):
        user_id = message.from_user.id
        if user_id not in user_sessions:
            return await message.reply_text("🔒 Pehle /login karein.")
        
        user_client = user_sessions[user_id]
        try:
            chat_id, msg_id = parse_tg_link(message.text)
            await message.reply_text("📥 Download queue mein add ho gaya hai...")
            
            # Background mein run hoga, user ko wait nahi karna padega
            asyncio.create_task(safe_download_upload(bot, user_client, chat_id, msg_id, user_id))
        except Exception as e:
            await message.reply_text(f"❌ Link error: {str(e)}")

    # Super Fast Batch Downloader (Parallel Processing)
    @bot.on_message(filters.command("batch") & filters.private)
    async def batch_downloader(client, message: Message):
        user_id = message.from_user.id
        if user_id not in user_sessions:
            return await message.reply_text("🔒 Pehle /login karein.")
            
        args = message.text.split()
        if len(args) < 3:
            return await message.reply_text("Format: /batch start_link end_link")
            
        start_link, end_link = args[1], args[2]
        user_client = user_sessions[user_id]
        
        try:chat_id, start_id = parse_tg_link(start_link)
            _, end_id = parse_tg_link(end_link)
            
            await message.reply_text(f"🚀 Batch processing started for messages {start_id} to {end_id}!")
            
            # Saare tasks ko ek sath load karna (Parallel Processing)
            tasks = []
            for m_id in range(start_id, end_id + 1):
                tasks.append(safe_download_upload(bot, user_client, chat_id, m_id, user_id))
                # Halaki tasks parallel hain, par har request ke beech halka gap zaroori h takki crash na ho
                await asyncio.sleep(0.1) 
            
            # Saare tasks ko ek sath run karna (Semaphore handle karega ki ek sath sirf 3 hi active hon)
            asyncio.create_task(asyncio.gather(*tasks))
            
        except Exception as e:
            await message.reply_text(f"❌ Batch Error: {str(e)}")
