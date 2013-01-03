class SparseList(list):
    def __setitem__(self, index, value):
        missing = index - len(self) + 1
        if missing > 0:
            self.extend([None] * missing)
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        try:
            return list.__getitem__(self, index)
        except IndexError:
            return None

class Mtr(object):
    def __init__(self):
        self._rows = SparseList()

    def feed(self, raw):
        line = MtrLine(raw)
        self._rows[line.pos] = line

    @property
    def rows(self):
        return self._rows

class MtrLine(object):
    def __init__(self, raw):
        if len(raw) == 0:
            raise TypeError('Invalid MTR Output')

        _pos, _name, _loss, _retr, _xmit, _best, _avg, _worst = raw.split(' ')

        self._pos = int(_pos)-1
        self._name = _name
        self._loss = float(_loss)/1000.0
        self._retr = int(_retr)
        self._xmit = int(_xmit)
        self._best = float(_best)
        self._avg = float(_avg)
        self._worst = float(_worst)

    @property
    def pos(self):
        return self._pos

    @property
    def name(self):
        return self._name

    @property
    def loss(self):
        return self._loss

    @property
    def returned(self):
        return self._retr

    @property
    def emit(self):
        return self._xmit

    @property
    def best(self):
        return self._best

    @property
    def avg(self):
        return self._avg

    @property
    def worst(self):
        return self._worst

    def __repr__(self):
        return '<MtrLine %s (%.2f%%, %.2f, %.2f, %.2f)>' % (self.name, self.loss, self.best, self.avg, self.worst)
