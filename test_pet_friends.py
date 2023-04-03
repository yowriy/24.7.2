from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

# СТУДЕНЧЕСКАЯ РАБОТА
def test_add_pet_photo(pet_photo='images/cat1.jpg'):
    """Проверяем что можно обновить фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_simple_pet(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на изменение фото
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

        # Проверяем что статус ответа = 200 и фото питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] != ''

def test_add_new_simple_pet(name='Флеш', animal_type='ккк', age='2'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Проверяем что при вводе НЕКОРРЕКТНЫХ данных сервер выдает ошибку об отсутствии такого пользователя в базе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>403 Forbidden</title>\n<h1>Forbidden</h1>\n<p>This user wasn&#x27;t found in database</p>\n' in result

def test_unsuccessful_add_pet(name='Флеш', animal_type='ккк', age='пять'):
    """Проверяем что нельзя добавить питомца с НЕКОРРЕТНЫМИ ДАННЫМИ возраста"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)

    assert status == 400
    assert Exception("Provided data is incorrect")

def test_unsuccessful_add_pet_photo(pet_photo='images/cat1.gif'):
    """Проверяем что нельзя обновить фото питомца недоступным форматом фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 400
    assert Exception("Provided data is incorrect")

def test_add_empty_name_pet(name='', animal_type='вж', age='уцу'):
    """Проверяем что нельзя добавить питомца без имени"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)
    assert status == 400
    assert Exception("Provided data is incorrect")

def test_add_empty_animal_type_pet(name='Лось', animal_type='', age='уцу'):
    """Проверяем что нельзя добавить питомца без указания вида животного"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)
    assert status == 400
    assert Exception("Provided data is incorrect")

def test_unsuccessful_update_name_pet(name='', animal_type='Котэ', age=5):
    """Проверяем возможность замены информации о питомце на пустые поля"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    assert status == 400
    assert Exception("Provided data is incorrect")

def test_unsuccessful_update_animal_type(name='Бодя', animal_type='', age=5):
    """Проверяем возможность замены информации о питомце на пустые поля"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    assert status == 400
    assert Exception("Provided data is incorrect")