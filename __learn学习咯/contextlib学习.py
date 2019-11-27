# -*- coding: utf-8 -*-

from contextlib import contextmanager


class OldQuery(object):

    def __init__(self, name):
        self.name = name

    def __enter__(self):  # 在enter里面打印一句话
        print('Begin')
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # 退出时又打印一句话
        if exc_type:
            print('Error')
        else:
            print('End')

    def query(self):
        print('Query info about %s...' % self.name)  # 这里就是上下文管理器中间执行的语句


def test_old_query():
    with OldQuery('Bob') as q:
        q.query()


class ContextQuery(object):

    def __init__(self, name):
        self.name = name

    def query(self):
        print('Query info about %s...' % self.name)


@contextmanager
def create_query(name):
    print('Begin')
    q = ContextQuery(name)
    yield q
    print('End')


def test_context_query():
    with create_query('Bob') as q:
        q.query()


@contextmanager
def tag(name):
    print("<%s>" % name)  # 相当于__enter__所执行的代码
    yield  # 此处会暂时返回，用于处理上下文管理器中真正的应用逻辑
    print("</%s>" % name)  # 相当于__exit__所执行的代码


def test_tag():
    """
    with语句首先执行yield之前的语句，因此打印出<h1>；
    yield调用会执行with语句内部的所有语句，因此打印出hello和world；
    最后执行yield之后的语句，打印出</h1>。
    :return:
    """
    with tag("h1"):  # <h1> hello world </h1>
        print("hello")
        print("world")


if __name__ == '__main__':
    test_old_query()
    test_context_query()
    test_tag()
