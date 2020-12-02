from dataclasses import dataclass


@dataclass
class ParsedField:
    name: str
    tag: str
