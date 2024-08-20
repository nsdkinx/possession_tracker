import flet

async def must_be_non_empty_string(event: flet.ControlEvent):
    text: str = event.control.value
    page: flet.Page = event.page

    if not text:
        event.control.error_text = "Поле не должно быть пустым!"
        event.control.update()
        await page.pubsub.send_all_on_topic_async(
            topic="dialog_confirm_button_action",
            message="disable_confirm_button"
        )
    else:
        event.control.error_text = None
        event.control.update()
        await page.pubsub.send_all_on_topic_async(
            topic="dialog_confirm_button_action",
            message="enable_confirm_button"
        )
