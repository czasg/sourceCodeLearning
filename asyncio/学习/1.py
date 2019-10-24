import threading
import asyncio
loop = asyncio.new_event_loop()


class _RunningLoop(threading.local):
    loop_pid = (None, None)

_running_loop = _RunningLoop()

if __name__ == '__main__':
    print(_running_loop.loop_pid)
