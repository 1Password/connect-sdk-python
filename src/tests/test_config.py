from httpx import Response
import onepasswordconnectsdk
from onepasswordconnectsdk import client

VAULT_ID = "abcdefghijklmnopqrstuvwxyz"
ITEM_NAME1 = "TEST USER"
ITEM_ID1 = "wepiqdxdzncjtnvmv5fegud4q1"
ITEM_NAME2 = "Another User"
ITEM_ID2 = "wepiqdxdzncjtnvmv5fegud4q2"
HOST = "https://mock_host"
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


def test_load(respx_mock):
    mock_items_list1 = respx_mock.get(f"v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_NAME1}\"").mock(
        return_value=Response(200, json=[item])
    )
    mock_item1 = respx_mock.get(f"v1/vaults/{VAULT_ID}/items/{ITEM_ID1}").mock(return_value=Response(200, json=item))
    mock_items_list2 = respx_mock.get(f"v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_NAME2}\"").mock(
        return_value=Response(200, json=[item2])
    )
    mock_item2 = respx_mock.get(f"v1/vaults/{VAULT_ID}/items/{ITEM_ID2}").mock(return_value=Response(200, json=item2))

    config_with_values = onepasswordconnectsdk.load(SS_CLIENT, CONFIG_CLASS)

    assert mock_items_list1.called
    assert mock_item1.called
    assert mock_items_list2.called
    assert mock_item2.called

    assert config_with_values.username == USERNAME_VALUE
    assert config_with_values.password == PASSWORD_VALUE
    assert config_with_values.host == HOST_VALUE


def test_load_dict(respx_mock):
    config_dict = {
        "username": {
            "opitem": ITEM_NAME1,
            "opfield": ".username",
            "opvault": VAULT_ID
        },
        "password": {
            "opitem": ITEM_NAME1,
            "opfield": "section1.password",
            "opvault": VAULT_ID
        }
    }

    mock_item_list = respx_mock.get(f"v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_NAME1}\"").mock(
        return_value=Response(200, json=[item]))
    mock_item = respx_mock.get(f"v1/vaults/{VAULT_ID}/items/{ITEM_ID1}").mock(return_value=Response(200, json=item))

    config_with_values = onepasswordconnectsdk.load_dict(SS_CLIENT, config_dict)

    assert mock_item_list.called
    assert mock_item.called
    assert config_with_values['username'] == USERNAME_VALUE
    assert config_with_values['password'] == PASSWORD_VALUE


item = {
    "id": ITEM_ID1,
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
    "id": ITEM_ID2,
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
