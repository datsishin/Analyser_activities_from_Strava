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


def check_api_limit():
    pass


def get_fresh_api_token():
    data = {'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'}
    response = requests.post(url_refresh_token, data=data).json()
    new_access_token = response['access_token']
    os.environ['ACCESS_TOKEN'] = new_access_token
    dotenv.set_key('.env', 'ACCESS_TOKEN', new_access_token)


def get_list_of_activities():
    while True:
        params = {'access_token': token}
        r = requests.get(url, params=params)
        status = r.status_code
        if status == 429:
            print("Too many requests, slow down dude!")
            time.sleep(2)

        if status == 401:
            print("API TOKEN is expired, I'll go for a new one...")
            get_fresh_api_token()
            time.sleep(2)

        if r.status_code == 403:
            raise Exception("VPN isn't work :(")

        if r.status_code == 200:
            data = r.json()
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return False


if __name__ == '__main__':
    get_list_of_activities()
