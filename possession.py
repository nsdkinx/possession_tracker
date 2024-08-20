from dataclasses import dataclass

from group import Group
from tag import Tag


@dataclass
class Possession:
    id: int
    name: str
    tags: list[Tag]
    group: Group
