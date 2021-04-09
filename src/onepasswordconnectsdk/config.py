import os
import shlex
from typing import List, Dict
from onepasswordconnectsdk.client import Client
from onepasswordconnectsdk.models import (
    SummaryItem,
    Item,
    ParsedField,
    ParsedItem,
    Section,
)
from onepasswordconnectsdk.models.constants import (
    ITEM_TAG,
    FIELD_TAG,
    VAULT_TAG,
    VAULT_ID_ENV_VARIABLE,
)


def load_dict(client: Client, config: dict):
    """Load: Takes a dictionary with keys specifiying the user
    desired naming scheme of the values to return. Each key's
    value is a dictionary that includes information on where
    to find the item field value in 1Password.

    Example dictionary
    {
        "foo": {
            "opitem": "Name of item in 1Password",  # noqa: RST301
            "opfield": "section_name.field_name"
        },  # noqa: RST203
        "bar": {
            "opitem": "Name of another item in 1Password",  # noqa: RST301
            "opfield": ".field_name",
            "opvault" "some_vault_id"
        }  # noqa: RST201
    }  # noqa: RST201

    opitem (required): describes the name of the item to access from 1Password

    offield (required): describes the name of the field to access within
    the specified item

    opvault: Only required if OP_VAULT is not set. Used to decribe the
    vault in which to fetch the item

    Args:
        client (Client): An instantied 1Password Connect client.

        config (dict): A dict with user specfied names for keys. Each key's
        value is a dictionary that includes information on where to find
        the item field value in 1Password.

    Returns:
        dict: A dictionary of user specified keys with values retrieved
        from 1Password
    """

    items: dict = {}
    config_values: Dict[str, str] = {}

    for field, tags in config.items():
        item_tag = tags.get(ITEM_TAG)
        field_tag = tags.get(FIELD_TAG)
        vault_tag = tags.get(VAULT_TAG)
        item_vault = _vault_uuid_for_field(field=field, vault_tag=vault_tag)
        key = f"{item_vault}/{item_tag}"
        item: ParsedItem = items.get(key)  # type: ignore

        if item:
            item.fields.append(ParsedField(field, field_tag))
        else:
            item = ParsedItem(
                vault_uuid=item_vault,
                item_title=item_tag,
                fields=[ParsedField(field, field_tag)],
            )
        items[key] = item
    for item_key, item in items.items():
        _set_values_for_item(client=client,
                             parsed_item=item,
                             config_dict=config_values)

    return config_values


def load(client: Client, config: object):
    """Load: Takes a an object with class attributes annotated with tags
    describing where to find desired fields in 1Password. Manipulates given object
    and fills attributes in with 1Password item field values.

    Example class object
    class Foo():
        foo: 'opitem:"Name of Item" opfield:section_name.field_name' # noqa: E501, RST301
        bar: 'opitem:"Name of another item" opfield:.field_name opvault:vault_id' # noqa: E501

    opitem (required): describes the name of the item to access from 1Password

    opfield (required): describes the name of the field to access
    within the specified item

    opvault: Only required if OP_VAULT is not set. Used to decribe
    the vault in which to fetch the item

    Args:
        client (Client): An instantied 1Password Connect client.
        config (object): An object of a custom annoted class.
    """
    items: dict = {}
    annotations = config.__class__.__annotations__

    for field, tags in annotations.items():
        parsed_tags = _parse_tags(tags)
        item_tag = parsed_tags.get(ITEM_TAG)
        field_tag = parsed_tags.get(FIELD_TAG)
        vault_tag = parsed_tags.get(VAULT_TAG)
        item_vault = _vault_uuid_for_field(field=field, vault_tag=vault_tag)
        key = f"{item_vault}/{item_tag}"
        item: ParsedItem = items.get(key)  # type: ignore

        if item:
            item.fields.append(ParsedField(field, field_tag))
        else:
            item = ParsedItem(
                vault_uuid=item_vault,
                item_title=item_tag,
                fields=[ParsedField(field, field_tag)],
            )
        items[key] = item

    for item_key, item in items.items():
        _set_values_for_item(client=client,
                             parsed_item=item,
                             config_object=config)

    return config


def _parse_tags(tags: str):
    """Takes a string of whitespace seperated tags
    and assigns them to a dict. Expects each tag to
    be of the format 'tag_name:tag_value'

    Args:
        tags (str): The tags to parse

    Returns:
        dict: The parsed tags
    """
    return dict(item.split(":") for item in shlex.split(tags))  # type: ignore


def _vault_uuid_for_field(field: str, vault_tag: dict):
    env_vault_uuid = os.environ.get(VAULT_ID_ENV_VARIABLE)
    if vault_tag:
        return vault_tag
    elif env_vault_uuid:
        return env_vault_uuid
    raise NoVaultSetForFieldException(
        f"There \
        is no vault for {field} field"
    )


def _set_values_for_item(
    client: Client,
    parsed_item: ParsedItem,
    config_dict={},
    config_object: object = None,
):
    # Retrieves a summary item
    summary_item: Item = client.get_item_by_title(
        parsed_item.item_title, parsed_item.vault_uuid
    )
    # Fetching the full item
    item: Item = client.get_item(summary_item.id, parsed_item.vault_uuid)

    sections = _convert_sections_to_dict(item.sections)

    for parsed_field in parsed_item.fields:
        if parsed_field.tag is None:
            raise NoFieldTagSetForFieldException(
                f"There is no {FIELD_TAG} specified \
                for {parsed_field.name}"
            )

        path_parts = parsed_field.tag.split(".")
        if len(path_parts) != 2:
            raise InvalidFieldPathException(
                f"Invalid field path format for \
                {parsed_field.name}"
            )

        value_found = False
        for field in item.fields:
            try:
                section_id = field.section.id
            except AttributeError:
                section_id = None

            if field.label == path_parts[1] and (
                section_id is None or section_id == sections[path_parts[0]]
            ):
                value_found = True

                if config_object:
                    setattr(config_object, parsed_field.name, field.value)
                else:
                    config_dict[parsed_field.name] = field.value
                break
        if not value_found:
            raise UnknownSectionAndFieldTag(
                f"There is no section {path_parts[0]} \
                for field {path_parts[1]}"
            )


def _convert_sections_to_dict(sections: List[Section]):
    if not sections:
        return {}
    section_dict = {section.label: section.id for section in sections}
    return section_dict


class ConfigurationError(RuntimeError):
    pass


class NoVaultSetForFieldException(ConfigurationError):
    pass


class NoFieldTagSetForFieldException(ConfigurationError):
    pass


class InvalidFieldPathException(ConfigurationError):
    pass


class UnknownSectionAndFieldTag(ConfigurationError):
    pass
