import json
import os
from datetime import datetime as dt
from time import strftime, gmtime, strptime
from dotenv import load_dotenv

load_dotenv()

user_weight = os.getenv('USER_WEIGHT')

bikes = ['заезд', 'виртуальный заезд', 'ride', 'virtualride']
run = ['забег', 'run']

"""
Здесь позже будет отсев по оборудованию,
 так как нет смысла брать стату по городскому велосипеду
 
# equipment = {'b11325507' :
#              }
"""

file = open('data.json')
load_data = json.load(file)

nl = '\n'


def get_type_of_activity(i):
    type_of_activity = str.lower(load_data[i]['type'])
    if type_of_activity in bikes:
        return 'Велосипед'
    if type_of_activity in run:
        return 'Бег'
    else:
        return 'Неизвестно 🤷'


def get_heartrate(i):
    has_heartrate = load_data[i]['has_heartrate']
    if has_heartrate:
        average_heartrate = int(load_data[i]['average_heartrate'])
        max_heartrate = int(load_data[i]['max_heartrate'])
        return average_heartrate, max_heartrate
    else:
        average_heartrate = 'Неизвестно'
        max_heartrate = 'Неизвестно'
        return average_heartrate, max_heartrate


def get_power(i):
    has_powermeter = load_data[i]['device_watts']
    if has_powermeter:
        weighted_average_watts = int(load_data[i]['weighted_average_watts'])
        average_power = int(load_data[i]['average_watts'])
        max_power = int(load_data[i]['max_watts'])
        relative_power = round(weighted_average_watts / float(user_weight), 1)
        return weighted_average_watts, relative_power, average_power, max_power
    else:
        weighted_average_watts = 'Неизвестно'
        relative_power = 'Неизвестно'
        average_power = 'Неизвестно'
        max_power = 'Неизвестно'
        return weighted_average_watts, relative_power, average_power, max_power


def get_cadence(i):
    if 'average_cadence' in load_data[i]:
        average_cadence = int(load_data[i]['average_cadence'])
        return average_cadence
    else:
        average_cadence = 'Неизвестно'
        return average_cadence


def get_energy_spent(i):
    if 'kilojoules' in load_data[i]:
        check_calories = int(load_data[i]['kilojoules'])
        return check_calories
    else:
        check_calories = 'Неизвестно'
        return check_calories


def generation_analyse():
    statistics = []
    for i in range(0, len(load_data)):
        type_of_activity = get_type_of_activity(i)
        date = dt.strptime(load_data[i]['start_date_local'], '%Y-%m-%dT%H:%M:%SZ').date()
        distance = round(load_data[i]['distance'] / 1000, 2)
        moving_time = strftime("%H:%M:%S", gmtime(load_data[i]['moving_time']))
        total_elevation_gain = int(load_data[i]['total_elevation_gain'])
        achievement_count = load_data[i]['achievement_count']
        athlete_count = load_data[i]['athlete_count'] - 1
        average_speed = round(load_data[i]['average_speed'] * 3.6, 2)
        max_speed = round(load_data[i]['max_speed'] * 3.6, 2)
        elev_high = int(load_data[i]['elev_high'])
        elev_low = int(load_data[i]['elev_low'])
        check_heartrate = get_heartrate(i)
        check_calories = get_energy_spent(i)

        if type_of_activity == 'Велосипед':
            check_power = get_power(i)
            check_cadence = get_cadence(i)

            item = [f'📅Дата – {date}{nl}'
                    f'🚴🏼‍Вид тренировки – {type_of_activity}{nl}'
                    f'📏Расстояние – {distance}км{nl}'
                    f'⏰Продолжительность тренировки – {moving_time}{nl}'
                    f'🏔️Суммарный набор высоты – {total_elevation_gain}м{nl}'
                    f'🎖️Количество наград – {achievement_count}{nl}'
                    f'👯Количество других участников – {athlete_count}{nl}'
                    f'🏎Средняя скорость – {average_speed}км/ч{nl}'
                    f'🔝Максимальная скорость – {max_speed}км/ч{nl}️'
                    f'🫀Средний пульс – {check_heartrate[0]}{nl}'
                    f'❤️‍Максимальный пульс – {check_heartrate[1]}{nl}'
                    f'🔋Средневзвешенная мощность – {check_power[0]}{nl}'
                    f'⚖️Удельная мощность – {check_power[1]}{nl}'
                    f'💪Средняя мощность – {check_power[2]}{nl}'
                    f'🧨‍Максимальная мощность – {check_power[3]}{nl}'
                    f'🔄Средний каденс – {check_cadence}{nl}'
                    f'⬆️Максимальная высота – {elev_high}м{nl}'
                    f'⬇️Минимальная высота – {elev_low}м{nl}'
                    f'🧁Потрачено калорий – {check_calories}{nl}']

            statistics.extend(item)
    # print(statistics)
        # ниже код выводит информацию если вид тренировки "Бег"
        if type_of_activity == 'Бег':
            item_of_run = f'📅Дата – {date}{nl}'
            f"🏃🏼‍‍Вид тренировки – {type_of_activity}{nl}"
            f"📏Расстояние – {distance}км{nl}"
            f"⏰Продолжительность тренировки – {moving_time}{nl}"
            f"🏔️Суммарный набор высоты – {total_elevation_gain}м{nl}"
            f"🎖️Количество наград – {achievement_count}{nl}"
            f"👯Количество других участников – {athlete_count}{nl}"
            f"🏎Средняя скорость – {average_speed}км/ч{nl}"
            f'🔝Максимальная скорость – {max_speed}км/ч{nl}️'
            f'🫀Средний пульс – {check_heartrate[0]}{nl}'
            f'❤️‍Максимальный пульс – {check_heartrate[1]}{nl}'
            f'⬆️Максимальная высота – {elev_high}м{nl}'
            f'⬇️Минимальная высота – {elev_low}м{nl}'
            f'🧁Потрачено калорий – {check_calories}{nl}'

            statistics.extend(item_of_run)

    return statistics[-1]


# if __name__ == '__main__':
#     generation_analyse()
