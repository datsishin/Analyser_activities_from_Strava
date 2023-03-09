import json
import os

from datetime import datetime
from time import strftime, gmtime

from dotenv import load_dotenv

from connect_mongo_db import get_last_training
from gpx_maker import get_initial_data
from main import get_list_of_activities

# from polyline_file import get_picture

load_dotenv()

user_weight = os.getenv('USER_WEIGHT')

bikes = ['заезд', 'виртуальный заезд', 'ride', 'virtualride']
run = ['забег', 'run']

# Специальный символ для переноса строки внутри f-строк
nl = '\n'


def get_type_of_activity():
    type_of_activity = str.lower(load_data['type'])
    if type_of_activity in bikes:
        return 'Велосипед'
    if type_of_activity in run:
        return 'Бег'
    else:
        return 'Неизвестно 🤷'


def get_heartrate():
    has_heartrate = load_data['has_heartrate']
    if has_heartrate:
        average_heartrate = int(load_data['average_heartrate'])
        max_heartrate = int(load_data['max_heartrate'])
        return average_heartrate, max_heartrate
    else:
        average_heartrate = 'Неизвестно'
        max_heartrate = 'Неизвестно'
        return average_heartrate, max_heartrate


def get_power():
    has_powermeter = load_data['device_watts']
    if has_powermeter:
        weighted_average_watts = int(load_data['weighted_average_watts'])
        average_power = int(load_data['average_watts'])
        max_power = int(load_data['max_watts'])
        relative_power = round(weighted_average_watts / float(user_weight), 1)
        return weighted_average_watts, relative_power, average_power, max_power
    else:
        weighted_average_watts = 'Неизвестно'
        relative_power = 'Неизвестно'
        average_power = 'Неизвестно'
        max_power = 'Неизвестно'
        return weighted_average_watts, relative_power, average_power, max_power


def get_cadence():
    if 'average_cadence' in load_data:
        average_cadence = int(load_data['average_cadence'])
        return average_cadence
    else:
        average_cadence = 'Неизвестно'
        return average_cadence


def get_ratio(check_power, check_hr):
    if check_power[0] and check_hr[0] != 'Неизвестно':
        ratio = round(check_power[0] / check_hr[0], 1)
        return ratio
    else:
        return 'Неизвестно'


def get_energy_spent():
    if 'kilojoules' in load_data:
        check_calories = int(load_data['kilojoules'])
        return check_calories
    else:
        check_calories = 'Неизвестно'
        return check_calories


def generation_analyse(user_id: int):
    get_list_of_activities(user_id)
    global load_data
    load_data = get_last_training(user_id)

    # get_picture(load_data)
    get_initial_data(load_data['id'], user_id)

    for i in range(0, len(load_data)):
        type_of_activity = get_type_of_activity()
        date = datetime.strptime(load_data['start_date_local'], '%Y-%m-%dT%H:%M:%SZ').date()
        distance = round(load_data['distance'] / 1000, 2)
        moving_time = strftime("%H:%M:%S", gmtime(load_data['moving_time']))
        total_elevation_gain = int(load_data['total_elevation_gain'])
        achievement_count = load_data['achievement_count']
        athlete_count = load_data['athlete_count'] - 1
        average_pace = strftime("%M:%S", gmtime((1 / load_data['average_speed'] * 1000)))
        average_speed = round(load_data['average_speed'] * 3.6, 2)
        max_speed = round(load_data['max_speed'] * 3.6, 2)
        elev_high = int(load_data['elev_high'])
        elev_low = int(load_data['elev_low'])
        check_hr = get_heartrate()
        check_calories = get_energy_spent()

        if type_of_activity == 'Велосипед':
            check_power = get_power()
            check_cadence = get_cadence()
            check_ratio = get_ratio(check_power, check_hr)

            item_of_bike = [
                f'📅Дата – {date}{nl}'
                f'🚴🏼‍Вид тренировки – {type_of_activity}{nl}'
                f'⏰Время тренировки – {moving_time}{nl}'
                f'📏Расстояние – {distance}км{nl}'
                f'🏔️Набор высоты – {total_elevation_gain}м{nl}'
                f'⬆️Максимальная высота – {elev_high}м{nl}'
                f'⬇️Минимальная высота – {elev_low}м{nl}'
                f'🎖️Количество наград – {achievement_count}{nl}'
                f'👯Количество других атлетов – {athlete_count}{nl}'
                f'🧁Потрачено калорий – {check_calories}{nl}'
                f'{nl}'

                f'🫀Средний пульс – {check_hr[0]}{nl}'
                f'❤️‍Максимальный пульс – {check_hr[1]}{nl}'
                f'⚖️Удельная мощность – {check_power[1]}{nl}'
                f'💪🏻Усредненная мощность – {check_power[0]}{nl}'
                f'💪Средняя мощность – {check_power[2]}{nl}'
                f'🧨‍Макс. мощность – {check_power[3]}{nl}'
                f'📶Мощность/пульс – {check_ratio}{nl}'
                f'🏎Средняя скорость – {average_speed}км/ч{nl}'
                f'🔝Макс. скорость – {max_speed}км/ч{nl}️'
                f'🔄Средний каденс – {check_cadence}{nl}'
            ]

            return item_of_bike

        if type_of_activity == 'Бег':
            item_of_run = [f'📅Дата – {date}{nl}'
                           f"🏃🏼‍‍Вид тренировки – {type_of_activity}{nl}"
                           f"📏Расстояние – {distance}км{nl}"
                           f"⏰Время тренировки – {moving_time}{nl}"
                           f"🏔️Набор высоты – {total_elevation_gain}м{nl}"
                           f"🎖️Количество наград – {achievement_count}{nl}"
                           f"👯Количество других атлетов – {athlete_count}{nl}"
                           f"🏎Средняя темп – {average_pace}{nl}"
                           f'🫀Средний пульс – {check_hr[0]}{nl}'
                           f'❤️‍Максимальный пульс – {check_hr[1]}{nl}'
                           f'⬆️Максимальная высота – {elev_high}м{nl}'
                           f'⬇️Минимальная высота – {elev_low}м{nl}'
                           f'🧁Потрачено калорий – {check_calories}{nl}']

            return item_of_run
