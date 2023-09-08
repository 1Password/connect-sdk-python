"""Python AsyncClient for connecting to 1Password Connect"""
import httpx
from httpx import HTTPError
import json
import os

from onepasswordconnectsdk.serializer import Serializer
from onepasswordconnectsdk.utils import build_headers, is_valid_uuid, PathBuilder
from onepasswordconnectsdk.errors import (
    FailedToRetrieveItemException,
    FailedToRetrieveVaultException,
)
from onepasswordconnectsdk.models import Item, ItemVault


class AsyncClient:
    """Python Async Client Class"""

    def __init__(self, url: str, token: str):
        """Initialize async client"""
        self.url = url
        self.token = token
        self.session = self.create_session(url, token)
        self.serializer = Serializer()

    def create_session(self, url: str, token: str):
        return httpx.AsyncClient(base_url=url, headers=self.build_headers(token))

    def build_headers(self, token: str):
        return build_headers(token)

    async def __aexit__(self):
        await self.session.aclose()

    async def get_file(self, file_id: str, item_id: str, vault_id: str):
        url = PathBuilder().vaults(vault_id).items(item_id).files(file_id).build()
        response = await self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to retrieve item. Received {response.status_code}\
                                     for {url} with message: {response.json().get('message')}"
            )
        return self.serializer.deserialize(response.content, "File")

    async def get_files(self, item_id: str, vault_id: str):
        url = PathBuilder().vaults(vault_id).items(item_id).files().build()
        response = await self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to retrieve item. Received {response.status_code}\
                             for {url} with message: {response.json().get('message')}"
            )
        return self.serializer.deserialize(response.content, "list[File]")

    async def get_file_content(self, file_id: str, item_id: str, vault_id: str, content_path: str = None):
        url = content_path
        if content_path is None:
            url = PathBuilder().vaults(vault_id).items(item_id).files(file_id).content().build()
        response = await self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to retrieve items. Received {response.status_code} \
                     for {url} with message: {response.json().get('message')}"
            )
        return response.content

    async def download_file(self, file_id: str, item_id: str, vault_id: str, path: str):
        file_object = await self.get_file(file_id, item_id, vault_id)
        filename = file_object.name or "1password_item_file.txt"
        content = await self.get_file_content(file_id, item_id, vault_id, file_object.content_path)
        global_path = os.path.join(path, filename)

        file = open(global_path, "wb")
        file.write(content)
        file.close()

    async def get_item(self, item: str, vault: str):
        """Get a specific item

        Args:
            item (str): the id or title of the item to be fetched
            vault (str): the id or name of the vault in which to get the item from

        Raises:
            FailedToRetrieveItemException: Thrown when a HTTP error is returned
            from the 1Password Connect API

        Returns:
            Item object: The found item
        """

        vault_id = vault
        if not is_valid_uuid(vault):
            vault = await self.get_vault_by_title(vault)
            vault_id = vault.id

        if is_valid_uuid(item):
            return await self.get_item_by_id(item, vault_id)
        else:
            return await self.get_item_by_title(item, vault_id)

    async def get_item_by_id(self, item_id: str, vault_id: str):
        """Get a specific item by uuid

        Args:
            item_id (str): The id of the item to be fetched
            vault_id (str): The id of the vault in which to get the item from

        Raises:
            FailedToRetrieveItemException: Thrown when a HTTP error is returned
            from the 1Password Connect API

        Returns:
            Item object: The found item
        """
        url = PathBuilder().vaults(vault_id).items(item_id).build()
        response = await self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to retrieve item. Received {response.status_code}\
                     for {url} with message: {response.json().get('message')}"
            )
        return self.serializer.deserialize(response.content, "Item")

    async def get_item_by_title(self, title: str, vault_id: str):
        """Get a specific item by title

        Args:
            title (str): The title of the item to be fetched
            vault_id (str): The id of the vault in which to get the item from

        Raises:
            FailedToRetrieveItemException: Thrown when a HTTP error is returned
            from the 1Password Connect API

        Returns:
            Item object: The found item
        """
        filter_query = f'title eq "{title}"'
        url = PathBuilder().vaults(vault_id).items().query("filter", filter_query).build()
        response = await self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to retrieve items. Received {response.status_code} \
                     for {url} with message: {response.json().get('message')}"
            )

        if len(response.json()) != 1:
            raise FailedToRetrieveItemException(
                f"Found {len(response.json())} items in vault {vault_id} with \
                    title {title}"
            )

        item_summary = self.serializer.deserialize(response.content, "list[SummaryItem]")[0]
        return await self.get_item_by_id(item_summary.id, vault_id)

    async def get_items(self, vault_id: str, filter_query: str = None):
        """Returns a list of item summaries for the specified vault

        Args:
            vault_id (str): The id of the vault in which to get the items from

        Raises:
            FailedToRetrieveItemException: Thrown when a HTTP error is returned
            from the 1Password Connect API

        Returns:
            List[SummaryItem]: A list of summarized items
        """
        if filter_query is None:
            url = PathBuilder().vaults(vault_id).items().build()
        else:
            url = PathBuilder().vaults(vault_id).items().query("filter", filter_query).build()
        response = await self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to retrieve items. Received {response.status_code} \
                     for {url} with message: {response.json().get('message')}"
            )

        return self.serializer.deserialize(response.content, "list[SummaryItem]")

    async def delete_item(self, item_id: str, vault_id: str):
        """Deletes a specified item from a specified vault

        Args:
            item_id (str): The id of the item in which to delete the item from
            vault_id (str): The id of the vault in which to delete the item
            from

        Raises:
            FailedToRetrieveItemException: Thrown when a HTTP error is returned
            from the 1Password Connect API
        """
        url = PathBuilder().vaults(vault_id).items(item_id).build()
        response = await self.build_request("DELETE", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to delete item. Received {response.status_code}\
                     for {url} with message: {response.json().get('message')}"
            )

    async def create_item(self, vault_id: str, item: Item):
        """Creates an item at the specified vault

        Args:
            vault_id (str): The id of the vault in which add the item to
            item (Item): The item to create

        Raises:
            FailedToRetrieveItemException: Thrown when a HTTP error is returned
            from the 1Password Connect API

        Returns:
            Item: The created item
        """

        url = PathBuilder().vaults(vault_id).items().build()
        response = await self.build_request("POST", url, item)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to post item. Received {response.status_code}\
                    for {url} with message: {response.json().get('message')}"
            )
        return self.serializer.deserialize(response.content, "Item")

    async def update_item(self, item_uuid: str, vault_id: str, item: Item):
        """Update the specified item at the specified vault.

        Args:
            item_uuid (str): The id of the item in which to update
            vault_id (str): The id of the vault in which to update the item
            item (Item): The updated item

        Raises:
            FailedToRetrieveItemException: Thrown when a HTTP error is returned
            from the 1Password Connect API

        Returns:
            Item: The updated item
        """
        url = PathBuilder().vaults(vault_id).items(item_uuid).build()
        item.id = item_uuid
        item.vault = ItemVault(id=vault_id)

        response = await self.build_request("PUT", url, item)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to post item. Received {response.status_code}\
                    for {url} with message: {response.json().get('message')}"
            )
        return self.serializer.deserialize(response.content, "Item")

    async def get_vault(self, vault_id: str):
        """Returns the vault with the given vault_id

        Args:
            vault_id (str): The id of the vault in which to fetch

        Raises:
            FailedToRetrieveVaultException: Thrown when a HTTP error is
            returned from the 1Password Connect API

        Returns:
            Vault: The specified vault
        """
        url = PathBuilder().vaults(vault_id).build()
        response = await self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveVaultException(
                f"Unable to retrieve vault. Received {response.status_code} \
                     for {url} with message {response.json().get('message')}"
            )

        return self.serializer.deserialize(response.content, "Vault")

    async def get_vault_by_title(self, name: str):
        """Returns the vault with the given name

        Args:
            name (str): The name of the vault in which to fetch

        Raises:
            FailedToRetrieveVaultException: Thrown when a HTTP error is
            returned from the 1Password Connect API

        Returns:
            Vault: The specified vault
        """
        filter_query = f'name eq "{name}"'
        url = PathBuilder().vaults().query("filter", filter_query).build()
        response = await self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveVaultException(
                f"Unable to retrieve vaults. Received {response.status_code} \
                     for {url} with message {response.json().get('message')}"
            )

        if len(response.json()) != 1:
            raise FailedToRetrieveItemException(
                f"Found {len(response.json())} vaults with \
                    name {name}"
            )

        return self.serializer.deserialize(response.content, "list[Vault]")[0]

    async def get_vaults(self):
        """Returns all vaults for service account set in client

        Raises:
            FailedToRetrieveVaultException: Thrown when a HTTP error is
            returned from the 1Password Connect API

        Returns:
            List[Vault]: All vaults for the service account in use
        """
        url = PathBuilder().vaults().build()
        response = await self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveVaultException(
                f"Unable to retrieve vaults. Received {response.status_code} \
                     for {url} with message {response.json().get('message')}"
            )

        return self.serializer.deserialize(response.content, "list[Vault]")

    def build_request(self, method: str, path: str, body=None):
        """Builds a http request
        Parameters:
        method (str): The rest method to be used
        path (str): The request path
        body (str): The request body

        Returns:
        Response object: The request response
        """

        if body:
            serialized_body = json.dumps(self.serializer.sanitize_for_serialization(body))
            response = self.session.request(method, path, data=serialized_body)
        else:
            response = self.session.request(method, path)
        return response

    def deserialize(self, response, response_type):
        return self.serializer.deserialize(response, response_type)

    def sanitize_for_serialization(self, obj):
        return self.serializer.sanitize_for_serialization(obj)
