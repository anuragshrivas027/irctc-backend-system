from pymongo import MongoClient
from django.conf import settings
import time

client = MongoClient("mongodb://localhost:27017/")
db = client["irctc_logs"]
collection = db["train_search_logs"]


def log_train_search(user_id, source, destination, execution_time):
    collection.insert_one({
        "user_id": user_id,
        "source": source,
        "destination": destination,
        "execution_time": execution_time,
        "timestamp": time.time()
    })