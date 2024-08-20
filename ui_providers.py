import flet

from ui_callbacks import (
    on_navigation_bar_change
)


def get_appbar() -> flet.AppBar:
    return flet.AppBar(
        leading=flet.Image('in_app_icon.png', scale=0.8),
        title=flet.Text('Мои принадлежности')
    )


navigation_bar = flet.NavigationBar(
    destinations=[
        flet.NavigationBarDestination(icon=flet.icons.HOME, label='Главная'),
        flet.NavigationBarDestination(icon=flet.icons.FOLDER, label='Категоризация'),
        flet.NavigationBarDestination(icon=flet.icons.SETTINGS, label='Настройки')
    ],
    on_change=on_navigation_bar_change
)
