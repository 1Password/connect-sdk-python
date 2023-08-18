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
