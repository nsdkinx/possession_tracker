from __future__ import annotations

import flet
from possession_tracker.database import Database
from possession_tracker.ui.tag_color import TagColor


class Tag(flet.Container):
    def __init__(
            self,
            tag_id: int,
            tag_label: str,
            tag_color: TagColor,
            enlarged: bool = False
    ) -> None:
        super().__init__()
        self.tag_id = tag_id
        self.tag_label = tag_label
        self.tag_color = tag_color

        if tag_color in [TagColor.YELLOW]:
            text_color = flet.colors.BLACK
        else:
            text_color = flet.colors.WHITE

        text_size = 16 if enlarged else 12

        self.padding = flet.padding.symmetric(horizontal=5, vertical=2.5)
        self.content = flet.Text(tag_label, size=text_size, color=text_color)
        self.bgcolor = tag_color
        self.border_radius = flet.border_radius.all(5)

    @classmethod
    async def create_new_tag(
            cls,
            tag_label: str,
            tag_color: TagColor,
            database: Database
    ) -> Tag:
        tag_dict_object = await database.create_tag(tag_label, tag_color)
        return cls(
            tag_id=tag_dict_object['tag_id'],
            tag_label=tag_dict_object['tag_label'],
            tag_color=tag_dict_object['tag_color']
        )

    @classmethod
    async def get_all(cls, database: Database) -> list[Tag]:
        all_tags_dict = await database.get_all_tags()
        return [
            cls(tag_id, tag_object['tag_label'], tag_object['tag_color'])  # noqa
            for tag_id, tag_object in all_tags_dict.items()
        ]

    @classmethod
    async def get_by_id(cls, tag_id: int, database: Database) -> Tag:
        all_tags_dict = await database.get_all_tags()
        tag_object = all_tags_dict[tag_id]
        return cls(
            tag_id=tag_id,
            tag_label=tag_object['tag_label'],
            tag_color=tag_object['tag_color']  # noqa
        )

    @classmethod
    async def get_by_label(cls, tag_label: str, database: Database) -> Tag | None:
        all_tags_dict = await database.get_all_tags()
        for tag_id, tag_object in all_tags_dict.items():
            if tag_object['tag_label'] == tag_label:
                return cls(
                    tag_id=tag_id,
                    **tag_object
                )
        return None

    async def delete(self, database: Database) -> None:
        return await database.delete_tag(self.tag_id)

    async def change_label(self, new_label: str, database: Database):
        await database.modify_tag(
            tag_id=self.tag_id,
            new_tag_label=new_label,
            new_tag_color=self.tag_color
        )
        self.content.value = new_label
        self.content.update()
        self.update()

    async def change_color(self, new_color: TagColor, database: Database):
        await database.modify_tag(
            tag_id=self.tag_id,
            new_tag_label=self.tag_label,
            new_tag_color=new_color
        )
        self.content.bgcolor = new_color
        self.content.update()
        self.update()
