import pytest
import os
from os.path import dirname
from modules.main import main, create_operation_objects, mask, Operation, str_operation
from modules.main import load_json_file, json_list_check

EMPTY_FILE = os.path.join(dirname(os.getcwd()), 'course_work_3', 'empty_file.json')
TEST_FILE = os.path.join(dirname(os.getcwd()), 'course_work_3', 'test_list.json')
INVALID_FILE = os.path.join(dirname(os.getcwd()), 'course_work_3', 'invalid_file.json')
NON_EXISTENT_FILE = os.path.join(dirname(os.getcwd()), 'course_work_3', 'bla_bla_bla.json')
# EMPTY_FILE = os.path.join(dirname(os.getcwd()), 'empty_file.json')
# TEST_FILE = os.path.join(dirname(os.getcwd()), 'test_list.json')
# INVALID_FILE = os.path.join(dirname(os.getcwd()), 'invalid_file.json')
# NON_EXISTENT_FILE = os.path.join(dirname(os.getcwd()), 'bla_bla_bla.json')

check_empty_list = []
test_object1 = []
test_object2 = []
test_json_list1 = [
  {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
  }
]
test_json_list2 = [
  {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Открытие вклада",
    "to": "Счет 64686473678894779589"
  }
]
test_inv_json_list = [
  {
    "idd": 441945886,
    "stat": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Открытие вклада",
    "to": "Счет 64686473678894779589"
  }
]


def test_mask():
    """Проверка установки масок на счета в зависимости вида и содердимого счета."""
    assert mask('Visa Gold 7305799447374042') == 'Visa Gold 7305 79** **** 4042'
    assert mask('Maestro 4598300720424501') == 'Maestro 4598 30** **** 4501'
    assert mask('Счет 97584898735659638967') == 'Счет **8967'


# Фикустуры test_list1 и test_list2 тем, что фикстура test_list2 подготовлена для операции "Открытие счета".
@pytest.fixture
def test_list1():
    o = Operation(test_json_list1[0].get("id"),
                  test_json_list1[0].get("state"),
                  test_json_list1[0].get("date"),
                  test_json_list1[0].get("operationAmount"),
                  test_json_list1[0].get("description"),
                  test_json_list1[0].get("from"),
                  test_json_list1[0].get("to"))
    test_object1.append(o)
    return test_object1[0]


@pytest.fixture
def test_list2():
    o = Operation(test_json_list2[0].get("id"),
                  test_json_list2[0].get("state"),
                  test_json_list2[0].get("date"),
                  test_json_list2[0].get("operationAmount"),
                  test_json_list2[0].get("description"),
                  test_json_list2[0].get("from"),
                  test_json_list2[0].get("to"))
    test_object2.append(o)
    return test_object2[0]


def test_create_operation_objects():
    """Проверка методов класса Operation."""
    assert create_operation_objects(test_json_list1)[0].get_date() == "26.08.2019"
    assert create_operation_objects(test_json_list1)[0].get_description() == "Перевод организации"
    assert create_operation_objects(test_json_list1)[0].get_payer() == "Maestro 1596837868705199"
    assert create_operation_objects(test_json_list1)[0].get_receiver() == "Счет 64686473678894779589"
    assert create_operation_objects(test_json_list1)[0].get_amount() == "31957.58 руб."


def test_load_json_file():
    """Проверка json - файла. TEST_FILE - правильный файл, EMPTY_FILE - пустой файл, NON_EXISTENT_FILE -
    имя несуществующего файла, INVALID_FILE - файл неверным содержимым."""
    assert load_json_file(TEST_FILE) is not None
    assert load_json_file(EMPTY_FILE) is None
    assert load_json_file(NON_EXISTENT_FILE) is None
    assert load_json_file(INVALID_FILE) is None


def test_json_file_check():
    """Проверка структуры загруженного json - файла."""
    assert json_list_check(test_json_list1)
    assert not json_list_check(test_inv_json_list)


def test_str_operation(test_list1, test_list2):
    """Проверка вывода в зависимости от вида и банковской операции.
    Выводимые строки отделены друг от друга символом '/'."""
    assert (str_operation(test_object1[0]) ==
            "26.08.2019 Перевод организации/Maestro 1596 83** **** 5199 -> Счет **9589/31957.58 руб.")
    assert (str_operation(test_object2[0]) ==
            "26.08.2019 Открытие вклада/Счет **9589/31957.58 руб.")


def test_main():
    assert main(TEST_FILE)
    assert main(INVALID_FILE) is None
    assert main(EMPTY_FILE) is None
    assert main(NON_EXISTENT_FILE) is None
