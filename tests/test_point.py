import pytest 

from bitcoin import FieldElement, Point


def test_initialization():
    with pytest.raises(ValueError) as e:
        _ = Point(3, 10, 5, 7)
    assert str(e.value) == '(3, 10) is not on the curve.'

    p1 = Point(-1, -1, 5, 7)
    assert str(p1) == 'Point(-1,-1)_5_7'


def test_equality():
    p1 = Point(-1, -1, 5, 7)
    p2 = Point(-1, -1, 5, 7)
    assert p1 == p2


def test_inequality():
    p1 = Point(-1, -1, 5, 7)
    p2 = Point(18, 77, 5, 7)
    assert p1 != p2


def test_addition():
    p1 = Point(-1, -1, 5, 7)
    p2 = Point(-1, 1, 5, 7)
    inf = Point(None, None, 5, 7)

    assert p1+inf == p1
    assert p2+inf == p2
    assert p1+p2 == inf

    p1 = Point(-1, -1, 5, 7)
    p2 = Point(2, 5, 5, 7)
    p3 = Point(3, -7, 5, 7)
    assert p1+p2 == p3

    p1 = Point(-1, -1, 5, 7)
    p2 = Point(18, 77, 5, 7)
    assert p1+p1 == p2


class TestPointWithFieldElement:
    def test_initialization(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(192, prime)
        y = FieldElement(105, prime)

        p1 = Point(x, y, a, b)
        assert str(p1) == 'Point(192,105)_0_7 FieldElement(223)'
