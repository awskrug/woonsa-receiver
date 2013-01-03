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
        if line.type == 'h':
            self.rows[line.pos] = [line.val, None, []]
        elif line.type == 'd':
            self.rows[line.pos][1] = line.val
        elif line.type == 'p':
            self.rows[line.pos][2].append(line.val)

    @property
    def rows(self):
        return self._rows

class MtrLine(object):
    def __init__(self, raw):
        if len(raw) == 0:
            raise TypeError('Invalid MTR Output')

        _type = raw[0]
        if _type != 'h' and _type != 'p' and _type != 'd':
            raise TypeError('Invalid MTR Output')
        _type, _pos, _val = raw.split(' ')

        self._type = _type
        self._pos = int(_pos)
        self._val = _val if _type != 'p' else int(_val)/1000.0

    @property
    def type(self):
        return self._type

    @property
    def pos(self):
        return self._pos

    @property
    def val(self):
        return self._val
