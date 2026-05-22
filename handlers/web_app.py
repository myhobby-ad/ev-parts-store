import json
from aiogram import Router, F
from aiogram.types import Message
from loader import bot
from config import ADMIN_ID  # ADMIN_ID config.py da to'g'ri yozilganligiga ishonch hosil qiling

web_app_router = Router()

@web_app_router.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    # WebApp dan kelgan ma'lumotni o'qiymiz
    data = json.loads(message.web_app_data.data)
    
    # 1. Mijozga javob
    await message.answer("✅ Buyurtmangiz qabul qilindi! Tez orada bog'lanamiz.")
    
    # 2. Adminga xabar yuborish
    admin_text = f"🔔 Yangi buyurtma!\n\nMijoz: {message.from_user.full_name}\nMa'lumotlar: {data}"
    await bot.send_message(chat_id=ADMIN_ID, text=admin_text)