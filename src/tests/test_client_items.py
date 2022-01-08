import json
from requests import Session, Response
from unittest.mock import patch
from onepasswordconnectsdk import client, models

VAULT_ID = "hfnjvi6aymbsnfc2xeeoheizda"
VAULT_TITLE = "VaultA"
ITEM_ID = "wepiqdxdzncjtnvmv5fegud4qy"
ITEM_TITLE = "Test Login"
HOST = "mock_host"
TOKEN = "jwt_token"
SS_CLIENT = client.new_client(HOST, TOKEN)


@patch.object(Session, 'request')
def test_get_item_by_id(mock):
    expected_item = get_item()
    expected_path = f"{HOST}/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock.return_value.ok = True
    response = Response()
    response.status_code = 200
    response._content = json.dumps(expected_item).encode("utf8")
    mock.return_value = response

    item = SS_CLIENT.get_item_by_id(ITEM_ID, VAULT_ID)
    compare_items(expected_item, item)
    mock.assert_called_with("GET", expected_path)


@patch.object(Session, 'request')
def test_get_item_by_title(mock):
    expected_item = get_item()
    expected_path_item_title = f"{HOST}/v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_TITLE}\""
    expected_path_item = f"{HOST}/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock.return_value.ok = True

    response_item_summary = Response()
    response_item_summary.status_code = 200
    response_item_summary._content = json.dumps(get_items()).encode("utf8")

    response_item = Response()
    response_item.status_code = 200
    response_item._content = json.dumps(get_item()).encode("utf8")

    mock.side_effect = [response_item_summary, response_item]

    item = SS_CLIENT.get_item_by_title(ITEM_TITLE, VAULT_ID)
    compare_items(expected_item, item)
    mock.assert_any_call("GET", expected_path_item_title)
    mock.assert_called_with("GET", expected_path_item)


@patch.object(Session, 'request')
def test_get_item_by_item_id_vault_id(mock):
    expected_item = get_item()
    expected_path = f"{HOST}/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock.return_value.ok = True
    response = Response()
    response.status_code = 200
    response._content = json.dumps(expected_item).encode("utf8")
    mock.return_value = response

    item = SS_CLIENT.get_item(ITEM_ID, VAULT_ID)
    compare_items(expected_item, item)
    mock.assert_called_with("GET", expected_path)


@patch.object(Session, 'request')
def test_get_item_by_item_id_vault_title(mock):
    expected_item = get_item()
    expected_path_vault_title = f"{HOST}/v1/vaults?filter=name eq \"{VAULT_TITLE}\""
    expected_path_item = f"{HOST}/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock.return_value.ok = True

    response_vault = Response()
    response_vault.status_code = 200
    response_vault._content = json.dumps(get_vaults()).encode("utf8")

    response_item = Response()
    response_item.status_code = 200
    response_item._content = json.dumps(expected_item).encode("utf8")

    mock.side_effect = [response_vault, response_item]

    item = SS_CLIENT.get_item(ITEM_ID, VAULT_TITLE)
    compare_items(expected_item, item)
    mock.assert_any_call("GET", expected_path_vault_title)
    mock.assert_called_with("GET", expected_path_item)


@patch.object(Session, 'request')
def test_get_item_by_item_title_vault_id(mock):
    expected_item = get_item()
    expected_path_item_title = f"{HOST}/v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_TITLE}\""
    expected_path_item = f"{HOST}/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock.return_value.ok = True

    response_item_summary = Response()
    response_item_summary.status_code = 200
    response_item_summary._content = json.dumps(get_items()).encode("utf8")

    response_item = Response()
    response_item.status_code = 200
    response_item._content = json.dumps(get_item()).encode("utf8")

    mock.side_effect = [response_item_summary, response_item]

    item = SS_CLIENT.get_item(ITEM_TITLE, VAULT_ID)
    compare_items(expected_item, item)
    mock.assert_any_call("GET", expected_path_item_title)
    mock.assert_called_with("GET", expected_path_item)


@patch.object(Session, 'request')
def test_get_item_by_item_title_vault_title(mock):
    expected_item = get_item()
    expected_path_vault_title = f"{HOST}/v1/vaults?filter=name eq \"{VAULT_TITLE}\""
    expected_path_item_title = f"{HOST}/v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_TITLE}\""
    expected_path_item = f"{HOST}/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock.return_value.ok = True

    response_vault = Response()
    response_vault.status_code = 200
    response_vault._content = json.dumps(get_vaults()).encode("utf8")

    response_item_summary = Response()
    response_item_summary.status_code = 200
    response_item_summary._content = json.dumps(get_items()).encode("utf8")

    response_item = Response()
    response_item.status_code = 200
    response_item._content = json.dumps(get_item()).encode("utf8")

    mock.side_effect = [response_vault, response_item_summary, response_item]

    item = SS_CLIENT.get_item(ITEM_TITLE, VAULT_TITLE)
    compare_items(expected_item, item)
    mock.assert_any_call("GET", expected_path_vault_title)
    mock.assert_any_call("GET", expected_path_item_title)
    mock.assert_called_with("GET", expected_path_item)


@patch.object(Session, 'request')
def test_get_items(mock):
    expected_items = get_items()
    expected_path = f"{HOST}/v1/vaults/{VAULT_ID}/items"

    mock.return_value.ok = True
    response = Response()
    response.status_code = 200
    response._content = json.dumps(expected_items).encode("utf8")
    mock.return_value = response

    items = SS_CLIENT.get_items(VAULT_ID)
    assert len(expected_items) == len(items)
    compare_summary_items(expected_items[0], items[0])
    mock.assert_called_with("GET", expected_path)


@patch.object(Session, 'request')
def test_delete_item(mock):
    expected_items = get_items()
    expected_path = f"{HOST}/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock.return_value.ok = True
    response = Response()
    response.status_code = 200
    response._content = json.dumps(expected_items).encode("utf8")
    mock.return_value = response

    SS_CLIENT.delete_item(ITEM_ID, VAULT_ID)
    mock.assert_called_with("DELETE", expected_path)


@patch.object(Session, 'request')
def test_create_item(mock):
    mock.return_value.ok = True
    mock.side_effect = create_item_side_effect

    item = generate_full_item()

    created_item = SS_CLIENT.create_item(VAULT_ID, item)
    assert mock.called
    compare_full_items(item, created_item)


@patch.object(Session, 'request')
def test_update_item(mock):
    mock.return_value.ok = True
    mock.side_effect = create_item_side_effect

    item = generate_full_item()

    updated_item = SS_CLIENT.update_item(ITEM_ID, VAULT_ID, item)
    assert mock.called
    compare_full_items(item, updated_item)


def compare_full_items(expected_item, returned_item):
    assert expected_item.id == returned_item.id
    assert expected_item.title == returned_item.title
    assert expected_item.vault.id == returned_item.vault.id
    assert expected_item.category == returned_item.category
    assert expected_item.last_edited_by == returned_item.last_edited_by
    assert expected_item.created_at == returned_item.created_at
    assert expected_item.updated_at == returned_item.updated_at

    assert len(expected_item.sections) == len(returned_item.sections)
    for i in range(len(expected_item.sections)):
        compare_full_item_sections(expected_item.sections[i], returned_item.sections[i])

    assert len(expected_item.fields) == len(returned_item.fields)
    for i in range(len(expected_item.fields)):
        compare_full_item_fields(expected_item.fields[i], returned_item.fields[i])


def create_item_side_effect(method, url, data):
    response = Response()
    response.status_code = 200
    response._content = data
    return response


def compare_full_item_fields(expected_field, returned_field):
    assert expected_field.id == returned_field.id
    assert expected_field.label == returned_field.label
    assert expected_field.value == returned_field.value
    assert expected_field.purpose == returned_field.purpose
    assert expected_field.section.id == returned_field.section.id
    assert expected_field.type == returned_field.type


def compare_full_item_sections(expected_section, returned_section):
    assert expected_section.id == returned_section.id
    assert expected_section.label == returned_section.label


def compare_summary_items(expected_item, returned_item):
    assert expected_item["id"] == returned_item.id
    assert expected_item["title"] == returned_item.title
    assert expected_item["vault"]["id"] == returned_item.vault.id
    assert expected_item["category"] == returned_item.category
    assert expected_item["version"] == returned_item.version


def compare_items(expected_item, returned_item):
    compare_summary_items(expected_item, returned_item)
    assert expected_item["lastEditedBy"] == returned_item.last_edited_by

    assert len(expected_item["sections"]) == len(returned_item.sections)
    for i in range(len(expected_item["sections"])):
        compare_sections(expected_item["sections"][i], returned_item.sections[i])

    assert len(expected_item["fields"]) == len(returned_item.fields)
    for i in range(len(expected_item["fields"])):
        compare_fields(expected_item["fields"][i], returned_item.fields[i])


def compare_fields(expected_field, returned_field):
    assert expected_field["id"] == returned_field.id
    assert expected_field["label"] == returned_field.label
    assert expected_field["value"] == returned_field.value
    assert expected_field["purpose"] == returned_field.purpose
    assert expected_field["section"]["id"] == returned_field.section.id
    assert expected_field["type"] == returned_field.type
    assert expected_field["totp"] == returned_field.totp


def compare_sections(expected_section, returned_section):
    assert expected_section["id"] == returned_section.id
    assert expected_section["label"] == returned_section.label


def get_items():
    return [{
        "id": "wepiqdxdzncjtnvmv5fegud4qy",
        "title": "Test Login",
        "version": 21,
        "vault": {
            "id": "hfnjvi6aymbsnfc2xeeoheizda"
        },
        "category": "LOGIN",
        "lastEditedBy": "DOIHOHSV2NHK5HMSOLCWJUXFDM",
        "createdAt": "2020-10-29T17:52:17Z",
        "updatedAt": "2020-11-10T14:05:53Z"
    }]


def get_item():
    return {
        "id": "wepiqdxdzncjtnvmv5fegud4qy",
        "title": "Test Login",
        "version": 21,
        "vault": {
            "id": "hfnjvi6aymbsnfc2xeeoheizda"
        },
        "category": "LOGIN",
        "sections": [
            {
                "id": "linked items",
                "label": "Related Items"
            },
            {
                "id": "Section_47DC4DDBF26640AB8B8618DA36D5A492",
                "label": "section"
            }
        ],
        "fields": [
            {
                "id": "password",
                "type": "CONCEALED",
                "purpose": "PASSWORD",
                "label": "password",
                "value": "Z9gKLhP{zxDJPGbYWFAtApzg",
                "entropy": 130.0688473607018,
                "section": {
                    "id": "Section_47DC4DDBF26640AB8B8618DA36D5A499"
                },
            },
            {
                "id": "716C5B0E95A84092B2FE2CC402E0DDDF",
                "section": {
                    "id": "Section_47DC4DDBF26640AB8B8618DA36D5A492"
                },
                "purpose": "USERNAME",
                "type": "STRING",
                "label": "something",
                "value": "test"
            },
            {
                "id": "TOTP_acf2fgvsa312c9sd4vs8jhkli",
                "section": {
                    "id": "Section_47DC4DDBF26640AB8B8618DA36D5A492"
                },
                "type": "OTP",
                "label": "one-time password",
                "value": "otpauth://totp=testop?secret=test",
                "totp": "134253"
            }
        ],
        "lastEditedBy": "DOIHOHSV2NHK5HMSOLCWJUXFDM",
        "createdAt": "2020-10-29T17:52:17Z",
        "updatedAt": "2020-11-10T14:05:53Z"
    }


def get_vaults():
    return [
        {
            "id": "hfnjvi6aymbsnfc2xeeoheizda",
            "name": "VaultA",
            "attributeVersion": 2,
            "contentVersion": 196,
            "items": 2,
            "type": "USER_CREATED",
        }
    ]


def generate_full_item():
    item = models.Item(vault=models.ItemVault(id="av223f76ydutdngislnkbz6z5u"),
                       id="kp2td65r4wbuhocwhhijpdbfqq",
                       title="newtitle",
                       category="LOGIN",
                       tags=["secret-service"],
                       fields=[models.Field(value="new_user",
                                            purpose="USERNAME",
                                            type="STRING",
                                            section=models.FieldSection(
                                                id="Section_47DC4DDBF26640AB8B8618DA36D5A499"))],
                       sections=[models.Section(id="id", label="label")])
    return item
