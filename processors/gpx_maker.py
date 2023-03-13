from copy import copy

import requests as r
from processors.hr_analyser import get_hr_statistics
from processors.power_analyser import get_power_statistics
from main import status_code_checker
from users import users_data


def get_initial_data(id: int, user_id: int):
    url = f'https://www.strava.com/api/v3/activities/{id}/streams'
    token = users_data[f'{user_id}']['access_token']
    headers = {'Authorization': 'Bearer ' + token}
    params = {'access_token': token}
    heartrate = {'keys': 'heartrate'}
    power = {'keys': 'watts'}

    response = status_code_checker(url, params, user_id)

    if type(response) == str:
        new_token = response
        headers['Authorization'] = f'Bearer ' + new_token

    response_hr = r.get(url, headers=headers, params=heartrate).json()
    response_power = r.get(url, headers=headers, params=power).json()
    return processing_data(response_hr, response_power, user_id)


def processing_data(response_hr: list, response_power: list, user_id: int):
    global hr_data, power_data

    for i in range(0, len(response_hr)):
        if response_hr[i]['type'] == 'heartrate':
            hr_data = list(response_hr)[i]['data']
            # get_hr_statistics(hr_data, user_id)
            break
        hr_data = []

    for i in range(0, len(response_power)):
        if response_power[i]['type'] == 'watts':
            power_data = list(response_power)[i]['data']
            # get_power_statistics(power_data, user_id)
            break
        power_data = []

    return data_checker(user_id)


def data_checker(user_id: int):
    if hr_data and power_data:
        get_hr_statistics(hr_data, user_id)
        get_power_statistics(power_data, user_id)
        return get_power_by_hr()
    if power_data:
        get_power_statistics(power_data, user_id)
    if hr_data:
        get_hr_statistics(hr_data, user_id)
    else:
        pass


def get_power_by_hr():
    hr_list = get_middle_item(hr_data)
    power_list = get_middle_item(power_data)

    first_half = sum(power_list[0]) / sum(hr_list[0])
    second_half = sum(power_list[1]) / sum(hr_list[1])

    index = (first_half - second_half) / first_half * 100
    return index


def get_middle_item(data):
    middle = float(len(data) / 2)

    if middle % 2 != 0:
        middle_item = data[int(middle - 0.5)]
        first_list = []
        second_list = []
        for i in range(0, int(middle_item - 0.5)):
            item = data[i]
            first_list.append(item)
        for i in range(int(middle_item + 0.5), len(data)):
            item = data[i]
            second_list.append(item)

        final_list = [first_list, second_list]
        return final_list

    else:
        first_list = []
        second_list = []
        for i in range(0, int(data[int(middle)]) - 1):
            item = data[i]
            first_list.append(item)
        for i in range(data[int(middle)] - 1, len(data)):
            item = data[i]
            second_list.append(item)

        final_list = [first_list, second_list]
        return final_list

# if __name__ == '__main__':
#     get_power_by_hr()
