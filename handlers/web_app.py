import json
from aiogram import Router, F
from aiogram.types import Message
from loader import bot
import config  # config ni to'liq import qilamiz

web_app_router = Router()

@web_app_router.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    raw_data = message.web_app_data.data
    
    # DEBUG: ADMIN_ID ni terminalda tekshiramiz
    print(f"DEBUG: Hozirgi ADMIN_ID = {config.ADMIN_ID}")
    
    try:
        data = json.loads(raw_data)
        items = data.get("items", [])
        total_price = data.get("total", 0)
        
        # ... (sizning yozgan user_text va admin_text kodlaringizni shu yerga qo'ying) ...
        # (matn yig'ish qismi o'zgarishsiz qolaveradi)
        
        admin_text = "🔔 YANGI BUYURTMA!\n" + ... # (matnni saqlang)
        
        # Xabarlarni yuborish
        await message.answer("✅ Buyurtmangiz qabul qilindi!", parse_mode="Markdown")
        
        # ADMINGA yuborish (SHU YERNI TEKSHIRAMIZ)
        if config.ADMIN_ID:
            await bot.send_message(chat_id=config.ADMIN_ID, text=admin_text, parse_mode="Markdown")
            print("DEBUG: Buyurtma adminga yuborildi.")
        else:
            print("DEBUG: Xatolik! ADMIN_ID topilmadi.")
            
    except Exception as e:
        print(f"DEBUG: Xatolik yuz berdi: {e}")
        await message.answer(f"❌ Xatolik: {e}")
        