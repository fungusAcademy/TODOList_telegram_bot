import os
from dotenv import load_dotenv

def get_database_url():
    if 'DATABASE_URL' in os.environ:
        db_url = os.environ['DATABASE_URL']
        # some libs use postgres://
        if db_url.startswith('postgresql://'):
            db_url = db_url.replace('postgresql://', 'postgres://', 1)
        return db_url
     
    load_dotenv()
    if "DATABASE_DSN" in os.environ:
        return os.environ['DATABASE_DSN']
    
    raise ValueError("Cannot find DATABASE URL or DSN in env var!!!")

def get_bot_token():
    if 'BOT_TOKEN' in os.environ:
        return os.environ['BOT_TOKEN']
    
    load_dotenv()
    if 'BOT_TOKEN' in os.environ:
        return os.environ['BOT_TOKEN']
    
    raise ValueError("Cannot find BOT_TOKEN!")


BOT_TOKEN = get_bot_token()
DATABASE_DSN = get_database_url()
# DATABASE_DSN = os.getenv("DATABASE_DSN", "postgresql://user:pass@localhost/dbname")