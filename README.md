# 1Password Connect Python SDK

The 1Password Connect SDK provides access to the 1Password via 1Password Connect hosted on your infrastructure. The library is intended to be used by Python applications to simplify accessing `items` in 1Password `vaults`.

## Prerequisites

- 1Password Connect deployed in your infrastructure.
## Installation

To install the 1Password Connect Python SDK use the following command:
```bash
$ pip install onepasswordconnectsdk
```

To install a specific release of the 1Password Connect Python SDK use the following command:
```bash
$ pip install onepasswordconnectsdk==1.0.1
```

## Usage

**Import 1Password Connect Python SDK**

```python
import onepasswordconnectsdk
```

**Environment Variables**

- **OP_CONNECT_TOKEN** – The token to be used to authenticate with the 1Password Connect API.
- **OP_VAULT** - The default vault to fetch items from if not specified.

**Creating a Client**

There are two methods available for creating a client:

- `new_client_from_environment`: Builds a new client for interacting with 1Password Connect using the `OP_CONNECT_TOKEN` *environment variable (ie a 1Password Connect API token)* and the hostname of 1Password Connect.
- `new_client`: Builds a new client for interacting with 1Password Connect. Accepts the hostname of 1Password Connect and the API token generated for the application.

```python
from onepasswordconnectsdk.client import (
    Client,
    new_client_from_environment,
    new_client
)

# creating client using OP_CONNECT_TOKEN environment variable
client: Client = new_client_from_environment(
     "{1Password_Connect_Host}")

# creating client by supplying hostname and 1Password Connect API token
client: Client = new_client(
    "{1Password_Connect_Host}",
    "{1Password_Connect_API_Token}")
```

**Get Item**

Get a specific item by item and vault uuids:

```python
client.get_item("{item_id}", "{vault_id}")
```

**Get Item By Title**

Get item by item title and vault id

```python
client.get_item_by_title("{item_title}", "{vault_id}")
```

**Get Items**

Get a summarized list of all items for a specified vault

```python
client.get_items("{vault_id}")
```

**Delete Item**

Delete an item by item and vault ids:

```python
client.delete_item("{item_id}", "{vault_id}")
```

**Create Item**

Create an item in the specified vault.

```python
# Example item creation. Create an item with your desired arguments. 
item = onepasswordconnectsdk.models.Item(vault=ItemVault(id="av223f76ydutdngislnkbz6z5u"),
                                      id="kp2td65r4wbuhocwhhijpdbfqq",
                                      title="newtitle",
                                      category="LOGIN",
                                      tags=["1password-connect"],
                                      fields=[Field(value="new_user",
                                                                  purpose="USERNAME")],
                                      )
client.create_item("{vault_id}", item)
```

**Update Item**

Item the item with the specified item and vault ids. The existing item will be overwritten with the newly supplied item.

```python
# Example item creation. Create an item with your desired arguments. 
item = onepasswordconnectsdk.models.Item(vault=ItemVault(id="av223f76ydutdngislnkbz6z5u"),
                                      id="kp2td65r4wbuhocwhhijpdbfqq",
                                      title="newtitle",
                                      category="LOGIN",
                                      tags=["1password-connect"],
                                      fields=[Field(value="new_user",
                                                                  purpose="USERNAME")],
                                      )
client.update_item("{item_id}", "{vault_id}", item)
```

**Get Vault**

Get vault by vault id

```python
client.get_vault("{vault_id}")
```

**Get Vaults**

Retrieve all vaults available to the service account.

```python
client.get_vaults()
```

**Load Configuration**

Users can create `classes` or `dicts` that describe fields they wish to get the values from in 1Password. Two convienience methods are provided that will handle the fetching of values for these fields:

- **load_dict**: Takes a dictionary with keys specifying the user desired naming scheme of the values to return. Each key's value is a dictionary that includes information on where to find the item field value in 1Password. This returns a dictionary of user specified keys with values retrieved from 1Password
- **load**: Takes an object with class attributes annotated with tags describing where to find desired fields in 1Password. Manipulates given object and fills attributes in with 1Password item field values.

```python
# example dict configuration for onepasswordconnectsdk.load_dict(CONFIG)
CONFIG = {
    "server": {
        "opitem": "My database item",
        "opfield": "specific_section.hostname",
        "opvault": "some_vault_id",
    },
    "database": {
        "opitem": "My database item",
        "opfield": ".database",
    },
    "username": {
        "opitem": "My database item",
        "opfield": ".username",
    },
    "password": {
        "opitem": "My database item",
        "opfield": ".password",
    },
}

values_dict = onepasswordconnectsdk.load_dict(CONFIG)
```

```python
# example class configuration for onepasswordconnectsdk.load(CONFIG)
class Config:
    server: 'opitem:"My database item" opvault:some_vault_id opfield:specific_section.hostname' = None
    database: 'opitem:"My database item" opfield:.database' = None
    username: 'opitem:"My database item" opfield:.username' = None
    password: 'opitem:"My database item" opfield:.password' = None

CONFIG = Config()

values_object = onepasswordconnectsdk.load(CONFIG)
```

## Development

**Testing**

```bash
make test
```

## Security

1Password requests you practice responsible disclosure if you discover a vulnerability. 

Please file requests via [**BugCrowd**](https://bugcrowd.com/agilebits). 

For information about security practices, please visit our [Security homepage](https://bugcrowd.com/agilebits).
