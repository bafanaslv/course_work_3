# Программа предназанчена для показа успешных операций клиента
# по банковской карте.

import os.path
import json
import os
from os.path import dirname

OPERATION_JSON_FILE = os.path.join(dirname(os.getcwd()), 'data', 'operations.json')

def create_operation_list(path):
    """Получаем список operations__list из json-файла.
    Создаем список объектов operations__objects из экземпляров класса Operation."""
    operations_list = load_json_file(path)
    operations_objects = []
    for op_object in operations_list:
        if len(op_object) > 0 and op_object["state"] == 'EXECUTED':
            operations_objects.append(op_object)
    return operations_objects


def load_json_file(path):
    """Проверяем файл вопросов-ответов на корректность и загружаем его."""
    if not os.path.exists(path):
        print(f'Файл {path} не существует или указан неверный путь к нему !\n')
        exit()
    elif os.stat(path).st_size == 0:
        print('Файл пустой - тест прерван !')
        exit()
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def main():
    operations_objects = create_operation_list(OPERATION_JSON_FILE)
    operations_objects.sort(key=lambda x: x['date'], reverse=True)
    for operation in operations_objects:
        print(operation)


if __name__ == '__main__':
    main()
