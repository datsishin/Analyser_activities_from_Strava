import os
import requests as r
from dotenv import load_dotenv
from hr_analyser import get_hr_statistics
from main import get_fresh_api_token, status_code_checker
from power_analyser import get_power_statistics

load_dotenv()


def get_initial_data(id: int, user_id: int):
    first_user = os.getenv('FIRST_USER_ID')
    second_user = os.getenv('SECOND_USER_ID')

    users_data = {first_user: {'token': os.getenv('FIRST_ACCESS_TOKEN')},
                  second_user: {'token': os.getenv('SECOND_ACCESS_TOKEN')}}

    url = f'https://www.strava.com/api/v3/activities/{id}/streams'
    token = users_data[f'{user_id}']['token']
    headers = {'Authorization': 'Bearer ' + token}
    params = {'access_token': token}
    heartrate = {'keys': 'heartrate'}
    power = {'keys': 'watts'}

    response = status_code_checker(url, params, user_id)

    if type(response) == str:
        new_token = response
        headers['Authorization'] = f'Bearer ' + new_token

    response_hr = r.get(url, headers=headers, params=heartrate).json()
    response_power = r.get(url, headers=headers, params=power).json()
    processing_data(response_hr, response_power, user_id)


def processing_data(response_hr: list, response_power: list, user_id: int):
    for i in range(0, len(response_hr)):
        if response_hr[i]['type'] == 'heartrate':
            hr_data = list(response_hr)[i]['data']
            get_hr_statistics(hr_data, user_id)
            break

    for i in range(0, len(response_power)):
        if response_power[i]['type'] == 'watts':
            power_data = list(response_power)[i]['data']
            get_power_statistics(power_data, user_id)
            break
