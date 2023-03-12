import requests as r
from datetime import datetime, timedelta
from db.training import post_many_training
from db.mongo import db_connect
from main import status_code_checker
from processors.graph_creater import make_TSS_graph
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

    post_many_training(list_of_training, user_id)
    return list_of_training


def get_stats(user_id: int):
    data = list(db_connect(user_id, param='training').find({}))

    if not data:
        return 'Данных нет, загрузите все тренировки'

    today = datetime.now().date()
    week_total_seconds = 0
    month_total_seconds = 0
    year_total_seconds = 0
    total_seconds = 0
    week_TSS = 0
    six_weeks_TSS = 0

    for i in range(0, len(data)):
        date_of_activity = datetime.strptime(data[i]['start_date_local'], '%Y-%m-%dT%H:%M:%SZ').date()

        if today - date_of_activity <= timedelta(days=7):
            week_total_seconds += data[i]['moving_time']
            month_total_seconds += data[i]['moving_time']
            year_total_seconds += data[i]['moving_time']
            total_seconds += data[i]['moving_time']
            power = type_of_activity_checker(data[i])

            if power:
                moving_time = data[i]['moving_time']
                week_TSS += calc_TSS(power, moving_time, user_id)
                six_weeks_TSS += week_TSS

        if timedelta(days=7) < today - date_of_activity <= timedelta(days=31):
            month_total_seconds += data[i]['moving_time']
            year_total_seconds += data[i]['moving_time']
            total_seconds += data[i]['moving_time']

            power = type_of_activity_checker(data[i])
            if power:
                moving_time = data[i]['moving_time']
                six_weeks_TSS += calc_TSS(power, moving_time, user_id)

        if timedelta(days=31) < today - date_of_activity <= timedelta(days=42):
            year_total_seconds += data[i]['moving_time']
            total_seconds += data[i]['moving_time']

            power = type_of_activity_checker(data[i])
            if power:
                moving_time = data[i]['moving_time']
                six_weeks_TSS += calc_TSS(power, moving_time, user_id)

        if timedelta(days=42) < today - date_of_activity <= timedelta(days=365):
            year_total_seconds += data[i]['moving_time']
            total_seconds += data[i]['moving_time']
        else:
            total_seconds += data[i]['moving_time']

    week_total_time = str(timedelta(seconds=week_total_seconds))
    month_total_time = str(timedelta(seconds=month_total_seconds))
    year_total_time = str(timedelta(seconds=year_total_seconds))
    total_seconds_time = str(timedelta(seconds=total_seconds))

    avg_week_TSS = round(week_TSS / 7, 0)
    avg_six_weeks_TSS = round(six_weeks_TSS / 42, 0)
    TBS = avg_six_weeks_TSS - avg_week_TSS

    response_list = [week_total_time, month_total_time, year_total_time,
                     total_seconds_time, avg_week_TSS, avg_six_weeks_TSS, TBS]

    return response_list


def get_full_stats(user_id: int) -> str:
    list_of_all_training = get_list_of_training(user_id)
    return post_many_training(list_of_all_training, user_id)


def type_of_activity_checker(data: dict):
    if 'weighted_average_watts' in data:
        return data['weighted_average_watts']

    elif 'average_watts' in data:
        return data['average_watts']


def calc_TSS(power: int, moving_time: int, user_id: int):
    ftp = int(users_data[f'{user_id}']['ftp'])
    tss = round((power ** 2 * moving_time) / (ftp ** 2 * 3600) * 100, 1)
    return tss


def get_TSS_diagram(user_id: int):
    list_of_date = []
    list_of_TSS = []
    list_of_all_training = get_list_of_training(user_id)

    for i in range(0, len(list_of_all_training)):
        if list_of_all_training[i]['type'] in ['VirtualRide', 'Ride']:
            power = type_of_activity_checker(list_of_all_training[i])
            if power:
                moving_time = list_of_all_training[i]['moving_time']
                date_of_activity = datetime.strptime(list_of_all_training[i]['start_date_local'],
                                                     '%Y-%m-%dT%H:%M:%SZ').date()
                TSS = calc_TSS(power, moving_time, user_id)
                list_of_date.append(date_of_activity)
                list_of_TSS.append(TSS)
            pass
        pass

    return make_TSS_graph(list_of_date, list_of_TSS)

# if __name__ == '__main__':
#     get_TSS_diagram(666785382)
