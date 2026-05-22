import json
from aiogram import Router, F
from aiogram.types import Message
from loader import bot
from config import ADMIN_ID

web_app_router = Router()

@web_app_router.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    # Terminalda ishlashini tekshirish uchun
    print("✅ Web App dan ma'lumot keldi!")
    
    try:
        data = json.loads(message.web_app_data.data)
        items = data.get("items", [])
        total = data.get("total", 0)

        # Admin uchun xabar shakllantirish
        admin_text = (
            f"🔔 **YANGI BUYURTMA!**\n\n"
            f"👤 Mijoz: {message.from_user.full_name}\n"
            f"📦 Mahsulotlar:\n"
        )
        for i, item in enumerate(items, 1):
            admin_text += f"{i}. {item['name']} - {item['qty']} ta - {item['price']:,} so'm\n"
        admin_text += f"\n💰 **Jami: {total:,} so'm**"

        # Adminga xabar yuborish
        await bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")
        
        # Mijozga tasdiq xabari
        await message.answer("✅ Buyurtmangiz qabul qilindi!")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        await message.answer("❌ Buyurtmani qabul qilishda xatolik yuz berdi.")