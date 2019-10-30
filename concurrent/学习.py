import sys
link1 = ['link1']  # link1: 0 -> 1
link2 = ['link2']  # link2: 0 -> 1
link3 = ['link3']  # link3: 0 -> 1
A = link1  # link1&A: 1 -> 2

link1.append(link2)  # link2: 1 -> 2
link2.append(link3)  # link3: 1 -> 2
link3.append(link1)  # link1&A: 2 -> 3

del link1  # 删除link1, 容器link1引用减一, 3 -> 2  现在['link1']引用还有A和['link3']
# del link2
# del link3
print(sys.getrefcount(A))  # 3
# print(A)  # ['link1', ['link2', ['link3', [...]]]]



# import weakref
# import threading
# def _cb1(a=0): print('11111this will run when test is over')
# def _test1():...
# def _test2():...
# wr = weakref.ref(_test1, _cb1)  # 这种弱引用，设定了回调函数，只有当对象被销毁时才会调用
# del _test1
# print(wr())  # 当引用已被销毁，则再次调用弱引用对象，则会直接返回一个None -> ref() is not None
# weakref.finalize(_test2, print, '22222this will run when test is over')  # 终结器调用。感觉很强大。
# def target():
#     def _t(a): ...
#     wr = weakref.ref(_t, _cb1)
# threading.Thread(target=target).start()  # 在线程中设定了弱引用，然后线程结束。会触发弱引用回调函数的调用
# threading.Thread(target=target).start()
# while True:
#     import time
#     time.sleep(3)
#     break
#
# def cb2():
#     print('callback')
#     return 666
# class Test:
#     def hello(self): print('hello')
# o = Test()
# wt = weakref.finalize(o, cb2)  # 手动终结者????我自己触发则直接调用回调函数，原引用也没了???这也太狠了吧
# print(o)
# del o
# print('asd')
# # print(w is o)












# import concurrent.futures
# import urllib.request
# import itertools
#
# URLS = ['http://www.foxnews.com/',
#         # 'http://www.cnn.com/',
#         'http://europe.wsj.com/',
#         'http://www.bbc.co.uk/',
#         'http://some-made-up-domain.com/']
#
# # Retrieve a single page and report the URL and contents
# def load_url(url, timeout):
#     with urllib.request.urlopen(url, timeout=timeout) as conn:
#         return conn.read()
#
# # We can use a with statement to ensure threads are cleaned up promptly
# if __name__ == '__main__':
#     # print(itertools.count().__next__)
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         # Start the load operations and mark each future with its URL
#         future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
#         for future in concurrent.futures.as_completed(future_to_url):
#             url = future_to_url[future]
#             try:
#                 data = future.result()
#             except Exception as exc:
#                 print('%r generated an exception: %s' % (url, exc))
#             else:
#                 print('%r page is %d bytes' % (url, len(data)))








# import time
# import threading
# import concurrent.futures
# local = threading.local()  # threading.local是一个全局变量，可以很强。
#
# def test(a):
#     local.x = a
#     time.sleep(3)
#     print('Good!', local.x)
#
# if __name__ == '__main__':
#     # with concurrent.futures.ThreadPoolExecutor() as executor:
#     #     [executor.submit(test, i) for i in range(10)]
#
#     # [threading.Thread(target=test, args=(i,)).start() for i in range(10)]
#
#     threading.Timer(5, test, args=[1]).start()




