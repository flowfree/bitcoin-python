from bitcoin import FieldElement


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
    def is_infinity(self):
        return self.x is None and self.y is None

    @property
    def is_finite(self):
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
        if self.is_finite:
            return f'{class_name}({self.x.num},{self.y.num})_{self.a.num}_{self.b.num} ' \
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

        if self.is_infinity:
            return other
        elif other.is_infinity:
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
