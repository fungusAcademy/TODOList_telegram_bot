# database.py
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def get_connection():
    """Простое подключение к базе данных"""
    return await asyncpg.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

async def init_db():
    """Создание таблиц если их нет"""
    conn = await get_connection()
    try:
        # await conn.execute('DROP TABLE IF EXISTS tasks')
        
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                task_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        print("Таблица tasks успешно создана")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        await conn.close()