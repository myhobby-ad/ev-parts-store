import logging
import asyncio
import sys
from loader import bot, dp
from handlers.start import start_router
from handlers.web_app import web_app_router

# Routerlarni ulash
dp.include_router(start_router)
dp.include_router(web_app_router)

async def main():
    # Loggingni to'liq yoqish (barcha ma'lumotlarni ko'rish uchun)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    
    try:
        # Webhooklarni tozalash
        await bot.delete_webhook(drop_pending_updates=True)
        # Pollingni boshlash
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot ishlashida xatolik: {e}")

if __name__ == "__main__":
    try:
        # Windows tizimida asyncio bilan bog'liq xatolik kelib chiqmasligi uchun
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi!")
