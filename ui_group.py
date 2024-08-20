from typing import Callable
import flet
from group import Group


def get_group_widget(group: Group, on_click: Callable | None = None) -> flet.Container:
    return flet.ListTile(
        leading=flet.Text(group.id, opacity=0.5, size=20),
        title=flet.Text(group.name, size=18),
        on_click=on_click
    )
