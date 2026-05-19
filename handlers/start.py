from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.filters import CommandStart
from config import WEB_APP_URL

# Router yaratamiz
start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    # Web App tugmasini yaratish
    kb = [
        [KeyboardButton(
            text="🛒 Do'konni ochish (EV Parts)", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb, 
        resize_keyboard=True, 
        one_time_keyboard=False
    )
    
    welcome_text = (
        f"Xush kelibsiz, {message.from_user.full_name}!\n\n"
        f"⚡ **EV PARTS STORE** ga xush kelibsiz. Elektromobillar uchun "
        f"ehtiyot qismlarni buyurtma qilish uchun pastdagi tugmani bosing."
    )
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")