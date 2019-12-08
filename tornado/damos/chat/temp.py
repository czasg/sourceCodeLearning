import time
import threading
import asyncio

loop = asyncio.get_event_loop()

if __name__ == '__main__':
    async def ttest():
        s = time.time()
        for _ in range(100000000):
            a = None
        print(time.time() - s)


    def test():
        s = time.time()
        for _ in range(100000000):
            a = None
        print(time.time() - s)


    # threading.Thread(target=test).start()  # 计算密集型 - 多线程简直是灾难
    # threading.Thread(target=test).start()
    # threading.Thread(target=test).start()

    task1 = asyncio.Task(ttest(), loop=loop)
    task2 = asyncio.Task(ttest(), loop=loop)
    task3 = asyncio.Task(ttest(), loop=loop)
    loop.run_until_complete(asyncio.wait([task1, task2, task3]))

    # test()
