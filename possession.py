from dataclasses import dataclass

from group import Group
from tag import Tag


@dataclass
class Possession:
    id: int
    name: str
    tags: list[Tag]
    group: Group

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'tags': [tag.to_json() for tag in self.tags],
            'group': self.group.to_json()
        }
