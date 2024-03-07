# Программа предназанчена для показа успешных операций клиента

# import os.path
import json
import os
from os.path import dirname

FILE = 'test.json'
# FILE = 'operations.json'
OPERATION_JSON_FILE = os.path.join(dirname(os.getcwd()), 'data', FILE)


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
        """Возвращает дату операции перевода в классическом формате."""
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


def mask_card(card_account):
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
    """Проверяем файл вопросов-ответов на корректность и загружаем его."""
    if not os.path.exists(path):
        print(f'Файл {FILE} не содержит записей или указан неверный путь к нему !\n')
        return None
    elif os.stat(path).st_size == 0:
        print(f'Файл {FILE} не содержит записей или указан неверный путь к нему !\n')
        return None
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def create_operation_objects(path):
    """Получаем список operations_list из json-файла с помощью функции load_json_file.
    Создаем список объектов operations_objects из экземпляров класса Operation."""
    operations_list = load_json_file(path)
    if operations_list is not None:
        operations_objects = []
        for op_object in operations_list:
            if len(op_object) > 0 and op_object["state"] == 'EXECUTED':
                o = Operation(op_object.get("id"), op_object.get("state"), op_object.get("date"),
                              op_object.get("operationAmount"), op_object.get("description"),
                              op_object.get("from"), op_object.get("to"))
                operations_objects.append(o)
        return operations_objects
    else:
        return None


def main():
    """create_operation_objects создает список объектов операций, сортирует список по дата (x.date)
    и выводит результаты операций в требуемомо виде."""
    operations_objects = create_operation_objects(OPERATION_JSON_FILE)
    if operations_objects is not None:
        operations_objects.sort(key=lambda x: x.date, reverse=True)
        # i - счетчик операций
        # quantity - количество элементов списка которое нужно обработат
        i = 0
        if len(operations_objects) < 5:
            print(f'Файл {FILE} не содержит необходимого количества платежей (< 5) !\n')
            quantity = len(operations_objects)
        else:
            quantity = 5

        while i <= quantity - 1:
            # метод get_date() класса Operation выводит дату в формате dd.mm.yyyy, get_description - описание операции
            # метод get_payer() выводит счет или карту плательщика, get_receiver() - получателя.
            # функция mask_card() перед выводом накладывает маску (*) на часть номера карты или счета.
            # метод get_amount() выводит сумму банковской операции.
            print(operations_objects[i].get_date()+' '+operations_objects[i].get_description())
            if operations_objects[i].get_payer() is None:
                print(mask_card(operations_objects[i].get_receiver()))
            else:
                print(mask_card(operations_objects[i].get_payer())+' -> '+mask_card(operations_objects[i].get_receiver()))
            print(f'{operations_objects[i].get_amount()}\n')
            i += 1


if __name__ == '__main__':
    main()
