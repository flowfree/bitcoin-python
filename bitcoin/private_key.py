from random import randint 

from .constants import N, G
from .signature import Signature


class PrivateKey(object):
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G

    def __str__(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = randint(0, N)
        r = (k * G).x.num
        k_inv = pow(k, N-2, N)
        s = (z + r * self.secret) * k_inv % N
        if s > N/2:
            s = N - s
        return Signature(r, s)
