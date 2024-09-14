from __future__ import annotations

import flet
from typing import Callable
from possession_tracker.database import Database
from possession_tracker.controls.tag import Tag


class Possession(flet.ListTile):
    def __init__(
            self,
            possession_id: int,
            possession_name: str,
            group_id: int,
            tag_ids: list[int],
            on_edit_click: Callable | None = None,
            on_remove_click: Callable | None = None,
            list_tile_subtitle: flet.Control | None = None
    ) -> None:
        super().__init__()
        self.possession_id = possession_id
        self.possession_name = possession_name
        self.group_id = group_id
        self.tag_ids = tag_ids
        self._on_edit_click = on_edit_click
        self._on_remove_click = on_remove_click

        self.leading = flet.Text(str(possession_id), size=30, opacity=0.3)
        self.title = flet.Text(possession_name, size=18)
        self.subtitle = list_tile_subtitle

        self.trailing = flet.PopupMenuButton(
            items=[
                flet.PopupMenuItem(icon=flet.icons.DELETE, text='Избавиться', on_click=self._on_remove_click),
                flet.PopupMenuItem(icon=flet.icons.EDIT, text='Редактировать', on_click=self._on_edit_click)
            ]
        )

    @classmethod
    async def build_possession_control_with_tags(
            cls,
            possession_id: int,
            possession_name: str,
            group_id: int,
            tag_ids: list[int],
            database: Database,
            on_edit_click: Callable | None = None,
            on_remove_click: Callable | None = None
    ):
        # Workaround because __init__ method is fucking sync
        tags = [await Tag.get_by_id(tag_id, database) for tag_id in tag_ids]
        return cls(
            possession_id,
            possession_name,
            group_id,
            tag_ids,
            on_edit_click,
            on_remove_click,
            list_tile_subtitle=flet.Row(tags)
        )

    @classmethod
    async def create_new_possession(
            cls,
            possession_name: str,
            group_id: int,
            tag_ids: list[int],
            database: Database
    ) -> Possession:
        possession_dict_object = await database.create_possession(possession_name, group_id, tag_ids)
        return await cls.build_possession_control_with_tags(
            possession_id=possession_dict_object['possession_id'],
            possession_name=possession_dict_object['possession_name'],
            group_id=possession_dict_object['group_id'],
            tag_ids=possession_dict_object['tag_ids'],
            database=database
        )

    @classmethod
    async def get_all(cls, database: Database) -> list[Possession]:
        all_possessions_dict = await database.get_all_possessions()
        return [
            await cls.build_possession_control_with_tags(
                possession_id=possession_id,
                possession_name=possession_object['possession_name'],
                group_id=possession_object['group_id'],
                tag_ids=possession_object['tag_ids'],
                database=database
            )
            for possession_id, possession_object in all_possessions_dict.items()
        ]

    @classmethod
    async def get_by_id(cls, possession_id: int, database: Database) -> Possession:
        all_possessions = await database.get_all_possessions()
        possession_object = all_possessions[possession_id]
        return await cls.build_possession_control_with_tags(
            possession_id=possession_id,
            database=database,
            **possession_object
        )

    async def get_rid_of(self, database: Database) -> None:
        return await database.get_rid_of_possession(self.possession_id)

    async def change_name(self, new_name: str, database: Database):
        await database.modify_possession(
            possession_id=self.possession_id,
            new_possession_name=new_name,
            new_group_id=self.group_id,
            new_tag_ids=self.tag_ids
        )
        self.title.value = new_name
        self.title.update()
        self.update()

    async def change_group_id(self, new_group_id: int, database: Database):
        await database.modify_possession(
            possession_id=self.possession_id,
            new_possession_name=self.possession_name,
            new_group_id=new_group_id,
            new_tag_ids=self.tag_ids
        )
        self.update()

    async def change_tag_ids(self, new_tag_ids: list[int], database: Database):
        await database.modify_possession(
            possession_id=self.possession_id,
            new_possession_name=self.possession_name,
            new_group_id=self.group_id,
            new_tag_ids=new_tag_ids
        )
        tags = [await Tag.get_by_id(tag_id, database) for tag_id in new_tag_ids]
        self.subtitle = flet.Row(tags)
        self.subtitle.update()
        self.update()

    async def set_edit_button_callback(self, edit_button_callback: Callable):
        self._on_edit_click = edit_button_callback
        self.trailing.items[1].on_click = edit_button_callback  # noqa

    async def set_remove_button_callback(self, remove_button_callback: Callable):
        self._on_remove_click = remove_button_callback
        self.trailing.items[0].on_click = remove_button_callback  # noqa
