import json
import os

import requests as r
from dotenv import load_dotenv

from hr_analyser import get_hr_statistics
from power_analyser import get_power_statistics

load_dotenv()

first_user = os.getenv('FIRST_USER_ID')
second_user = os.getenv('SECOND_USER_ID')

users_data = {first_user: {'token': os.getenv('FIRST_ACCESS_TOKEN')},
              second_user: {'token': os.getenv('SECOND_ACCESS_TOKEN')}}


def get_initial_data(id: int, user_id: int):
    url = f'https://www.strava.com/api/v3/activities/{id}/streams'
    token = users_data[f'{user_id}']['token']
    header = {'Authorization': 'Bearer ' + token}
    heartrate = {'keys': 'heartrate'}
    power = {'keys': 'watts'}

    response_hr = r.get(url, headers=header, params=heartrate).json()
    response_power = r.get(url, headers=header, params=power).json()

    for i in range(1, len(response_hr)):
        if response_hr[i]['type'] == 'heartrate':
            hr_data = list(response_hr)[i]['data']
            get_hr_statistics(hr_data, user_id)
            break

    for i in range(0, len(response_power)):
        if response_power[i]['type'] == 'watts':
            power_data = list(response_power)[i]['data']
            get_power_statistics(power_data, user_id)
            break
