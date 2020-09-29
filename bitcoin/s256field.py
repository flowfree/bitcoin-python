class FieldElement(object):
    """
    Represents a number in a finite field.

    Attributes
    ----------
    num : int
        The finite field element.
    prime : int
        The size of the finite field.
    """

    def __init__(self, num, prime):
        if num >= prime or num < 0:
            raise ValueError(f'Num {num} not in field range 0 to {prime}')
        self.num = num
        self.prime = prime

    def __str__(self):
        class_name = self.__class__.__name__
        return f'{class_name}_{self.prime}({self.num})'

    def __eq__(self, other):
        if other is None:
            return False
        return self.prime == other.prime and self.num == other.num

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError(f'Cannot add two numbers in different fields.')
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError(f'Cannot substract two numbers in different fields.')
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError(f'Cannot multiply two numbers in different fields.')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __rmul__(self, other):
        if type(other) == int:
            other = self.__class__(other, self.prime)
        return other * self

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError(f'Cannot divide two numbers in different fields.')
        num = self * (other ** (self.prime - 2))
        return num



class S256Field(FieldElement):
    P = 2**256 - 2**32 - 977

    def __init__(self, num, *args, **kwargs):
        super().__init__(num, self.P)

    def __str__(self):
        return '{:x}'.format(self.num).zfill(64)
