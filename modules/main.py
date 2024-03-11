# Программа предназанчена для показа пяти последних успешных банковских операций.

import json
import os
from os.path import dirname

FILE = 'operations.json'
OPERATIONS_JSON_FILE = os.path.join(dirname(os.getcwd()), 'data', FILE)


class Operation:
    """id_ - идентификатор, state - состояние, date - дата операции, amount - сумма операции,
     description - описание, payer - плательщик, receiver - получатель"""

    def __init__(self, id_, state, date, amount, description, payer, receiver):
        self.id = id_
        self.state = state
        self.date = date
        self.amount = amount
        self.description = description
        self.payer = payer
        self.receiver = receiver

    def get_date(self):
        """Возвращает дату операции перевода в классическом формате dd.mm.yyyy."""
        rus_date = self.date[:10].split("-")[::-1]
        return '.'.join(rus_date)

    def get_description(self):
        """Возвращает описание операции."""
        return self.description

    def get_payer(self):
        """Возвращает плательщика."""
        return self.payer

    def get_receiver(self):
        """Возвращает получателя."""
        return self.receiver

    def get_amount(self):
        """Возвращает сумму операции."""
        currency = self.amount["currency"]
        return self.amount["amount"]+' '+currency["name"]


def mask(card_account):
    """Возвращает номера карты или счета в маске."""
    if card_account[:4] == 'Счет':
        # Здесь и так понятно :)
        return "Счет **"+card_account[-4:]
    else:
        # Делим номер карты на список с частями имени и номером и кладем в список card. Далее разделяем номер на нужные
        # фрагменты с цифрами и получаем маскированный номер карты card_number.
        # Далее склеиваем список с частями имени карты с маскированным номером карты.
        # len_card - количество элементов в списке card.
        card = card_account.split(" ")
        len_card = len(card)
        card_number = card[-1][0:4] + " " + card[-1][4:6]+'** ****' + " " + card[-1][-4:]
        return " ".join(card[0:len_card - 1])+" " + card_number


def load_json_file(path):
    """Загрузка json - файла банковских операций."""
    if not os.path.exists(path):
        print(f'Файл {FILE} отсуствует или указан неверный путь к нему !\n')
        return None
    else:
        with open(path, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError:
                print(f'Неверная структура файла {FILE} !')
                return None


def json_list_check(operations_list):
    """Проверка структуры объекта банковской операции."""
    if ("id" not in operations_list[0] or "state" not in operations_list[0] or
        "date" not in operations_list[0] or "operationAmount" not in operations_list[0] or
        "description" not in operations_list[0] or "from" not in operations_list[0] or
        "to" not in operations_list[0]):
        return False
    else:
        return True


def create_operation_objects(operations_list):
    """Формирование списка operations_list из json-файла с помощью функции load_json_file.
    Создаение список объектов operations_objects из экземпляров класса Operation."""
    operations_objects = []
    for op_object in operations_list:
        if len(op_object) > 0 and op_object["state"] == 'EXECUTED':
            o = Operation(op_object.get("id"), op_object.get("state"), op_object.get("date"),
                          op_object.get("operationAmount"), op_object.get("description"),
                          op_object.get("from"), op_object.get("to"))
            operations_objects.append(o)
    return operations_objects


def str_operation(operation):
    """Подготовка банковских операций к выводу. Готовится строка из трех частей разделенных символоам '/'. """
    line_1 = operation.get_date() + ' ' + operation.get_description()
    if operation.get_payer() is None:
        line_2 = mask(operation.get_receiver())
    else:
        line_2 = mask(operation.get_payer()) + ' -> ' + mask(operation.get_receiver())
    line_3 = operation.get_amount()
    return line_1+'/'+line_2+'/'+line_3


def print_operations(operations_objects):
    """Вывод банковских операций в три строки. Если поступил неверный объект выводится сообщение."""
    if len(operations_objects) > 0:
        for operation in operations_objects:
            str_op = str_operation(operation).split("/")
            print(str_op[0])
            print(str_op[1])
            print(str_op[2])
    else:
        print(f'Неверная структура файла {FILE} - отсутствуют банковские операции !')
        return None


def main(path):
    """Функция load_json_file загружает json - файл и выполняет первичную проверу файла. После проверки структуры
    полученного списка функцией json_list_check функция create_operation_objects создает список операций. Далее
    список сортируется по дате и функцией print_operations выводится результат операций в требуемом виде."""
    operations_list = load_json_file(path)
    if operations_list is not None:
        if json_list_check(operations_list) is True:
            operations_objects = create_operation_objects(operations_list)
            operations_objects.sort(key=lambda x: x.date, reverse=True)
            print_operations(operations_objects)
            return True
        else:
            return False
    else:
        return None


if __name__ == '__main__':
    main(OPERATIONS_JSON_FILE)
