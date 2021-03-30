from pymongo import MongoClient
from settings import mongoUrl, database_name
connect = MongoClient(mongoUrl)
databases = connect[database_name]

def get_collection(collection_name):
    return databases[collection_name]
