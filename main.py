import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher
# Bot tokeningizni (config.py o'rniga) Render'dagi Environment Variables'dan oling
import os

# 1. Sozlamalar
BOT_TOKEN = os.getenv("BOT_TOKEN") 
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

# 2. CORS sozlamasi (Frontend va Backend bog'lanishi uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. API yo'llari (Frontend shu yerdan ma'lumot oladi)
@app.get("/products")
async def get_products():
    # Bu yerda bazadan ma'lumot olishingiz mumkin
    return [
        {"name": "Batareya", "price": "500 000"},
        {"name": "Zaryadlovchi", "price": "200 000"}
    ]

@app.get("/")
async def root():
    return {"message": "Backend ishlamoqda!"}

# 4. Bot va FastAPI'ni birga ishga tushirish
async def run_bot():
    await dp.start_polling(bot)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_bot())

# Render uchun muhim: Uvicorn buni 'main:app' orqali chaqiradi