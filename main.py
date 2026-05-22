import asyncio
import json
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import config  # Bu yerda config.py faylingizdagi token va ID saqlanadi

# Loglarni sozlash (Xatoliklarni terminalda ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# Bot va FastAPI sozlamalari
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

# CORS (Frontend va Backend bog'lanishi uchun shart!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. TELEGRAM BOT QISMI ---
@dp.message()
async def handle_web_app_data(message: Message):
    # Agar Web App dan ma'lumot kelsa
    if message.web_app_data:
        try:
            # Saytdan kelgan JSON ni o'qiymiz
            data = json.loads(message.web_app_data.data)
            
            # Buyurtmani chiroyli ko'rinishda shakllantiramiz
            order_text = (
                f"📦 **YANGI BUYURTMA!**\n\n"
                f"👤 Mijoz: {message.from_user.full_name}\n"
                f"🆔 ID: {message.from_user.id}\n\n"
                f"Mahsulotlar:\n"
            )
            
            for item in data['items']:
                order_text += f"- {item['name']} | {item['qty']} ta | {item['price']} so'm\n"
            
            order_text += f"\n💰 **JAMI: {data['total']} so'm**"
            
            # Adminga (sizga) xabar yuborish
            await bot.send_message(config.ADMIN_ID, order_text, parse_mode="Markdown")
            
            # Mijozga javob yuborish
            await message.answer("✅ Buyurtmangiz muvaffaqiyatli qabul qilindi! Tez orada bog'lanamiz.")
            
        except Exception as e:
            logging.error(f"Buyurtmani qayta ishlashda xatolik: {e}")

# --- 2. FASTAPI (API) QISMI ---
@app.get("/products")
async def get_products():
    # Bu yerda mahsulotlar bazasini qaytaring
    return [
        {"id": 1, "name": "Batareya", "price": 500000},
        {"id": 2, "name": "Zaryadlovchi", "price": 200000}
    ]

@app.get("/")
async def root():
    return {"status": "Server ishlamoqda!"}

# --- 3. ISHGA TUSHIRISH ---
@app.on_event("startup")
async def startup_event():
    # Botni fon rejimida (background) ishga tushiramiz
    asyncio.create_task(dp.start_polling(bot))
    logging.info("Bot va Server ishga tushdi!")

# Render yoki localhost da ishga tushirish uchun
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)