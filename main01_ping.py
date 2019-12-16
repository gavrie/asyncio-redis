import asyncio
import logging

import asyncredis


logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting...")
    result = await asyncredis.client("PING")
    logger.info("Result: %r", result)
    logger.info("Done.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    asyncio.run(main())
