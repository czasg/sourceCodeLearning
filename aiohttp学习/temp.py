import asyncio
import aiohttp

loop = asyncio.get_event_loop()

async def get_func():
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get('http://www.baidu.com') as response:
            print(response.status)
            # print(type(await response.text()), await response.text())  # 已解码的数据
            # print('\n')
            # print(type(await response.read()), await response.read())  # 数据会加载到内存中
            # print('\n')
            # print(type(await response.json()), await response.json())  # 获取的是JSON数据，则可以直接使用这不获取结果
            # print(type(await response.content.read()))
            print(await response.content.read())

if __name__ == '__main__':
    loop.run_until_complete(get_func())
