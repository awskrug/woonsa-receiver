import gevent
import signal
from woonsa.receiver import ReceiveServer

server = ReceiveServer(('0.0.0.0', 12114))

gevent.signal(signal.SIGTERM, server.close)
gevent.signal(signal.SIGINT, server.close)
server.start()
gevent.wait()
