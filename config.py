

import os

# Login feature, if you want then True , if you don't want then False
LOGIN_SYSTEM = bool(os.environ.get('LOGIN_SYSTEM', True)) # True or False

if LOGIN_SYSTEM == False:
    # if login system is False then fill your tg account session below 
    STRING_SESSION = os.environ.get("STRING_SESSION", "")
else:
    STRING_SESSION =1BVtsOHYBuwx-yNsL_WjHHf6U5MVokGunIDcx0O-1mfR8lBRfCBA4vXvwIz73Aqn2pQjKogkgCnXvmFBRpFAWJgyo_RRZ3mqcFzNJM3vheaP4sE3p4Se0d2hyliGt-JZWqetv9OkXakdOOAsIvqrDwJh--YXXMLJgQKTGhKLcp57Xui01yIdGE-nF6LtySB9cP-CYJL7kz7Sd1_8iRVriL5zanRJhQzGkKKJG2ibpT5s4sdV2uoyuHoNmaRnt12wKPzWPafqGubTeqi12qyNgIh_5GJjbYSM9Uzq-_kYoErBxO_3ZtAQd_BdgjNhDUCuGNi2rXJQtJTuiL6FRT4YaJkOyzDGJJaE=

# Bot token @Botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN","8983611509:AAGURaQ5d3UOV4ifDm_y9HP7M0i9MXF7xF4")

# Your API ID from my.telegram.org
API_ID = int(os.environ.get("API_ID", "33016948"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "0d86424aba3761436da03c5331c38509")

# Your Owner / Admin Id For Broadcast 
ADMINS = int(os.environ.get("ADMINS", "6863647592"))

# Your Channel Id In Which Bot Upload Downloaded Video/File/Message etc.
# And Make Your Bot Admin In this channel with full rights.
# if you don't want to upload in channel then leave it blank don't fill anything.
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")

# Your Mongodb Database Url
# Warning - Give Db uri in deploy server environment variable, don't give in repo.
DB_URI = os.environ.get("DB_URI", "") # Warning - Give Db uri in deploy server environment variable, don't give in repo.
DB_NAME = os.environ.get("DB_NAME", "Abhisavecontentbot")

# Increase time as much as possible to avoid floodwait, spamming and tg account ban issues.
WAITING_TIME = int(os.environ.get("WAITING_TIME", "10")) # time in seconds

# If You Want Error Message In Your Personal Message Then Turn It True Else If You Don't Want Then Flase
ERROR_MESSAGE = bool(os.environ.get('ERROR_MESSAGE', True))
