from db.mongo import db_connect
from users import users_data, nl


def check_mileage(name: str, new_mileage: int, user_id: int):
    coll = db_connect(user_id, param='service')
    bike = users_data[f'{user_id}']['bike']
    document = {'bike': bike,
                'name': name,
                'mileage': new_mileage}

    record = coll.find_one({'bike': {'$eq': bike},
                            'last_chain_service': {'$exists': True},
                            'last_drive_service': {'$exists': True}})
    if record:
        old_mileage = record['mileage']
        last_chain_service = record['last_drive_service']
        last_drive_service = record['last_drive_service']

        if new_mileage > old_mileage:
            coll.update_one(record, {'$set': {'mileage': new_mileage}})
            service_text = service(new_mileage, last_chain_service, last_drive_service)
            return f'Пробег {name} увеличился на {new_mileage - old_mileage} км{nl}' \
                   f'Общий пробег составляет – {new_mileage} км{nl}{nl}' \
                   f'{service_text}'

        if new_mileage == old_mileage:
            text = f'Пробег {name} составляет – {old_mileage} км'
            service_text = service(new_mileage, last_chain_service, last_drive_service)
            if service_text:
                return f'{text}{nl}{nl}{service_text}'
            return f'{text}'

    record = coll.find_one({'bike': {'$eq': bike}})
    text = f'Пробег {name} составляет – {new_mileage} км'
    if record:
        return f'{text}{nl}{nl}' \
               f'Нет данных по обслуживанию велосипеда, добавьте информацию'

    coll.insert_one(document)
    text = f'Пробег {name} составляет – {new_mileage} км'
    return text


def service(new_mileage: int, last_chain_service: int, last_drive_service: int):
    chain_interval = 100
    drive_interval = 500

    chain_dif = new_mileage - last_chain_service
    drive_dif = new_mileage - last_drive_service

    if chain_dif > chain_interval and drive_dif > drive_interval:
        return f'Интервал смазки цепи превышен на {chain_dif - chain_interval} км,' \
               f' чистки привода на {drive_dif - drive_interval} км, обслужи велосипед!'

    if chain_dif > chain_interval:
        return f'Интервал смазки цепи превышен на {chain_dif - chain_interval} км, смажь цепь!'

    if drive_dif > drive_interval:
        return f'Интервал чистки привода превышен на {drive_dif - drive_interval} км, почистить привод!'
