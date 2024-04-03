import os

from httpx._client import DEFAULT_TIMEOUT_CONFIG, Timeout

UUIDLength = 26
ENV_CLIENT_REQUEST_TIMEOUT = "OP_CONNECT_CLIENT_REQ_TIMEOUT"


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


class PathBuilder:
    def __init__(self, version: str = "/v1"):
        self.path: str = version

    def build(self) -> str:
        return self.path

    def vaults(self, uuid: str = None) -> 'PathBuilder':
        self._append_path("vaults")
        if uuid is not None:
            self._append_path(uuid)
        return self

    def items(self, uuid: str = None) -> 'PathBuilder':
        self._append_path("items")
        if uuid is not None:
            self._append_path(uuid)
        return self

    def files(self, uuid: str = None) -> 'PathBuilder':
        self._append_path("files")
        if uuid is not None:
            self._append_path(uuid)
        return self

    def content(self) -> 'PathBuilder':
        self._append_path("content")
        return self

    def query(self, key: str, value: str) -> 'PathBuilder':
        key_value_pair = f"{key}={value}"
        self._append_path(query=key_value_pair)
        return self

    def _append_path(self, path_chunk: str = None, query: str = None) -> 'PathBuilder':
        if path_chunk is not None:
            self.path += f"/{path_chunk}"
        if query is not None:
            self.path += f"?{query}"


def get_timeout() -> Timeout:
    """Get the timeout to be used in the HTTP Client"""
    raw_timeout = os.getenv(ENV_CLIENT_REQUEST_TIMEOUT, '0.0')
    if raw_timeout == 'None':
        return Timeout(None)  # disable all timeouts
    elif raw_timeout.isnumeric():
        timeout = float(raw_timeout)
        return timeout if timeout else DEFAULT_TIMEOUT_CONFIG
    else:
        return DEFAULT_TIMEOUT_CONFIG
