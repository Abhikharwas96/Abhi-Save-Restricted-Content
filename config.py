import os

API_ID = int(os.environ.get("API_ID",33016948)  
API_HASH = os.environ.get("API_HASH", "0d86424aba3761436da03c5331c38509")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8983611509:AAGURaQ5d3UOV4ifDm_y9HP7M0i9MXF7xF4")

# Temporary dict to store user sessions in memory
user_sessions = {}
