# src/utils/backup.py
import asyncpg
import asyncio
from datetime import datetime
from config import DATABASE_DSN

async def create_backup():
    """Create DB backup"""
    try:
        # Connecting to DB
        conn = await asyncpg.connect(DATABASE_DSN)
        
        # Fetch all data
        tasks = await conn.fetch("SELECT * FROM tasks ORDER BY id")
        users = await conn.fetch("SELECT * FROM users ORDER BY user_id")
        
        # Creting backup file
        backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{backup_time}.sql"
        
        with open(filename, 'w') as f:
            f.write("-- Database Backup\n")
            f.write(f"-- Created: {backup_time}\n\n")
            
            # Save users
            for user in users:
                f.write(f"INSERT INTO users VALUES ({user['user_id']}, '{user['username']}', '{user['first_name']}', '{user['last_name']}', '{user['created_at']}');\n")
            
            # Save tasks
            for task in tasks:
                f.write(f"INSERT INTO tasks VALUES ({task['id']}, {task['user_id']}, '{task['text']}', '{task['created_at']}', {task['is_completed']});\n")
        
        print(f"Backup created: {filename}")
        await conn.close()
        
    except Exception as e:
        print(f"Backup error: {e}")