from db.mongo import db_connect
from main import get_mileage
from users import users_data


def cleaning(message, param: str):
    user_id = message.chat.id
    coll = db_connect(user_id, param='service')
    bike = users_data[f'{user_id}']['bike']
    bike_service_info = coll.find_one(filter={'bike': bike})

    if bike_service_info is None:
        get_mileage(user_id)
        bike_chain_info = coll.find_one(filter={'bike': bike})
        coll.update_one(bike_chain_info, {'$set': {'last_chain_service': bike_chain_info['mileage'],
                                                   'last_drive_service': bike_chain_info['mileage']}})
        return 'Данные по велосипеду загружены'

    if param == 'chain':
        coll.update_one(bike_service_info, {'$set': {'last_chain_service': bike_service_info['mileage']}})
        return 'Молодец что обслужил цепь, ей приятно 😽'

    elif param == 'drive':
        coll.update_one(bike_service_info, {'$set': {'last_drive_service': bike_service_info['mileage']}})
        return 'Молодец что обслужил привод, ему приятно 😽'
