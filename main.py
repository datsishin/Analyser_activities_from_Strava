import os

import dotenv
import requests as r

from service import check_mileage
from users import users_data, first_user, second_user


def get_fresh_api_token(user_id: int):
    url_refresh_token = 'https://www.strava.com/oauth/token'

    data = {'client_id': users_data[f'{user_id}']['client_id'],
            'client_secret': users_data[f'{user_id}']['client_secret'],
            'refresh_token': users_data[f'{user_id}']['refresh_token'],
            'grant_type': 'refresh_token'}

    response = r.post(url_refresh_token, data=data).json()
    new_access_token = response['access_token']
    if str(user_id) == first_user:
        dotenv.set_key('.env', 'FIRST_ACCESS_TOKEN', new_access_token, quote_mode='never')
        return new_access_token
    elif str(user_id) == second_user:
        dotenv.set_key('.env', 'SECOND_ACCESS_TOKEN', new_access_token, quote_mode='never')
        return new_access_token


def get_mileage(user_id: int) -> list:
    if str(user_id) == first_user:
        token = users_data[f'{user_id}']['access_token']
        bike_id = os.getenv('FIRST_USER_BIKE_ID')
        url_bike = f'https://www.strava.com/api/v3/gear/{bike_id}'
        params = {'access_token': token}

        data = status_code_checker(url_bike, params, user_id)
        if type(data) == dict:
            name = data['name']
            new_mileage = int(data['converted_distance'])
            return check_mileage(name, new_mileage, user_id)

        else:
            params = {'access_token': data}
            data = status_code_checker(url_bike, params, user_id)
            if type(data) == dict:
                name = data['name']
                new_mileage = int(data['converted_distance'])
                return check_mileage(name, new_mileage, user_id)

    return 'Нет данных по статистике оборудования'


def get_last_activity(user_id: int):
    url = 'https://www.strava.com/api/v3/athlete/activities'
    token = users_data[f'{user_id}']['access_token']
    params = {'access_token': token,
              'per_page': 200,
              'page': 1}

    response = status_code_checker(url, params, user_id)
    if type(response) == list:
        return response

    else:
        params = {'access_token': response}
        response = status_code_checker(url, params, user_id)
        if type(response) == list:
            return response


def status_code_checker(url, params, user_id):
    response = r.get(url, params=params)
    status = response.status_code

    while True:

        if status == 200:
            return response.json()

        elif status == 401:
            return get_fresh_api_token(user_id)

        elif status == 403:
            print('VPN isn\'t connect')
            break

        elif status == 404:
            print('Not found')

        elif status == 429:
            print('Too many requests, slow down dude!')

        elif status == 500:
            print("Strava's API is broken, please try again later")
