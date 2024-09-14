import flet

from possession_tracker.database import Database
from possession_tracker.tag import Tag

class TagChooser(flet.PopupMenuButton):
    def __init__(self, database: Database, ref: flet.Ref):
        super().__init__(ref=ref)
        self._database = database
        self.content = flet.Text('Добавить теги...')

    async def _on_item_selection_callback(self, event: flet.ControlEvent):
        item: flet.PopupMenuItem = event.control
        # tag = Tag.get_by_name(item.content.value)  # noqa
        if item.checked:
            item.checked = False
        else:
            item.checked = True
        item.update()
        await self.update_content()

    async def populate_items(self):
        self.items = [
            flet.PopupMenuItem(
                content=flet.Text(tag.tag_label, color=tag.tag_color),
                on_click=self._on_item_selection_callback
            )
            for tag in await Tag.get_all(self._database)
        ]
        self.update()

    async def update_content(self):
        selected_tags = await self.get_selected_tags()
        if not selected_tags:
            self.content = flet.Text('Добавить теги...')
        else:
            self.content = flet.Row(selected_tags)
        # self.content.update()
        self.update()
        return

    async def get_selected_tags(self) -> list[Tag]:
        return [
            await Tag.get_by_label(item.content.value, self._database)  # noqa
            for item in self.items if item.checked == True
        ]
