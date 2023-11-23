from asyncio import sleep

from aiohttp import web

async def retention(request):
    print(f"got message: {await request.text()}")
    await sleep(0.35)  # simulate response time
    return web.Response(text="{status: 200}")

if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.post("/retention", retention)])
    web.run_app(app)