import os
from dotenv import load_dotenv

load_dotenv()

global nl
nl = '\n'

first_user = os.getenv('FIRST_USER_ID')
second_user = os.getenv('SECOND_USER_ID')

users_data = {first_user: {'client_id': os.getenv('FIRST_CLIENT_ID'),
                           'athlete_id': os.getenv('FIRST_ATHLETE_ID'),
                           'access_token': os.getenv('FIRST_ACCESS_TOKEN'),
                           'refresh_token': os.getenv('FIRST_REFRESH_TOKEN'),
                           'client_secret': os.getenv('FIRST_CLIENT_SECRET'),
                           'user_weight': os.getenv('FIRST_USER_WEIGHT'),
                           'hr_max': os.getenv('FIRST_USER_HRMAX'),
                           'threshold': os.getenv('FIRST_USER_THRESHOLD'),
                           'ftp': os.getenv('FIRST_USER_FTP'),
                           'weight': os.getenv('FIRST_USER_WEIGHT'),
                           'bike': os.getenv('FIRST_USER_BIKE_ID')},
              second_user: {'client_id': os.getenv('SECOND_CLIENT_ID'),
                            'athlete_id': os.getenv('SECOND_ATHLETE_ID'),
                            'access_token': os.getenv('SECOND_ACCESS_TOKEN'),
                            'refresh_token': os.getenv('SECOND_REFRESH_TOKEN'),
                            'client_secret': os.getenv('SECOND_CLIENT_SECRET'),
                            'user_weight': os.getenv('SECOND_USER_WEIGHT'),
                            'hr_max': os.getenv('SECOND_USER_HRMAX'),
                            'threshold': os.getenv('SECOND_USER_THRESHOLD'),
                            'ftp': os.getenv('SECOND_USER_FTP')}}
