from datetime import datetime
from time import strftime, gmtime
from db.training import get_last_training
from processors.gpx_maker import get_initial_data
# from processors.polyline_file import get_picture
from users import users_data, nl

bikes = ['заезд', 'виртуальный заезд', 'ride', 'virtualride']
run = ['забег', 'run']


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


def get_power(user_id: int):
    if 'device_watts' in load_data.keys() and load_data['device_watts']:
        ftp = int(users_data[f'{user_id}']['ftp'])
        weighted_average_watts = int(load_data['weighted_average_watts'])
        average_power = int(load_data['average_watts'])
        max_power = int(load_data['max_watts'])
        user_weight = float(users_data[f'{user_id}']['weight'])
        relative_power = round(weighted_average_watts / user_weight, 2)
        tss = round((weighted_average_watts ** 2 * load_data['moving_time']) / (ftp ** 2 * 3600) * 100, 1)

    else:
        weighted_average_watts = relative_power = average_power = max_power = tss = 'Неизвестно'

    return weighted_average_watts, relative_power, average_power, max_power, tss


def get_cadence():
    if 'average_cadence' in load_data:
        average_cadence = int(load_data['average_cadence'])
        return average_cadence
    else:
        average_cadence = 'Неизвестно'
        return average_cadence


def get_ratio(check_power, check_hr) -> float or None:
    ratio = None
    if check_power[0] != 'Неизвестно' and check_hr[0] != 'Неизвестно':
        ratio = round(check_power[0] / check_hr[0], 2)
    return ratio


def get_energy_spent() -> int or None:
    spent_calories = None
    if 'kilojoules' in load_data:
        spent_calories = int(load_data['kilojoules'])

    return spent_calories


def get_index(user_id: int) -> float or None:
    ratio = None
    index = get_initial_data(load_data['id'], user_id)
    if index:
        ratio = round(index, 2)

    return ratio


def get_temperature() -> int or None:
    temperature = None
    if 'average_temp' in load_data:
        temperature = int(load_data['average_temp'])

    return temperature


def generation_analyse(user_id: int):
    global load_data
    load_data = get_last_training(user_id)[0]
    # get_picture(load_data)

    for i in range(0, len(load_data)):
        type_of_activity = get_type_of_activity()
        date = datetime.strptime(load_data['start_date_local'], '%Y-%m-%dT%H:%M:%SZ').date()
        distance = round(load_data['distance'] / 1000, 2)
        moving_time = strftime("%H:%M:%S", gmtime(load_data['moving_time']))
        total_elevation_gain = int(load_data['total_elevation_gain'])
        achievement_count = load_data['achievement_count']
        athlete_count = load_data['athlete_count'] - 1
        average_pace = strftime("%M:%S", gmtime((1 / load_data['average_speed'] * 1000))) if load_data['average_speed'] > 0 else 0
        average_speed = round(load_data['average_speed'] * 3.6, 2) if load_data['average_speed'] > 0 else 0
        max_speed = round(load_data['max_speed'] * 3.6, 2) if load_data['max_speed'] > 0 else 0
        elev_high = int(load_data['elev_high'])
        elev_low = int(load_data['elev_low'])
        check_hr = get_heartrate()
        check_calories = get_energy_spent()
        check_index = get_index(user_id)
        check_temperature = get_temperature()

        if type_of_activity == 'Велосипед':
            check_power = get_power(user_id)
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
                f'🌡️Средняя температура  – {check_temperature if check_temperature else "Неизвестно"}{nl}'
                f'🧁Потрачено калорий – {check_calories if check_calories else "Неизвестно"}{nl}'
                f'{nl}'

                f'🫀Средний пульс – {check_hr[0]}{nl}'
                f'❤️‍Максимальный пульс – {check_hr[1]}{nl}'
                f'💪Средняя мощность – {check_power[2]}{nl}'
                f'🧨‍Макс. мощность – {check_power[3]}{nl}'
                f'🏎Средняя скорость – {average_speed}{nl}'
                f'🔝Макс. скорость – {max_speed}{nl}️'
                f'🔄Средний каденс – {check_cadence}{nl}'
                f'{nl}'

                f'⚖️Удельная мощность – {check_power[1]}{nl}'
                f'💪🏻Усредненная мощность – {check_power[0]}{nl}'
                f'😰TSS – {check_power[4] if len(check_power) == 5 else check_power[3]}{nl}'
                f'📉Изменение мощность/пульс – {check_index if check_index else "Неизвестно"}{nl}'
                f'📶Мощность/пульс – {check_ratio if check_ratio else "Неизвестно"}{nl}'
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
