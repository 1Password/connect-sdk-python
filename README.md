<!-- Image sourced from https://blog.1password.com/introducing-secrets-automation/ -->
<img alt="" role="img" src="https://blog.1password.com/posts/2021/secrets-automation-launch/header.svg"/>

<div align="center">
  <h1>1Password Connect SDK for Python</h1>
  <p>Access your 1Password items in your Python applications through your self-hosted <a href="https://developer.1password.com/docs/connect">1Password Connect server</a>.</p>
  <a href="link/to/dev-portal">
    <img alt="Get started" src="https://user-images.githubusercontent.com/45081667/226940040-16d3684b-60f4-4d95-adb2-5757a8f1bc15.png" height="37"/>
  </a>
</div>

---

The 1Password Connect SDK provides access to 1Password via [1Password Connect](https://developer.1password.com/docs/connect) hosted in your infrastructure. The library is intended to be used by Python applications to simplify accessing items in 1Password vaults.

## ✨ Quickstart

1. Install the 1Password Connect Python SDK:

   ```sh
   pip install onepasswordconnectsdk
   ```

2. Use the SDK:

   - Read a secret:

     ```python
     from onepasswordconnectsdk.client import (
         Client,
         new_client,
     }

     connect_client: Client = new_client(
         "{1Password_Connect_Host}",
         "{1Password_Connect_API_Token}"
     )

     client.get_item("{item_id}", "{vault_id}")
     ```

   - Write a secret:

     ```python
     from onepasswordconnectsdk.client import (
         Client,
         new_client,
     }

     connect_client: Client = new_client(
         "{1Password_Connect_Host}",
         "{1Password_Connect_API_Token}"
     )

     # Example item creation. Create an item with your desired arguments.
     item = Item(
         vault=ItemVault(id=op_vault),
         id="custom_id",
         title="newtitle",
         category="LOGIN",
         tags=["1password-connect"],
         fields=[Field(value="new_user", purpose="USERNAME")],
     )
     new_item = op_client.create_item(op_vault, item)
     ```

For more examples, check out [USAGE.md](USAGE.md).

## 💙 Community & Support

- File an [issue](https://github.com/1Password/connect-sdk-python/issues) for bugs and feature requests.
- Join the [Developer Slack workspace](https://join.slack.com/t/1password-devs/shared_invite/zt-1halo11ps-6o9pEv96xZ3LtX_VE0fJQA).
- Subscribe to the [Developer Newsletter](https://1password.com/dev-subscribe/).

## 🔐 Security

1Password requests you practice responsible disclosure if you discover a vulnerability.

Please file requests via [**BugCrowd**](https://bugcrowd.com/agilebits).

For information about security practices, please visit the [1Password Bug Bounty Program](https://bugcrowd.com/agilebits).

<!-- # 1Password Connect Python SDK

[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org)
[![PyPI version](https://badge.fury.io/py/onepasswordconnectsdk.svg)](https://badge.fury.io/py/onepasswordconnectsdk)
![CI](https://github.com/1Password/connect-sdk-python/workflows/Test/badge.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://en.wikipedia.org/wiki/MIT_License)
[![codecov](https://codecov.io/gh/1Password/connect-sdk-python/branch/main/graph/badge.svg?token=VBPCH0CU2E)](https://codecov.io/gh/1Password/connect-sdk-python)

The 1Password Connect SDK provides access to 1Password via [1Password Connect](https://support.1password.com/secrets-automation/) hosted in your infrastructure. The library is intended to be used by Python applications to simplify accessing items in 1Password vaults.

## Prerequisites

- [1Password Connect](https://support.1password.com/secrets-automation/#step-2-deploy-a-1password-connect-server) deployed in your infrastructure
## Installation

To install the 1Password Connect Python SDK:
```bash
$ pip install onepasswordconnectsdk
```

To install a specific release of the 1Password Connect Python SDK:
```bash
$ pip install onepasswordconnectsdk==1.0.1
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

-->
