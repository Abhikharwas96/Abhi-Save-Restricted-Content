from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, user_sessions

async def init_auth_handlers(bot: Client):

    @bot.on_message(filters.command("login") & filters.private)
    async def login_handler(client, message: Message):
        user_id = message.from_user.id
        
        # Phone number maangna
        phone_number_msg = await message.chat.ask("Please send your phone number with country code (e.g., +919876543210):")
        phone_number = phone_number_msg.text.strip()
        
        try:
            # Naya user client create karna
            user_client = Client(f"session_{user_id}", api_id=API_ID, api_hash=API_HASH)
            await user_client.connect()
            
            # OTP bhejna
            code_info = await user_client.send_code(phone_number)
            
            otp_msg = await message.chat.ask("Enter the OTP received on Telegram:")
            otp = otp_msg.text.strip()
            
            # Sign in process
            await user_client.sign_in(phone_number, code_info.phone_code_hash, otp)
            
            # Session ko memory mein save karna
            user_sessions[user_id] = user_client
            await message.reply_text("✅ Login Successful! Ab aap links process kar sakte hain.")
            
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")

    @bot.on_message(filters.command("logout") & filters.private)
    async def logout_handler(client, message: Message):
        user_id = message.from_user.id
        if user_id in user_sessions:
            try:
                await user_sessions[user_id].disconnect()
                del user_sessions[user_id]
                await message.reply_text("🔒 Logged out successfully.")
            except Exception as e:
                await message.reply_text(f"Error during logout: {str(e)}")
        else:
            await message.reply_text("Aap pehle se logged out hain.")
