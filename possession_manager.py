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
        possession = Possession(
            id=str(uuid.uuid4),
            name=name,
            tags=tags,
            group=group
        )
        self._possessions.append(possession)
    
    def remove_possession(self, possession: Possession):
        self._possessions.remove(possession)
    
    def get_possession_by_id(self, id: str) -> Possession | None:
        for possession in self._possessions:
            if possession.id == id:
                return possession
        return None
