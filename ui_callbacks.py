import flet


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
