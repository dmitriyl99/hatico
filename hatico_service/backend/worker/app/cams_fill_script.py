from pymongo import MongoClient
import pandas as pd

import os

from core.config import settings

db = MongoClient(host=settings.MONGO_DB_HOST)[settings.MONGO_DB_NAME]
df = pd.read_csv(os.path.join(settings.DATA_DIR, 'datasets/moscow_cameras.csv'))
df = df.drop(['Unnamed: 0'], axis=1)
cameras_dict = df.sample(500).to_dict('records')
db.cameras.insert_many(cameras_dict)
