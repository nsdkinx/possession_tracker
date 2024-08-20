import flet

from ui_providers import (
    get_appbar,
    navigation_bar,
    get_floating_action_button
)

root_view = flet.View(
    route='/',

    appbar=get_appbar(),
    floating_action_button=get_floating_action_button(),
    navigation_bar=navigation_bar,

    controls=[
        flet.ExpansionTile(title=flet.Text('amogus'))
    ]
)
