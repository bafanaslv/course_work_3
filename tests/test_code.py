import os
from os.path import dirname
from modules.main import load_json_file, create_operation_objects, mask_card, Operation

OPERATION_JSON_FILE = os.path.join(dirname(os.getcwd()), 'data', 'operations.json')
operation_list = load_json_file(OPERATION_JSON_FILE)


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
