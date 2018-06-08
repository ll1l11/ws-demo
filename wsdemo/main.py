import asyncio
import random

from aiohttp import web

from .views import hello, websocket_handler


async def send_data(app):
    try:
        while True:
            data = [round(random.random(), 2) for _ in range(6)]
            for ws in app['websockets']:
                await ws.send_json(data)
            await asyncio.sleep(random.random() * 10)
    except asyncio.CancelledError:
        pass


async def start_background_tasks(app):
    app['ws_listener'] = app.loop.create_task(send_data(app))


async def cleanup_background_tasks(app):
    app['ws_listener'].cancel()
    await app['ws_listener']


async def init_app():
    app = web.Application()

    app['websockets'] = set()

    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    app.on_shutdown.append(shutdown)

    app.add_routes([
        web.get('/', websocket_handler),
        web.get('/hello', hello),
    ])

    return app


async def shutdown(app):
    while True:
        try:
            ws = app['websockets'].pop()
            await ws.close()
        except KeyError:
            break

    print(len(app['websockets']))


def main():
    app = init_app()
    web.run_app(app, port=5441)
