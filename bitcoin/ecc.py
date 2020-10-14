from io import BytesIO
from random import randint 

from .exceptions import BadSignature
from .helpers import hash160, encode_base58_checksum


class FieldElement(object):
    """
    Represents a number in a finite field.

    Attributes
    ----------
    val : int
        The finite field element.
    prime : int
        The size of the finite field.
    """

    def __init__(self, val, prime):
        if val >= prime or val < 0:
            raise ValueError(f'Num {val} not in field range 0 to {prime}')
        self.val = val
        self.prime = prime

    def __str__(self):
        class_name = self.__class__.__name__
        return f'{class_name}_{self.prime}({self.val})'

    def __eq__(self, other):
        if other is None:
            return False
        return self.prime == other.prime and self.val == other.val

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError(f'Cannot add two numbers in different fields.')
        val = (self.val + other.val) % self.prime
        return self.__class__(val, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError(f'Cannot substract two numbers in different fields.')
        val = (self.val - other.val) % self.prime
        return self.__class__(val, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError(f'Cannot multiply two numbers in different fields.')
        val = (self.val * other.val) % self.prime
        return self.__class__(val, self.prime)

    def __rmul__(self, other):
        if type(other) == int:
            other = self.__class__(other, self.prime)
        return other * self

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        val = pow(self.val, n, self.prime)
        return self.__class__(val, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError(f'Cannot divide two numbers in different fields.')
        val = self * (other ** (self.prime - 2))
        return val


class Point(object):
    """
    Represents a point in an elliptic curve.

    Attributes
    ----------
    x, y : int, int
        The x-axis and y-axis location of the point.
    a, b : int, int
        The parameters for the elliptic curve y^2 = x^3 + ax + b
    """

    @property
    def curve(self):
        return (self.a, self.b)

    @property
    def is_identity(self):
        return self.x is None and self.y is None

    @property
    def is_finite_field(self):
        if self.is_identity:
            return (type(self.a) == type(self.b) == FieldElement)
        else:
            return (type(self.x) == type(self.y) == \
                    type(self.a) == type(self.b) == FieldElement)

    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if self.x is None and self.y is None:
            return
        if self.y**2 != self.x**3 + a*x + b:
            raise ValueError(f'({x}, {y}) is not on the curve.')

    def __str__(self):
        class_name = self.__class__.__name__
        if self.is_finite_field:
            if self.is_identity:
                return f'{class_name}(infinity) FieldElement({self.a.prime})'
            else:
                return f'{class_name}({self.x.val},{self.y.val})_{self.a.val}_{self.b.val} ' \
                    f'FieldElement({self.x.prime})'
        else:
            return f'{class_name}({self.x},{self.y})_{self.a}_{self.b}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
               self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        assert self.curve == other.curve 

        if self.is_identity:
            return other
        elif other.is_identity:
            return self
        elif self == other:
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x = s**2 - 2*self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        elif self == other and self.y == 0:
            return self.__class__(None, None, self.a, self.b)
        elif self.x == other.x:
            return self.__class__(None, None, self.a, self.b)
        elif self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s**2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

    def __rmul__(self, coefficient):
        coef = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result


class S256Field(FieldElement):
    P = 2**256 - 2**32 - 977

    def __init__(self, val, *args, **kwargs):
        super().__init__(val, self.P)

    def __str__(self):
        return '{:x}'.format(self.val).zfill(64)

    def sqrt(self):
        return self**((self.P + 1) // 4)


A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


class S256Point(Point):
    def __init__(self, x, y, *args, **kwargs):
        a = S256Field(A)
        b = S256Field(B)
        if type(x) == int:
            x = S256Field(x)
            y = S256Field(y)
        super().__init__(x, y, a, b)

    def __str__(self):
        if self.x == None and self.y == None:
            return f'S256Point(infinity)'
        else:
            return f'S256Point({hex(self.x.val)}, {hex(self.y.val)})'

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)

    def verify(self, z, sig):
        s_inv = pow(sig.s, N-2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N 
        point = (u * G) + (v * self)
        return point.x.val == sig.r

    def sec(self, compressed=True):
        """
        Serialize current point to the binary version of the SEC format.
        """
        if compressed:
            if self.y.val % 2 == 0:
                prefix = b'\x02' 
            else:
                prefix = b'\x03'
            return prefix + self.x.val.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.val.to_bytes(32, 'big') \
                           + self.y.val.to_bytes(32, 'big')

    @staticmethod
    def parse(sec_bin):
        """
        Returns a Point object from a SEC binary.
        """
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x, y)

        is_even = sec_bin[0] == 2
        x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
        alpha = x**3 + S256Field(B)
        beta = alpha.sqrt()
        if beta.val % 2 == 0:
            even_beta = beta
            odd_beta = S256Field(S256Field.P - beta.val)
        else:
            even_beta = S256Field(S256Field.P - beta.val)
            odd_beta = beta
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)

    def address(self, compressed=True, testnet=False):
        """
        Return the address string.
        """
        h160 = hash160(self.sec(compressed))
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)


G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
)


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


class PrivateKey(object):
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G

    def __str__(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = randint(0, N)
        r = (k * G).x.val
        k_inv = pow(k, N-2, N)
        s = (z + r * self.secret) * k_inv % N
        if s > N/2:
            s = N - s
        return Signature(r, s)

    def wif(self, compressed=True, testnet=False):
        secret_bytes = self.secret.to_bytes(32, 'big')
        if testnet:
            prefix = b'\xef'
        else:
            prefix = b'\x80'
        if compressed:
            suffix = b'\x01'
        else:
            suffix = b''
        return encode_base58_checksum(prefix + secret_bytes + suffix)
