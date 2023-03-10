import requests as r
from processors.hr_analyser import get_hr_statistics
from processors.power_analyser import get_power_statistics
from main import status_code_checker
from users import users_data


def get_initial_data(id: int, user_id: int):
    url = f'https://www.strava.com/api/v3/activities/{id}/streams'
    token = users_data[f'{user_id}']['access_token']
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
