import os
from dotenv import load_dotenv

def get_database_url():
    if 'DATABASE_URL' in os.environ:
        db_url = os.environ['DATABASE_URL']
        # Некоторые библиотеки требуют замену postgresql:// на postgres://
        if db_url.startswith('postgresql://'):
            db_url = db_url.replace('postgresql://', 'postgres://', 1)
        return db_url
    if "DATABASE_DSN" in os.environ:
        return os.environ['DATABASE_DSN']
    
    raise ValueError("Cannot find DATABASE URL or DSN in env var!!!")

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_DSN = get_database_url()
# DATABASE_DSN = os.getenv("DATABASE_DSN", "postgresql://user:pass@localhost/dbname")

if not BOT_TOKEN:
    raise ValueError("Cannot find BOT_TOKEN in .env file")