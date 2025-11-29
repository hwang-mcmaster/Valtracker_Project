import os
from dotenv import load_dotenv

load_dotenv()

PANDASCORE_API_KEY = os.getenv("PANDASCORE_API_KEY")

PGHOST = os.getenv("host")
PGPORT = int(os.getenv("port", "5432"))
PGDATABASE = os.getenv("dbname")
PGUSER = os.getenv("user")
PGPASSWORD = os.getenv("password")
