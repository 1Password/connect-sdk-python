import pytest
from httpx import Response
from onepasswordconnectsdk import async_client, client, models

VAULT_ID = "hfnjvi6aymbsnfc2xeeoheizda"
VAULT_TITLE = "VaultA"
ITEM_ID = "wepiqdxdzncjtnvmv5fegud4qy"
ITEM_TITLE = "Test Login"
HOST = "https://mock_host"
TOKEN = "jwt_token"
SS_CLIENT = client.new_client(HOST, TOKEN)
SS_CLIENT_ASYNC = async_client.new_async_client(HOST, TOKEN)


def test_get_item_by_id(respx_mock):
    expected_item = get_item()
    expected_path = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_item))

    item = SS_CLIENT.get_item_by_id(ITEM_ID, VAULT_ID)
    compare_items(expected_item, item)
    assert mock.called


@pytest.mark.asyncio
async def test_get_item_by_id_async(respx_mock):
    expected_item = get_item()
    expected_path = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_item))

    item = await SS_CLIENT_ASYNC.get_item_by_id(ITEM_ID, VAULT_ID)
    compare_items(expected_item, item)
    assert mock.called


def test_get_item_by_title(respx_mock):
    expected_item = get_item()
    expected_path_item_title = f"/v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_TITLE}\""
    expected_path_item = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    items_summary_mock = respx_mock.get(expected_path_item_title).mock(return_value=Response(200, json=get_items()))
    item_mock = respx_mock.get(expected_path_item).mock(return_value=Response(200, json=expected_item))

    item = SS_CLIENT.get_item_by_title(ITEM_TITLE, VAULT_ID)
    compare_items(expected_item, item)
    assert items_summary_mock.called
    assert item_mock.called


@pytest.mark.asyncio
async def test_get_item_by_title_async(respx_mock):
    expected_item = get_item()
    expected_path_item_title = f"/v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_TITLE}\""
    expected_path_item = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    items_summary_mock = respx_mock.get(expected_path_item_title).mock(return_value=Response(200, json=get_items()))
    item_mock = respx_mock.get(expected_path_item).mock(return_value=Response(200, json=expected_item))

    item = await SS_CLIENT_ASYNC.get_item_by_title(ITEM_TITLE, VAULT_ID)
    compare_items(expected_item, item)
    assert items_summary_mock.called
    assert item_mock.called


def test_get_item_by_item_id_vault_id(respx_mock):
    expected_item = get_item()
    expected_path = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_item))

    item = SS_CLIENT.get_item(ITEM_ID, VAULT_ID)
    compare_items(expected_item, item)
    assert mock.called


@pytest.mark.asyncio
async def test_get_item_by_item_id_vault_id_async(respx_mock):
    expected_item = get_item()
    expected_path = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_item))

    item = await SS_CLIENT_ASYNC.get_item(ITEM_ID, VAULT_ID)
    compare_items(expected_item, item)
    assert mock.called


def test_get_item_by_item_id_vault_title(respx_mock):
    expected_item = get_item()
    expected_path_vault_title = f"/v1/vaults?filter=name eq \"{VAULT_TITLE}\""
    expected_path_item = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    vaults_by_title_mock = respx_mock.get(expected_path_vault_title).mock(
        return_value=Response(200, json=get_vaults()))
    item_mock = respx_mock.get(expected_path_item).mock(return_value=Response(200, json=expected_item))

    item = SS_CLIENT.get_item(ITEM_ID, VAULT_TITLE)
    compare_items(expected_item, item)
    assert vaults_by_title_mock.called
    assert item_mock.called


@pytest.mark.asyncio
async def test_get_item_by_item_id_vault_title_async(respx_mock):
    expected_item = get_item()
    expected_path_vault_title = f"/v1/vaults?filter=name eq \"{VAULT_TITLE}\""
    expected_path_item = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    vaults_by_title_mock = respx_mock.get(expected_path_vault_title).mock(
        return_value=Response(200, json=get_vaults()))
    item_mock = respx_mock.get(expected_path_item).mock(return_value=Response(200, json=expected_item))

    item = await SS_CLIENT_ASYNC.get_item(ITEM_ID, VAULT_TITLE)
    compare_items(expected_item, item)
    assert vaults_by_title_mock.called
    assert item_mock.called


def test_get_item_by_item_title_vault_id(respx_mock):
    expected_item = get_item()
    expected_path_item_title = f"/v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_TITLE}\""
    expected_path_item = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    items_by_title_mock = respx_mock.get(expected_path_item_title).mock(
        return_value=Response(200, json=get_items()))
    item_mock = respx_mock.get(expected_path_item).mock(return_value=Response(200, json=expected_item))

    item = SS_CLIENT.get_item(ITEM_TITLE, VAULT_ID)
    compare_items(expected_item, item)
    assert items_by_title_mock.called
    assert item_mock.called


@pytest.mark.asyncio
async def test_get_item_by_item_title_vault_id_async(respx_mock):
    expected_item = get_item()
    expected_path_item_title = f"/v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_TITLE}\""
    expected_path_item = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    items_by_title_mock = respx_mock.get(expected_path_item_title).mock(
        return_value=Response(200, json=get_items()))
    item_mock = respx_mock.get(expected_path_item).mock(return_value=Response(200, json=expected_item))

    item = await SS_CLIENT_ASYNC.get_item(ITEM_TITLE, VAULT_ID)
    compare_items(expected_item, item)
    assert items_by_title_mock.called
    assert item_mock.called


def test_get_item_by_item_title_vault_title(respx_mock):
    expected_item = get_item()
    expected_path_vault_title = f"/v1/vaults?filter=name eq \"{VAULT_TITLE}\""
    expected_path_item_title = f"/v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_TITLE}\""
    expected_path_item = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    vaults_by_title_mock = respx_mock.get(expected_path_vault_title).mock(
        return_value=Response(200, json=get_vaults()))
    items_by_title_mock = respx_mock.get(expected_path_item_title).mock(
        return_value=Response(200, json=get_items()))
    item_mock = respx_mock.get(expected_path_item).mock(return_value=Response(200, json=expected_item))

    item = SS_CLIENT.get_item(ITEM_TITLE, VAULT_TITLE)
    compare_items(expected_item, item)
    assert vaults_by_title_mock.called
    assert items_by_title_mock.called
    assert item_mock.called


@pytest.mark.asyncio
async def test_get_item_by_item_title_vault_title_async(respx_mock):
    expected_item = get_item()
    expected_path_vault_title = f"/v1/vaults?filter=name eq \"{VAULT_TITLE}\""
    expected_path_item_title = f"/v1/vaults/{VAULT_ID}/items?filter=title eq \"{ITEM_TITLE}\""
    expected_path_item = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    vaults_by_title_mock = respx_mock.get(expected_path_vault_title).mock(
        return_value=Response(200, json=get_vaults()))
    items_by_title_mock = respx_mock.get(expected_path_item_title).mock(
        return_value=Response(200, json=get_items()))
    item_mock = respx_mock.get(expected_path_item).mock(return_value=Response(200, json=expected_item))

    item = await SS_CLIENT_ASYNC.get_item(ITEM_TITLE, VAULT_TITLE)
    compare_items(expected_item, item)
    assert vaults_by_title_mock.called
    assert items_by_title_mock.called
    assert item_mock.called


def test_get_items(respx_mock):
    expected_items = get_items()
    expected_path = f"/v1/vaults/{VAULT_ID}/items"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_items))

    items = SS_CLIENT.get_items(VAULT_ID)
    assert len(expected_items) == len(items)
    compare_summary_items(expected_items[0], items[0])
    assert mock.called


@pytest.mark.asyncio
async def test_get_items_async(respx_mock):
    expected_items = get_items()
    expected_path = f"/v1/vaults/{VAULT_ID}/items"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_items))

    items = await SS_CLIENT_ASYNC.get_items(VAULT_ID)
    assert len(expected_items) == len(items)
    compare_summary_items(expected_items[0], items[0])
    assert mock.called


def test_delete_item(respx_mock):
    expected_items = get_items()
    expected_path = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock = respx_mock.delete(expected_path).mock(return_value=Response(200, json=expected_items))

    SS_CLIENT.delete_item(ITEM_ID, VAULT_ID)
    assert mock.called


@pytest.mark.asyncio
async def test_delete_item_async(respx_mock):
    expected_items = get_items()
    expected_path = f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"

    mock = respx_mock.delete(expected_path).mock(return_value=Response(200, json=expected_items))

    await SS_CLIENT_ASYNC.delete_item(ITEM_ID, VAULT_ID)
    assert mock.called



def test_create_item(respx_mock):
    item = generate_full_item()
    mock = respx_mock.post(f"/v1/vaults/{item.vault.id}/items").mock(return_value=Response(201, json=item.to_dict()))

    created_item = SS_CLIENT.create_item(item.vault.id, item)
    assert mock.called
    compare_full_items(item, created_item)


@pytest.mark.asyncio
async def test_create_item_async(respx_mock):
    item = generate_full_item()
    mock = respx_mock.post(f"/v1/vaults/{item.vault.id}/items").mock(return_value=Response(201, json=item.to_dict()))

    created_item = await SS_CLIENT_ASYNC.create_item(item.vault.id, item)
    assert mock.called
    compare_full_items(item, created_item)


def test_update_item(respx_mock):
    item = generate_full_item()
    mock = respx_mock.put(f"/v1/vaults/{item.vault.id}/items/{item.id}").mock(return_value=Response(200, json=item.to_dict()))

    updated_item = SS_CLIENT.update_item(item.id, item.vault.id, item)
    assert mock.called
    compare_full_items(item, updated_item)


@pytest.mark.asyncio
async def test_update_item_async(respx_mock):
    item = generate_full_item()
    mock = respx_mock.put(f"/v1/vaults/{item.vault.id}/items/{item.id}").mock(return_value=Response(200, json=item.to_dict()))

    updated_item = await SS_CLIENT_ASYNC.update_item(item.id, item.vault.id, item)
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
    assert expected_field.get("id") == returned_field.id
    assert expected_field.get("label") == returned_field.label
    assert expected_field.get("value") == returned_field.value
    assert expected_field.get("purpose") == returned_field.purpose
    assert expected_field.get("section").get("id") == returned_field.section.id
    assert expected_field.get("type") == returned_field.type
    assert expected_field.get("totp") == returned_field.totp


def compare_sections(expected_section, returned_section):
    assert expected_section.get("id") == returned_section.id
    assert expected_section.get("label") == returned_section.label


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
