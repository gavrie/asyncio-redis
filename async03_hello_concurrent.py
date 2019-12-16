import asyncio


async def do_something(before, after):
    print(f'{before} ...')
    await asyncio.sleep(1)
    print(f'... {after}')


async def main():
    tasks = [
        asyncio.create_task(do_something("Hello", "World")),
        asyncio.create_task(do_something("Goodbye", "everyone")),
    ]

    for t in tasks:
        await t


asyncio.run(main())
