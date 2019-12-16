import asyncio
import logging
import time

import asyncredis


logger = logging.getLogger(__name__)


async def blpop(key, timeout):
    command = f"BLPOP {key} {timeout}"
    return await asyncredis.client(command)


async def lpush(key, element):
    command = f"LPUSH {key} {element}"
    return await asyncredis.client(command)


async def main():
    logger.info("Starting...")
    start = time.time()

    coros = [
        blpop("foo", 2),
        blpop("foo", 1),
        blpop("foo", 3),
    ]

    tasks = [asyncio.create_task(c) for c in coros]

    for t in tasks:
        result = await t
        logger.info("Result: %r", result)

    logger.info("Done; elapsed: %.2f", time.time() - start)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    asyncio.run(main())
