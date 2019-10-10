'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''

import signal
import sys
import ssl
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser

class SimpleEcho(WebSocket):

   def handleMessage(self):
      self.sendMessage(self.data + 'heihei')

   def handleConnected(self):
      print(self.address)

   def handleClose(self):
      pass

clients = []
class SimpleChat(WebSocket):

   def handleMessage(self):
      for client in clients:
         if client != self:
            client.sendMessage(self.address[0] + u' - ' + self.data)

   def handleConnected(self):
      print (self.address, 'connected')
      for client in clients:
         client.sendMessage(self.address[0] + u' - connected heihei')
      clients.append(self)

   def handleClose(self):
      clients.remove(self)
      print (self.address, 'closed')
      for client in clients:
         client.sendMessage(self.address[0] + u' - disconnected')


if __name__ == "__main__":

   # parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
   # parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
   # parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
   # parser.add_option("--example", default='echo', type='string', action="store", dest="example", help="echo, chat")
   # parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
   # parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
   # parser.add_option("--key", default='./key.pem', type='string', action="store", dest="key", help="key (./key.pem)")
   # parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")
   #
   # (options, args) = parser.parse_args()
   #
   # cls = SimpleEcho
   # if options.example == 'chat':
   #    cls = SimpleChat
   # print(options.ssl)
   # if options.ssl == 1:
   #    server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.key, version=options.ver)
   # else:
   #    server = SimpleWebSocketServer(options.host, options.port, cls)
   #
   # def close_sig_handler(signal, frame):
   #    server.close()
   #    sys.exit()
   #
   # signal.signal(signal.SIGINT, close_sig_handler)  # 采用这个好像可以很简单的控制
   #
   # server.serveforever()

   cls = SimpleEcho
   server = SimpleWebSocketServer('', 8000, cls)
   server.serveforever()
