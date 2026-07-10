import asyncio
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession

# ================= CONFIGURATION =================
API_ID = 33016948  
API_HASH = "0d86424aba3761436da03c5331c38509"  
MY_DESTINATION = 8509692514       

# Render की एनवायरनमेंट सेटिंग्स से स्ट्रिंग उठाएगा (ज्यादा सुरक्षित तरीका)
STRING_SESSION = os.environ.get("STRING_SESSION")
# =================================================

# --- RENDER PORT BINDING FIX ---
class RenderHealthServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Python3 Userbot is Live and Running on Render!")
    def log_message(self, format, *args):
        return

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), RenderHealthServer)
    print(f"🌍 Web server active on port {port} for Render.")
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()
# --------------------------------------------------

if not STRING_SESSION:
    print("❌ ERROR: STRING_SESSION env variable is missing!")
    exit(1)

print("⚡ Starting Telethon Userbot via Python 3...")
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# Rule 1: Link Detection & Auto Join
@client.on(events.NewMessage(outgoing=True))
async def join_and_fetch(event):
    text = event.raw_text.strip()
    if "t.me" in text:
        await event.reply("🔄 Link detected! Joining channel...")
        try:
            chat = await client.get_entity(text)
            await client(functions.channels.JoinChannelRequest(channel=chat))
            await event.reply(f"✅ Joined: {chat.title}\n⏳ Fetching last 20 messages...")
            
            async for msg in client.iter_messages(chat, limit=20):
                try:
                    await client.send_message(MY_DESTINATION, msg)
                    await asyncio.sleep(1)
                except Exception:
                    pass
            await event.reply("✨ Done!")
        except Exception as e:
            await event.reply(f"❌ Error while joining: {e}")

# Rule 2: Instant Auto Forward
@client.on(events.NewMessage)
async def auto_forward(event):
    if event.is_private:
        return
    try:
        if event.chat_id == MY_DESTINATION:
            return
        await client.send_message(MY_DESTINATION, event.message)
    except Exception:
        pass

if name == "main":
    with client:
        print("🚀 Userbot is now Online 24/7 on Render!")
        client.run_until_disconnected()
