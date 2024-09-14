import logging

import asyncio
import flet

from possession_tracker.database import Database

from possession_tracker.views.root import create_root_view

# logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


async def main(page: flet.Page):
    page.title = 'Мои принадлежности'

    database = Database(page.client_storage)

    if await database.is_first_run():
        await database.reset_or_create_database()

    root_view = await create_root_view(database, page)

    views: dict[str, flet.View] = {
        '/': root_view,
        # '/categorization': categorization_view
    }

    async def _on_route_change(event: flet.RouteChangeEvent):
        logger.info(f'Route changed to {event.route}')
        page.views.clear()
        page.views.append(root_view)
        page.views.append(views[event.route])
        page.update()
    
    async def _on_view_pop(_: flet.View):
        logger.info(f'View pop requested')
        page.views.pop()
        page.go(page.views[-1].route)

    page.on_route_change = _on_route_change
    page.on_view_pop = _on_view_pop

    logger.info('App prepared, going to root view')
    page.go('/')


if __name__ == "__main__":
    asyncio.run(flet.app_async(main, assets_dir='assets/'))
