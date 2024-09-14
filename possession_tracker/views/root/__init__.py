import flet

from possession_tracker.controls.group import Group
from possession_tracker.database import Database
from possession_tracker.ui.providers import get_appbar, navigation_bar
from possession_tracker.controls.possession import Possession

from possession_tracker.views.root.remove_possession import on_remove_possession_callback


async def build_root_view_ui(database: Database, page: flet.Page):
    possessions = await Possession.get_all(database)

    expansion_tiles: dict[str, flet.ExpansionTile] = {}

    for possession in possessions:
        await possession.set_remove_button_callback(on_remove_possession_callback)
        await possession.set_edit_button_callback(on_remove_possession_callback)

        possession_group_name = (
            await Group.get_by_id(group_id=possession.group_id, database=database)
        ).group_name

        if possession_group_name not in expansion_tiles:
            expansion_tiles[possession_group_name] = flet.ExpansionTile(
                initially_expanded=True,
                title=flet.Text(possession_group_name),
                controls=[possession]
            )
        else:
            expansion_tiles[possession_group_name].controls.append(possession)

    for expansion_tile in expansion_tiles.values():
        expansion_tile.subtitle = flet.Text(f'{len(expansion_tile.controls)} принадлежностей')

    return flet.Column(
        tight=True,
        controls=list(expansion_tiles.values())
    )

async def create_root_view(database: Database, page: flet.Page):
    return flet.View(
        route='/',

        appbar=get_appbar(),
        floating_action_button=flet.FloatingActionButton(
            icon=flet.icons.ADD,
            # on_click=add_button_callback,
            enable_feedback=True
        ),
        navigation_bar=navigation_bar,

        controls=[await build_root_view_ui(database, page)]
    )
