import os
from threading import Thread
from flask import Flask
from pyrogram import Client, filters

# --- Flask Server (Render ke Free Tier ke liye zaroori hai) ---
flask_app = Flask(name)

@flask_app.route('/')
def home():
    return "Bot is Running Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# --- Aapka Telegram Bot Code ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("restricted_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! Mujhe restricted channel ka post link bhejo.")

@app.on_message(filters.text & filters.private)
async def clone_content(client, message):
    text = message.text
    if "t.me/" not in text:
        await message.reply_text("Valid link bhejein.")
        return

    msg = await message.reply_text("Processing...")
    try:
        parts = text.split('/')
        message_id = int(parts[-1])
        chat_share_url = parts[-2]
        
        if chat_share_url.isdigit() or chat_share_url.startswith("-100"):
            chat_id = int(f"-100{chat_share_url.replace('c/', '')}")
        else:
            chat_id = chat_share_url

        await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=chat_id,
            message_id=message_id
        )
        await msg.delete()
    except Exception as e:
        await msg.edit(f"Error: {str(e)}")

if name == "main":
    # Flask ko background me chalana taaki Render ise block na kare
    Thread(target=run_flask).start()
    app.run()

