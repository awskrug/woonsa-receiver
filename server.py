import os
import gevent
import signal
from woonsa.receiver import ReceiveServer
from woonsa.config import load_config_from_file

config = load_config_from_file(os.environ.get('WOONSA_CONFIG'))
server = ReceiveServer(('0.0.0.0', 12114), config)

gevent.signal(signal.SIGTERM, server.close)
gevent.signal(signal.SIGINT, server.close)
server.start()
gevent.wait()
