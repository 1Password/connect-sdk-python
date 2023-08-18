UUIDLength = 26


def is_valid_uuid(uuid):
    if len(uuid) is not UUIDLength:
        return False
    for c in uuid:
        valid = (c >= 'a' and c <= 'z') or (c >= '0' and c <= '9')
        if valid is False:
            return False
    return True


def build_headers(token: str):
    """Builds the headers needed to make a request to the server

    Returns:
        dict: The 1Password Connect API request headers
    """
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
