import asyncio
import csv
from datetime import datetime
import json
from random import randint
from time import perf_counter

import aiofiles
from aiohttp import ClientSession


API_URL = "http://localhost:8080/retention"   # test_server.py path: http://localhost:8080/retention
HEADERS = {"Authorization": "bearer 123456", "content-type": "application/json", "accept": "application/json"}
RETENTION_PATH = "./retentions.csv"
DELIMITER = ","


async def send_request(sem, payload, session, logger, log_lock):
    async with sem:
        async with session.post(API_URL, data=payload) as res:
            content = await res.text();

            async with log_lock:
                await logger.write(f"[{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] REQUEST={json.dumps(payload)} RESPONSE={json.dumps(content)}\n")

            return content


async def main():
    # generate_test_retentions(100_000)  # uncomment this to generate test file

    sem = asyncio.Semaphore(100)  # throttle concurrent requests to 100
    logger_lock = asyncio.Lock()  # prevent multiple concurrent writes to the log file

    start = perf_counter()

    async with aiofiles.open("responses.log", mode="a") as logger:
        async with ClientSession(headers=HEADERS) as session:
            tasks = []

            with open(RETENTION_PATH, "r") as f:
                reader = csv.reader(f, delimiter=DELIMITER)

                for r in reader:
                    payload = { "directory": r[0], "offset": int(r[1]) if r[1] != "" else 0 }  # this may need to be adjusted

                    tasks.append(asyncio.ensure_future(send_request(sem, payload, session, logger, logger_lock)))

            await asyncio.gather(*tasks) 

    end = perf_counter()
    print(f"FINISHED in {end-start} seconds")


def generate_test_retentions(rows):
    with open("retentions.csv", "w") as f:
        for i in range(rows):
            f.write(f"C:\\Users\\TEST\\Desktop\\test,{randint(-3650, 3650)}\n")


if __name__ == "__main__":  # only run if not imported
    asyncio.run(main())
