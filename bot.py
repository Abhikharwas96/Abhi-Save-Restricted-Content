import os
from pyrogram import Client, filters

# Environment variables se credentials lena
API_ID = int(os.environ.get("33016948"))
API_HASH = os.environ.get("0d86424aba3761436da03c5331c38509")
BOT_TOKEN = os.environ.get("8983611509:AAGURaQ5d3UOV4ifDm_y9HP7M0i9MXF7xF4")

app = Client("restricted_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! Mujhe restricted channel ka post link bhejo, main content nikal kar dunga.")

@app.on_message(filters.text & filters.private)
async def clone_content(client, message):
    text = message.text
    if "t.me/" not in text:
        await message.reply_text("Kripya ek valid Telegram link bhejein.")
        return

    msg = await message.reply_text("Processing...")
    try:
        # Link se chat_id aur message_id nikalna
        parts = text.split('/')
        message_id = int(parts[-1])
        chat_share_url = parts[-2]
        
        # Restricted content ko copy/forward karna
        await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=chat_share_url,
            message_id=message_id
        )
        await msg.delete()
    except Exception as e:
        await msg.edit(f"Error: {str(e)}\n\n(Note: Agar channel private hai toh bot ka wahan hona zaroori hai.)")

app.run()


