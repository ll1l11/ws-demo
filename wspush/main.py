from aiohttp import web

from .views import index


async def init_app():
    app = web.Application()
    app.add_routes([web.get('/', index)])
    return app


def main():
    app = init_app()
    web.run_app(app)
