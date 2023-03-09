import os

import pymongo
from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()

first_user = os.getenv('FIRST_USER_ID')
second_user = os.getenv('SECOND_USER_ID')
first_athlete_id = int(os.getenv('FIRST_ATHLETE_ID'))
second_athlete_id = int(os.getenv('SECOND_ATHLETE_ID'))

users_data = {first_user: first_athlete_id,
              second_user: second_athlete_id}


def db_connect(user_id: int):
    client = MongoClient('localhost', 27017)
    db = client['training_db']
    athlete_id = users_data[f'{user_id}']
    collection = db[f'{athlete_id}_training']
    collection.create_index([('athlete.id', pymongo.DESCENDING)])
    return collection


def post_to_db(response: list, user_id: int):
    coll = db_connect(user_id)
    document = response[0]
    if coll.find_one(filter={'id': document['id']}) is None:
        coll.insert_one(document)


def post_to_db_many(list_of_all_training: list, user_id: int) -> str:
    coll = db_connect(user_id)
    count = len(list_of_all_training)
    for i in range(0, count):
        document = list_of_all_training[i]
        if coll.find_one(filter={'id': document['id']}) is None:
            coll.insert_one(document)

    return f'Тренировок успешно загружено – {count}'


def get_last_training(user_id: int):
    coll = db_connect(user_id)
    list_of_date = list(coll.find({}).sort([("start_date_local", -1)]))
    max_date = list_of_date[0]
    return max_date
