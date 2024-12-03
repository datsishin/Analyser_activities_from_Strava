from processors.graph_creater import make_chart
from users import users_data, nl


def get_hr_statistics(hr_data: list, user_id: int):
    threshold = int(users_data[f'{user_id}']['threshold'])
    hr_max = int(users_data[f'{user_id}']['hr_max'])

    # zone_1_by_hr = [threshold * 0.65, threshold * 0.81]
    # zone_2_by_hr = [threshold * 0.81, threshold * 0.88]
    # zone_3_by_hr = [threshold * 0.88, threshold * 0.93]
    # zone_4_by_hr = [threshold * 0.93, threshold * 1.00]
    # zone_5_by_hr = [threshold * 1.00, threshold * 1.02]
    # zone_6_by_hr = [threshold * 1.02, threshold * 1.05]
    # zone_7_by_hr = [threshold * 1.05, hr_max]

    zone_1_by_hr = [threshold * 0.60, threshold * 0.75]
    zone_2_by_hr = [threshold * 0.76, threshold * 0.84]
    zone_3_by_hr = [threshold * 0.85, threshold * 0.94]
    zone_4_by_hr = [threshold * 0.95, threshold * 1.01]
    zone_5_by_hr = [threshold * 1.02, hr_max]

    # list_of_zone = {
    #     'zone_1_by_hr': f'Восстановление {nl}{int(zone_1_by_hr[0])} – {int(zone_1_by_hr[1])}',
    #     'zone_2_by_hr': f'Экстенсивная {nl} выносливость {nl}{int(zone_2_by_hr[0])} – {int(zone_2_by_hr[1])}',
    #     'zone_3_by_hr': f'Интенсивная {nl} выносливость {nl}{int(zone_3_by_hr[0])} – {int(zone_3_by_hr[1])}',
    #     'zone_4_by_hr': f'СубПАНО {nl}{int(zone_4_by_hr[0])} – {int(zone_4_by_hr[1])}',
    #     'zone_5_by_hr': f'СверхПАНО {nl}{int(zone_5_by_hr[0])} – {int(zone_5_by_hr[1])}',
    #     'zone_6_by_hr': f'Аэробная {nl}{int(zone_6_by_hr[0])} – {int(zone_6_by_hr[1])}',
    #     'zone_7_by_hr': f'Анаэробная {nl}{int(zone_7_by_hr[0])} – {int(zone_7_by_hr[1])}',
    # }

    list_of_zone = {
        'zone_1_by_hr': f'Восстановление {nl}{int(zone_1_by_hr[0])} – {int(zone_1_by_hr[1])}',
        'zone_2_by_hr': f'Выносливость {nl}{int(zone_2_by_hr[0])} – {int(zone_2_by_hr[1])}',
        'zone_3_by_hr': f'Темповая {nl}{int(zone_3_by_hr[0])} – {int(zone_3_by_hr[1])}',
        'zone_4_by_hr': f'ПАНО {nl}{int(zone_4_by_hr[0])} – {int(zone_4_by_hr[1])}',
        'zone_5_by_hr': f'VO2 Max {nl}{int(zone_5_by_hr[0])} – ∞',
    }

    dicts_of_zones = {}

    i = 1
    while i <= len(list_of_zone):
        keyword = f'time_in_zone_' + str(i) + '_by_hr'
        value = 0
        dicts_of_zones[keyword] = value
        i += 1

    all_hr_items = 0

    seconds = hr_data.size
    for _ in range(0, seconds):
        hr = hr_data[_]
        if hr:
            if hr != 0:
                all_hr_items += 1

                for i in range(1, len(list_of_zone) + 1):
                    start_range = eval(f'zone_' + str(i) + '_by_hr')[0]
                    finish_range = eval(f'zone_' + str(i) + '_by_hr')[1]
                    key = f'time_in_zone_' + str(i) + '_by_hr'

                    if start_range <= hr <= finish_range:
                        new_value = dicts_of_zones[key] + 1
                        dicts_of_zones.update({key: new_value})

    list_of_percents = []
    for i in range(1, len(dicts_of_zones) + 1):
        keyword = f'time_in_zone_' + str(i) + '_by_hr'
        new_value = round((dicts_of_zones[keyword] / all_hr_items * 100), 1)
        list_of_percents.append(new_value)
        dicts_of_zones.update({keyword: new_value})

    option = 'hr'

    make_chart(list_of_zone, dicts_of_zones, option)
