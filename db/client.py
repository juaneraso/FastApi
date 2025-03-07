from pymongo import MongoClient

## Base de datos local
# db_client = MongoClient().local

from dotenv import load_dotenv
import os

load_dotenv()

# Acceder a las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

#base de datos remota


db_client = MongoClient(DATABASE_URL).test