# -*- coding: utf-8 -*-
import threading
import time
import _threading_local


class Local(_threading_local.local):
    argv1 = None
    argv2 = None


print(id(threading.current_thread()), 'This is the main-thread')
ll = Local()


def process(data1, data2):
    # print(threading.current_thread().__dict__)
    # print('##################')
    ll.argv1 = data1  # 在进行赋值的时候会报错
    ll.argv2 = data2
    # print('##################')
    # print(ll.__dict__)
    # print(ll._local__impl)
    print(f"{threading.get_ident()}-{data1}-{data2}-before")
    time.sleep(1)
    show()


def show():
    print(f"{threading.get_ident()}-{ll.argv1}-{ll.argv2}-after")


if __name__ == '__main__':
    data = [
        ['cza', 'sg'],
        # ['ha', 'good'],
        # ['whats', 'ready']
    ]


    for d in data:
        threading.Thread(target=process, args=d).start()

    # class Test:
    #     pass
    #
    #
    # ar = []
    # kw = {}
    # test = Test()
    # test.__init__(*ar, **kw)
