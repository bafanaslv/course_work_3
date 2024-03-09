import pytest
import os
from os.path import dirname
from modules.main import main, create_operation_objects, mask, Operation, str_operation
from modules.main import json_file_check, load_json_file, print_operations

EMPTY_JSON_FILE = os.path.join(dirname(os.getcwd()), 'course_work_3', 'empty_file.json')
TEST_JSON_FILE = os.path.join(dirname(os.getcwd()), 'course_work_3', 'test_list.json')
NON_EXISTENT_FILE = os.path.join(dirname(os.getcwd()), 'course_work_3', 'bla_bla_bla.json')

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

test_json_list_err = [
  {
    "idd": 441945886,
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

check_empty_list = []

def test_mask():
    assert mask('Visa Gold 7305799447374042') == 'Visa Gold 7305 79** **** 4042'
    assert mask('Maestro 4598300720424501') == 'Maestro 4598 30** **** 4501'
    assert mask('Счет 97584898735659638967') == 'Счет **8967'


test_object1 = []
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

test_object2 = []
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


def test_class_methods(test_list1):
    assert test_list1.get_date() == "26.08.2019"
    assert test_list1.get_description() == "Перевод организации"
    assert test_list1.get_payer() == "Maestro 1596837868705199"
    assert test_list1.get_receiver() == "Счет 64686473678894779589"
    assert test_list1.get_amount() == "31957.58 руб."


def test_create_operation_objects():
    assert create_operation_objects(NON_EXISTENT_FILE) is None
    assert create_operation_objects(TEST_JSON_FILE)[0].get_date() == "26.08.2019"

def test_json_file_check():
    assert json_file_check(test_json_list1) is True
    assert json_file_check(test_json_list_err) is False

def test_load_json_file():
    assert load_json_file(NON_EXISTENT_FILE) is None

def test_str_operation(test_list1, test_list2):
    assert (str_operation(test_object1[0]) ==
            "26.08.2019 Перевод организации/Maestro 1596 83** **** 5199 -> Счет **9589/31957.58 руб.")
    assert (str_operation(test_object2[0]) ==
            "26.08.2019 Открытие вклада/Счет **9589/31957.58 руб.")

def test_print_operations():
    assert print_operations(check_empty_list) is None

def test_main():
    assert main(EMPTY_JSON_FILE) is None
