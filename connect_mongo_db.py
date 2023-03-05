import os

import pymongo
from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()
client = MongoClient('localhost', 27017)

db = client['training_db']
collection = db['training']

first_user = os.getenv('FIRST_USER_ID')
second_user = os.getenv('SECOND_USER_ID')
first_athlete_id = int(os.getenv('FIRST_ATHLETE_ID'))
second_athlete_id = int(os.getenv('SECOND_ATHLETE_ID'))


def post_to_db(first_data: list):
    document = first_data[0]
    if collection.find_one(filter={'id': document['id']}) is None:
        collection.insert_one(document)


def get_last_training(user_id: int):
    users_data = {first_user: first_athlete_id,
                  second_user: second_athlete_id}
    return collection.find_one({'athlete.id': users_data[f'{user_id}']}, sort=[('_id', pymongo.DESCENDING)])

