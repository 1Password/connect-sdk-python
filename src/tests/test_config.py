import json
from requests import Session, Response
from unittest.mock import Mock, patch
import pytest
import onepasswordconnectsdk
from onepasswordconnectsdk import client, models

VAULT_ID = "some_vault_id"
ITEM_NAME1 = "TEST USER"
ITEM_NAME2 = "Another User"
HOST = "mock_host"
TOKEN = "jwt_token"
SS_CLIENT = client.new_client(HOST, TOKEN)

USERNAME_VALUE = "new_user"
PASSWORD_VALUE = "password"
HOST_VALUE = "http://somehost"

class Config:
    username: f'opitem:"{ITEM_NAME1}" opfield:.username opvault:{VAULT_ID}' = None
    password: f'opitem:"{ITEM_NAME1}" opfield:section1.password opvault:{VAULT_ID}' = None
    host: f'opitem:"{ITEM_NAME2}" opfield:.host opvault:{VAULT_ID}' = None


CONFIG_CLASS = Config()

@patch.object(Session, 'request')
def test_load(mock):
    mock.return_value.ok = True
    mock.side_effect = get_item_side_effect

    config_with_values = onepasswordconnectsdk.load(SS_CLIENT, CONFIG_CLASS)
    assert mock.called
    assert config_with_values.username == USERNAME_VALUE
    assert config_with_values.password == PASSWORD_VALUE
    assert config_with_values.host == HOST_VALUE

@patch.object(Session, 'request')
def test_load_dict(mock):
    config_dict = {
        "username": {
            "opitem": ITEM_NAME1,
            "opfield": ".username",
            "opvault":VAULT_ID
        },
        "password": {
            "opitem": ITEM_NAME1,
            "opfield": "section1.password",
            "opvault": VAULT_ID
        }
    }
    mock.return_value.ok = True
    mock.side_effect = get_item_side_effect

    config_with_values = onepasswordconnectsdk.load_dict(SS_CLIENT, config_dict)
    assert mock.called
    assert config_with_values['username'] == USERNAME_VALUE
    assert config_with_values['password'] == PASSWORD_VALUE

def get_item_side_effect(method, url):
    response = Response()
    response.status_code = 200

    item = {
            "id": ITEM_NAME1,
            "title": ITEM_NAME1,
            "vault": {
                "id": VAULT_ID
            },
            "category": "LOGIN",
            "sections": [
                {
                    "id": "section1",
                    "label": "section1"
                }
            ],
            "fields": [
                {
                    "id": "password",
                    "label": "password",
                    "value": PASSWORD_VALUE,
                    "section": {
                        "id": "section1"
                    }
                },
                {
                    "id": "716C5B0E95A84092B2FE2CC402E0DDDF",
                    "label": "username",
                    "value": USERNAME_VALUE
                }
            ]
        }

    item2 = {
            "id": ITEM_NAME2,
            "title": ITEM_NAME2,
            "vault": {
                "id": VAULT_ID
            },
            "category": "LOGIN",
            "fields": [
                {
                    "id": "716C5B0E95A84092B2FE2CC402E0DDDF",
                    "label": "host",
                    "value": HOST_VALUE
                }
            ]
        }

    if ITEM_NAME1 in url:
        if "eq" in url:
            item = [item]
        else:
            item = item
    elif ITEM_NAME2 in url:
        if "eq" in url:
            item = [item2]
        else:
            item = item2

    response._content=str.encode(json.dumps(item))

    return response
