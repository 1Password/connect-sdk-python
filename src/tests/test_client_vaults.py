import pytest
from httpx import Response
from onepasswordconnectsdk import async_client, client

VAULT_ID = "hfnjvi6aymbsnfc2xeeoheizda"
VAULT_NAME = "VaultA"
HOST = "https://mock_host"
TOKEN = "jwt_token"
SS_CLIENT = client.new_client(HOST, TOKEN)
SS_CLIENT_ASYNC = async_client.new_async_client(HOST, TOKEN)


def test_get_vaults(respx_mock):
    expected_vaults = list_vaults()
    expected_path = "/v1/vaults"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_vaults))

    vaults = SS_CLIENT.get_vaults()
    compare_vaults(expected_vaults[0], vaults[0])
    assert mock.called


@pytest.mark.asyncio
async def test_get_vaults_async(respx_mock):
    expected_vaults = list_vaults()
    expected_path = "/v1/vaults"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_vaults))

    vaults = await SS_CLIENT_ASYNC.get_vaults()
    compare_vaults(expected_vaults[0], vaults[0])
    assert mock.called


def test_get_vault(respx_mock):
    expected_vault = get_vault()
    expected_path = f"/v1/vaults/{VAULT_ID}"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_vault))

    vault = SS_CLIENT.get_vault(VAULT_ID)
    compare_vaults(expected_vault, vault)
    assert mock.called


@pytest.mark.asyncio
async def test_get_vault_async(respx_mock):
    expected_vault = get_vault()
    expected_path = f"/v1/vaults/{VAULT_ID}"

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_vault))

    vault = await SS_CLIENT_ASYNC.get_vault(VAULT_ID)
    compare_vaults(expected_vault, vault)
    assert mock.called


def test_get_vault_by_title(respx_mock):
    expected_vaults = list_vaults()
    expected_path = f"/v1/vaults?filter=name eq \"{VAULT_NAME}\""

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_vaults))

    vault = SS_CLIENT.get_vault_by_title(VAULT_NAME)
    compare_vaults(expected_vaults[0], vault)
    assert mock.called


@pytest.mark.asyncio
async def test_get_vault_by_title_async(respx_mock):
    expected_vaults = list_vaults()
    expected_path = f"/v1/vaults?filter=name eq \"{VAULT_NAME}\""

    mock = respx_mock.get(expected_path).mock(return_value=Response(200, json=expected_vaults))

    vault = await SS_CLIENT_ASYNC.get_vault_by_title(VAULT_NAME)
    compare_vaults(expected_vaults[0], vault)
    assert mock.called


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
