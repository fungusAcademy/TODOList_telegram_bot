import os
from dotenv import load_dotenv

def get_database_url():
    # AlwaysData предоставляет переменную DATABASE_URL
    if 'DATABASE_URL' in os.environ:
        return os.environ['DATABASE_URL']
    if "DATABASE_DSN" in os.environ:
        return os.environ['DATABASE_DSN']
    
    raise ValueError("Cannot find DATABASE URL or DSN in env var!!!")

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_DSN = get_database_url()
# DATABASE_DSN = os.getenv("DATABASE_DSN", "postgresql://user:pass@localhost/dbname")

if not BOT_TOKEN:
    raise ValueError("Cannot find BOT_TOKEN in .env file")