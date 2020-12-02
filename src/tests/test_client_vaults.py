import json
from requests import Session, Response
from unittest.mock import Mock, patch
import pytest
from onepasswordconnectsdk import client, models

VAULT_ID = "some_vault_id"
HOST = "mock_host"
TOKEN = "jwt_token"
SS_CLIENT = client.new_client(HOST, TOKEN)

@patch.object(Session, 'request')
def test_get_vaults(mock):
    expected_vaults = list_vaults()
    expected_path = f"{HOST}/v1/vaults"

    mock.return_value.ok = True
    response = Response()
    response.status_code = 200
    response._content = json.dumps(expected_vaults)
    mock.return_value = response

    vaults = SS_CLIENT.get_vaults()
    compare_vaults(expected_vaults[0], vaults[0])
    mock.assert_called_with("GET", expected_path)

@patch.object(Session, 'request')
def test_get_vault(mock):
    expected_vault = get_vault()
    expected_path = f"{HOST}/v1/vaults/{VAULT_ID}"

    mock.return_value.ok = True
    response = Response()
    response.status_code = 200
    response._content = json.dumps(expected_vault)
    mock.return_value = response

    vault = SS_CLIENT.get_vault(VAULT_ID)
    compare_vaults(expected_vault, vault)
    mock.assert_called_with("GET", expected_path)

def list_vaults():
    return [
        get_vault()
    ]

def get_vault():
    return {
        "id": "hfnjvi6aymbsnfc2xeeoheizda",
        "name": "VaultA",
        "attributeVersion": 2,
        "contentVersion": 196,
        "items": 2,
        "type": "USER_CREATED",
    }

def compare_vaults(expected_vault, returned_vault):
    assert expected_vault["id"] == returned_vault.id
    assert expected_vault["name"] == returned_vault.name
    assert expected_vault["attributeVersion"] == returned_vault.attribute_version
    assert expected_vault["contentVersion"] == returned_vault.content_version
    assert expected_vault["items"] == returned_vault.items
    assert expected_vault["type"] == returned_vault.type