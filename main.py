import io
import sqlite3
from typing import List, Optional
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio

# 🔑 config.py ichidan tokenni chaqiramiz
from config import BOT_TOKEN  

app = FastAPI(
    title="EV-Parts Web Market API",
    description="Mahsulot qo'shish funksiyasi mavjud mukammal Backend tizimi",
    version="1.1.4"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    conn = sqlite3.connect('ev_parts.db')
    conn.row_factory = sqlite3.Row  
    return conn


@app.on_event("startup")
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            category TEXT NOT NULL,
            tag TEXT DEFAULT '',
            name TEXT NOT NULL,
            price REAL DEFAULT 0.0,
            image_url TEXT DEFAULT ''
        );
    """)
    conn.commit()
    conn.close()
    print("📢 'products' jadvali tayyor!")


# --- PYDANTIC MODELLARI ---
class ProductCreate(BaseModel):
    brand: str
    category: str
    tag: str = ""
    name: str
    price: float
    image_url: str = ""

class ProductResponse(BaseModel):
    id: int
    brand: str
    category: str
    tag: str
    name: str
    price: float
    image_url: str

class OrderItem(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: float

class OrderModel(BaseModel):
    user_id: int
    user_name: str
    phone: str
    cart_items: List[OrderItem]
    total_price: float


# --- API YO'LAKLARI ---

# 🆕 TOVAR QO'SHISH UCHUN YANGI YO'LAK!
@app.post("/api/add-product", response_model=ProductResponse)
async def add_product(product: ProductCreate):
    """
    Ushbu yo'lak orqali Swagger panelidan turib bazaga xohlagancha mahsulot qo'shishingiz mumkin!
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (brand, category, tag, name, price, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (product.brand, product.category, product.tag, product.name, product.price, product.image_url))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "id": product_id,
            "brand": product.brand,
            "category": product.category,
            "tag": product.tag,
            "name": product.name,
            "price": product.price,
            "image_url": product.image_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qo'shishda xatolik: {str(e)}")


@app.get("/api/products", response_model=List[ProductResponse])
async def get_products(
    brand: Optional[str] = Query(None), 
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        if brand and brand != "Barchasi":
            query += " AND brand = ?"
            params.append(brand)
        if category and category != "Barchasi":
            query += " AND category = ?"
            params.append(category)
        if search:
            query += " AND name LIKE ?"
            params.append(f"%{search}%")
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Baza xatoligi: {str(e)}")


@app.get("/api/brands")
async def get_brands():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT brand FROM products WHERE brand IS NOT NULL AND brand != ''")
        brands = [row['brand'] for row in cursor.fetchall()]
        conn.close()
        return {"brands": ["Barchasi"] + brands}
    except Exception:
        return {"brands": ["Barchasi", "Tesla", "BYD", "NIO"]}


@app.get("/api/categories")
async def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL AND category != ''")
        categories = [row['category'] for row in cursor.fetchall()]
        conn.close()
        return {"categories": ["Barchasi"] + categories}
    except Exception:
        return {"categories": ["Barchasi", "Batareya", "Zaryad", "Suspension"]}


@app.get("/api/image/{file_id}")
async def get_telegram_image(file_id: str):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    try:
        response = requests.get(telegram_url).json()
        if not response.get("ok"):
            raise HTTPException(status_code=404, detail="Fayl topilmadi")
        file_path = response["result"]["file_path"]
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        img_response = requests.get(download_url)
        return StreamingResponse(io.BytesIO(img_response.content), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rasm yuklashda xatolik: {str(e)}")


@app.post("/api/orders")
async def create_order(order: OrderModel):
    print(f"🛒 Yangi Buyurtma! Mijoz: {order.user_name}, Jami: {order.total_price} so'm")
    return {"status": "success", "message": "Buyurtma qabul qilindi!"}

@app.get("/products")
async def get_products():
    return [{"name": "Batareya", "price": 500000}, {"name": "Zaryadlovchi", "price": 200000}]
