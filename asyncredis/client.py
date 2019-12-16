import asyncio
import logging

from asyncredis import resp


logger = logging.getLogger(__name__)


async def client(command: str) -> resp.RedisValue:
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 6379)
    logger.info("Connection opened")

    logger.info(">>> %r", command)

    encoded_command = f"{command}\r\n".encode()
    writer.write(encoded_command)
    await writer.drain()

    data = await reader.read(1024)
    result = resp.parse(data)
    logger.info("<<< %r", result)

    logger.info("Closing the connection")
    writer.close()
    await writer.wait_closed()

    logger.info("[DONE] >>> %r", command)
    return result
