
class locked_cached_property:
    def __init__(self, func, name=None):
        self.func = func

class test:

    @locked_cached_property
    def name(self):
        print('hello')

if __name__ == '__main__':
    test = test()
    print(type(test.name))
    print(test.name.func())