from . import P
from .field_element import FieldElement


class S256Field(FieldElement):
    def __init__(self, num, *args, **kwargs):
        super().__init__(num, P)

    def __str__(self):
        return '{:x}'.format(self.num).zfill(64)
