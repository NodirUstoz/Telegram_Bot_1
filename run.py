import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN

# Keyboards faylidan klaviaturalarni import qilamiz
from keyboards import (
    main_menu_keyboard,       # Asosiy menyu tugmalari
    settings_keyboard,        # Sozlamalar tugmalari
    contact_keyboard,         # Kontakt so'rash tugmalari
    inline_menu,              # Inline tugmalar
    links_keyboard,           # Havolalar tugmalari
    product_keyboard,         # Mahsulot tugmalari
    remove_keyboard,          # Klaviaturani olib tashlash
    create_confirm_keyboard,  # Tasdiqlash tugmalarini yaratuvchi funksiya
)

bot = Bot(token=TOKEN)
dp = Dispatcher()



# COMMAND HANDLERS (Buyruqlar)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """
    /start buyrug'iga javob.
    Asosiy menyu klaviaturasini ko'rsatadi.
    """
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n\n"
        f"Quyidagi tugmalardan birini tanlang:",
        reply_markup=main_menu_keyboard  # Reply keyboard qo'shamiz
    )


@dp.message(Command('salom'))
async def cmd_salom(message: Message):
    await message.reply('Vaaleykum Assalom!')


@dp.message(Command('help'))
async def cmd_help(message: Message):
    """
    /help buyrug'iga javob.
    Inline tugmalar bilan yordam ko'rsatadi.
    """
    await message.answer(
        "Sizga qanday yordam kerak?\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=links_keyboard  # Inline keyboard qo'shamiz
    )


@dp.message(Command('inline'))
async def cmd_inline(message: Message):
    """
    /inline buyrug'i - Inline tugmalarni ko'rsatish uchun.
    """
    await message.answer(
        "Bu xabarni baholang:",
        reply_markup=inline_menu
    )


@dp.message(Command('product'))
async def cmd_product(message: Message):
    """
    /product buyrug'i - Mahsulot tugmalarini ko'rsatish uchun.
    """
    await message.answer(
        "Mahsulot: iPhone 15 Pro\n"
        "Narxi: $999\n\n"
        "Miqdorni tanlang:",
        reply_markup=product_keyboard
    )


@dp.message(Command('contact'))
async def cmd_contact(message: Message):
    """
    /contact buyrug'i - Kontakt so'rash tugmalarini ko'rsatish.
    """
    await message.answer(
        "Iltimos, ma'lumotlaringizni yuboring:",
        reply_markup=contact_keyboard
    )


@dp.message(Command('remove'))
async def cmd_remove(message: Message):
    """
    /remove buyrug'i - Klaviaturani olib tashlash.
    """
    await message.answer(
        "Klaviatura olib tashlandi.",
        reply_markup=remove_keyboard
    )



# REPLY KEYBOARD HANDLERS (Tugma matnlariga javob)

# Reply keyboard bosilganda tugma matni xabar sifatida keladi
# Shuning uchun F.text filteri orqali ushlaymiz


@dp.message(F.text == 'Assalomu alaykum')
async def cmd_assalom(message: Message):
    await message.reply('Valeykum Assalom!')


@dp.message(F.text == "Biz haqimizda")
async def about_us(message: Message):
    """'Biz haqimizda' tugmasi bosilganda"""
    await message.answer(
        "Biz - zamonaviy IT kompaniyamiz.\n"
        "2020-yildan beri xizmat ko'rsatamiz."
    )


@dp.message(F.text == "Xizmatlar")
async def services(message: Message):
    """'Xizmatlar' tugmasi bosilganda"""
    await message.answer(
        "Bizning xizmatlarimiz:\n\n"
        "1. Web dasturlash\n"
        "2. Mobil ilovalar\n"
        "3. Telegram botlar\n"
        "4. IT konsalting"
    )


@dp.message(F.text == "Bog'lanish")
async def contact_info(message: Message):
    """'Bog'lanish' tugmasi bosilganda"""
    await message.answer(
        "Biz bilan bog'lanish:\n\n"
        "Tel: +998 90 123 45 67\n"
        "Email: info@example.com\n"
        "Telegram: @example_support"
    )


@dp.message(F.text == "Sozlamalar")
async def settings(message: Message):
    """'Sozlamalar' tugmasi bosilganda"""
    await message.answer(
        "Sozlamalar bo'limi:",
        reply_markup=settings_keyboard  # Yangi keyboard ko'rsatamiz
    )


@dp.message(F.text == "Orqaga")
async def back_to_main(message: Message):
    """'Orqaga' tugmasi bosilganda - asosiy menyuga qaytish"""
    await message.answer(
        "Asosiy menyu:",
        reply_markup=main_menu_keyboard
    )


@dp.message(F.text == "Bekor qilish")
async def cancel_action(message: Message):
    """'Bekor qilish' tugmasi bosilganda"""
    await message.answer(
        "Amal bekor qilindi.\nAsosiy menyu:",
        reply_markup=main_menu_keyboard
    )



# CALLBACK QUERY HANDLERS (Inline tugmalar uchun)

# Inline tugma bosilganda callback_query keladi
# Bu yerda callback_data orqali qaysi tugma bosilganini aniqlaymiz


@dp.callback_query(F.data == "like")
async def callback_like(callback: CallbackQuery):
    """
    'Like' inline tugmasi bosilganda.

    callback.answer() - Telegram'ga "javob oldim" deb signal beradi
    show_alert=True - Popup oyna chiqaradi
    """
    await callback.answer("Rahmat! Sizga yoqdi!", show_alert=True)

    # Xabarni tahrirlash (ixtiyoriy)
    await callback.message.edit_text(
        "Siz Like bosdingiz!",
        reply_markup=inline_menu  # Tugmalarni saqlab qolamiz
    )


@dp.callback_query(F.data == "dislike")
async def callback_dislike(callback: CallbackQuery):
    """'Dislike' inline tugmasi bosilganda"""
    await callback.answer("Afsuski sizga yoqmadi")

    await callback.message.edit_text(
        "Siz Dislike bosdingiz",
        reply_markup=inline_menu
    )


@dp.callback_query(F.data == "detail")
async def callback_detail(callback: CallbackQuery):
    """'Batafsil' inline tugmasi bosilganda"""
    # callback.answer() - tez javob, kutish belgisini o'chiradi
    await callback.answer()

    # Batafsil ma'lumot bilan yangi xabar yuborish
    await callback.message.answer(
        "Batafsil ma'lumot:\n\n"
        "Bu yerda to'liq ma'lumot bo'ladi..."
    )


@dp.callback_query(F.data == "back_to_menu")
async def callback_back(callback: CallbackQuery):
    """'Orqaga' inline tugmasi bosilganda"""
    await callback.answer()
    await callback.message.edit_text(
        "Asosiy menyu:",
        reply_markup=inline_menu
    )


@dp.callback_query(F.data == "plus")
async def callback_plus(callback: CallbackQuery):
    """'+' tugmasi bosilganda"""
    await callback.answer("Miqdor oshirildi")


@dp.callback_query(F.data == "minus")
async def callback_minus(callback: CallbackQuery):
    """'-' tugmasi bosilganda"""
    await callback.answer("Miqdor kamaytirildi")


@dp.callback_query(F.data == "add_to_cart")
async def callback_add_cart(callback: CallbackQuery):
    """'Savatga qo'shish' tugmasi bosilganda"""
    await callback.answer("Mahsulot savatga qo'shildi!", show_alert=True)


@dp.callback_query(F.data == "buy_now")
async def callback_buy(callback: CallbackQuery):
    """'Sotib olish' tugmasi bosilganda - tasdiqlash so'rash"""
    await callback.answer()

    # Tasdiqlash tugmalarini ko'rsatamiz
    await callback.message.edit_text(
        "Rostdan ham sotib olmoqchimisiz?",
        reply_markup=create_confirm_keyboard("buy")
    )


@dp.callback_query(F.data == "confirm_buy")
async def callback_confirm_buy(callback: CallbackQuery):
    """Sotib olishni tasdiqlash"""
    await callback.answer("Buyurtma qabul qilindi!", show_alert=True)
    await callback.message.edit_text("Rahmat! Buyurtmangiz qabul qilindi.")


@dp.callback_query(F.data == "cancel_buy")
async def callback_cancel_buy(callback: CallbackQuery):
    """Sotib olishni bekor qilish"""
    await callback.answer("Bekor qilindi")
    await callback.message.edit_text(
        "Buyurtma bekor qilindi.\n\n"
        "Mahsulot: iPhone 15 Pro\n"
        "Narxi: $999",
        reply_markup=product_keyboard
    )



# CONTENT TYPE HANDLERS (Maxsus kontent turlari)


@dp.message(F.contact)
async def handle_contact(message: Message):
    """
    Foydalanuvchi telefon raqamini yuborganda.
    request_contact tugmasi orqali keladi.
    """
    phone = message.contact.phone_number
    await message.answer(
        f"Rahmat! Telefon raqamingiz: {phone}\n"
        f"Tez orada siz bilan bog'lanamiz.",
        reply_markup=main_menu_keyboard
    )


@dp.message(F.location)
async def handle_location(message: Message):
    """
    Foydalanuvchi joylashuvini yuborganda.
    request_location tugmasi orqali keladi.
    """
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer(
        f"Rahmat! Joylashuvingiz:\n"
        f"Kenglik: {lat}\n"
        f"Uzunlik: {lon}",
        reply_markup=main_menu_keyboard
    )



# MAIN


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Siz klaviatura orqali dasturni to'xtatdingiz!\nGoodbye!")
