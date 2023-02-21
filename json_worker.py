import json
import os
import time
from datetime import datetime, timedelta
from time import strftime, gmtime

from dotenv import load_dotenv

from hr_analyser import get_data_by_hr
from power_analyser import get_data_by_power
from main import get_list_of_activities
from polyline_file import get_picture

load_dotenv()

user_weight = os.getenv('USER_WEIGHT')

bikes = ['заезд', 'виртуальный заезд', 'ride', 'virtualride']
run = ['забег', 'run']

nl = '\n'


def get_stat():
    get_list_of_activities()

    global load_data
    with open('data/data.json') as f:
        load_data = json.load(f)

    today = datetime.now().date()
    week_total_seconds = 0
    month_total_seconds = 0
    for i in range(0, len(load_data)):
        date_of_activity = datetime.strptime(load_data[i]['start_date_local'], '%Y-%m-%dT%H:%M:%SZ').date()
        if today - date_of_activity < timedelta(days=7):
            week_total_seconds += load_data[i]['moving_time']
            month_total_seconds += load_data[i]['moving_time']
        if timedelta(days=7) < today - date_of_activity < timedelta(days=31):
            month_total_seconds += load_data[i]['moving_time']

    week_total_time = str(timedelta(seconds=week_total_seconds))
    month_total_time = str(timedelta(seconds=month_total_seconds))
    list_of_time = [week_total_time, month_total_time]
    return list_of_time


def get_type_of_activity():
    type_of_activity = str.lower(load_data[0]['type'])
    if type_of_activity in bikes:
        return 'Велосипед'
    if type_of_activity in run:
        return 'Бег'
    else:
        return 'Неизвестно 🤷'


def get_heartrate():
    has_heartrate = load_data[0]['has_heartrate']
    if has_heartrate:
        average_heartrate = int(load_data[0]['average_heartrate'])
        max_heartrate = int(load_data[0]['max_heartrate'])
        return average_heartrate, max_heartrate
    else:
        average_heartrate = 'Неизвестно'
        max_heartrate = 'Неизвестно'
        return average_heartrate, max_heartrate


def get_power():
    has_powermeter = load_data[0]['device_watts']
    if has_powermeter:
        weighted_average_watts = int(load_data[0]['weighted_average_watts'])
        average_power = int(load_data[0]['average_watts'])
        max_power = int(load_data[0]['max_watts'])
        relative_power = round(weighted_average_watts / float(user_weight), 1)
        return weighted_average_watts, relative_power, average_power, max_power
    else:
        weighted_average_watts = 'Неизвестно'
        relative_power = 'Неизвестно'
        average_power = 'Неизвестно'
        max_power = 'Неизвестно'
        return weighted_average_watts, relative_power, average_power, max_power


def get_cadence():
    if 'average_cadence' in load_data[0]:
        average_cadence = int(load_data[0]['average_cadence'])
        return average_cadence
    else:
        average_cadence = 'Неизвестно'
        return average_cadence


def get_energy_spent():
    if 'kilojoules' in load_data[0]:
        check_calories = int(load_data[0]['kilojoules'])
        return check_calories
    else:
        check_calories = 'Неизвестно'
        return check_calories


def generation_analyse():
    get_data_by_hr()
    get_data_by_power()
    get_list_of_activities()

    global load_data
    with open('data/data.json') as f:
        load_data = json.load(f)
    get_picture(load_data[0])

    for i in range(0, len(load_data)):
        type_of_activity = get_type_of_activity()
        date = datetime.strptime(load_data[0]['start_date_local'], '%Y-%m-%dT%H:%M:%SZ').date()
        distance = round(load_data[0]['distance'] / 1000, 2)
        moving_time = strftime("%H:%M:%S", gmtime(load_data[0]['moving_time']))
        total_elevation_gain = int(load_data[0]['total_elevation_gain'])
        achievement_count = load_data[0]['achievement_count']
        athlete_count = load_data[0]['athlete_count'] - 1
        average_pace = strftime("%M:%S", gmtime((1 / load_data[0]['average_speed'] * 1000)))
        average_speed = round(load_data[0]['average_speed'] * 3.6, 2)
        max_speed = round(load_data[0]['max_speed'] * 3.6, 2)
        elev_high = int(load_data[0]['elev_high'])
        elev_low = int(load_data[0]['elev_low'])
        check_heartrate = get_heartrate()
        check_calories = get_energy_spent()

        if type_of_activity == 'Велосипед':
            check_power = get_power()
            check_cadence = get_cadence()

            item_of_bike = [f'📅Дата – {date}{nl}'
                            f'🚴🏼‍Вид тренировки – {type_of_activity}{nl}'
                            f'📏Расстояние – {distance}км{nl}'
                            f'⏰Время тренировки – {moving_time}{nl}'
                            f'🏔️Набор высоты – {total_elevation_gain}м{nl}'
                            f'🎖️Количество наград – {achievement_count}{nl}'
                            f'👯Количество других атлетов – {athlete_count}{nl}'
                            f'🏎Средняя скорость – {average_speed}км/ч{nl}'
                            f'🔝Макс. скорость – {max_speed}км/ч{nl}️'
                            f'🫀Средний пульс – {check_heartrate[0]}{nl}'
                            f'❤️‍Максимальный пульс – {check_heartrate[1]}{nl}'
                            f'⚖️Удельная мощность – {check_power[1]}{nl}'
                            f'💪Средняя мощность – {check_power[2]}{nl}'
                            f'🧨‍Макс. мощность – {check_power[3]}{nl}'
                            f'🔄Средний каденс – {check_cadence}{nl}'
                            f'⬆️Максимальная высота – {elev_high}м{nl}'
                            f'⬇️Минимальная высота – {elev_low}м{nl}'
                            f'🧁Потрачено калорий – {check_calories}{nl}']

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
                           f'🫀Средний пульс – {check_heartrate[0]}{nl}'
                           f'❤️‍Максимальный пульс – {check_heartrate[1]}{nl}'
                           f'⬆️Максимальная высота – {elev_high}м{nl}'
                           f'⬇️Минимальная высота – {elev_low}м{nl}'
                           f'🧁Потрачено калорий – {check_calories}{nl}']

            return item_of_run
