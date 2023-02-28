import xml.etree.ElementTree as ET
import glob
import matplotlib

from graph_creater import make_chart

matplotlib.use('agg')

glob.glob('./*.gpx')

tree = ET.parse(glob.glob('./*.gpx')[0])
root = tree.getroot()

nl = '\n'

hr_max = 202
threshold = 185


def get_data_by_zone():
    list_of_zone_by_hr = {
        'zone_1_by_hr': 'Восстановление',
        'zone_2_by_hr': 'Аэробная',
        'zone_3_by_hr': 'Темповая',
        'zone_4_by_hr': 'ПАНО',
        'zone_5_by_hr': 'МПК'
    }

    zone_1_by_hr = [0, threshold * 0.69]
    zone_2_by_hr = [threshold * 0.69, threshold * 0.84]
    zone_3_by_hr = [threshold * 0.84, threshold * 0.95]
    zone_4_by_hr = [threshold * 0.95, threshold * 1.06]
    zone_5_by_hr = [threshold * 1.06, hr_max]

    dicts_of_zones_by_hr = {}

    i = 1
    while i <= 5:
        keyword = f'time_in_zone_' + str(i) + '_by_hr'
        value = 0
        dicts_of_zones_by_hr[keyword] = value
        i += 1

    all_hr_items = 0

    seconds = root[1][2]
    for _ in range(1, len(seconds), 1):
        hr = int(root[1][2][_][2][1][0].text)
        if hr != 0:
            all_hr_items += 1
            if zone_1_by_hr[0] < hr < zone_1_by_hr[1]:
                dicts_of_zones_by_hr['time_in_zone_1_by_hr'] += 1
            if zone_2_by_hr[0] < hr < zone_2_by_hr[1]:
                dicts_of_zones_by_hr['time_in_zone_2_by_hr'] += 1
            if zone_3_by_hr[0] < hr < zone_3_by_hr[1]:
                dicts_of_zones_by_hr['time_in_zone_3_by_hr'] += 1
            if zone_4_by_hr[0] < hr < zone_4_by_hr[1]:
                dicts_of_zones_by_hr['time_in_zone_4_by_hr'] += 1
            if zone_5_by_hr[0] < hr < zone_5_by_hr[1]:
                dicts_of_zones_by_hr['time_in_zone_5_by_hr'] += 1

    list_of_percents = []
    for i in range(1, len(dicts_of_zones_by_hr) + 1):
        keyword = f'time_in_zone_' + str(i) + '_by_hr'
        new_value = round((dicts_of_zones_by_hr[keyword] / all_hr_items * 100), 0)
        list_of_percents.append(new_value)
        dicts_of_zones_by_hr.update({keyword: new_value})

    make_chart(list_of_zone_by_hr, dicts_of_zones_by_hr)

# if __name__ == '__main__':
#     get_data_by_zone()
