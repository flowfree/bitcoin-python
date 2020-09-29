from .s256_field import FieldElement, S256Field


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


class S256Point(Point):
    A = 0
    B = 7
    N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

    def __init__(self, x, y, *args, **kwargs):
        a = S256Field(self.A)
        b = S256Field(self.B)
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
        coef = coefficient % self.N
        return super().__rmul__(coef)

    def verify(self, z, sig):
        s_inv = pow(sig.s, self.N-2, self.N)
        u = z * s_inv % self.N
        v = sig.r * s_inv % self.N 
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
        alpha = x**3 + S256Field(S256Point.B)
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



G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
)
