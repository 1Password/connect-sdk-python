# Python Connect SDK Example

This example has been created in order to illustrate the main available functionality with regard to item manipulation, in the Python Connect SDK.
Given a (secret) string, this example will create an item, add it to given vault, retrieve it and, eventually, remove it.

## Prerequisites

In order to be able to run this example, one will need:

* [Docker](https://docs.docker.com/install/), installed and running
* an [1Password Connect](https://support.1password.com/secrets-automation/#step-2-deploy-a-1password-connect-server) instance, hosted on your infrastructure
* a Connect token, with read/write permissions for at least one vault accessible by the service account


## Running the example

Build the Python Docker example:
```
 docker build -t  python-connect-sdk-example .
```

Run the Docker example with the required fields passed as environment variables:
```
docker run -it -e OP_CONNECT_TOKEN=<YOUR_CONNECT_TOKEN> -e OP_VAULT=<YOUR_VAULT_ID> /
    -e 1PASSWORD_CONNECT_HOST=<YOUR_CONNECT_HOST> -e SECRET_STRING=<ANY_RANDOM_STRING> /
    python-connect-sdk-example
```

If your Connect instance is deployed locally, the `1PASSWORD_CONNECT_HOST` environment variable should be set to `http://host.docker.internal:8080`.

You will now see, in real time, the 5 different steps (creation of client, creation of item, posting to vault, retrieval from vault, deletion) as they happen.
