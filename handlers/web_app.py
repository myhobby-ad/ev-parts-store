import json
from aiogram import Router, F
from aiogram.types import Message
from loader import bot
from config import ADMIN_ID

web_app_router = Router()

@web_app_router.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    raw_data = message.web_app_data.data
    
    try:
        data = json.loads(raw_data)
        items = data.get("items", [])
        total_price = data.get("total", 0)
        
        # Xaridor uchun matn
        user_text = "🎉 **Buyurtmangiz muvaffaqiyatli qabul qilindi!**\n\n"
        user_text += "📦 **Xarid qilingan mahsulotlar:**\n"
        
        # Admin uchun matn
        admin_text = "🔔 **YANGI BUYURTMA KELDI!**\n\n"
        admin_text += f"👤 **Xaridor:** {message.from_user.full_name}\n"
        if message.from_user.username:
            admin_text += f"🔗 **Telegram:** @{message.from_user.username}\n"
        admin_text += f"🆔 **User ID:** `{message.from_user.id}`\n\n"
        admin_text += "📦 **Mahsulotlar ro'yxati:**\n"
        
        # Mahsulotlarni hisoblash tsikli
        for index, item in enumerate(items, 1):
            name = item.get("name", "Noma'lum")
            qty = item.get("qty", 1)
            price = item.get("price", 0)
            item_total = price * qty
            
            line = f"{index}. {name} — {qty} dona x {price:,} so'm = {item_total:,} so'm\n"
            user_text += line
            admin_text += line
            
        user_text += f"\n💰 **Jami summa:** {total_price:,} so'm\n"
        user_text += "⏳ Tez orada operatorlarimiz siz bilan bog'lanishadi."
        
        admin_text += f"\n💰 **Jami summa:** {total_price:,} so'm"
        
        # Xabarlarni yuborish
        await message.answer(user_text, parse_mode="Markdown")
        await bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")
        
    except json.JSONDecodeError:
        await message.answer("❌ Ma'lumotlarni qayta ishlashda xatolik yuz berdi (Noto'g'ri format).")
    except Exception as e:
        await message.answer(f"❌ Kutilmagan xatolik: {e}")
        