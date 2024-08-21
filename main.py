import logging

import asyncio
import flet

from group_manager import GroupManager
from possession_manager import PossessionManager
from tag_manager import TagManager

import managers

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


async def main(page: flet.Page):
    managers.possession_manager = PossessionManager(page.client_storage)
    managers.group_manager = GroupManager()
    managers.tag_manager = TagManager()
    
    await managers.possession_manager.prepare()

    page.title = 'Мои принадлежности'

    from view_root import root_view
    from view_categorization import categorization_view

    views: dict[str, flet.View] = {
        '/': root_view,
        '/categorization': categorization_view
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
    asyncio.run(flet.app_async(main, view=None, host='192.168.1.100', port='1234', assets_dir='assets/'))
