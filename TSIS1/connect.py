import pg8000.dbapi
from config import DB_CONFIG

def get_connection():
    return pg8000.dbapi.connect(
        host=DB_CONFIG['host'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        port=DB_CONFIG['port']
    )
