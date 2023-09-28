import re
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
PORT = environ.get("PORT", "8080")
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 9999))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS' ,'https://telegra.ph/file/79bd83439254ed9c4bbca.jpg')).split()
NOR_IMG = environ.get('NOR_IMG', "https://graph.org/file/ebecf2e8bd05f866ea862.jpg")
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "6"))
START_MESSAGE = environ.get('START_MESSAGE', '🥀Hᴇʟʟᴏ{user},\nNɪᴄᴇ Tᴏ Mᴇᴇᴛ Yᴏᴜ👀\n\nI Cᴀɴ Pʀᴏᴠɪᴅᴇ Mᴏᴠɪᴇs Aɴᴅ WEB-Sᴇʀɪᴇs Fᴏʀ Yᴏᴜ Jᴜsᴛ Mᴀᴋᴇ Tᴏ Aᴅᴍɪɴ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Uᴇs Mᴇ..💫\n\n🍃Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ : : <a href=https://t.me/copycod_Official>CopyCode™ [#Official] 🇮🇳</a>')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "📣 ʜᴇʏ {query}! ᴛʜᴀᴛ's ɴᴏᴛ ғᴏʀ ʏᴏᴜ. ᴘʟᴇᴀsᴇ ʀᴇϙᴜᴇsᴛ ʏᴏᴜʀ ᴍᴏᴠɪᴇ")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', 'Fɪʀsᴛ ᴄʟɪᴄᴋ ᴏɴ Rᴇǫᴜᴇꜱᴛ Tᴏ Jᴏɪɴ Cʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ . ᴛʜᴇɴ ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴄʟɪᴄᴋ ᴏɴ ᴍᴇ ᴊᴏɪɴᴇᴅ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇ...')
WELCOM_PIC = environ.get("WELCOM_PIC", "https://telegra.ph/file/a54075479d67bf0125792.jpg")
WELCOM_TEXT = environ.get("WELCOM_TEXT", "<b>🥀 Hᴇʏ {user},\n💥 Wᴇʟᴄᴏᴍᴇ Tᴏ › {chat}\n\n💞 Tʜᴀɴᴋ 𖨆 Yᴏᴜ Fᴏʀ Jᴏɪɴ</b>")
PMFILTER = bool(environ.get("PMFILTER", True))
G_FILTER = bool(environ.get("G_FILTER", True))
BUTTON_LOCK = bool(environ.get("BUTTON_LOCK", True))

# Others
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '0').split()]
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "9999"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'copycod_Official')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
IMDB = is_enabled((environ.get('IMDB', "False")), False)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>🗃ғɪʟᴇ ɴᴀᴍᴇ</b> : <b><code>{file_name}</code></b><b>\n\n╭────── • ◆ • ──────╮\n📮Join :[ᴄʜᴀɴɴᴇʟ](https://t.me/cinema_flix_updates)\n🔖 ᴍᴏᴠɪᴇs :[ɢʀᴏᴜᴘ](https://t.me/+iEbhY7mM4oE1OTVl)\n╰────── • ◆ • ──────╯</b>\n🎗 ʝσιи • ѕнαяє • ѕυρρσят 🎗<b>\n\n🌿ғɪʟᴇ sɪᴢᴇ</b> : <b><i>{file_size}</i></b>")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", None)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Title </b> :<code>{title}</code>\n<b>Rating :</b> {rating}</a> / 10\n<b>Genres :</b>{genres}")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

#log srt
LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"


