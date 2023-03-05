import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import requests as r

load_dotenv()

url = 'https://www.strava.com/api/v3/athlete/activities'

first_user = os.getenv('FIRST_USER_ID')
second_user = os.getenv('SECOND_USER_ID')

users_data = {first_user: {'token': os.getenv('FIRST_ACCESS_TOKEN')},
              second_user: {'token': os.getenv('SECOND_ACCESS_TOKEN')}}


def get_count_of_training(user_id: int):
    token = users_data[f'{user_id}']['token']
    headers = {'Authorization': 'Bearer ' + token}
    params = {'per_page': 200,
              'page': 1}

    today = datetime.now().date()
    week_total_seconds = 0
    month_total_seconds = 0
    year_total_seconds = 0

    while True:
        response = r.get(url, params=params, headers=headers).json()

        if len(response) != 0:
            for i in range(0, len(response)):
                date_of_activity = datetime.strptime(response[i]['start_date_local'], '%Y-%m-%dT%H:%M:%SZ').date()
                if today - date_of_activity <= timedelta(days=7):
                    week_total_seconds += response[i]['moving_time']
                    month_total_seconds += response[i]['moving_time']
                    year_total_seconds += response[i]['moving_time']
                if timedelta(days=7) < today - date_of_activity <= timedelta(days=31):
                    month_total_seconds += response[i]['moving_time']
                    year_total_seconds += response[i]['moving_time']
                if timedelta(days=31) < today - date_of_activity <= timedelta(days=365):
                    year_total_seconds += response[i]['moving_time']

            new_page = params['page'] + 1
            params['page'] = new_page

        break

    week_total_time = str(timedelta(seconds=week_total_seconds))
    month_total_time = str(timedelta(seconds=month_total_seconds))
    year_total_time = str(timedelta(seconds=year_total_seconds))
    list_of_time = [week_total_time, month_total_time, year_total_time]

    return list_of_time
