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
    collection = db[f'{users_data[f"{user_id}"]}_training']
    return collection


def post_to_db(first_data: list, user_id: int):
    coll = db_connect(user_id)
    document = first_data[0]
    if coll.find_one(filter={'id': document['id']}) is None:
        coll.insert_one(document)


def get_last_training(user_id: int):
    coll = db_connect(user_id)
    return coll.find_one({'athlete.id': users_data[f'{user_id}']}, sort=[('_id', pymongo.DESCENDING)])


# if __name__ == '__main__':
#     db_connect(666785382)
