# -*- coding: utf-8 -*-
import asyncio
import contextvars

# 申明Context变量
request_id = contextvars.ContextVar('Id of request')


async def get():
    # Get Value
    print(f'Request ID (Inner): {request_id.get()}')


async def new_coro(req_id):
    # Set Value
    request_id.set(req_id)
    await get()
    print(f'Request ID (Outer): {request_id.get()}')


async def main():
    tasks = []
    for req_id in range(0, 5):
        tasks.append(asyncio.create_task(new_coro(req_id)))

    await asyncio.gather(*tasks)


asyncio.run(main())


# import asyncio
#
# loop = asyncio.get_event_loop()
#
# async def test():
#     print('test')
#
# async def main():
#     await asyncio.gather(
#         test(),
#         test(),
#     )
#
# if __name__ == '__main__':
#     loop.run_until_complete(main())



# import socket
# import selectors
# selector = selectors.DefaultSelector()
# _ssock, _csock = socket.socketpair()
# _ssock.setblocking(False)
# _csock.setblocking(False)
# selector.register(_ssock.fileno(), selectors.EVENT_READ, lambda x: x)
# while True:
#     a = selector.select(timeout=1)  # 这就是asyncio的超时机制。利用timeout来处理
#     print(a)





# import asyncio
# import aiohttp
#
#
# async def test():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://www.baidu.com') as response:
#             # print(await response.read())
#             ...
#
# async def test_for_sleep():
#     # await asyncio.sleep(3)
#     print('hello')
#
#
# async def main():
#     print('hello')
#     # await asyncio.gather(
#     #     # test(),
#     #     # test_for_sleep(),
#     #     test_for_sleep(),
#     # )


# if __name__ == '__main__':
#     asyncio.run(main())

# from contextvars import ContextVar, copy_context
#
# var = ContextVar('var')
# var.set('spam')
#
# def main(a):
#     print(a)
#
#     # 'var' was set to 'spam' before
#     # calling 'copy_context()' and 'ctx.run(main)', so:
#     # var.get() == ctx[var] == 'spam'
#
#     var.set('ham')
#
#     # Now, after setting 'var' to 'ham':
#     # var.get() == ctx[var] == 'ham'
#
# ctx = copy_context()
#
# # Any changes that the 'main' function makes to 'var'
# # will be contained in 'ctx'.
# ctx.run(main, 'asd')
#
# # The 'main()' function was run in the 'ctx' context,
# # so changes to 'var' are contained in it:
# # ctx[var] == 'ham'
# print(ctx[var])
#
# # However, outside of 'ctx', 'var' is still set to 'spam':
# # var.get() == 'spam'
# print(var.get())
