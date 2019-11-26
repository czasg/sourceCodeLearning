from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import time


def test(a, b):
    time.sleep(3)
    print('????????')
    return f"Hello World"


"""
a.start();
b.start();
a.join();
主线程开始->a 和 b 看脸谁先开始 ->a 和 b 看脸谁先死 -> 
                                                    如果是a先死,那么主线程终止,b继续跑,跑完死
                                                    如果是b先死,那么a继续跑,跑完a死,主线程死
也就是说a使用了join。那么主线程就会阻塞直至a完成咯
"""
if __name__ == '__main__':
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     futures = [executor.submit(test, 2, 2) for _ in range(2)]
    #     for tes in wait(futures):
    #         print('?')
    #     print('在这里卡死了吗')
    #     import time
    #     time.sleep(2)

    import itertools
    _counter = itertools.count().__next__
    print(_counter(), _counter(), _counter())

    # aim = ThreadPoolExecutor(max_workers=2)
    # [aim.submit(test, 2, 2) for _ in range(2)]  # 原来如此，调用了join导致主线程会等待所有线程直至结束
    # import time
    # time.sleep(2)
    # print('停不下来咯')
    # time.sleep(2)
    # print('停不下来咯')
    # time.sleep(2)

    # from multiprocessing.managers import BaseManager
    # manager = BaseManager(address=('', 50000), authkey=b'abc')
    # server = manager.get_server()
    # server.serve_forever()

# from minitools import MiniCache
# import time
# miniCache = MiniCache.get_instance()
# @miniCache.miniCache(600)
# def test():
#     time.sleep(3)
#     return 10
# @miniCache.miniCache(600)
# def test1():
#     time.sleep(3)
#     return 3
# if __name__ == '__main__':
#     # print(test())
#     # print(test1())
#     # print(test())
#     # print(test1())
#     # print(test())
#
#     # import weakref
#     # class Dict(dict):
#     #     pass
#     # obj1 = Dict(a=123,b=456,c=789)
#     # obj2 = Dict(a=123,b=456,c=789, d=234)
#     #
#     # di = weakref.WeakValueDictionary()
#     # di['test1'] = obj1
#     # di['test2'] = obj2
#     # # print(dict(di))
#     # # print(list(di.values()))
#     #
#     # # def callback(ddd=di):
#     # #     print(ddd)
#     # #
#     # # weakref.finalize(obj1, callback)
#     #
#     # # del obj1
#     # # print(dict(di))
#     # # print(list(di.values()))
#     #
#     # # dd = dict(obj1=obj1, obj2=obj2)
#     # # print(dd)
#     # def callback1(_, ddi=di):
#     #     print(_, dict(ddi))
#     # te = weakref.ref(obj1, callback1)
#     # del obj1
#     # # print(dd)
