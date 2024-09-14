from typing import Sequence

from flet_core.client_storage import ClientStorage

from possession_tracker.ui.tag_color import TagColor


class Database:
    def __init__(self, client_storage: ClientStorage) -> None:
        self._client_storage = client_storage

    # --- UTILITY METHODS ---

    async def _add_to_client_storage_dict(self, key: str, value_to_add: dict, value_id: int) -> dict:
        _value: dict = await self._client_storage.get_async(key)
        _value[value_id] = value_to_add
        await self._client_storage.set_async(key=key, value=_value)
        return _value

    @staticmethod
    async def _create_incremental_id(on: Sequence):
        if not on:
            return 1
        else:
            return len(on) + 1

    # --- GENERAL METHODS ---

    async def is_first_run(self) -> bool:
        return not await self._client_storage.contains_key_async('pt.is_initialized')

    async def reset_or_create_database(self):
        await self._client_storage.set_async(key='pt.is_initialized', value=True)
        await self._client_storage.set_async(key='pt.possessions', value={})
        await self._client_storage.set_async(key='pt.tags', value={})
        await self._client_storage.set_async(key='pt.groups', value={})

    # --- TAGS ---

    async def create_tag(self, tag_label: str, tag_color: TagColor) -> dict:
        all_tags = await self.get_all_tags()
        tag_id = await self._create_incremental_id(on=all_tags)

        new_dict_tag_object = {
            'tag_label': tag_label,
            'tag_color': tag_color
        }
        await self._add_to_client_storage_dict(
            key='pt.tags',
            value_to_add=new_dict_tag_object,
            value_id=tag_id
        )
        return {
            'tag_id': tag_id,
            **new_dict_tag_object
        }

    async def get_all_tags(self) -> dict[int, dict[str, str]]:
        return await self._client_storage.get_async('pt.tags')

    async def delete_tag(self, tag_id: int) -> None:
        all_tags = await self.get_all_tags()
        all_tags.pop(tag_id)
        await self._client_storage.set_async(key='pt.tags', value=all_tags)

    async def modify_tag(
            self,
            tag_id: int,
            new_tag_label: str,
            new_tag_color: TagColor
    ) -> dict:
        all_tags = await self.get_all_tags()
        all_tags[tag_id]['tag_label'] = new_tag_label
        all_tags[tag_id]['tag_color'] = new_tag_color
        await self._client_storage.set_async(key='pt.tags', value=all_tags)
        return all_tags[tag_id]

    # --- GROUPS ---

    async def create_group(self, group_name: str) -> dict:
        all_groups = await self.get_all_groups()
        group_id = await self._create_incremental_id(on=all_groups)

        new_dict_group_object = {
            'group_name': group_name
        }
        await self._add_to_client_storage_dict(
            key='pt.groups',
            value_to_add=new_dict_group_object,
            value_id=group_id
        )
        return {
            'group_id': group_id,
            **new_dict_group_object
        }

    async def get_all_groups(self) -> dict[int, dict[str, str]]:
        return await self._client_storage.get_async('pt.groups')

    async def delete_group(self, group_id: int) -> None:
        all_groups = await self.get_all_groups()
        all_groups.pop(group_id)
        await self._client_storage.set_async(key='pt.groups', value=all_groups)

    async def modify_group(
            self,
            group_id: int,
            new_group_name: str
    ) -> dict:
        all_groups = await self.get_all_groups()
        all_groups[group_id]['group_name'] = new_group_name
        await self._client_storage.set_async(key='pt.groups', value=all_groups)
        return all_groups[group_id]

    # --- POSSESSIONS ---

    async def create_possession(
            self,
            possession_name: str,
            group_id: int,
            tag_ids: list[int]
    ) -> dict:
        all_possessions = await self.get_all_possessions()
        possession_id = await self._create_incremental_id(on=all_possessions)

        new_dict_possession_object = {
            'possession_name': possession_name,
            'group_id': group_id,
            'tag_ids': tag_ids
        }
        await self._add_to_client_storage_dict(
            key='pt.possessions',
            value_to_add=new_dict_possession_object,
            value_id=possession_id
        )
        return {
            'possession_id': group_id,
            **new_dict_possession_object
        }

    async def get_all_possessions(self) -> dict[int, dict[str, ...]]:
        return await self._client_storage.get_async('pt.possessions')

    async def get_rid_of_possession(self, possession_id: int) -> None:
        all_possessions = await self.get_all_possessions()
        all_possessions.pop(possession_id)
        await self._client_storage.set_async(key='pt.possessions', value=all_possessions)

    async def modify_possession(
            self,
            possession_id: int,
            new_possession_name: str,
            new_group_id: int,
            new_tag_ids: list[int]
    ) -> dict:
        all_possessions = await self.get_all_possessions()
        all_possessions[possession_id]['possession_name'] = new_possession_name
        all_possessions[possession_id]['group_id'] = new_group_id
        all_possessions[possession_id]['tag_ids'] = new_tag_ids
        await self._client_storage.set_async(key='pt.possessions', value=all_possessions)
        return all_possessions[possession_id]
