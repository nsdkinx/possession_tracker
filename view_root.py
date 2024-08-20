import flet

from tag import Tag
from ui_providers import (
    get_appbar,
    navigation_bar
)

from managers import possession_manager, group_manager, tag_manager

from ui_possession import get_possession_widget

from ui_validation import must_be_non_empty_string

confirm_button = flet.Ref[flet.ElevatedButton]()

inner_possessions = flet.Container(
    alignment=flet.alignment.center,
    content=flet.Column(
        alignment=flet.MainAxisAlignment.CENTER,
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        controls=[
            flet.Icon(flet.icons.QUESTION_MARK, color=flet.colors.BLACK, opacity=0.5),
            flet.Text('У вас пока нет принадлежностей', opacity=0.5, weight=flet.FontWeight.W_500)
        ]
    )
)


def populate_inner_possessions():
    possessions = possession_manager.get_possessions()
    if not possessions:
        return inner_possessions  # TODO

    expansion_tiles: dict[str, flet.ExpansionTile] = {}

    for possession in possessions:
        if possession.group.name not in expansion_tiles:
            expansion_tiles[possession.group.name] = flet.ExpansionTile(
                initially_expanded=True,
                title=flet.Text(possession.group.name),
                subtitle=flet.Text('? принадлежностей'),
                controls=[get_possession_widget(possession)]
            )
        else:
            expansion_tiles[possession.group.name].controls.append(
                get_possession_widget(possession)
            )
    
    i = 1
    for expansion_tile in expansion_tiles.values():
        expansion_tile.subtitle.value = f'{len(expansion_tile.controls)} принадлежностей'
        for possession_ctl in expansion_tile.controls:
            possession_ctl.leading.value = i
            possession = possession_manager.get_possession_by_name(possession_ctl.title.value)
            possession.id = i
            i += 1

    expansion_tiles_column = flet.Column(
        tight=True,
        controls=list(expansion_tiles.values())
    )

    inner_possessions.content = expansion_tiles_column
    inner_possessions.update()


async def _close_dialog(event: flet.ControlEvent):
    page: flet.Page = event.page
    await page.pubsub.unsubscribe_topic_async("dialog_confirm_button_action")
    print('unsubscribed from "dialog_confirm_button_action"')
    page.close(possession_add_dialog.current)


name_field = flet.Ref[flet.TextField]()
group_dropdown = flet.Ref[flet.Dropdown]()
tag_popup = flet.Ref[flet.PopupMenuButton]()

async def _on_confirm_callback(event: flet.ControlEvent):
    page: flet.Page = event.page

    name = name_field.current.value
    group = group_manager.get_group_by_name(group_dropdown.current.value)

    selected_tags = [tag_manager.get_tag_by_name(item.content.value) for item in tag_popup.current.items if item.checked == True]

    possession_manager.add_possession(
        name=name, group=group, tags=selected_tags
    )

    page.open(flet.SnackBar(flet.Text('Принадлежность добавлена!')))
    page.close(possession_add_dialog.current)
    populate_inner_possessions()


possession_add_dialog = flet.Ref[flet.AlertDialog]()


async def _on_confirm_button_action_message(topic: str, message: str):
    print(f'[{topic}] {message}')
    if message == "disable_confirm_button":
        confirm_button.current.disabled = True
        confirm_button.current.update()
    elif message == "enable_confirm_button":
        confirm_button.current.disabled = False
        confirm_button.current.update()
    return

async def add_button_callback(event: flet.ControlEvent):
    page: flet.Page = event.page
    await page.pubsub.subscribe_topic_async(
        topic="dialog_confirm_button_action",
        handler=_on_confirm_button_action_message
    )
    print(f'subscribed to "dialog_confirm_button_action", handler: "_on_confirm_button_action_message"')

    async def _on_select_tag_callback(event: flet.ControlEvent):
        item: flet.PopupMenuItem = event.control
        tag = tag_manager.get_tag_by_name(item.content.value)

        if item.checked:
            item.checked = False
        else:
            item.checked = True

        tag_popup.current.update()

    page.open(
        flet.AlertDialog(
            ref=possession_add_dialog,
            modal=True,
            title=flet.Text("Добавление принадлежности"),

            content=flet.Column(
                tight=True,
                controls=[
                    flet.TextField(label="Название", on_change=must_be_non_empty_string, ref=name_field),
                    flet.Dropdown(
                        ref=group_dropdown,
                        label="Группа",
                        options=[
                            flet.dropdown.Option(text=group.name, key=group.name)
                            for group in group_manager.get_groups()
                        ]
                    ),
                    flet.PopupMenuButton(
                        ref=tag_popup,
                        content=flet.Text('Выбрать теги...'),
                        items=[
                            flet.PopupMenuItem(content=flet.Text(tag.label, color=tag.color), on_click=_on_select_tag_callback)
                            for tag in tag_manager.get_tags()
                        ]
                    )
                ]
            ),

            actions=[
                flet.ElevatedButton("Отмена", icon=flet.icons.CANCEL, on_click=_close_dialog),
                flet.ElevatedButton("Добавить", icon=flet.icons.DONE, ref=confirm_button, on_click=_on_confirm_callback)
            ]
        )
    )


root_view = flet.View(
    route='/',

    appbar=get_appbar(),
    floating_action_button=flet.FloatingActionButton(
        icon=flet.icons.ADD,
        on_click=add_button_callback,
        enable_feedback=True
    ),
    navigation_bar=navigation_bar,

    controls=[
        populate_inner_possessions()
    ]
)
