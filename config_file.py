valid_keys = ['DefaultDir']


def b2u(string):
    """ bytes to unicode """
    if isinstance(string, bytes):
        return string.decode('utf-8', 'replace')
    return string


class mdv_conf:
    def __init__(self, filename):
        self.filename = filename
        self.clear()

    def clear(self):
        self._config = {}
        self._deleted = []

    def get(self, key):
        return self._config.get(key.strip())

    def set(self, key, value):
        _key = b2u(key.strip())
        self._config[_key] = b2u(value.strip())
        if _key in self._deleted:
            self._deleted.remove[_key]

    # load self.filename
    def read(self):
        self.clear()
        try:
            f = open(self.filename, 'r')
        except Exception as msg:
            print('Failed to open %s: %s' % (self.filename, msg))
            raise

        for line in f:
            if not line:
                break
            line = line.strip()
            if len(line) < 1 or line[0] in ['#', ';']:
                continue
            # get key/value pair
            pair = [x.strip() for x in line.split('=')]
            if len(pair) != 2:
                print('Invalid option definition: %s', line.strip())
                continue
            elif pair[0] not in valid_keys:
                print('Invalid option: %s', line.strip())
                continue
            elif pair[1] == '':
                print('Missing value: %s', line.strip())
                continue
            elif self._config.get(pair[0]) is not None:
                print('Duplicate option definition: %s', line.strip())
                continue
            self._config[pair[0]] = pair[1]
        f.close()
