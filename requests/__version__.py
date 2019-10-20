# .-. .-. .-. . . .-. .-. .-. .-.
# |(  |-  |.| | | |-  `-.  |  `-.
# ' ' `-' `-`.`-' `-' `-'  '  `-'

__title__ = 'requests'
__description__ = 'Python HTTP for Humans.'
__url__ = 'http://python-requests.org'
__version__ = '2.21.0'
__build__ = 0x022100
__author__ = 'Kenneth Reitz'
__author_email__ = 'me@kennethreitz.org'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2018 Kenneth Reitz'
__cake__ = u'\u2728 \U0001f370 \u2728'


if __name__ == '__main__':
    import urllib.request
    print(urllib.request.urlopen('http://www.baidu.com').read())
    # urlopen -> http.client.HTTPConnection -> socket.create_connection => socket.socket() + socket.connect()