from dataclasses import dataclass


@dataclass
class Group:
    id: int
    name: str

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
