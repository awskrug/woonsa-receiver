import gevent
from gevent import monkey; monkey.patch_all()
from gevent.server import StreamServer

from .logger import get_logger
from .mtr import Mtr
from .emitter import CarbonEmitter, DynamoDbEmitter

import time

class ReceiveServer(StreamServer):
    def __init__(self, listener, config, **kwargs):
        StreamServer.__init__(self, listener, **kwargs)
        self.logger = get_logger(__name__)
        self.config = config

    def handle(self, socket, addr):
        self.logger.info("New connection from %s:%s" % addr)
        gevent.spawn(self.recv_all, socket, addr)

    def recv_all(self, socket, addr):
        mtr = Mtr()
        sockf = socket.makefile()
        client_id = None
        ts = int(time.time())
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
                self.logger.info("Client id: %s ts: %d" % (client_id, ts))
                continue

            lines.append(line)
            try:
                mtr.feed(line)
            except ValueError:
                #skip
                pass

        for l in mtr.rows:
            self.logger.debug('%r' % l)

        gevent.spawn(self.emit_lines, ts, client_id, lines)
        if client_id:
            gevent.spawn(self.emit_carbon, ts, client_id, mtr.rows[-1])

    def emit_carbon(self, ts, client_id, line):
        _config = self.config.get('emitter').get('carbon')
        emitter = CarbonEmitter(
            CARBON_HOST=_config.get('host'),
            CARBON_PORT=_config.get('port'))
        emitter.emit('woonsa.rtt.%s' % client_id, line.avg, ts)
        emitter.emit('woonsa.loss.%s' % client_id, line.loss, ts)

    def emit_lines(self, ts, client_id, lines):
        _config = self.config.get('emitter').get('dynamodb')
        emitter = DynamoDbEmitter(
            AWS_ACCESS_KEY_ID=_config.get('aws_access_key_id'),
            AWS_SECRET_ACCESS_KEY=_config.get('aws_secret_access_key'),
            AWS_DYNAMODB_SCHEMA=_config.get('aws_dynamo_db_schema'),
            AWS_REGION=_config.get('aws_region'))

        val = '\n'.join(lines)
        emitter.emit(client_id, val, ts)

    def close(self):
        if not self.closed:
            self.logger.info("Close Server")
            StreamServer.close(self)

