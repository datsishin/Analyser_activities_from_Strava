import requests as r
from datetime import datetime, timedelta
from db.worker import post_to_db_many
from db.mongo import db_connect
from main import status_code_checker
from users import users_data

url = 'https://www.strava.com/api/v3/athlete/activities'


def get_list_of_training(user_id: int) -> list:
    token = users_data[f'{user_id}']['access_token']
    params = {'access_token': token,
              'per_page': 200,
              'page': 1}
    response = status_code_checker(url, params, user_id)

    if type(response) == str:
        new_token = response
        params['access_token'] = new_token

    list_of_training = []

    while True:
        response = r.get(url, params=params).json()
        count = len(response)
        if count != 0:
            for i in range(0, count):
                list_of_training.append(response[i])

            next_page = params['page'] + 1
            params['page'] = next_page
        if count == 0:
            break

    post_to_db_many(list_of_training, user_id)
    return list_of_training


def get_volume_stats(user_id: int) -> list:
    data = list(db_connect(user_id, param='training').find({}))

    today = datetime.now().date()
    week_total_seconds = 0
    month_total_seconds = 0
    year_total_seconds = 0
    total_seconds = 0

    for i in range(0, len(data)):
        date_of_activity = datetime.strptime(data[i]['start_date_local'], '%Y-%m-%dT%H:%M:%SZ').date()
        if today - date_of_activity <= timedelta(days=7):
            week_total_seconds += data[i]['moving_time']
            month_total_seconds += data[i]['moving_time']
            year_total_seconds += data[i]['moving_time']
            total_seconds += data[i]['moving_time']
        if timedelta(days=7) < today - date_of_activity <= timedelta(days=31):
            month_total_seconds += data[i]['moving_time']
            year_total_seconds += data[i]['moving_time']
            total_seconds += data[i]['moving_time']
        if timedelta(days=31) < today - date_of_activity <= timedelta(days=365):
            year_total_seconds += data[i]['moving_time']
            total_seconds += data[i]['moving_time']
        else:
            total_seconds += data[i]['moving_time']

    week_total_time = str(timedelta(seconds=week_total_seconds))
    month_total_time = str(timedelta(seconds=month_total_seconds))
    year_total_time = str(timedelta(seconds=year_total_seconds))
    total_seconds_time = str(timedelta(seconds=total_seconds))
    list_of_time = [week_total_time, month_total_time, year_total_time, total_seconds_time]

    return list_of_time


def get_full_stats(user_id: int) -> str:
    list_of_all_training = get_list_of_training(user_id)
    return post_to_db_many(list_of_all_training, user_id)
