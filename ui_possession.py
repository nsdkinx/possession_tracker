import flet
from possession import Possession
from ui_tag import get_tag_widget

def get_possession_widget(possession: Possession) -> flet.ListTile:
    return flet.ListTile(
        leading=flet.Text(possession.id, size=30, opacity=0.3),
        title=flet.Text(possession.name, size=18),
        subtitle=flet.Row(
            wrap=True,
            controls=[get_tag_widget(tag) for tag in possession.tags]
        ),
        trailing=flet.PopupMenuButton()  # TODO
    )
