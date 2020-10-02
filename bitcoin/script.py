from .helpers import read_varints


class Script(object):
    @staticmethod
    def parse(stream):
        length = read_varints(stream)
        _ = stream.read(length)
        return Script()
