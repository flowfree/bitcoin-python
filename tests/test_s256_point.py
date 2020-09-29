import pytest 

from bitcoin.s256_field import FieldElement, S256Field
from bitcoin.s256_point import Point, S256Point
from bitcoin.signature import Signature


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


class TestS256Point:
    def test_verify(self):
        p = S256Point(
            0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c, 
            0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34,
        )
        tests = [
            (0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60,    # z
             0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395,    # r
             0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4),    # s
            (0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d,    # z
             0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c,      # r
             0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6)    # s
        ]
        for z, r, s in tests:
            signature = Signature(r, s)
            assert p.verify(z, signature) == True
