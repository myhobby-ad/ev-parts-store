from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

# Router nomini asosiy faylingiz (main.py) tanishi uchun aynan shunday nomlaymiz
admin_router = Router()

# 1. /admin buyrug'i kelganda ishlaydigan qism
@admin_router.message(Command("admin"))
async def admin_command_handler(message: Message):
    await message.answer(
        "👋 Admin paneliga xush kelibsiz!\n\n"
        "Mahsulot qo'shish uchun quyidagi buyruqni bering:\n"
        "➡️ /add_product"
    )

# 2. /add_product buyrug'i kelganda ishlaydigan qism
@admin_router.message(Command("add_product"))
async def add_product_command_handler(message: Message):
    await message.answer(
        "📦 Yangi mahsulot qo'shish bo'limi:\n\n"
        "Iltimos, mahsulot ma'lumotlarini bazaga kiritish uchun "
        "FastAPI Swagger UI (http://127.0.0.1:8000/docs) interfeysidan foydalaning."
    )