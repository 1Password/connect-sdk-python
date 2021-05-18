import os
import steps
import time

import onepasswordconnectsdk
from onepasswordconnectsdk.models import (ItemVault, Field)

op_connect_token = os.environ["OP_CONNECT_TOKEN"]
default_vault = os.environ["OP_VAULT"]
connect_host = os.environ["OP_CONNECT_HOST"]
secret_string = os.environ["SECRET_STRING"]

print(steps.steps['intro'])

# CREATE A NEW 1P CONNECT CLIENT
client = onepasswordconnectsdk.client.new_client_from_environment(connect_host)
print(steps.steps["step1"])

# CREATE A NEW ITEM
username_item = onepasswordconnectsdk.models.Item(
    title="Secret String",
    category="LOGIN",
    tags=["1password-connect"],
    fields=[Field(value=secret_string)])
print(steps.steps["step2"])

# ADD THE ITEM TO THE 1P VAULT
posted_item = client.create_item(default_vault, username_item)
print(steps.steps["step3"])

# GIVE SOME TIME SUCH THAT THE ITEM IS FOR SURE IN THE VAULT
time.sleep(10)

# RETRIEVE THE ITEM FROM THE VAULT
item3 = client.get_item(posted_item.id, default_vault)
print(steps.steps["step4"])

print(steps.steps["confirmation"])
answer = input()

while answer != ('y' or 'n'):
    print(steps.steps["confirmation2"])
    answer = input()

# DELETE THE ITEM FROM THE VAULT
if answer == 'y':
    client.delete_item(posted_item.id, default_vault)
    print(steps.steps["step5"])

print(steps.steps["outro"])
