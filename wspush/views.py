import aiohttp
from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)
    async for msg in ws:
        print('this is msg.type', msg.type)
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')
    request.app['websockets'].discard(ws)
    return ws
