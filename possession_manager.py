import uuid
from possession import Possession
from group import Group
from tag import Tag


class PossessionManager:
    def __init__(self) -> None:
        self._possessions: list[Possession] = []
    
    def get_possessions(self) -> list[Possession]:
        return self._possessions

    def add_possession(self, name: str, tags: list[Tag], group: Group) -> Possession:
        try:
            id_ = self._possessions[-1].id + 1
        except:
            id_ = 1

        possession = Possession(
            id=id_,
            name=name,
            tags=tags,
            group=group
        )
        self._possessions.append(possession)
        return possession
    
    def remove_possession(self, possession: Possession):
        self._possessions.remove(possession)
    
    def get_possession_by_id(self, id: int) -> Possession | None:
        for possession in self._possessions:
            if possession.id == id:
                return possession
        return None
    
    def get_possession_by_name(self, name: str) -> Possession | None:
        for possession in self._possessions:
            if possession.name == name:
                return possession
        return None
    
    def edit_possession(self, possession: Possession, name: str, group: Group, tags: list[Tag]) -> Possession:
        for possession_ in self._possessions:
            if possession_.name == possession.name:
                possession_.name = name
                possession_.group = group
                possession.tags = tags
                return possession_
