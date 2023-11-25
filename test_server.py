from asyncio import sleep
from random import randint

from aiohttp import web


async def retention(request):
    print(f"got message: {await request.text()}")
    await sleep(15 if randint(0, 15) == 1 else 0.35)  # simulate response time, timeout 1 in 15 times

    status = 400 if randint(0, 50) == 1 else 200  # simulate rejected requests
    body = f"status: {status}"

    return web.Response(text=body, status=status)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.post("/retention", retention)])
    web.run_app(app)