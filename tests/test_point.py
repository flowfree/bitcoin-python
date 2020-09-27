import pytest 

from bitcoin import Point


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
