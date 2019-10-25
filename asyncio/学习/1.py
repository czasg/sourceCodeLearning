import threading
import asyncio
import socket
import selectors
import socketserver

loop = asyncio.new_event_loop()
selector = selectors.DefaultSelector()


def selector_loop():
    while True:
        for sock, mask in selector.select():
            pass


class _RunningLoop(threading.local):
    loop_pid = (None, None)


_running_loop = _RunningLoop()

if __name__ == '__main__':
    sock = socket.socket()
    print(_running_loop.loop_pid)
    selector_loop()
