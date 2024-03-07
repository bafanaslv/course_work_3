# Программа предназанчена для показа успешных операций клиента

import json
import os
from os.path import dirname

FILE = 'test.json'
#FILE = 'empty_file.json'
OPERATION_JSON_FILE = os.path.join(dirname(os.getcwd()), FILE)
#FILE = 'operations.json'
#OPERATION_JSON_FILE = os.path.join(dirname(os.getcwd()), 'data', FILE)

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


def json_file_check(operations_list):
    if ("id" not in operations_list[0] or
        "state" not in operations_list[0] or
        "date" not in operations_list[0] or
        "operationAmount" not in operations_list[0] or
        "description" not in operations_list[0] or
        "from" not in operations_list[0] or
        "to" not in operations_list[0]):
        return False
    else:
        return True


def load_json_file(path):
    """Проверяем файл вопросов-ответов на корректность и загружаем его."""
    if not os.path.exists(path):
        print(f'Файл {FILE} отсуствует или указан неверный путь к нему !\n')
        return None
    else:
        with open(path, 'r', encoding='utf-8') as file:
            try:
                print(json.load(file))
                return json.load(file)
            except json.decoder.JSONDecodeError:
                print(f'Неверная структура файла {FILE} !')
                return None


def create_operation_objects(path):
    """Получаем список operations_list из json-файла с помощью функции load_json_file.
    Создаем список объектов operations_objects из экземпляров класса Operation."""
    operations_list = load_json_file(path)
    if type(operations_list) is list:
        operations_objects = []
        for op_object in operations_list:
            if len(op_object) > 0 and op_object["state"] == 'EXECUTED':
                o = Operation(op_object.get("id"), op_object.get("state"), op_object.get("date"),
                              op_object.get("operationAmount"), op_object.get("description"),
                              op_object.get("from"), op_object.get("to"))
                operations_objects.append(o)
        print(type(operations_objects))
        return operations_objects
    else:
        return None


def check_quantity(operations_objects):
    # quantity - количество операций которое нужно обработать
    if len(operations_objects) < 5:
        print(f'Файл {FILE} не содержит необходимого количества операций (< 5) !\n')
        return len(operations_objects)
    else:
        return 5

def print_operations(operations_objects):
    quantity = check_quantity(operations_objects)
    # i - счетчик операций
    i = 0
    while i <= quantity - 1:
        # метод get_date() класса Operation выводит дату в формате dd.mm.yyyy, get_description - описание операции
        # метод get_payer() выводит счет или карту плательщика, get_receiver() - получателя.
        # функция mask() перед выводом накладывает маску (*) на часть номера карты или счета.
        # метод get_amount() выводит сумму банковской операции.
        line_1 = operations_objects[i].get_date() + ' ' + operations_objects[i].get_description()
        if operations_objects[i].get_payer() is None:
            line_2 = mask(operations_objects[i].get_receiver())
        else:
            line_2 = mask(operations_objects[i].get_payer()) + ' -> ' + mask(operations_objects[i].get_receiver())
        line_3 = operations_objects[i].get_amount()
        print(f'{line_1}\n{line_2}\n{line_3}\n')
        i += 1


def main():
    """create_operation_objects создает список объектов операций, сортирует список по дата (x.date)
    и выводит результаты операций в требуемомо виде."""
    operations_objects = create_operation_objects(OPERATION_JSON_FILE)
    if operations_objects is not None:
        operations_objects.sort(key=lambda x: x.date, reverse=True)
        print_operations(operations_objects)


if __name__ == '__main__':
    main()
