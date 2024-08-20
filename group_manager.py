import uuid
from group import Group


class GroupManager:
    def __init__(self) -> None:
        self._groups: list[Group] = []
    
    def get_groups(self) -> list[Group]:
        return self._groups

    def add_group(self, name: str) -> Group:
        try:
            id_ = self._groups[-1].id + 1
        except:
            id_ = 1

        group = Group(
            id=id_,
            name=name
        )
        self._groups.append(group)
    
    def remove_group(self, group: Group):
        self._groups.remove(group)
    
    def get_group_by_id(self, id: int) -> Group | None:
        for group in self._groups:
            if group.id == id:
                return group
        return None
    
    def get_group_by_name(self, name: str) -> Group | None:
        for group in self._groups:
            if group.name == name:
                return group
        return None
    
    def edit_group(self, group: Group, name: str) -> Group:
        for group_ in self._groups:
            if group_.name == group.name:
                group_.name = name
                return group
