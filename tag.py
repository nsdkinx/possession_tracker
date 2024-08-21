from dataclasses import dataclass

from tag_color import TagColor


@dataclass
class Tag:
    id: int
    label: str
    color: TagColor

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'label': self.label,
            'color': self.color.value
        }
