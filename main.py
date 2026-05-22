import asyncio
import json
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@dp.message()
async def handle_web_app_data(message: Message):
    if message.web_app_data:
        try:
            data = json.loads(message.web_app_data.data)
            order_text = (
                f"📦 **YANGI BUYURTMA!**\n\n"
                f"👤 Mijoz: {message.from_user.full_name}\n"
                f"🆔 ID: {message.from_user.id}\n\n"
                f"Mahsulotlar:\n"
            )
            for item in data['items']:
                order_text += f"- {item['name']} | {item['qty']} ta | {item['price']} so'm\n"
            order_text += f"\n💰 **JAMI: {data['total']} so'm**"
            
            await bot.send_message(config.ADMIN_ID, order_text, parse_mode="Markdown")
            await message.answer("✅ Buyurtmangiz muvaffaqiyatli qabul qilindi!")
        except Exception as e:
            logging.error(f"Xatolik: {e}")

# Eng muhim qism: Botni ishga tushirish funksiyasi
async def start_bot():
    # Eski ulanishlarni tozalash (Conflict oldini oladi)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

@app.on_event("startup")
async def startup_event():
    # Botni alohida task sifatida ishga tushiramiz
    asyncio.create_task(start_bot())
    logging.info("Bot va Server ishga tushdi!")

if __name__ == "__main__":
    # Render yoki mahalliy muhit uchun port sozlamasi
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)