# Программа предназанчена для показа успешных операций клиента
# по банковской карте.

import os.path
import json
import os
from os.path import dirname
from operator import itemgetter

OPERATION_JSON_FILE = os.path.join(dirname(os.getcwd()), 'data', 'operations.json')

class Operation:
    """question - вопрос, difficulty - сложность, true_answer - правильный ответ, question_asked - задан ли вопрос,
     answer - ответ, score - количество баллов за правильный ответ"""

    def __init__(self, id_, state, date, amount, description, payer, receiver):
        self.id = id_
        self.state = state
        self.date = date
        self.amount = amount
        self.description = description
        self.payer = payer
        self.receiver = receiver

    def get_state(self):
        """Возвращает сумму перевода."""
        return self.state

    def get_amount(self):
        """Возвращает сумму перевода."""
        return self.amount

#    def sorting(self):
#        return sorted(self, key=lambda x: x['date'], reverse=True)



def create_operation_list(path):
    """Получаем список operations__list из json-файла.
    Создаем список объектов operations__objects из экземпляров класса Operation."""
    operations_list = load_json_file(path)
#    sorted_list = sorted(operations_list, key=itemgetter('date'), reverse=True)
    operations_objects = []
    for op_object in operations_list:
        if len(op_object) > 0 and op_object["state"] == 'EXECUTED':
#            print(op_object)
 #           o = Operation(op_object.get("id"), op_object.get("state"), op_object.get("date"),
 #          op_object.get("operationAmount"), op_object.get("description"), op_object.get("from"), op_object.get("to"))
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
#    sorted_list = sorted(operations_objects, key=itemgetter('date'), reverse=True)
    sorted_list = sorted(operations_objects, key=lambda x: x['date'], reverse=True)
#    for operation in operations_objects:
#        print(operation.get_amount())
    for operation in sorted_list:
        print(operation)


if __name__ == '__main__':
    main()
