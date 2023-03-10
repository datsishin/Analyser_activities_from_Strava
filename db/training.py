from main import get_last_activity
from db.mongo import db_connect

# Специальный символ для переноса строки внутри f-строк
nl = '\n'


def post_training(response: list, user_id: int):
    coll = db_connect(user_id, param='training')
    document = response[0]
    if coll.find_one(filter={'id': document['id']}) is None:
        coll.insert_one(document)


def post_many_training(list_of_all_training: list, user_id: int) -> str:
    coll = db_connect(user_id, param='training')
    count = len(list_of_all_training)
    for i in range(0, count):
        document = list_of_all_training[i]
        if coll.find_one(filter={'id': document['id']}) is None:
            coll.insert_one(document)

    return f'Тренировок успешно загружено – {count}'


def get_last_training(user_id: int):
    response = get_last_activity(user_id)

    coll = db_connect(user_id, param='training')
    list_of_date = coll.find().sort("start_date_local", -1).limit(1)
    max_date = list(list_of_date)

    if max_date:
        if response[0]['id'] == max_date[0]['id']:
            return max_date
        return response
    return response
