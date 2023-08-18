from onepasswordconnectsdk.connect import PathBuilder

VAULT_ID = "hfnjvi6aymbsnfc2xeeoheizda"
ITEM_ID = "wepiqdxdzncjtnvmv5fegud4qy"
FILE_ID = "fileqdxczsc2tn32vsfegud123"


def test_all_vaults_path():
    path = PathBuilder().vaults().build()
    assert path == "/v1/vaults"


def test_single_vault_path():
    path = PathBuilder().vaults(VAULT_ID).build()
    assert path == f"/v1/vaults/{VAULT_ID}"


def test_all_items_path():
    path = PathBuilder().vaults(VAULT_ID).items().build()
    assert path == f"/v1/vaults/{VAULT_ID}/items"


def test_filter_items_path():
    path = PathBuilder().vaults(VAULT_ID).items().query("filter", "title").build()
    assert path == f"/v1/vaults/{VAULT_ID}/items?filter=title"


def test_single_item_path():
    path = PathBuilder().vaults(VAULT_ID).items(ITEM_ID).build()
    assert path == f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}"


def test_all_files_path():
    path = PathBuilder().vaults(VAULT_ID).items(ITEM_ID).files().build()
    assert path == f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}/files"


def test_single_file_path():
    path = PathBuilder().vaults(VAULT_ID).items(ITEM_ID).files(FILE_ID).build()
    assert path == f"/v1/vaults/{VAULT_ID}/items/{ITEM_ID}/files/{FILE_ID}"
