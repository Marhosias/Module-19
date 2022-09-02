from api import PetFriends
from settings import *
import os

pf = PetFriends()

#1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

#2
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

#3
def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#4
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

#5
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#6
def test_get_api_key_for_invalid_user(email=invalid_user, password=valid_password):
    """Проверка получение ключа с неправильным пользователем"""
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result

#7
def test_get_list_of_pets_with_invalid_key(filter=''):
    """Проверка получение списка питомцев с неправильным ключом"""
    auth_key = invalid_auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200
    assert 'pets' not in result

#8
def test_add_new_pet_with_symbol_in_name(name=symbol_name, animal_type=pet_type,
                                          age=pet_age, pet_photo=pet_image):
    """Проверка на создание питомца со специальными символами в имени"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#9
def test_add_new_pet_with_invalid_age(name=pet_name, animal_type=pet_type,
                                       age=invalid_age, pet_photo=pet_image):
    """Проверка создания питомца с str в графе 'age'"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    assert 'age' not in result

#10
def test_add_new_pet_without_photo_valid_data(name=pet_name, animal_type=pet_type, age=pet_age):
    """Проверка создания питомца без фотографии с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

#11
def test_add_new_pet_without_photo_invalid_key(name=pet_name, animal_type=pet_type, age=pet_age):
    """Проверка создания питомца без фотографии с некорректным ключом"""
    auth_key = invalid_auth_key
    status, result = pf.add_new_pet_without_photo(auth_key,name,animal_type,age)

    assert status != 200
    assert 'name' not in result

#12
def test_add_new_pet_without_photo_invalid_age(name=pet_name, animal_type=pet_type, age=invalid_age):
    """Проверка добавления нового питомца с некорректным возратом"""
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status != 200
    assert 'age' not in result

#13
def test_add_correct_photo_to_pet(pet_photo=pet_image):
    """Проверка добавление фотографии к питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key,pet_id,pet_photo)

    assert status == 200
    assert 'jpg' or 'png' in 'pet_photo'

#14
def test_add_incorrect_photo_to_pet(pet_photo=incorrect_photo):
    """Проверка добавления не корректного формата фотографии к питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status != 200
    assert status != 503
    assert 'jpg' or 'png' not in 'pet_photo'

#15
def test_delete_with_incorrect_id_pet():
    """Проверка удаления питомца с некорректным ID"""
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key)
    my_pets['pets'][0]['id'] = incorrect_id_pet

    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
        assert status == 200
    else:
        raise Exception("There's no my pets")

#16 Фейлится, так как принимает str в графу "age"
def test_update_inform_about_pet_incorrect_age(name=pet_name, animal_type=pet_type, age=invalid_age):
    """Проверка обновления информации о питомце с некорретным возрастом (str)"""
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status != 200
        assert 'age' not in result
    else:
        raise Exception("There is no my pets")