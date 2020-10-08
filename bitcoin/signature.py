from io import BytesIO

from .exceptions import BadSignature


class Signature(object):
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __str__(self):
        return f'Signature({self.r},{self.s})'

    def __eq__(self, other):
        return self.r == other.r and self.s == other.s

    def der(self):
        """
        Serialize the signature to DER format.
        """
        rbin = self.r.to_bytes(32, 'big')
        rbin = rbin.lstrip(b'\x00')
        if rbin[0] & 0x80:
            rbin = b'\x00' + rbin
        result = bytes([2, len(rbin)]) + rbin

        sbin = self.s.to_bytes(32, 'big')
        sbin = sbin.lstrip(b'\x00')
        if sbin[0] & 0x80:
            sbin = b'\x00' + sbin
        result += bytes([2, len(sbin)]) + sbin

        return bytes([0x30, len(result)]) + result

    @staticmethod
    def parse(signature_bin):
        """
        Parse signature from DER format bytes.
        """
        stream = BytesIO(signature_bin)
        compound = stream.read(1)[0]
        if compound != 0x30:
            raise BadSignature
        length = stream.read(1)[0]
        if length + 2 != len(signature_bin):
            raise BadSignature
        marker = stream.read(1)[0]
        if marker != 0x02:
            raise BadSignature
        r_length = stream.read(1)[0]
        r = int.from_bytes(stream.read(r_length), 'big')
        marker = stream.read(1)[0]
        if marker != 0x02:
            raise BadSignature
        s_length = stream.read(1)[0]
        s = int.from_bytes(stream.read(s_length), 'big')
        if len(signature_bin) != r_length + s_length + 6:
            raise BadSignature

        return Signature(r, s)
