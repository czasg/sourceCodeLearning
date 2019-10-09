from io import StringIO, BytesIO


rfile = BytesIO(b'asd\n123\nasd')
print(rfile.readline())
print(rfile.readline())