from . import A, B, N
from .point import Point
from .s256field import S256Field


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
            return f'S256Point({hex(self.x.num)}, {hex(self.y.num)})'

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)

    def verify(self, z, sig):
        s_inv = pow(sig.s, N-2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N 
        point = (u * G) + (v * self)
        return point.x.num == sig.r


G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
)
