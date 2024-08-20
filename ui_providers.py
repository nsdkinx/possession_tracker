import flet

from ui_callbacks import (
    add_button_callback,
    on_navigation_bar_change
)


def get_appbar() -> flet.AppBar:
    return flet.AppBar(
        leading=flet.Image('in_app_icon.png', scale=0.8),
        title=flet.Text('Мои принадлежности')
    )


def get_floating_action_button() -> flet.FloatingActionButton:
    return flet.FloatingActionButton(
        icon=flet.icons.ADD,
        on_click=add_button_callback,
        enable_feedback=True
    )


navigation_bar = flet.NavigationBar(
    destinations=[
        flet.NavigationBarDestination(icon=flet.icons.HOME, label='Главная'),
        flet.NavigationBarDestination(icon=flet.icons.FOLDER, label='Категоризация'),
        flet.NavigationBarDestination(icon=flet.icons.SETTINGS, label='Настройки')
    ],
    on_change=on_navigation_bar_change
)
