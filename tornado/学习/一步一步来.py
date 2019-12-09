from typing import overload

class Test:
    # @overload
    # def hello(self, text: None) -> None: ...
    #
    # @overload
    # def hello(self, text: str) -> None: ...

    def hello(self, text):
        print(f"text is {text}, and type is {type(text)}")

if __name__ == '__main__':
    # t = Test()
    # t.hello('Cza')
    # t.hello(None)

    exec("""for i in range(5):
        print(i)
    """)

