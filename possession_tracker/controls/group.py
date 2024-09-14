from __future__ import annotations

from typing import Callable

import flet

from possession_tracker.database import Database


class Group(flet.ListTile):
    def __init__(
            self,
            group_id: int,
            group_name: str,
            on_click: Callable | None = None
    ) -> None:
        super().__init__()
        self.group_id = group_id
        self.group_name = group_name

        self.leading = flet.Text(str(self.group_id), opacity=0.5, size=20)
        self.title = flet.Text(self.group_name, size=18)
        self.on_click = on_click

    @classmethod
    async def create_new_group(
            cls,
            group_name: str,
            database: Database
    ) -> Group:
        group_dict_object = await database.create_group(group_name)
        return cls(
            group_id=group_dict_object['group_id'],
            group_name=group_dict_object['group_name']
        )

    @classmethod
    async def get_all(cls, database: Database) -> list[Group]:
        all_groups_dict = await database.get_all_groups()
        return [
            cls(group_id, group_object['group_name'])
            for group_id, group_object in all_groups_dict.items()
        ]

    @classmethod
    async def get_by_id(cls, group_id: int, database: Database) -> Group:
        all_groups_dict = await database.get_all_groups()
        group_object = all_groups_dict[group_id]
        return cls(
            group_id=group_id,
            group_name=group_object['group_name']
        )

    async def delete(self, database: Database) -> None:
        return await database.delete_group(self.group_id)

    async def change_name(self, new_name: str, database: Database):
        await database.modify_group(
            group_id=self.group_id,
            new_group_name=new_name
        )
        self.title.value = new_name
        self.title.update()
        self.update()
