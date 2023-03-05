import json
import os

import dotenv
import requests as r
from dotenv import load_dotenv

from connect_mongo_db import post_to_db

load_dotenv()

# Специальный символ для переноса строк внутри f-строк
nl = '\n'

first_user = os.getenv('FIRST_USER_ID')
second_user = os.getenv('SECOND_USER_ID')

client_data = {first_user: {'client_id': os.getenv('FIRST_CLIENT_ID'),
                            'access_token': os.getenv('FIRST_ACCESS_TOKEN'),
                            'refresh_token': os.getenv('FIRST_REFRESH_TOKEN'),
                            'client_secret': os.getenv('FIRST_CLIENT_SECRET')},
               second_user: {'client_id': os.getenv('SECOND_CLIENT_ID'),
                             'access_token': os.getenv('SECOND_ACCESS_TOKEN'),
                             'refresh_token': os.getenv('SECOND_REFRESH_TOKEN'),
                             'client_secret': os.getenv('SECOND_CLIENT_SECRET')}}


def get_fresh_api_token(user_id: int):
    url_refresh_token = 'https://www.strava.com/oauth/token'

    data = {'client_id': client_data[f'{user_id}']['client_id'],
            'client_secret': client_data[f'{user_id}']['client_secret'],
            'refresh_token': client_data[f'{user_id}']['refresh_token'],
            'grant_type': 'refresh_token'}

    response = r.post(url_refresh_token, data=data).json()
    new_access_token = response['access_token']
    if str(user_id) == first_user:
        dotenv.set_key('.env', 'FIRST_ACCESS_TOKEN', new_access_token, quote_mode='never')
        return new_access_token
    elif str(user_id) == second_user:
        dotenv.set_key('.env', 'SECOND_ACCESS_TOKEN', new_access_token, quote_mode='never')
        return new_access_token


def check_change_of_mileage(new_mileage: int) -> str:
    if os.path.exists('data/mileage.json'):
        with open('data/mileage.json', 'r+', encoding='utf-8') as file:
            load_data = json.load(file)
            mileage = load_data['converted_distance']
            if mileage != new_mileage:
                dif_mileage = new_mileage - mileage
                data = {'converted_distance': new_mileage}
                with open('data/mileage.json', 'w') as new_file:
                    json.dump(data, new_file)
                return f'Старый пробег составлял – {mileage} км{nl}{nl}' \
                       f'Пробег увеличился на – {dif_mileage} км{nl}{nl}' \
                       f'Общий пробег составляет – {new_mileage} км'
            else:
                return f'Общий пробег составляет – {mileage} км'
    else:
        data = {'converted_distance': new_mileage}
        with open("data/mileage.json", "w") as file:
            json.dump(data, file)
        return f'Общий пробег составляет – {new_mileage} км'


def get_mileage_for_service():
    token = os.getenv('ACCESS_TOKEN')
    bike_id = os.getenv('BIKE_ID')
    url_bike = f'https://www.strava.com/api/v3/gear/{bike_id}'
    params = {'access_token': token}

    first_data = status_code_checker(url_bike, params)
    if type(first_data) == dict:
        new_mileage = int(first_data['converted_distance'])
        return check_change_of_mileage(new_mileage)
    else:
        params = {'access_token': first_data}
        data = status_code_checker(url_bike, params)
        if type(data) == dict:
            new_mileage = int(data['converted_distance'])
            return check_change_of_mileage(new_mileage)


def get_list_of_activities(user_id: int):
    url = 'https://www.strava.com/api/v3/athlete/activities'
    token = client_data[f'{user_id}']['access_token']
    params = {'access_token': token}

    first_data = status_code_checker(url, params, user_id)

    if type(first_data) == list:
        post_to_db(first_data)
        # with open('data/data.json', 'w') as first_file:
        #     json.dump(first_data, first_file)

    else:
        params = {'access_token': first_data}
        data = status_code_checker(url, params, user_id)
        if type(data) == list:
            with open('data/data.json', 'w') as file:
                json.dump(data, file)


def status_code_checker(url, params, user_id: int):
    response = r.get(url, params=params)
    status = response.status_code

    while True:

        if status == 200:
            return response.json()

        elif status == 401:
            return get_fresh_api_token(user_id)

        elif status == 403:
            print('VPN isn\'t connect')

        elif status == 404:
            print('Not found')

        elif status == 429:
            print('Too many requests, slow down dude!')

        elif status == 500:
            print("Strava's API is broken, please try again later")
