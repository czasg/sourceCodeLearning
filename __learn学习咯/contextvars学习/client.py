import socket

sock = socket.socket()
sock.connect(("127.0.0.1", 8081))



sock.send(b"hello world\r\n")
sock.send(b"\r\n")
res = sock.recv(1024)
print(res)
res = sock.recv(1024)
print(res)
