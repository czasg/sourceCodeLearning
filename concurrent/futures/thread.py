# Copyright 2009 Brian Quinlan. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Implements ThreadPoolExecutor."""

__author__ = 'Brian Quinlan (brian@sweetapp.com)'

import atexit
from concurrent.futures import _base
import itertools
import queue
import threading
# 主要用途是实现保存大对象的高速缓存或映射，但又并希望大对象仅仅因为它出现在高速缓存或映射中而保持存活。
import weakref  # 卧槽，原来这个偌引用里面有一个超级牛的回调函数啊
import os

# Workers are created as daemon threads. This is done to allow the interpreter
# to exit when there are still idle threads in a ThreadPoolExecutor's thread
# pool (i.e. shutdown() was not called). However, allowing workers to die with
# the interpreter has two undesirable properties:
#   - The workers would still be running during interpreter shutdown,
#     meaning that they would fail in unpredictable ways.
#   - The workers could be killed while evaluating a work item, which could
#     be bad if the callable being evaluated has external side-effects e.g.
#     writing to a file.
#
# To work around this problem, an exit handler is installed which tells the
# workers to exit when their work queues are empty and then waits until the
# threads finish.

_threads_queues = weakref.WeakKeyDictionary()  # 弱引用字典
_shutdown = False

def _python_exit():
    global _shutdown
    _shutdown = True
    items = list(_threads_queues.items())
    for t, q in items:
        q.put(None)
    for t, q in items:
        t.join()

atexit.register(_python_exit)

# 这个类功能可真是mini呢
class _WorkItem(object):  # 入队列的实际对象
    def __init__(self, future, fn, args, kwargs):
        self.future = future  # 注册函数申请的未来对象
        self.fn = fn  # 注册函数
        self.args = args
        self.kwargs = kwargs

    def run(self):  # run就是真正执行函数的地方。获取结果后将结果传入未来对象
        if not self.future.set_running_or_notify_cancel():
            return

        try:
            result = self.fn(*self.args, **self.kwargs)  # 调用init中的fn函数，从而得到结果
        except BaseException as exc:
            self.future.set_exception(exc)
            # Break a reference cycle with the exception 'exc'
            self = None
        else:
            self.future.set_result(result)  # 将此结果作为结果传入未来对象


def _worker(executor_reference, work_queue, initializer, initargs):  # 线程调度的实际工作函数
    if initializer is not None:
        try:
            initializer(*initargs)
        except BaseException:
            _base.LOGGER.critical('Exception in initializer:', exc_info=True)
            executor = executor_reference()
            if executor is not None:
                executor._initializer_failed()
            return
    try:
        while True:
            work_item = work_queue.get(block=True)  # 阻塞get，如何唤醒就是很经典的操作
            if work_item is not None:
                work_item.run()  # 阻塞执行
                # Delete references to object. See issue16284
                del work_item
                continue  # 但是每一个线程都会阻塞在上面的get。只要能拿到workitem最后就会上去啊
            executor = executor_reference()  # 获取弱引用
            # Exit if:
            #   - The interpreter is shutting down OR
            #   - The executor that owns the worker has been collected OR
            #   - The executor that owns the worker has been shutdown.
            if _shutdown or executor is None or executor._shutdown:
                # Flag the executor as shutting down as early as possible if it
                # is not gc-ed yet.
                # print(_shutdown, executor, executor._shutdown)  # executor._shutdown -> True
                if executor is not None:
                    executor._shutdown = True
                # Notice other workers
                work_queue.put(None)  # ??怎么来的
                return
            del executor
    except BaseException:
        _base.LOGGER.critical('Exception in worker', exc_info=True)


class BrokenThreadPool(_base.BrokenExecutor):
    """
    Raised when a worker thread in a ThreadPoolExecutor failed initializing.
    """


class ThreadPoolExecutor(_base.Executor):

    # Used to assign unique thread names when thread_name_prefix is not supplied.
    _counter = itertools.count().__next__

    def __init__(self, max_workers=None, thread_name_prefix='',
                 initializer=None, initargs=()):
        """Initializes a new ThreadPoolExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            initializer: An callable used to initialize worker threads.
            initargs: A tuple of arguments to pass to the initializer.
        """
        if max_workers is None:
            # Use this number because ThreadPoolExecutor is often
            # used to overlap I/O instead of CPU work.
            max_workers = (os.cpu_count() or 1) * 5
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")

        if initializer is not None and not callable(initializer):
            raise TypeError("initializer must be a callable")

        self._max_workers = max_workers
        self._work_queue = queue.SimpleQueue()
        self._threads = set()
        self._broken = False
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._thread_name_prefix = (thread_name_prefix or
                                    ("ThreadPoolExecutor-%d" % self._counter()))
        self._initializer = initializer
        self._initargs = initargs

    def submit(self, fn, *args, **kwargs):  # 每创建一个submit，都是会创建一个新的线程
        with self._shutdown_lock:  # 确实是每一个都上锁操作
            if self._broken:
                raise BrokenThreadPool(self._broken)

            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            if _shutdown:
                raise RuntimeError('cannot schedule new futures after '
                                   'interpreter shutdown')

            f = _base.Future()  # 创建一个未来对象
            w = _WorkItem(f, fn, args, kwargs)  # 实际工作对象
            # 所谓的submit其实就是用目标函数注册一个未来对象，用此未来对象申请一个工作调度对象，然后将此工作对象推到队列中就完事了
            self._work_queue.put(w)  # 每一次submit都会将实际工作对象推入队列中
            self._adjust_thread_count()
            return f  # 返回注册函数申请的未来对象
    submit.__doc__ = _base.Executor.submit.__doc__

    def _adjust_thread_count(self):
        # When the executor gets lost, the weakref callback will wake up
        # the worker threads.
        def weakref_cb(_, q=self._work_queue):  # 当前对象没有引用的时候，会执行此回调函数
            q.put(None)
        # TODO(bquinlan): Should avoid creating new threads if there are more
        # idle threads than items in the work queue.
        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self._thread_name_prefix or self,
                                     num_threads)
            t = threading.Thread(name=thread_name, target=_worker,
                                 args=(weakref.ref(self, weakref_cb),
                                       self._work_queue,
                                       self._initializer,
                                       self._initargs))
            t.daemon = True  # 居然设置为了守护进程，就是为了防止程序停不下来
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue  # 这是一个弱引用字典。key的弱引用

    def _initializer_failed(self):
        with self._shutdown_lock:
            self._broken = ('A thread initializer failed, the thread pool '
                            'is not usable anymore')
            # Drain work queue and mark pending futures failed
            while True:
                try:
                    work_item = self._work_queue.get_nowait()
                except queue.Empty:
                    break
                if work_item is not None:
                    work_item.future.set_exception(BrokenThreadPool(self._broken))

    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown = True
            self._work_queue.put(None)  # 传入一个空，然后空的会继续不同的往里面put值，直至所有完成
        if wait:
            for t in self._threads:
                t.join()
    shutdown.__doc__ = _base.Executor.shutdown.__doc__
