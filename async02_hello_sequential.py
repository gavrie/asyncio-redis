import asyncio


async def do_something(before, after):
    print(f'{before} ...')
    await asyncio.sleep(1)
    print(f'... {after}')


async def main():
    await do_something("Hello", "World")
    await do_something("Goodbye", "everyone")


asyncio.run(main())
