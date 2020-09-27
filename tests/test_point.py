import pytest 

from bitcoin import FieldElement, Point


class TestPointWithRealNumbers:
    def test_initialization(self):
        with pytest.raises(ValueError) as e:
            _ = Point(3, 10, 5, 7)
        assert str(e.value) == '(3, 10) is not on the curve.'

        p1 = Point(-1, -1, 5, 7)
        assert str(p1) == 'Point(-1,-1)_5_7'

    def test_equality(self):
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(-1, -1, 5, 7)
        assert p1 == p2

    def test_inequality(self):
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(18, 77, 5, 7)
        assert p1 != p2

    def test_addition(self):
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

    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        valid_points = [(192, 105), (17, 56), (1, 193)]
        for x_, y_ in valid_points:
            x = FieldElement(x_, prime)
            y = FieldElement(y_, prime)
            _ = Point(x, y, a, b)

        invalid_points = [(200, 119), (42, 99)]
        for x_, y_ in invalid_points:
            x = FieldElement(x_, prime)
            y = FieldElement(y_, prime)
            with pytest.raises(ValueError) as e:
                _ = Point(x, y, a, b)

    def test_addition(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x1 = FieldElement(192, prime)
        y1 = FieldElement(105, prime)
        x2 = FieldElement(17, prime)
        y2 = FieldElement(56, prime)
        p1 = Point(x1, y1, a, b)
        p2 = Point(x2, y2, a, b)

        assert p1+p2 == Point(
            FieldElement(170, prime),
            FieldElement(142, prime),
            a, b
        )

        tests = [
            (192, 105, 17, 56, 170, 142),
            (170, 142, 60, 139, 220, 181),
            (47, 71, 17, 56, 215, 68),
            (143, 98, 76, 66, 47, 71),
        ]
        for x1_, y1_, x2_, y2_, x3_, y3_ in tests:
            x1 = FieldElement(x1_, prime)
            y1 = FieldElement(y1_, prime)
            x2 = FieldElement(x2_, prime)
            y2 = FieldElement(y2_, prime)
            x3 = FieldElement(x3_, prime)
            y3 = FieldElement(y3_, prime)
            p1 = Point(x1, y1, a, b)
            p2 = Point(x2, y2, a, b)
            p3 = Point(x3, y3, a, b)

            assert p1+p2 == p3

    def test_addition_for_the_same_points(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        p = Point(x, y, a, b)

        assert p+p == Point(
            FieldElement(36, prime),
            FieldElement(111, prime),
            a, b
        )

    def test_scalar_multiplication(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)

        assert 6*p == Point(
            FieldElement(15, prime),
            FieldElement(137, prime),
            a, b
        )
        assert 7*p == Point(None, None, a, b)
