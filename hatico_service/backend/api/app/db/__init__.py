from pymongo import MongoClient

from app.core.config import settings

client = MongoClient(host=settings.MONGO_DB_HOST)
database = client[settings.MONGO_DB_NAME]
