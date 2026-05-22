import asyncio
import json
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- SOZLAMALAR ---
# Tokenni o'zgartiring: yoki Render'dan oling, yoki shu yerga yozing
BOT_TOKEN = os.getenv("BOT_TOKEN", "SIZNING_TOKENINGIZNI_SHU_YERGA_YOZING")
ADMIN_ID = os.getenv("ADMIN_ID", "SIZNING_TELEGRAM_IDINGIZ")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

# --- CORS (Sayt va Server bog'lanishi) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- TELEGRAM BOT LOGIKASI ---
@dp.message()
async def handle_message(message: types.Message):
    # Web App'dan ma'lumot kelganda
    if message.web_app_data:
        try:
            data = json.loads(message.web_app_data.data)
            
            # Buyurtmani chiroyli formatlash
            order_text = f"📦 **Yangi buyurtma!**\n\n"
            for item in data['items']:
                order_text += f"🔹 {item['name']} | {item['qty']} ta | {item['price']} so'm\n"
            order_text += f"\n💰 **Jami: {data['total']} so'm**"
            
            # Adminga yuborish
            await bot.send_message(ADMIN_ID, order_text, parse_mode="Markdown")
            # Mijozga javob
            await message.answer("✅ Buyurtmangiz qabul qilindi!")
        except Exception as e:
            print(f"Xatolik: {e}")

# --- API LOGIKASI ---
@app.get("/products")
async def get_products():
    return [
        {"id": 1, "name": "Batareya", "price": 500000},
        {"id": 2, "name": "Zaryadlovchi", "price": 200000}
    ]

# --- ISHGA TUSHIRISH ---
@app.on_event("startup")
async def startup_event():
    # Botni fon rejimida ishga tushirish
    asyncio.create_task(dp.start_polling(bot))
    print("Bot va Server ishga tushdi!")