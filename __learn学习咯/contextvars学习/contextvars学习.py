from contextvars import *

# var= ContextVar('var')
#
# x=[1]
# var.set(x)
#
# y=var.get()
# print(f'x: {id(x)},y: {id(y)},{id(x)==id(y)}')
#
# y=var.get()
# print(f'x: {id(x)},y: {id(y)},{id(x)==id(y)}')
#
#
# z=[2]
#
# token=var.set(z)
# print(f'z: {var.get()}')
#
# var.reset(token)
#
# y=var.get()
# print(f'x: {id(x)},y: {id(y)},{id(x)==id(y)}')


# var = ContextVar('var')
# var.set('spam')
#
# def main():
#     # 'var' was set to 'spam' before
#     # calling 'copy_context()' and 'ctx.run(main)', so:
#     print(list(ctx.items()))
#     print(var.get() == ctx[var] == 'spam')
#
#     var.set('ham')
#     print(list(ctx.items()))
#     # Now, after setting 'var' to 'ham':
#     print(var.get() == ctx[var] == 'ham')
#
# ctx = copy_context()
#
# # Any changes that the 'main' function makes to 'var'
# # will be contained in 'ctx'.
# ctx.run(main)
#
# # The 'main()' function was run in the 'ctx' context,
# # so changes to 'var' are contained in it:
# print(ctx[var] == 'ham')
#
# # However, outside of 'ctx', 'var' is still set to 'spam':
# print(var.get() == 'spam')


# from contextvars import ContextVar
# import asyncio
# import random
#
# cv = ContextVar('cv')
# ctx = copy_context()
#
# async def waiting_func(name):
#     ctx = copy_context()
#     print(list(ctx.items()))
#     print(f'{name} Before sleep: {cv.get()}')
#     await asyncio.sleep(random.random())
#     print(f'{name} After 1 sleep: {cv.get()}')
#     await asyncio.sleep(random.random())
#     print(f'{name} After 2 sleep: {cv.get()}')
#
#
# async def task(name):
#     await waiting_func(name)
#
#
# async def main():
#     for name in ('first', 'second', 'third'):
#         cv.set(name)
#         await task(name)
#
# if __name__ == '__main__':
#     asyncio.run(main())


import asyncio
import contextvars

client_addr_var = contextvars.ContextVar('client_addr')  # 创建一个var


# ctx = copy_context()
def render_goodbye():
    # The address of the currently handled client can be accessed
    # without passing it explicitly to this function.
    ctx = copy_context()
    # print(list(ctx.items()))
    # client_addr = client_addr_var.get()
    client_addr = ctx.get(client_addr_var)  # 卧槽, 怎么实现的, 好屌啊
    return f'Good bye, client @ {client_addr}\n'.encode()


async def handle_request(reader, writer):
    addr = writer.transport.get_extra_info('socket').getpeername()
    client_addr_var.set(addr)  # set here? and then?

    # In any code that we call is now possible to get
    # client's address by calling 'client_addr_var.get()'.

    while True:
        line = await reader.readline()
        print(line)
        if not line.strip():
            break
        writer.write(line)

    writer.write(render_goodbye())
    writer.close()


async def main():
    srv = await asyncio.start_server(
        handle_request, '127.0.0.1', 8081)

    async with srv:
        await srv.serve_forever()


asyncio.run(main())
