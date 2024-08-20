import asyncio
import flet

from view_root import root_view
from view_categorization import categorization_view


async def main(page: flet.Page):
    page.title = 'PossessionTracker'

    views: dict[str, flet.View] = {
        '/': root_view,
        '/categorization': categorization_view
    }

    async def _on_route_change(event: flet.RouteChangeEvent):
        page.views.clear()
        page.views.append(root_view)
        page.views.append(views[event.route])
        page.update()
    
    async def _on_view_pop(_: flet.View):
        page.views.pop()
        page.go(page.views[-1].route)

    page.on_route_change = _on_route_change
    page.on_view_pop = _on_view_pop

    page.go('/')


if __name__ == "__main__":
    asyncio.run(flet.app_async(main, assets_dir='assets/'))
