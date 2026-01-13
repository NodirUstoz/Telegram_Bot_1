# keyboards.py
# Bu faylda Telegram bot uchun turli xil klaviaturalar (buttonlar) yaratiladi
#
# Telegram botda 2 xil asosiy klaviatura mavjud:
# 1. Reply Keyboard - Xabar yozish maydonining ostida chiqadigan buttonlar
# 2. Inline Keyboard - Xabar ichida chiqadigan buttonlar

from aiogram.types import (
    ReplyKeyboardMarkup,      # Reply klaviatura yaratish uchun
    KeyboardButton,           # Reply klaviatura tugmasi
    InlineKeyboardMarkup,     # Inline klaviatura yaratish uchun
    InlineKeyboardButton,     # Inline klaviatura tugmasi
    ReplyKeyboardRemove       # Reply klaviaturani olib tashlash uchun
)


# 1-QISM: REPLY KEYBOARD (Oddiy tugmalar)

# Reply Keyboard - bu foydalanuvchi xabar yozadigan maydon ostida
# paydo bo'ladigan tugmalar. Foydalanuvchi tugmani bosganida,
# tugma matni xabar sifatida yuboriladi.


# --- 1.1 Oddiy Reply Keyboard ---
# Eng sodda ko'rinish - bir qatorli tugmalar
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        # Har bir ichki list - bu bitta qator (row)
        [KeyboardButton(text="Biz haqimizda"), KeyboardButton(text="Xizmatlar")],
        [KeyboardButton(text="Bog'lanish"), KeyboardButton(text="Sozlamalar")],
    ],
    resize_keyboard=True,  # Tugmalarni kichikroq qiladi (tavsiya etiladi)
    input_field_placeholder="Tanlang..."  # Input maydonida ko'rinadigan matn
)

# --- 1.2 Bir ustunli (vertikal) Reply Keyboard ---
# Har bir tugma alohida qatorda
settings_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Til o'zgartirish")],      # 1-qator
        [KeyboardButton(text="Bildirishnomalar")],     # 2-qator
        [KeyboardButton(text="Orqaga")],               # 3-qator
    ],
    resize_keyboard=True
)

# --- 1.3 Maxsus tugmalar (Telefon va Lokatsiya) ---
# Bu tugmalar foydalanuvchidan maxsus ma'lumot so'raydi
contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        # request_contact=True - Foydalanuvchining telefon raqamini so'raydi
        [KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)],

        # request_location=True - Foydalanuvchining joylashuvini so'raydi
        [KeyboardButton(text="Joylashuvni yuborish", request_location=True)],

        [KeyboardButton(text="Bekor qilish")],
    ],
    resize_keyboard=True
)



# 2-QISM: INLINE KEYBOARD (Xabar ichidagi tugmalar)

# Inline Keyboard - bu xabar ichida paydo bo'ladigan tugmalar.
# Reply keyboarddan farqi:
# - Xabar ichida ko'rinadi (ostki panelda emas)
# - Bosilganda xabar yuborilmaydi, callback_data yuboriladi
# - URL ga yo'naltirish mumkin
# - Tugmani bosganini faqat bot ko'radi


# --- 2.1 Oddiy Inline Keyboard ---
# callback_data - tugma bosilganda serverga yuboriladigan ma'lumot
# Bu ma'lumotni callback_query handler orqali ushlab olamiz
inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        # Har bir ichki list - bu bitta qator
        [
            InlineKeyboardButton(text="Like", callback_data="like"),
            InlineKeyboardButton(text="Dislike", callback_data="dislike"),
        ],
        [
            InlineKeyboardButton(text="Batafsil", callback_data="detail"),
        ],
    ]
)

# --- 2.2 URL tugmali Inline Keyboard ---
# url parametri orqali havolaga yo'naltirish mumkin
# DIQQAT: url va callback_data bir vaqtda ishlatib bo'lmaydi!
links_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            # url - tugma bosilganda bu manzilga o'tadi
            InlineKeyboardButton(text="Telegram kanal", url="https://t.me/example"),
            InlineKeyboardButton(text="Website", url="https://example.com"),
        ],
        [
            InlineKeyboardButton(text="YouTube", url="https://youtube.com"),
        ],
        [
            # callback_data ishlatilgan tugma
            InlineKeyboardButton(text="Orqaga", callback_data="back_to_menu"),
        ],
    ]
)

# --- 2.3 Mahsulot uchun Inline Keyboard misoli ---
# Real loyihalarda shunday ko'rinishda bo'ladi
product_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="-", callback_data="minus"),
            InlineKeyboardButton(text="1", callback_data="count"),
            InlineKeyboardButton(text="+", callback_data="plus"),
        ],
        [
            InlineKeyboardButton(text="Savatga qo'shish", callback_data="add_to_cart"),
        ],
        [
            InlineKeyboardButton(text="Sotib olish", callback_data="buy_now"),
        ],
    ]
)


# 3-QISM: DINAMIK KEYBOARD YARATISH (Funksiyalar)

# Ba'zan klaviaturani dinamik ravishda (o'zgaruvchan) yaratish kerak bo'ladi
# Masalan: foydalanuvchi ismini tugmaga qo'yish, yoki ma'lumotlar bazasidan
# kelgan ma'lumotlar asosida tugmalar yaratish


def create_category_keyboard(categories: list) -> InlineKeyboardMarkup:
    """
    Kategoriyalar ro'yxatidan inline keyboard yaratadi.

    Misol:
        categories = ["Elektronika", "Kiyimlar", "Oziq-ovqat"]
        keyboard = create_category_keyboard(categories)

    Args:
        categories: Kategoriya nomlari ro'yxati

    Returns:
        InlineKeyboardMarkup obyekti
    """
    # Har bir kategoriya uchun tugma yaratamiz
    buttons = []
    for category in categories:
        # callback_data uchun category nomini kichik harflarga o'zgartiramiz
        callback = f"category_{category.lower().replace(' ', '_')}"
        buttons.append([InlineKeyboardButton(text=category, callback_data=callback)])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_pagination_keyboard(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    """
    Sahifalash uchun keyboard yaratadi (oldingi/keyingi tugmalari).

    Misol:
        keyboard = create_pagination_keyboard(current_page=2, total_pages=5)
        # Natija: [< Oldingi] [2/5] [Keyingi >]

    Args:
        current_page: Hozirgi sahifa raqami
        total_pages: Jami sahifalar soni

    Returns:
        InlineKeyboardMarkup obyekti
    """
    buttons = []
    row = []

    # Oldingi tugma (agar 1-sahifa bo'lmasa)
    if current_page > 1:
        row.append(InlineKeyboardButton(
            text="< Oldingi",
            callback_data=f"page_{current_page - 1}"
        ))

    # Hozirgi sahifa ko'rsatkichi
    row.append(InlineKeyboardButton(
        text=f"{current_page}/{total_pages}",
        callback_data="current_page"  # Bu tugma hech narsa qilmaydi
    ))

    # Keyingi tugma (agar oxirgi sahifa bo'lmasa)
    if current_page < total_pages:
        row.append(InlineKeyboardButton(
            text="Keyingi >",
            callback_data=f"page_{current_page + 1}"
        ))

    buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    """
    Tasdiqlash/Bekor qilish keyboard yaratadi.

    Misol:
        keyboard = create_confirm_keyboard("delete")
        # Tugmalar: [Ha, o'chirish] [Yo'q, bekor qilish]

    Args:
        action: Amal nomi (masalan: "delete", "buy", "send")

    Returns:
        InlineKeyboardMarkup obyekti
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ha", callback_data=f"confirm_{action}"),
                InlineKeyboardButton(text="Yo'q", callback_data=f"cancel_{action}"),
            ]
        ]
    )



# 4-QISM: REPLY KEYBOARD NI OLIB TASHLASH

# ReplyKeyboardRemove - bu klaviaturani olib tashlash uchun ishlatiladi
# Masalan: foydalanuvchi ma'lumot kiritib bo'lgandan keyin


# Klaviaturani olib tashlash uchun
remove_keyboard = ReplyKeyboardRemove()



# ESLATMA VA MASLAHATLAR:

#
# 1. resize_keyboard=True - Har doim ishlatish tavsiya etiladi
#    Bu tugmalarni kichikroq va chiroyliroq qiladi
#
# 2. one_time_keyboard=True - Tugma bosilgandan keyin klaviatura yashirinadi
#    ReplyKeyboardMarkup(..., one_time_keyboard=True)
#
# 3. callback_data uzunligi 64 baytdan oshmasligi kerak!
#    Uzun ma'lumotlar uchun qisqa ID'lar ishlating
#
# 4. Inline tugmada url va callback_data bir vaqtda bo'lishi MUMKIN EMAS
#
# 5. Har bir qatorda eng ko'pi 8 ta inline tugma bo'lishi mumkin
#    Jami klaviaturada 100 ta tugmadan oshmasligi kerak

