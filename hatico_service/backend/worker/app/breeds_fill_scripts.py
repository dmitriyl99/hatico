from pymongo import MongoClient
import pandas as pd

import os

from core.config import settings


db = MongoClient(host=settings.MONGO_DB_HOST)[settings.MONGO_DB_NAME]
breeds = pd.read_csv(os.path.join(settings.DATA_DIR, 'datasets/breeds_labels.csv'))
breeds_names = sorted(breeds['breed'].unique())
breeds_names = map(lambda x: {'value': x, 'display': x}, breeds_names)

db.breeds.insert_many(breeds_names)
