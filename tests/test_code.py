import pytest
import os
from os.path import dirname
from modules.main import load_json_file, create_operation_objects, mask_card, Operation, main

OPERATION_JSON_FILE = os.path.join(dirname(os.getcwd()), 'operations.json')
operation_list = load_json_file(OPERATION_JSON_FILE)


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


def test_load_json_file():
    assert isinstance(operation_list, list)
    assert len(operation_list) > 0
    assert "id" in operation_list[0]
    assert "state" in operation_list[0]
    assert "date" in operation_list[0]
    assert "operationAmount" in operation_list[0]
    assert "description" in operation_list[0]
    assert "to" in operation_list[0]


def test_create_operation_objects():
    assert isinstance(create_operation_objects(OPERATION_JSON_FILE), list)
    assert isinstance(create_operation_objects(OPERATION_JSON_FILE)[0], Operation)


def test_mask_card():
    assert mask_card('Visa Gold 7305799447374042') == 'Visa Gold 7305 79** **** 4042'
    assert mask_card('Maestro 4598300720424501') == 'Maestro 4598 30** **** 4501'
    assert mask_card('Счет 97584898735659638967') == 'Счет **8967'


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
