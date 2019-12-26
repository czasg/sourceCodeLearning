from test1.tasks import add

if __name__ == '__main__':
    import time
    start = time.time()
    t = add.delay(1,2)
    print(t)
    print(t.result)
    print(time.time() - start)
