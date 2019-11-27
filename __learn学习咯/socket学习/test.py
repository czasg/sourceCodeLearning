
import socket

sock = socket.socket()
addr = ('127.0.0.1', 9999)
sock.connect(addr)

sock.send(b"cza is sg lololo\r\nczaczacza")
print(sock.recv(1024))

