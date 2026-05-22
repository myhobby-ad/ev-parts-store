import asyncio
import logging
from loader import dp, bot
from handlers.web_app import web_app_router
from handlers.admin import admin_router

async def main():
    # Logging sozlamasi
    logging.basicConfig(level=logging.INFO)
    
    # Routerlarni ulash
    dp.include_router(web_app_router)
    dp.include_router(admin_router)

    # Eski webhooklarni tozalash (Conflict oldini olish uchun)
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("🚀 Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi!")