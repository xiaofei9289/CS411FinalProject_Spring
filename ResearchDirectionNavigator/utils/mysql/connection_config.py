import os
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

_ROOT=Path(__file__).resolve().parent.parent.parent
load_dotenv(_ROOT / ".env")

# mysql settings
def get_mysql_config():
    port=os.getenv("MYSQL_PORT", "3306")
    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(port),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", ""),
    }


