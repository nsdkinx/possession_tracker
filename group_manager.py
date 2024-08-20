import uuid
from group import Group


class GroupManager:
    def __init__(self) -> None:
        self._groups: list[Group] = []
    
    def get_groups(self) -> list[Group]:
        return self._groups

    def add_group(self, name: str) -> Group:
        group = Group(
            id=str(uuid.uuid4),
            name=name
        )
        self._groups.append(group)
    
    def remove_group(self, group: Group):
        self._groups.remove(group)
    
    def get_group_by_id(self, id: str) -> Group | None:
        for group in self._groups:
            if group.id == id:
                return group
        return None
