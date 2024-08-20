import flet

from tag_color import TagColor
from ui_providers import (
    get_appbar,
    navigation_bar,
    get_floating_action_button
)

from ui_tag import get_tag_widget
from ui_validation import must_be_non_empty_string

from managers import tag_manager

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


categorization_view = flet.View(
    route='/categorization',

    appbar=get_appbar(),
    floating_action_button=get_floating_action_button(),
    navigation_bar=navigation_bar,

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
        )
    ]
)
