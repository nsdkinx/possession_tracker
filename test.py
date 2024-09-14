import asyncio
import flet
from flet_core import ElevatedButton

from possession_tracker.group import Group
from possession_tracker.possession import Possession
from possession_tracker.tag import Tag, TagColor
from possession_tracker.database import Database
from possession_tracker.tag_chooser import TagChooser


async def main(page: flet.Page):
    page.title = 'demo'

    database = Database(client_storage=page.client_storage)

    if await database.is_first_run():
        await database.reset_or_create_database()

    tag_label_textfield_ref = flet.Ref[flet.TextField]()
    tag_color_dropdown_ref = flet.Ref[flet.Dropdown]()
    tag_container_ref = flet.Ref[flet.Container]()

    group_name_textfield_ref = flet.Ref[flet.TextField]()
    group_container_ref = flet.Ref[flet.Container]()

    possession_name_textfield_ref = flet.Ref[flet.TextField]()
    possession_group_dropdown_ref = flet.Ref[flet.Dropdown]()
    possession_tag_container_ref = flet.Ref[flet.Container]()
    possession_container_ref = flet.Ref[flet.Container]()

    async def refresh_tag_container():
        tags = await Tag.get_all(database)
        tag_container_ref.current.content.controls.clear()
        for tag in tags:
            tag_container_ref.current.content.controls.append(tag)
        tag_container_ref.current.content.update()

    async def refresh_group_container():
        groups = await Group.get_all(database)
        group_container_ref.current.content.controls.clear()
        for group in groups:
            group_container_ref.current.content.controls.append(group)
        group_container_ref.current.content.update()

    async def refresh_possession_container():
        possessions = await Possession.get_all(database)
        possession_container_ref.current.content.controls.clear()
        for possession in possessions:
            possession_container_ref.current.content.controls.append(possession)
        possession_container_ref.current.content.update()
        for possession in possessions:
            await possession.populate_subtitle_with_tags(database)
        possession_container_ref.current.content.update()

    async def on_create_tag_button_callback(event: flet.ControlEvent):
        tag_label = tag_label_textfield_ref.current.value
        tag_color = tag_color_dropdown_ref.current.value

        new_tag = await Tag.create_new_tag(tag_label, tag_color, database)

        await refresh_tag_container()

    async def on_create_group_button_callback(event: flet.ControlEvent):
        group_name = group_name_textfield_ref.current.value

        new_group = await Group.create_new_group(group_name, database)

        await refresh_group_container()

    async def on_create_possession_button_callback(event: flet.ControlEvent):
        possession_name = possession_name_textfield_ref.current.value
        possession_group_id = possession_group_dropdown_ref.current.value
        possession_tag_ids = [tag.tag_id for tag in await possession_tag_container_ref.current.get_selected_tags()]
        print(possession_group_id)
        print(possession_name)
        print(possession_tag_ids)

        await database.create_possession(
            possession_name, possession_group_id, possession_tag_ids
        )

        await refresh_possession_container()

    all_groups = await database.get_all_groups()
    page.add(
        flet.Row(
            controls=[
                flet.TextField(hint_text='tag_label', ref=tag_label_textfield_ref),
                flet.Dropdown(
                    ref=tag_color_dropdown_ref,
                    label='tag_color',
                    options=[
                        flet.dropdown.Option(
                            key=color_.name,
                            content=flet.Text(f'{color_.name}', color=color_.value)
                        )
                        for color_ in TagColor
                    ]
                ),
                ElevatedButton('create_tag', on_click=on_create_tag_button_callback)
            ]
        ),

        flet.Row(
            controls=[
                flet.TextField(hint_text='group_name', ref=group_name_textfield_ref),
                ElevatedButton('create_group', on_click=on_create_group_button_callback)
            ]
        ),

        flet.Row(
            controls=[
                flet.TextField(hint_text='possession_name', ref=possession_name_textfield_ref),
                flet.Dropdown(
                    ref=possession_group_dropdown_ref,
                    hint_text='possession_group_id',
                    options=[
                        flet.dropdown.Option(
                            key=group_id,
                            content=flet.Text(group_object['group_name'])
                        )
                        for group_id, group_object in all_groups.items()
                    ]
                ),
                TagChooser(database, ref=possession_tag_container_ref),
                ElevatedButton('create_possession', on_click=on_create_possession_button_callback)
            ]
        ),

        flet.Container(
            ref=tag_container_ref,
            content=flet.Column(controls=[])
        ),

        flet.Container(
            ref=group_container_ref,
            content=flet.Column(controls=[])
        ),

        flet.Container(
            ref=possession_container_ref,
            content=flet.Column(controls=[])
        )
    )

    await possession_tag_container_ref.current.populate_items()
    await refresh_tag_container()
    await refresh_group_container()
    await refresh_possession_container()


if __name__ == "__main__":
    asyncio.run(flet.app_async(main))
