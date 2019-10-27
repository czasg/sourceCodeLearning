import threading
import asyncio
import socket
import selectors
import socketserver

# loop = asyncio.new_event_loop()


# loop = asyncio.get_event_loop()


async def test():
    await asyncio.sleep(2)
    print('hello')


async def main():
    try:
        await asyncio.wait_for(test(), 1)
    except asyncio.TimeoutError:
        print('TimeoutError')
    await asyncio.gather(*[
        # asyncio.create_task(test()),
        # asyncio.create_task(test()),
        # asyncio.create_task(test()),
        # asyncio.create_task(test()),
        test(),
        test(),
        test(),
    ])


if __name__ == '__main__':
    # loop.run_until_complete(test())
    # asyncio.run(test())
    asyncio.run(main())
