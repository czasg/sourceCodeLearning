import asyncio

loop = asyncio.get_event_loop()

async def main():
    await asyncio.sleep(5)

if __name__ == '__main__':
    loop.run_until_complete(main())



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
