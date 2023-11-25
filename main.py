import asyncio
import csv
from datetime import datetime
from random import randint
from time import perf_counter

import aiofiles
from aiohttp import ClientSession, ClientTimeout


API_URL = "http://localhost:8080/retention"   # test_server.py path: http://localhost:8080/retention
HEADERS = {"Authorization": "bearer 123456", "Content-Type": "plain/text", "Accept": "*/*"}
RETENTION_PATH = "./retentions.csv"
DELIMITER = ","


async def send_request(session, payload, limiter, logger, log_lock):
    async with limiter:
        try:
            async with session.post(API_URL, data=payload) as res:
                content = await res.text();

                await log(logger, f"{'[ERROR]' if res.status // 100 != 2 else ''} REQUEST={payload} RESPONSE=[{res.status}] {content.strip(' ')}", log_lock)
                
                return content

        except Exception as e:
            await log(logger, f"[ERROR] REQUEST={payload} ERROR={repr(e)}: {e}", log_lock)


async def log(logger, message, lock):
    async with lock:
        await logger.write(f"[{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")


async def main():
    # generate_test_retentions(100_000)  # uncomment this to generate test file

    limiter = asyncio.Semaphore(100)  # throttle concurrent requests to 100
    log_lock = asyncio.Lock()  # prevent multiple concurrent writes to the log file
    timeout = ClientTimeout(total=5)  # 5 second timeout

    start = perf_counter()

    async with aiofiles.open("responses.log", mode="a") as logger:
        async with ClientSession(headers=HEADERS, timeout=timeout) as session:
            tasks = []

            with open(RETENTION_PATH, "r") as f:
                reader = csv.reader(f, delimiter=DELIMITER)

                for r in reader:
                    dir = r[0]
                    offset = int(r[1]) if r[1] != "" else 0;

                    payload = f"directory: {dir} offset: {offset}"  # this may need to be adjusted

                    tasks.append(asyncio.ensure_future(send_request(session, payload, limiter, logger, log_lock)))

            await asyncio.gather(*tasks)

    end = perf_counter()
    print(f"FINISHED in {end-start} seconds")


def generate_test_retentions(rows):
    with open("retentions.csv", "w") as f:
        for i in range(rows):
            f.write(f"\"C:\\Use,rs\\TE..ST\\Des,,,ktop\\test\",{randint(-3650, 3650)}\n")


if __name__ == "__main__":  # only run if not imported
    asyncio.run(main())
