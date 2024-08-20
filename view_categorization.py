import flet

from tag_color import TagColor
from ui_providers import (
    get_appbar,
    navigation_bar,
    get_floating_action_button
)

from ui_tag import get_tag_widget
from ui_group import get_group_widget
from ui_validation import must_be_non_empty_string

from managers import tag_manager, group_manager

confirm_button = flet.Ref[flet.ElevatedButton]()

inner_tags = flet.Container(
    alignment=flet.alignment.center,
    content=flet.Column(
        alignment=flet.MainAxisAlignment.CENTER,
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        controls=[
            flet.Icon(flet.icons.QUESTION_MARK, color=flet.colors.BLACK, opacity=0.5),
            flet.Text('У вас пока нет тегов', opacity=0.5, weight=flet.FontWeight.W_500)
        ]
    )
)

inner_groups = flet.Container(
    alignment=flet.alignment.center,
    content=flet.Column(
        alignment=flet.MainAxisAlignment.CENTER,
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        controls=[
            flet.Icon(flet.icons.QUESTION_MARK, color=flet.colors.BLACK, opacity=0.5),
            flet.Text('У вас пока нет групп', opacity=0.5, weight=flet.FontWeight.W_500)
        ]
    )
)


async def _on_tag_click_callback(event: flet.ControlEvent):
    page: flet.Page = event.page
    tag_control: flet.Container = event.control.content

    async def _remove_tag_callback(event: flet.ControlEvent):
        async def _on_cancel_button_callback(event: flet.ControlEvent):
            page.close(remove_tag_dialog)

        async def _confirm_button_callback(event: flet.ControlEvent):
            tag = tag_manager.get_tag_by_name(tag_control.content.value)
            tag_manager.remove_tag(tag)

            page.open(flet.SnackBar(flet.Text('Тег удалён!')))
            page.close(remove_tag_dialog)

            populate_inner_tags()

        remove_tag_dialog = flet.AlertDialog(
            title=flet.Text('Удаление тега'),
            content=flet.Text(
                f'Вы точно хотите удалить тег {tag_control.content.value}? Будут удалены все принадлежности с этим тегом!'
            ),
            actions=[
                flet.ElevatedButton('Отмена', icon=flet.icons.CANCEL, on_click=_on_cancel_button_callback),
                flet.ElevatedButton('Удалить', icon=flet.icons.DELETE, color=flet.colors.RED, on_click=_confirm_button_callback)
            ]
        )

        page.open(remove_tag_dialog)

    async def _on_cancel_button_callback(event: flet.ControlEvent):
        await page.pubsub.unsubscribe_topic_async('dialog_confirm_button_action')
        print('unsubscribed from "dialog_confirm_button_action"')
        page.close(dialog)

    async def _on_confirm_button_action_message(topic: str, message: str):
        print(f'[{topic}] {message}')
        if message == "disable_confirm_button":
            confirm_button.current.disabled = True
            confirm_button.current.update()
        elif message == "enable_confirm_button":
            confirm_button.current.disabled = False
            confirm_button.current.update()
        return

    async def _on_confirm_callback(event: flet.ControlEvent):
        name = new_name_field.value
        color = new_color_dropdown.value

        tag_manager.edit_tag(
            tag=tag_manager.get_tag_by_name(tag_control.content.value),
            name=name,
            color=color
        )

        page.open(flet.SnackBar(flet.Text('Тег изменён!')))
        page.close(dialog)
        populate_inner_tags()

    await page.pubsub.subscribe_topic_async(
        topic='dialog_confirm_button_action',
        handler=_on_confirm_button_action_message
    )

    new_name_field = flet.TextField(
        label='Название',
        value=tag_control.content.value,
        on_change=must_be_non_empty_string
    )
    new_color_dropdown = flet.Dropdown(
        label='Цвет',
        options=[
            flet.dropdown.Option(
                key=color_,
                content=flet.Text(f'{color_.name}', color=color_.value)
            )
            for color_ in TagColor
        ],
        value=tag_control.bgcolor
    )
    delete_button = flet.ElevatedButton('Удалить тег', icon=flet.icons.DELETE, color=flet.colors.RED, on_click=_remove_tag_callback)

    dialog = flet.AlertDialog(
        title=flet.Text(tag_control.content.value),

        content=flet.Column(
            tight=True,
            controls=[
                new_name_field,
                new_color_dropdown,
                delete_button
            ]
        ),

        actions=[
            flet.ElevatedButton('Отмена', icon=flet.icons.CANCEL, on_click=_on_cancel_button_callback),
            flet.ElevatedButton('Применить', icon=flet.icons.DONE, ref=confirm_button, on_click=_on_confirm_callback)
        ]
    )

    page.open(dialog)


async def _on_group_click_callback(event: flet.ControlEvent):
    page: flet.Page = event.page
    group_control: flet.Container = event.control

    async def _remove_group_callback(event: flet.ControlEvent):
        async def _on_cancel_button_callback(event: flet.ControlEvent):
            page.close(remove_group_dialog)

        async def _confirm_button_callback(event: flet.ControlEvent):
            group = group_manager.get_group_by_name(group_control.title.value)
            group_manager.remove_group(group)

            page.open(flet.SnackBar(flet.Text('Группа удалена!')))
            page.close(remove_group_dialog)

            populate_inner_groups()

        remove_group_dialog = flet.AlertDialog(
            title=flet.Text('Удаление группы'),
            content=flet.Text(
                f'Вы точно хотите удалить группу {group_control.title.value}? Будут удалены все принадлежности в этой группе!'
            ),
            actions=[
                flet.ElevatedButton('Отмена', icon=flet.icons.CANCEL, on_click=_on_cancel_button_callback),
                flet.ElevatedButton('Удалить', icon=flet.icons.DELETE, color=flet.colors.RED, on_click=_confirm_button_callback)
            ]
        )

        page.open(remove_group_dialog)

    async def _on_cancel_button_callback(event: flet.ControlEvent):
        await page.pubsub.unsubscribe_topic_async('dialog_confirm_button_action')
        print('unsubscribed from "dialog_confirm_button_action"')
        page.close(dialog)

    async def _on_confirm_button_action_message(topic: str, message: str):
        print(f'[{topic}] {message}')
        if message == "disable_confirm_button":
            confirm_button.current.disabled = True
            confirm_button.current.update()
        elif message == "enable_confirm_button":
            confirm_button.current.disabled = False
            confirm_button.current.update()
        return

    async def _on_confirm_callback(event: flet.ControlEvent):
        name = new_name_field.value

        group_manager.edit_group(
            group=group_manager.get_group_by_name(group_control.title.value),
            name=name
        )

        page.open(flet.SnackBar(flet.Text('Группа изменена!')))
        page.close(dialog)
        populate_inner_groups()

    await page.pubsub.subscribe_topic_async(
        topic='dialog_confirm_button_action',
        handler=_on_confirm_button_action_message
    )

    new_name_field = flet.TextField(
        label='Название',
        value=group_control.title.value,
        on_change=must_be_non_empty_string
    )
    delete_button = flet.ElevatedButton('Удалить группу', icon=flet.icons.DELETE, color=flet.colors.RED, on_click=_remove_group_callback)

    dialog = flet.AlertDialog(
        title=flet.Text(group_control.title.value),

        content=flet.Column(
            tight=True,
            controls=[
                new_name_field,
                delete_button
            ]
        ),

        actions=[
            flet.ElevatedButton('Отмена', icon=flet.icons.CANCEL, on_click=_on_cancel_button_callback),
            flet.ElevatedButton('Применить', icon=flet.icons.DONE, ref=confirm_button, on_click=_on_confirm_callback)
        ]
    )

    page.open(dialog)


def populate_inner_tags():
    global inner_tags

    tags = tag_manager.get_tags()
    if not tags and inner_tags.alignment == flet.alignment.top_left:
        inner_tags.alignment = flet.alignment.center
        inner_tags.content = flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Icon(flet.icons.QUESTION_MARK, color=flet.colors.BLACK, opacity=0.5),
                flet.Text('У вас пока нет тегов', opacity=0.5, weight=flet.FontWeight.W_500)
            ]
        )
        inner_tags.update()
        return inner_tags

    elif not tags and inner_tags.alignment == flet.alignment.center:
        return inner_tags

    else:
        inner_tags.alignment = flet.alignment.top_left
        inner_tags.content = flet.Row(
            wrap=True,
            controls=[
                flet.Container(
                    content=get_tag_widget(tag, enlarged=True),
                    on_click=_on_tag_click_callback
                )
                for tag in tags
            ]
        )
        inner_tags.update()
        return inner_tags


def populate_inner_groups():
    global inner_groups

    groups = group_manager.get_groups()
    if not groups and inner_groups.alignment == flet.alignment.top_left:
        inner_groups.alignment = flet.alignment.center
        inner_groups.content = flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Icon(flet.icons.QUESTION_MARK, color=flet.colors.BLACK, opacity=0.5),
                flet.Text('У вас пока нет групп', opacity=0.5, weight=flet.FontWeight.W_500)
            ]
        )
        inner_groups.update()
        return inner_groups

    elif not groups and inner_groups.alignment == flet.alignment.center:
        return inner_groups

    else:
        inner_groups.alignment = flet.alignment.top_left
        inner_groups.content = flet.Row(
            wrap=True,
            controls=[
                get_group_widget(group, on_click=_on_group_click_callback)
                for group in groups
            ]
        )
        inner_groups.update()
        return inner_groups


async def add_tag_button_callback(event: flet.ControlEvent):
    page: flet.Page = event.page

    async def _on_cancel_button_callback(event: flet.ControlEvent):
        await page.pubsub.unsubscribe_topic_async('dialog_confirm_button_action')
        print('unsubscribed from "dialog_confirm_button_action"')
        page.close(dialog)

    async def _on_confirm_button_action_message(topic: str, message: str):
        print(f'[{topic}] {message}')
        if message == "disable_confirm_button":
            confirm_button.current.disabled = True
            confirm_button.current.update()
        elif message == "enable_confirm_button":
            confirm_button.current.disabled = False
            confirm_button.current.update()
        return

    await page.pubsub.subscribe_topic_async(
        topic='dialog_confirm_button_action',
        handler=_on_confirm_button_action_message
    )

    name_field = flet.TextField(label='Название', on_change=must_be_non_empty_string)
    color_dropdown = flet.Dropdown(
        label='Цвет',
        options=[
            flet.dropdown.Option(
                key=color_,
                content=flet.Text(f'{color_.name}', color=color_.value)
            )
            for color_ in TagColor
        ]
    )

    async def _on_confirm_callback(event: flet.ControlEvent):
        name = name_field.value
        color = color_dropdown.value

        tag = tag_manager.add_tag(label=name, color=color)

        page.open(flet.SnackBar(flet.Text('Тег добавлен!')))
        page.close(dialog)
        populate_inner_tags()


    dialog = flet.AlertDialog(
        title=flet.Text('Добавление тега'),

        content=flet.Column(
            tight=True,
            controls=[
                name_field,
                color_dropdown
            ]
        ),

        actions=[
            flet.ElevatedButton('Отмена', icon=flet.icons.CANCEL, on_click=_on_cancel_button_callback),
            flet.ElevatedButton('Добавить', icon=flet.icons.DONE, ref=confirm_button, on_click=_on_confirm_callback)
        ]
    )

    page.open(dialog)


async def add_group_button_callback(event: flet.ControlEvent):
    page: flet.Page = event.page

    async def _on_cancel_button_callback(event: flet.ControlEvent):
        await page.pubsub.unsubscribe_topic_async('dialog_confirm_button_action')
        print('unsubscribed from "dialog_confirm_button_action"')
        page.close(dialog)

    async def _on_confirm_button_action_message(topic: str, message: str):
        print(f'[{topic}] {message}')
        if message == "disable_confirm_button":
            confirm_button.current.disabled = True
            confirm_button.current.update()
        elif message == "enable_confirm_button":
            confirm_button.current.disabled = False
            confirm_button.current.update()
        return

    await page.pubsub.subscribe_topic_async(
        topic='dialog_confirm_button_action',
        handler=_on_confirm_button_action_message
    )

    async def _on_confirm_callback(event: flet.ControlEvent):
        name = name_field.value

        group = group_manager.add_group(name)

        page.open(flet.SnackBar(flet.Text('Группа добавлена!')))
        page.close(dialog)
        populate_inner_groups()

    name_field = flet.TextField(label='Название', on_change=must_be_non_empty_string)

    dialog = flet.AlertDialog(
        title=flet.Text('Добавление группы'),

        content=flet.Column(
            tight=True,
            controls=[
                name_field
            ]
        ),

        actions=[
            flet.ElevatedButton('Отмена', icon=flet.icons.CANCEL, on_click=_on_cancel_button_callback),
            flet.ElevatedButton('Добавить', icon=flet.icons.DONE, ref=confirm_button, on_click=_on_confirm_callback)
        ]
    )

    page.open(dialog)


categorization_view = flet.View(
    route='/categorization',

    appbar=get_appbar(),
    floating_action_button=get_floating_action_button(),
    navigation_bar=navigation_bar,
    scroll=flet.ScrollMode.ALWAYS,

    controls=[
        flet.Column(
            scroll=flet.ScrollMode.ALWAYS,
            tight=True,
            controls=[
                flet.Card(
                    content=flet.Container(
                        padding=10,
                        content=flet.Column(
                            controls=[
                                flet.Row([
                                    flet.Text('Теги', expand=True, size=24),
                                    flet.IconButton(icon=flet.icons.ADD, on_click=add_tag_button_callback)
                                ]),
                                populate_inner_tags()
                            ]
                        )
                    )
                ),

                flet.Card(
                    content=flet.Container(
                        padding=10,
                        content=flet.Column(
                            controls=[
                                flet.Row([
                                    flet.Text('Группы', expand=True, size=24),
                                    flet.IconButton(icon=flet.icons.ADD, on_click=add_group_button_callback)
                                ]),
                                populate_inner_groups()
                            ]
                        )
                    )
                )
            ]
        )
    ]
)
