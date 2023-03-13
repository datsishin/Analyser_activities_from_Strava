import pymongo
from pymongo import MongoClient

from users import users_data


def db_connect(user_id: int, param=str):
    client = MongoClient("mongodb://mongo_db/")
    athlete_id = users_data[f'{user_id}']['athlete_id']

    if param == 'training':
        db = client['training_db']
        collection = db[f'{athlete_id}_training']
        collection.create_index([('athlete', pymongo.DESCENDING)])
        collection.create_index([('id', pymongo.DESCENDING)])
        return collection

    if param == 'service':
        db = client['service_db']
        collection = db[f'{athlete_id}_service']
        collection.create_index([('mileage', pymongo.DESCENDING)])
        collection.create_index([('bike', pymongo.DESCENDING)])
        return collection
