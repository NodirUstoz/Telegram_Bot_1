# config.py
# Bu faylda bot uchun muhim sozlamalar saqlanadi
import os

# TOKEN — Telegram botning maxfiy kaliti
# Bu token orqali bot Telegram serverlari bilan bog'lanadi
# Token environment variable dan olinadi (xavfsizlik uchun)

TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable o'rnatilmagan!")
