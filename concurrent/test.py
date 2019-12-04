from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import time


def test(a, b):
    time.sleep(a + b)
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
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(test, 1, 1), executor.submit(test, 1, 1)]
        now = time.time()
        for future in as_completed(futures):
            print(future.result(), time.time() - now)
