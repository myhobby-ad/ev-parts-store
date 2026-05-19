import sqlite3

def init_db():
    conn = sqlite3.connect('ev_parts.db')
    cursor = conn.cursor()
    # Mahsulotlar jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            category TEXT,
            tag TEXT,
            name TEXT,
            price REAL,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_product(brand, category, tag, name, price, image_url):
    conn = sqlite3.connect('ev_parts.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (brand, category, tag, name, price, image_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (brand, category, tag, name, price, image_url))
    conn.commit()
    conn.close()