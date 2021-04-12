"""Python Client for connecting to 1Password Connect"""
from dateutil.parser import parse
import json
import os
import re
import six
import requests
import datetime
from requests.exceptions import HTTPError
import onepasswordconnectsdk
from onepasswordconnectsdk.models import Item, ItemVault


ENV_SERVICE_ACCOUNT_JWT_VARIABLE = "OP_CONNECT_TOKEN"


class Client:

    PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types
    NATIVE_TYPES_MAPPING = {
        "int": int,
        "long": int if six.PY3 else long,  # type: ignore # noqa: F821
        "float": float,
        "str": str,
        "bool": bool,
        "date": datetime.date,
        "datetime": datetime.datetime,
        "object": object,
    }

    """Python Client Class"""

    def __init__(self, url: str, token: str):
        """Initialize client"""
        self.url = url
        self.token = token
        self.session = self.create_session()

    def create_session(self):
        session = requests.Session()
        session.headers.update(self.build_headers())
        return session

    def build_headers(self):
        """Builds the headers needed to make a request to the server
        Parameters:

        Returns:
        dict: The 1Password Connect API request headers
        """

        headers = {}
        headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"
        return headers

    def get_item(self, item_id: str, vault_id: str):
        """Get a specific item by uuid
        Parameters:
        item_id (str): The id of the item to be fetched
        vault_id (str): The id of the vault in which to get the item from

        Returns:
        Item object: The found item
        """
        url = f"/v1/vaults/{vault_id}/items/{item_id}"

        response = self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to retrieve item. Received {response.status_code}\
                     for {url} with message: {response.json().get('message')}"
            )
        return self.deserialize(response.content, "Item")

    def get_item_by_title(self, title: str, vault_id: str):
        """Get a specific item by title
        Parameters:
        title (str): The title of the item to be fetched
        vault_id (str): The id of the vault in which to get the item from

        Returns:
        Item object: A summary of the found item
        """
        filter_query = f'title eq "{title}"'
        url = f"/v1/vaults/{vault_id}/items?filter={filter_query}"

        response = self.build_request("GET", url)
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

        return self.deserialize(response.content, "list[SummaryItem]")[0]

    def get_items(self, vault_id: str):
        """Returns a list of item summaries for the specified vault

        Args:
            vault_id (str): The id of the vault in which to get the items from

        Raises:
            FailedToRetrieveItemException: Thrown when a HTTP error is returned
            from the 1Password Connect API

        Returns:
            List[SummaryItem]: A list of summarized items
        """
        url = f"/v1/vaults/{vault_id}/items"

        response = self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to retrieve items. Received {response.status_code} \
                     for {url} with message: {response.json().get('message')}"
            )

        return self.deserialize(response.content, "list[SummaryItem]")

    def delete_item(self, item_id: str, vault_id: str):
        """Deletes a specified item from a specified vault

        Args:
            item_id (str): The id of the item in which to delete the item from
            vault_id (str): The id of the vault in which to delete the item
            from

        Raises:
            FailedToRetrieveItemException: Thrown when a HTTP error is returned
            from the 1Password Connect API
        """
        url = f"/v1/vaults/{vault_id}/items/{item_id}"

        response = self.build_request("DELETE", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to delete item. Received {response.status_code}\
                     for {url} with message: {response.json().get('message')}"
            )

    def create_item(self, vault_id: str, item: Item):
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

        url = f"/v1/vaults/{vault_id}/items"

        response: requests.Response = self.build_request("POST", url, item)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to post item. Received {response.status_code}\
                    for {url} with message: {response.json().get('message')}"
            )
        return self.deserialize(response.content, "Item")

    def update_item(self, item_uuid: str, vault_id: str, item: Item):
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
        url = f"/v1/vaults/{vault_id}/items/{item_uuid}"
        item.id = item_uuid
        item.vault = ItemVault(id=vault_id)

        response: requests.Response = self.build_request("PUT", url, item)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveItemException(
                f"Unable to post item. Received {response.status_code}\
                    for {url} with message: {response.json().get('message')}"
            )
        return self.deserialize(response.content, "Item")

    def get_vault(self, vault_id: str):
        """Returns the vault with the given vault_id

        Args:
            vault_id (str): The id of the vault in which to fetch

        Raises:
            FailedToRetrieveVaultException: Thrown when a HTTP error is
            returned from the 1Password Connect API

        Returns:
            Vault: The specified vault
        """
        url = f"/v1/vaults/{vault_id}"
        response = self.build_request("GET", url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveVaultException(
                f"Unable to retrieve vault. Received {response.status_code} \
                     for {url} with message {response.json().get('message')}"
            )

        return self.deserialize(response.content, "Vault")

    def get_vaults(self):
        """Returns all vaults for service account set in client

        Raises:
            FailedToRetrieveVaultException: Thrown when a HTTP error is
            returned from the 1Password Connect API

        Returns:
            List[Vault]: All vaults for the service account in use
        """
        url = "/v1/vaults"
        response = self.build_request("GET", url)

        try:
            response.raise_for_status()
        except HTTPError:
            raise FailedToRetrieveVaultException(
                f"Unable to retrieve vaults. Received {response.status_code} \
                     for {url} with message {response.json().get('message')}"
            )

        return self.deserialize(response.content, "list[Vault]")

    def build_request(self, method: str, path: str, body=None):
        """Builds a http request
        Parameters:
        method (str): The rest method to be used
        path (str): The request path
        body (str): The request body

        Returns:
        Response object: The request response
        """
        url = f"{self.url}{path}"

        if body:
            serialized_body = json.dumps(self.sanitize_for_serialization(body))
            response = self.session.request(method, url, data=serialized_body)
        else:
            response = self.session.request(method, url)
        return response

    def deserialize(self, response, response_type):
        """Deserializes response into an object.

        :param response: RESTResponse object to be deserialized.
        :param response_type: class literal for
            deserialized object, or string of class name.

        :return: deserialized object.
        """
        # fetch data from response object
        try:
            data = json.loads(response)
        except ValueError:
            data = response

        return self.__deserialize(data, response_type)

    def sanitize_for_serialization(self, obj):
        """Builds a JSON POST object.

        If obj is None, return None.
        If obj is str, int, long, float, bool, return directly.
        If obj is datetime.datetime, datetime.date convert to string
        in iso8601 format.
        If obj is list, sanitize each element in the list.
        If obj is dict, return the dict.
        If obj is OpenAPI model, return the properties dict.

        :param obj: The data to serialize.
        :return: The serialized form of data.
        """
        if obj is None:
            return None
        elif isinstance(obj, self.PRIMITIVE_TYPES):
            return obj
        elif isinstance(obj, list):
            return [self.sanitize_for_serialization(sub_obj) for sub_obj in obj]  # noqa: E501
        elif isinstance(obj, tuple):
            return tuple(self.sanitize_for_serialization(sub_obj) for sub_obj in obj)  # noqa: E501
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        if isinstance(obj, dict):
            obj_dict = obj
        else:
            # Convert model obj to dict except
            # attributes `openapi_types`, `attribute_map`
            # and attributes which value is not None.
            # Convert attribute name to json key in
            # model definition for request.
            obj_dict = {
                obj.attribute_map[attr]: getattr(obj, attr)
                for attr, _ in six.iteritems(obj.openapi_types)
                if getattr(obj, attr) is not None
            }

        return {
            key: self.sanitize_for_serialization(val)
            for key, val in six.iteritems(obj_dict)
        }

    def __deserialize(self, data, klass):
        """Deserializes dict, list, str into an object.

        :param data: dict, list or str.
        :param klass: class literal, or string of class name.

        :return: object.
        """
        if data is None:
            return None

        if type(klass) == str:
            if klass.startswith("list["):
                sub_kls = re.match(r"list\[(.*)\]", klass).group(1)
                return [self.__deserialize(sub_data, sub_kls) for sub_data in data]  # noqa: E501

            if klass.startswith("dict("):
                sub_kls = re.match(r"dict\(([^,]*), (.*)\)", klass).group(2)
                return {
                    k: self.__deserialize(v, sub_kls) for k, v in six.iteritems(data)  # noqa: E501
                }

            # convert str to class
            if klass in self.NATIVE_TYPES_MAPPING:
                klass = self.NATIVE_TYPES_MAPPING[klass]
            else:
                klass = getattr(onepasswordconnectsdk.models, klass)

        if klass in self.PRIMITIVE_TYPES:
            return self.__deserialize_primitive(data, klass)
        elif klass == object:
            return self.__deserialize_object(data)
        elif klass == datetime.date:
            return self.__deserialize_date(data)
        elif klass == datetime.datetime:
            return self.__deserialize_datetime(data)
        else:
            return self.__deserialize_model(data, klass)

    def __deserialize_primitive(self, data, klass):
        """Deserializes string to primitive type.

        :param data: str.
        :param klass: class literal.

        :return: int, long, float, str, bool.
        """
        try:
            return klass(data)
        except UnicodeEncodeError:
            return six.text_type(data)
        except TypeError:
            return data

    def __deserialize_object(self, value):
        """Return an original value.

        :return: object.
        """
        return value

    def __deserialize_date(self, string):
        """Deserializes string to date.

        :param string: str.
        :return: date.
        """
        try:
            return parse(string).date()
        except ImportError:
            return string
        except ValueError:
            raise FailedToDeserializeException(
                f'Failed to parse `{0}`\
                 as date object".format(string)'
            )

    def __deserialize_datetime(self, string):
        """Deserializes string to datetime.

        The string should be in iso8601 datetime format.

        :param string: str.
        :return: datetime.
        """
        try:
            return parse(string)
        except ImportError:
            return string
        except ValueError:
            raise FailedToDeserializeException(
                f'Failed to parse `{0}`\
                 as date object".format(string)'
            )

    def __deserialize_model(self, data, klass):
        """Deserializes list or dict to model.

        :param data: dict, list.
        :param klass: class literal.
        :return: model object.
        """
        has_discriminator = False
        if (
            hasattr(klass, "get_real_child_model")
            and klass.discriminator_value_class_map
        ):
            has_discriminator = True

        if not klass.openapi_types and has_discriminator is False:
            return data

        kwargs = {}
        if (
            data is not None
            and klass.openapi_types is not None
            and isinstance(data, (list, dict))
        ):
            for attr, attr_type in six.iteritems(klass.openapi_types):
                if klass.attribute_map[attr] in data:
                    value = data[klass.attribute_map[attr]]
                    kwargs[attr] = self.__deserialize(value, attr_type)

        instance = klass(**kwargs)

        if has_discriminator:
            klass_name = instance.get_real_child_model(data)
            if klass_name:
                instance = self.__deserialize(data, klass_name)
        return instance


def new_client(url: str, token: str):
    """Builds a new client for interacting with 1Password Connect
    Parameters:
    url: The url of the 1Password Connect API
    token: The 1Password Service Account token

    Returns:
    Client: The 1Password Connect client
    """
    return Client(url=url, token=token)


def new_client_from_environment(url: str):
    """Builds a new client for interacting with 1Password Connect
    using the OP_TOKEN environment variable

    Parameters:
    url: The url of the 1Password Connect API
    token: The 1Password Service Account token

    Returns:
    Client: The 1Password Connect client
    """
    token = os.environ.get(ENV_SERVICE_ACCOUNT_JWT_VARIABLE)

    if token is None:
        raise EnvironmentTokenNotSetException(
            "There is no token available in the "
            f"{ENV_SERVICE_ACCOUNT_JWT_VARIABLE} variable"
        )

    return Client(url=url, token=token)


class OnePasswordConnectSDKError(RuntimeError):
    pass


class EnvironmentTokenNotSetException(OnePasswordConnectSDKError, TypeError):
    pass


class FailedToRetrieveItemException(OnePasswordConnectSDKError):
    pass


class FailedToRetrieveVaultException(OnePasswordConnectSDKError):
    pass


class FailedToDeserializeException(OnePasswordConnectSDKError, TypeError):
    pass
