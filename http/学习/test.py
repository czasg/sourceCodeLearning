from enum import IntEnum

__all__ = ['HTTPStatus']

class HTTPStatus(IntEnum):
    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj
    CONTINUE = 100, 'Continue', 'Request received, please continue'
    SWITCHING_PROTOCOLS = (101, 'Switching Protocols',
            'Switching to new protocol; obey Upgrade header')
    PROCESSING = 102, 'Processing'

if __name__ == '__main__':
    import email.parser
    import email.message


    class HTTPMessage(email.message.Message):

        def getallmatchingheaders(self, name):
            name = name.lower() + ':'
            n = len(name)
            lst = []
            hit = 0
            for line in self.keys():
                if line[:n].lower() == name:
                    hit = 1
                elif not line[:1].isspace():
                    hit = 0
                if hit:
                    lst.append(line)
            return lst
    hstring = "cza:czaissg Host:fanyi.youdao.com"
    print(email.parser.Parser(_class=HTTPMessage).parsestr(hstring))