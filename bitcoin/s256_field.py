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



class S256Field(FieldElement):
    P = 2**256 - 2**32 - 977

    def __init__(self, val, *args, **kwargs):
        super().__init__(val, self.P)

    def __str__(self):
        return '{:x}'.format(self.val).zfill(64)

    def sqrt(self):
        return self**((self.P + 1) // 4)
