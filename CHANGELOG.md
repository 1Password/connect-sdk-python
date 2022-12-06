[//]: # (START/LATEST)
# Latest

## Features
  * A user-friendly description of a new feature. {issue-number}

## Fixes
 * A user-friendly description of a fix. {issue-number}

## Security
 * A user-friendly description of a security fix. {issue-number}

---

[//]: # "START/v1.3.0"

# v1.3.0

## Features

- The TOTP code of a OTP field can now be accessed using the `.totp` property of a field. {#33}
- Release of the SDK also includes `wheel` format. {#45}

## Fixes

- Sections without a label can now be correctly accessed. {#49}
- Retrieving an item no longer returns "Invalid value for `type`" or "Invalid value for `category`" when retrieving an item with a field type or item category that is not defined in the SDK. {#52,#54}

---

[//]: # "START/v1.2.0"

# v1.2.0

## Features

- Add support for downloading documents stored in 1Password {#26}

## Fixes

- Updates to README to clarify how to use HOST_NAME {#25}
- Fixed load and load_dict method examples in the README {#35}
- get_item_by_tile now retrieves item details instead of a summary {#27}
- retrieving items using the get_item method can now be done using either vault/item names or ids {#27}
- added pipeline for running tests {#28}

---

[//]: # "START/v1.1.0"

# v1.1.0

## Features

- Connect host can now also be supplied through the `OP_CONNECT_HOST` envrionment variable.
- The `API_CREDENTIAL` category is now supported. {#13}

## Fixes

- The `OTP` field type is no longer considered to be invalid. {#12}

---

[//]: # "START/v1.0.1"

# v1.0.1

## Fixes

- Code snippet for setting up client now functions correctly.
- Package correctly shows information like readme and the GitHub repository on PyPi.

---

[//]: # "START/v1.0.0"

# v1.0.0

## Features

- Release Automation
- Updating pip install instructions in readme
- Converting models to use more user friendly names

---

[//]: # "START/v0.0.1"

# v0.0.1

## Features

- Inaugural release for the 1Password Connect Python SDK.
- API Client
- Models generated from our OpenAPIv3 spec
- Support for reading, updating, creating, and deleting Items in 1Password vaults.

---
