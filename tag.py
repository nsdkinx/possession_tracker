from dataclasses import dataclass

from tag_color import TagColor


@dataclass
class Tag:
    id: int
    label: str
    color: TagColor
