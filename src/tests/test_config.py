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
API_KEY_VALUE = "sk-test-abc123"
DB_PORT_VALUE = "5432"


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
            "id": "username",
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

# Item with field ids that differ from their labels, used to test
# the field.id fallback lookup path.
ITEM_NAME3 = "Service Credentials"
ITEM_ID3 = "wepiqdxdzncjtnvmv5fegud4q3"

item_with_distinct_ids = {
    "id": ITEM_ID3,
    "title": ITEM_NAME3,
    "vault": {
        "id": VAULT_ID
    },
    "category": "LOGIN",
    "sections": [
        {
            "id": "Section_A1B2C3",
            "label": "api_settings"
        }
    ],
    "fields": [
        {
            "id": "Field_X9Y8Z7",
            "label": "API Key",
            "value": API_KEY_VALUE,
            "section": {
                "id": "Section_A1B2C3"
            }
        },
        {
            "id": "Field_D4E5F6",
            "label": "Database Port",
            "value": DB_PORT_VALUE
        }
    ]
}


def test_load_dict_by_field_id(respx_mock):
    """load_dict should resolve fields by id when label doesn't match."""
    config_dict = {
        "api_key": {
            "opitem": ITEM_NAME3,
            "opfield": "api_settings.Field_X9Y8Z7",
            "opvault": VAULT_ID
        },
        "db_port": {
            "opitem": ITEM_NAME3,
            "opfield": ".Field_D4E5F6",
            "opvault": VAULT_ID
        }
    }

    respx_mock.get(
        f"v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_NAME3}\""
    ).mock(return_value=Response(200, json=[item_with_distinct_ids]))
    respx_mock.get(
        f"v1/vaults/{VAULT_ID}/items/{ITEM_ID3}"
    ).mock(return_value=Response(200, json=item_with_distinct_ids))

    config_values = onepasswordconnectsdk.load_dict(SS_CLIENT, config_dict)

    assert config_values["api_key"] == API_KEY_VALUE
    assert config_values["db_port"] == DB_PORT_VALUE


def test_load_by_field_id(respx_mock):
    """load should resolve fields by id when label doesn't match."""

    class ConfigById:
        api_key: f'opitem:"{ITEM_NAME3}" opfield:api_settings.Field_X9Y8Z7 opvault:{VAULT_ID}' = None
        db_port: f'opitem:"{ITEM_NAME3}" opfield:.Field_D4E5F6 opvault:{VAULT_ID}' = None

    respx_mock.get(
        f"v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_NAME3}\""
    ).mock(return_value=Response(200, json=[item_with_distinct_ids]))
    respx_mock.get(
        f"v1/vaults/{VAULT_ID}/items/{ITEM_ID3}"
    ).mock(return_value=Response(200, json=item_with_distinct_ids))

    config_obj = onepasswordconnectsdk.load(SS_CLIENT, ConfigById())

    assert config_obj.api_key == API_KEY_VALUE
    assert config_obj.db_port == DB_PORT_VALUE


def test_load_dict_label_takes_priority(respx_mock):
    """When both label and id could match, label should win."""
    ambiguous_item = {
        "id": "wepiqdxdzncjtnvmv5fegud4q4",
        "title": "Ambiguous Item",
        "vault": {"id": VAULT_ID},
        "category": "LOGIN",
        "fields": [
            {
                "id": "shared_ref",
                "label": "wrong_label",
                "value": "value_from_id_match"
            },
            {
                "id": "other_id",
                "label": "shared_ref",
                "value": "value_from_label_match"
            }
        ]
    }

    config_dict = {
        "result": {
            "opitem": "Ambiguous Item",
            "opfield": ".shared_ref",
            "opvault": VAULT_ID
        }
    }

    respx_mock.get(
        f"v1/vaults/{VAULT_ID}/items?filter=title eq \"Ambiguous Item\""
    ).mock(return_value=Response(200, json=[ambiguous_item]))
    respx_mock.get(
        f"v1/vaults/{VAULT_ID}/items/wepiqdxdzncjtnvmv5fegud4q4"
    ).mock(return_value=Response(200, json=ambiguous_item))

    config_values = onepasswordconnectsdk.load_dict(SS_CLIENT, config_dict)

    assert config_values["result"] == "value_from_label_match"
