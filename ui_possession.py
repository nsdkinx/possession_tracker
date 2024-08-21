from typing import Callable
import flet
from possession import Possession
from ui_tag import get_tag_widget


def get_possession_widget(
        possession: Possession,
        on_edit_click: Callable | None = None,
        on_remove_click: Callable | None = None
    ) -> flet.ListTile:
    tag_controls = [get_tag_widget(tag) for tag in possession.tags]

    return flet.ListTile(
        leading=flet.Text(possession.id, size=30, opacity=0.3),
        title=flet.Text(possession.name, size=18),
        subtitle=flet.Row(
            wrap=True,
            controls=tag_controls
        ) if tag_controls else None,
        trailing=flet.PopupMenuButton(
            items=[
                flet.PopupMenuItem(icon=flet.icons.DELETE, text='Избавиться', on_click=on_remove_click),
                flet.PopupMenuItem(icon=flet.icons.EDIT, text='Редактировать', on_click=on_edit_click)
            ]
        )
    )
