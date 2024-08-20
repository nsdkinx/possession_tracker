import uuid
from tag import Tag
from tag_color import TagColor


class TagManager:
    def __init__(self) -> None:
        self._tags: list[Tag] = []
    
    def get_tags(self) -> list[Tag]:
        return self._tags

    def add_tag(self, label: str, color: TagColor) -> Tag:
        tag = Tag(
            id=str(uuid.uuid4()),
            label=label,
            color=color
        )
        self._tags.append(tag)
        return tag
    
    def remove_tag(self, tag: Tag):
        for tag_ in self._tags:
            if tag.label == tag_.label:
                self._tags.remove(tag_)
    
    def edit_tag(self, tag: Tag, name: str, color: TagColor) -> Tag:
        for tag_ in self._tags:
            if tag_.label == tag.label:
                tag_.label = name
                tag_.color = color
                return tag_

    def get_tag_by_id(self, id: str) -> Tag | None:
        for tag in self._tags:
            if tag.id == id:
                return tag
        return None

    def get_tag_by_name(self, name: str) -> Tag | None:
        for tag in self._tags:
            if tag.label == name:
                return tag
        return None
