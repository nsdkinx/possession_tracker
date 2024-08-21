import flet_core.client_storage
from possession import Possession
from group import Group
from tag import Tag


class PossessionManager:
    def __init__(self, client_storage: flet_core.client_storage.ClientStorage) -> None:
        self._client_storage = client_storage
    
    async def prepare(self):
        if not await self._client_storage.contains_key_async('pt.possessions'):
            await self._client_storage.set_async(key='pt.possessions', value=[])

    async def get_possessions(self) -> list[Possession]:
        json_data = await self._client_storage.get_async('pt.possessions')
        return [Possession(**data) for data in json_data]

    async def add_possession(self, name: str, tags: list[Tag], group: Group) -> Possession:
        possessions = await self.get_possessions()
        try:
            id_ = possessions[-1].id + 1
        except:
            id_ = 1

        possession = Possession(
            id=id_,
            name=name,
            tags=tags,
            group=group
        )

        possessions.append(possession.to_json())

        await self._client_storage.set_async(
            key='pt.possessions',
            value=[p.to_json() for p in possessions]
        )
        
        return possession
    
    async def remove_possession(self, possession: Possession):
        possessions = await self.get_possessions()
        possessions.remove(possession)
        await self._client_storage.set_async(
            key='pt.possessions',
            value=[p.to_json() for p in possessions]
        )
    
    async def get_possession_by_id(self, id: int) -> Possession | None:
        possessions = await self.get_possessions()
        for possession in possessions:
            if possession.id == id:
                return possession
        return None
    
    async def get_possession_by_name(self, name: str) -> Possession | None:
        possessions = await self.get_possessions()
        for possession in possessions:
            if possession.name == name:
                return possession
        return None
    
    async def edit_possession(self, possession: Possession, name: str, group: Group, tags: list[Tag]) -> Possession:
        possessions = await self.get_possessions()
        for possession_ in possessions:
            if possession_.name == possession.name:
                possession_.name = name
                possession_.group = group
                possession.tags = tags

                await self._client_storage.set_async(
                    key='pt.possessions',
                    value=[p.to_json() for p in possessions]
                )

                return possession_
