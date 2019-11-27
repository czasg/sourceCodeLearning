# -*- coding: utf-8 -*-
import threading, logging, socket

DATEFMT = "%H:%M:%S"
FORMAT = "[%(asctime)s]\t [%(threadName)s,%(thread)d] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)

sock = socket.socket()
addr = ('127.0.0.1', 9999)
event = threading.Event()

sock.bind(addr)
sock.listen()


def _accept(sock: socket.socket):
    s, addrinfo = sock.accept()
    fr = s.makefile(mode='rb', buffering=1024)
    fw = s.makefile(mode='wb', buffering=1024)

    while True:
        line = fr.readline()  # read(10) 文本使用readlin
        logging.info(line)

        if line.strip() == 'quit':
            break

        msg = "Your msg = {}. ack".format(line)
        fw.write(msg.encode())
        fw.flush()
    fw.close()
    fr.close()
    sock.close()


threading.Thread(target=_accept, args=(sock,)).start()

# while not event.wait(2):
#     logging.info(sock)