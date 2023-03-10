from db.mongo import db_connect
from users import users_data, nl


def check_mileage(name: str, new_mileage: int, user_id: int):
    coll = db_connect(user_id, param='gear')
    document = {'bike': users_data[f'{user_id}']['bike'],
                'name': name,
                'mileage': new_mileage}

    old_mileage = coll.find_one({'mileage': {'$exists': True}})

    if old_mileage:
        old_mileage_data = old_mileage['mileage']

        if new_mileage > old_mileage_data:
            coll.update_one(old_mileage, {'$set': {'mileage': new_mileage}})
            return service(name, new_mileage, user_id)

        if new_mileage == old_mileage_data:
            text = f'Пробег {name} не изменился и составляет – {old_mileage_data} км'
            service_text = service(name, new_mileage, user_id)
            return f'{text}{nl}{nl}{service_text}'

    coll.insert_one(document)
    text = f'Пробег {name} составляет – {new_mileage} км'
    service_text = service(name, new_mileage, user_id)
    if service_text:
        return f'{text}{nl}{nl}{service_text}'
    return text


def service(name: str, new_mileage: int, user_id: int):
    chain_interval = 100
    drive_interval = 500

    coll = db_connect(user_id, param='service')
    old_service = coll.find_one({'bike': {'$eq': users_data[f'{user_id}']['bike']}})

    if old_service:
        last_chain_service = old_service['last_chain_service']
        last_drive_service = old_service['last_drive_service']
        chain_dif = new_mileage - last_chain_service
        drive_dif = new_mileage - last_drive_service

        if chain_dif > chain_interval and drive_dif > drive_interval:
            return f'Интервал смазки цепи превышен на {chain_dif - chain_interval} км,' \
                   f' чистки привода на {drive_dif - drive_interval} км, обслужи велосипед!'

        if chain_dif > chain_interval:
            return f'Интервал смазки цепи превышен на {chain_dif - chain_interval} км, смажь цепь!'

        if drive_dif > drive_interval:
            return f'Интервал чистки привода превышен на {drive_dif - drive_interval} км, почистить привод!'

    else:
        coll.insert_one({'bike': users_data[f'{user_id}']['bike'], 'name': name, 'mileage': new_mileage,
                         'last_chain_service': new_mileage, 'last_drive_service': new_mileage})
