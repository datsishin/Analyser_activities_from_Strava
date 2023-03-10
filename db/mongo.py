import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

first_user = os.getenv('FIRST_USER_ID')
second_user = os.getenv('SECOND_USER_ID')
first_athlete_id = int(os.getenv('FIRST_ATHLETE_ID'))
second_athlete_id = int(os.getenv('SECOND_ATHLETE_ID'))

users_data = {first_user: first_athlete_id,
              second_user: second_athlete_id}


def db_connect(user_id: int, param=str):
    client = MongoClient('localhost', 27017)
    athlete_id = users_data[f'{user_id}']

    if param == 'training':
        db = client['training_db']
        collection = db[f'{athlete_id}_training']
        collection.create_index([('athlete', pymongo.DESCENDING)])
        collection.create_index([('id', pymongo.DESCENDING)])
        return collection

    if param == 'gear':
        db = client['gear_db']
        collection = db[f'{athlete_id}_gears']
        collection.create_index([('bike', pymongo.DESCENDING)])
        return collection

    if param == 'service':
        db = client['service_db']
        collection = db[f'{athlete_id}_service']
        collection.create_index([('mileage', pymongo.DESCENDING)])
        collection.create_index([('bike', pymongo.DESCENDING)])
        return collection
