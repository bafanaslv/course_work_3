import pytest
import os
from os.path import dirname
from modules.main import create_operation_objects, mask, Operation, json_file_check, check_quantity

TEST_JSON_FILE = os.path.join(dirname(os.getcwd()), 'data', 'empty_test.json')


test_json_list = [
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

check_quantity_list = [1, 2, 3, 4, 5, 6]

def test_mask():
    assert mask('Visa Gold 7305799447374042') == 'Visa Gold 7305 79** **** 4042'
    assert mask('Maestro 4598300720424501') == 'Maestro 4598 30** **** 4501'
    assert mask('Счет 97584898735659638967') == 'Счет **8967'


@pytest.fixture
def test_list():
    test_object = []
    o = Operation(test_json_list[0].get("id"),
                  test_json_list[0].get("state"),
                  test_json_list[0].get("date"),
                  test_json_list[0].get("operationAmount"),
                  test_json_list[0].get("description"),
                  test_json_list[0].get("from"),
                  test_json_list[0].get("to"))
    test_object.append(o)
    return test_object[0]


def test_class_methods(test_list):
    assert test_list.get_date() == "26.08.2019"
    assert test_list.get_description() == "Перевод организации"
    assert test_list.get_payer() == "Maestro 1596837868705199"
    assert test_list.get_receiver() == "Счет 64686473678894779589"
    assert test_list.get_amount() == "31957.58 руб."


def test_create_operation_objects():
    assert create_operation_objects('bla_bla_vla.json') is None
    assert create_operation_objects(TEST_JSON_FILE) is None


def test_json_file_check():
    assert json_file_check(test_json_list) is True
    assert json_file_check(test_json_list_err) is False

def test_check_quantity():
    assert check_quantity(test_json_list) == 1
    assert check_quantity(check_quantity_list) == 5
