from asyncio import sleep
from random import randint

from aiohttp import web


async def retention(request):
    print(f"got message: {await request.text()}")
    await sleep(15 if randint(0, 15) == 1 else 0.35)  # simulate response time, timeout 1 in 15 times
    return web.Response(text="{status: 200}")


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.post("/retention", retention)])
    web.run_app(app)