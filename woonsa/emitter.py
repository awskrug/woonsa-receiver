from gevent.socket import create_connection

class Emitter(object):
    def __init__(self, *args, **kwargs):
        pass

    def emit(self, key, value, ts):
        pass

class CarbonEmitter(Emitter):
    def __init__(self, *args, **kwargs):
        Emitter.__init__(self)
        self.host = kwargs.get('CARBON_HOST')
        self.port = kwargs.get('CARBON_PORT')

    def _make_packet(self, key, value, ts):
        return "%s %s %d\n" % (key, value, ts)

    def emit(self, key, value, ts):
        try:
            sock = create_connection((self.host, self.port))
            sock.sendall(self._make_packet(key, value, ts))
        finally:
            sock.close()
