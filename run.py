# run.py
# Telegram botni ishga tushiruvchi asosiy fayl

# Asinxron dasturlash uchun kerakli modul
import asyncio

# Log (xatolik va holatlar)ni ko‘rish uchun
import logging

# Aiogram kutubxonasidan bot va dispatcherlarni chaqiramiz
from aiogram import Bot, Dispatcher, F

# Start va oddiy buyruqlar uchun filterlar
from aiogram.filters import CommandStart, Command

# Xabar (message) obyektini ishlatish uchun
from aiogram.types import Message

# Bot tokeni saqlangan config faylidan TOKEN ni import qilamiz
from config import TOKEN


# Bot obyektini yaratamiz (Telegram bilan bog‘lanish uchun)
bot = Bot(token=TOKEN)

# Dispatcher — kelayotgan xabarlarni qabul qilib, kerakli handlerga yo‘naltiradi
dp = Dispatcher()


# /start buyrug‘i uchun handler
@dp.message(CommandStart())
async def cmd_start(message: Message):
    """
    Foydalanuvchi /start buyrug‘ini yuborganda ishlaydi.
    Bot salomlashadi va oddiy xabar yuboradi.
    """
    await message.answer('Assalomu alaykum\nNa gap?')


# /salom buyrug‘i uchun handler
@dp.message(Command('salom'))  # /salom
async def cmd_salom(message: Message):
    """
    Foydalanuvchi /salom deb yozsa,
    bot unga javob qaytaradi.
    """
    await message.reply('Vaaleykum Assalom!')


# Matn aniq "Assalomu alaykum" bo‘lsa ishlaydigan handler
@dp.message(F.text == 'Assalomu alaykum')
async def cmd_assalom(message: Message):
    """
    Agar foydalanuvchi oddiy matn sifatida
    'Assalomu alaykum' deb yozsa,
    bot javob qaytaradi.
    """
    await message.reply('Valeykum Assalom!')


# Asosiy asinxron funksiya
async def main():
    """
    Botni polling rejimida ishga tushiradi.
    Polling — Telegram serveridan doimiy yangilanishlarni olish usuli.
    """
    await dp.start_polling(bot)


# Fayl to‘g‘ridan-to‘g‘ri ishga tushirilganda ishlaydi
if __name__ == '__main__':

    # Log darajasini INFO qilib sozlaymiz
    logging.basicConfig(level=logging.INFO)

    try:
        # Asinxron main funksiyani ishga tushiramiz
        asyncio.run(main())

    except KeyboardInterrupt:
        # Ctrl + C bosilganda botni to'xtatish
        print("Siz klaviatura orqali dasturni to'xtatdingiz!\nGoodbye!")
