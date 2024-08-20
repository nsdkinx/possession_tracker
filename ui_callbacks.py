import flet
from ui_validation import must_be_non_empty_string

confirm_button = flet.Ref[flet.ElevatedButton]()


async def on_navigation_bar_change(event: flet.ControlEvent):
    page: flet.Page = event.page
    ctl: flet.NavigationBar = event.control

    HOME = '0'
    CATEGORIZATION = '1'
    SETTINGS = '2'

    if event.data == HOME:
        page.go('/')
    elif event.data == CATEGORIZATION:
        page.go('/categorization')
    elif event.data == SETTINGS:
        page.go('/settings')
    else:
        print(event.data)
        page.go('/')


async def _close_dialog(event: flet.ControlEvent):
    page: flet.Page = event.page
    await page.pubsub.unsubscribe_topic_async("dialog_confirm_button_action")
    print('unsubscribed from "dialog_confirm_button_action"')
    page.close(possession_add_dialog)


possession_add_dialog = flet.AlertDialog(
    modal=True,
    title=flet.Text("Добавление принадлежности"),

    content=flet.Column(
        tight=True,
        controls=[
            flet.TextField(label="Название", on_change=must_be_non_empty_string)
        ]
    ),

    actions=[
        flet.ElevatedButton("Отмена", icon=flet.icons.CANCEL, on_click=_close_dialog),
        flet.ElevatedButton("Добавить", icon=flet.icons.DONE, ref=confirm_button)
    ]
)


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

    page.open(possession_add_dialog)
