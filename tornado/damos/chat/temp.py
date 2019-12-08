if __name__ == '__main__':
    async def test1():
        pass
    def test2():
        yield 1
    def test3(t=1):
        if t:
            return 'cza'
        else:
            return test2()
