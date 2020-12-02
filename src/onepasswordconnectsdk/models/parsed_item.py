from dataclasses import dataclass
from typing import List
from onepasswordconnectsdk.models import ParsedField


@dataclass
class ParsedItem:
    vault_uuid: str
    item_title: str
    fields: List[ParsedField]
