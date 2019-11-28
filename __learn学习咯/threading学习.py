# -*- coding: utf-8 -*-
import threading
import time
import _threading_local
# from greenlet import getcurrent
from werkzeug.local import LocalStack, LocalProxy


class Local(_threading_local.local):
    argv1 = None
    argv2 = None


# print(id(threading.current_thread()), 'This is the main-thread')
ll = Local()
ll.cza_test = "cza_test"


# print('1111', threading.current_thread().__dict__)

def process(data1, data2):
    # print(threading.current_thread().__dict__)
    # print('##################')
    ll.argv1 = data1  # 在进行赋值的时候会报错
    ll.argv2 = data2
    # print('2222', threading.current_thread().__dict__)
    # print('##################')
    # print(ll.__dict__)
    # print(ll._local__impl.dicts)
    print(f"{threading.get_ident()}-{data1}-{data2}-before")
    time.sleep(1)
    show()


def show():
    # 像这样使用 ll._local__impl.dicts 就可以查询到其他线程的变量了
    print(f"{threading.get_ident()}-{ll.argv1}-{ll.argv2}-after-{ll._local__impl.dicts}")


if __name__ == '__main__':
    # aa = LocalStack()
    # aa.push(123)
    # print(aa.top)
    # aa.push(12)
    # print(aa.top)
    # aa.push(456)
    # print(aa.top)
    # print(aa.pop())
    # print(aa.pop())
    # print(aa.pop())

    # print(getcurrent(), id(threading.current_thread()))
    data = [
        ['cza', 'sg'],
        ['ha', 'good'],
        ['whats', 'ready']
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
