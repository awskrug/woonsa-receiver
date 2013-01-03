import gevent
from gevent import monkey; monkey.patch_all()
from gevent.server import StreamServer

from .logger import get_logger
from .mtr import Mtr
from .emitter import CarbonEmitter

import time

class ReceiveServer(StreamServer):
    def __init__(self, listener, **kwargs):
        StreamServer.__init__(self, listener, **kwargs)
        self.logger = get_logger(__name__)

    def handle(self, socket, addr):
        self.logger.info("New connection from %s:%s" % addr)
        gevent.spawn(self.recv_all, socket, addr)

    def recv_all(self, socket, addr):
        mtr = Mtr()
        sockf = socket.makefile()
        client_id = None
        lines = []
        while True:
            line = sockf.readline()
            if not line:
                self.logger.info("client disconnected")
                break
            line = line.strip()
            self.logger.debug(line)

            if not client_id:
                client_id = line
                self.logger.info("Client id: %s" % client_id)
                continue

            lines.append(line)
            try:
                mtr.feed(line)
            except ValueError:
                #skip
                pass

        for l in mtr.rows:
            self.logger.debug('%r' % l)

        gevent.spawn(self.emit_lines, lines)
        if client_id:
            gevent.spawn(self.emit_carbon, client_id, mtr.rows[-1])

    def emit_carbon(self, client_id, line):
        ts = int(time.time())
        emitter = CarbonEmitter(CARBON_HOST='localhost', CARBON_PORT=2003)
        emitter.emit('woonsa.rtt.%s' % client_id, line.avg, ts)
        emitter.emit('woonsa.loss.%s' % client_id, line.loss, ts)

    def emit_lines(self, lines):
        val = '\n'.join(lines)

    def close(self):
        if not self.closed:
            self.logger.info("Close Server")
            StreamServer.close(self)

