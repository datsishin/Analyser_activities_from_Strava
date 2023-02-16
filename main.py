import json
import os
import time

import dotenv
import requests
from dotenv import load_dotenv

load_dotenv()

url = 'https://www.strava.com/api/v3/athlete/activities'
url_refresh_token = 'https://www.strava.com/oauth/token'
token = os.getenv('ACCESS_TOKEN')
refresh_token = os.getenv('REFRESH_TOKEN')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_fresh_api_token():
    data = {'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'}
    response = requests.post(url_refresh_token, data=data).json()
    new_access_token = response['access_token']
    dotenv.set_key('.env', 'ACCESS_TOKEN', new_access_token, quote_mode='never')


def get_mileage_for_service():
    params = {'access_token': token}
    bike_id = os.getenv('BIKE_ID')
    bike_url = f'https://www.strava.com/api/v3/gear/{bike_id}'
    r = requests.get(bike_url, params=params)
    status = r.status_code
    while True:
        if status == 401:
            print("API TOKEN is expired, I'll go for a new one...")
            get_fresh_api_token()
            return 'API TOKEN is expired, try other command first'

        if status == 200:
            if os.path.isfile('mileage.json'):
                with open('mileage.json', 'r', encoding='utf-8') as file:
                    load_data = json.load(file)
                    fresh_mileage = load_data['converted_distance']
                    if load_data['converted_distance'] == fresh_mileage:
                        return f"Пробег составляет {load_data['converted_distance']}км"
                    else:
                        increasing_mileage = fresh_mileage - load_data['converted_distance']
                        load_data['converted_distance'] = fresh_mileage
                        with open("mileage.json", "w") as f:
                            json.dump(load_data, f)
                        return f"Пробег с последнего обновления увеличился на" \
                               f" {increasing_mileage}км и составляет {load_data['converted_distance']}км"

            else:
                with open("mileage.json", "w") as file:
                    json.dump(r.json(), file)
                return f'Данные загружены, повторите запрос'


def get_list_of_activities():
    params = {'access_token': token}
    r = requests.get(url, params=params)
    status = r.status_code
    while True:
        if status == 429:
            print("Too many requests, slow down dude and try again later!")
            time.sleep(2)
            return False

        if status == 401:
            print("API TOKEN is expired, I'll go for a new one...")
            get_fresh_api_token()
            time.sleep(3)
            return False

        if r.status_code == 403:
            raise Exception("VPN isn't work :(")

        if r.status_code == 200:
            data = r.json()
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return False
