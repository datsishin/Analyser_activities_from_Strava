import xml.etree.ElementTree as ET
import glob
import matplotlib

from graph_creater import make_chart

matplotlib.use('agg')

glob.glob('data/*.gpx')

tree = ET.parse(glob.glob('data/*.gpx')[0])
root = tree.getroot()

nl = '\n'

hr_max = 202
threshold = 185


def get_data_by_hr():
    zone_1_by_hr = [0, threshold * 0.68]
    zone_2_by_hr = [threshold * 0.69, threshold * 0.83]
    zone_3_by_hr = [threshold * 0.84, threshold * 0.94]
    zone_4_by_hr = [threshold * 0.95, threshold * 1.05]
    zone_5_by_hr = [threshold * 1.06, hr_max]

    list_of_zone = {
        'zone_1_by_hr': f'Восстановление {nl}{int(zone_1_by_hr[0])} – {int(zone_1_by_hr[1])}',
        'zone_2_by_hr': f'Аэробная {nl}{int(zone_2_by_hr[0])} – {int(zone_2_by_hr[1])}',
        'zone_3_by_hr': f'Темповая {nl}{int(zone_3_by_hr[0])} – {int(zone_3_by_hr[1])}',
        'zone_4_by_hr': f'ПАНО {nl}{int(zone_4_by_hr[0])} – {int(zone_4_by_hr[1])}',
        'zone_5_by_hr': f'МПК {nl}{int(zone_5_by_hr[0])} – ∞',
    }

    dicts_of_zones = {}

    i = 1
    while i <= 5:
        keyword = f'time_in_zone_' + str(i) + '_by_hr'
        value = 0
        dicts_of_zones[keyword] = value
        i += 1

    all_hr_items = 0

    seconds = root[1][2]
    for _ in range(1, len(seconds), 1):
        hr = int(root[1][2][_][2][1][0].text)
        if hr:
            if hr != 0:
                all_hr_items += 1

                for i in range(1, len(list_of_zone) + 1):
                    start_range = eval(f'zone_' + str(i) + '_by_hr')[0]
                    finish_range = eval(f'zone_' + str(i) + '_by_hr')[1]
                    key = f'time_in_zone_' + str(i) + '_by_hr'

                    if start_range < hr < finish_range:
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


# if __name__ == '__main__':
#     get_data_by_zone()
