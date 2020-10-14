import pytest

from bitcoin.ecc import (
    G, FieldElement, Point, PrivateKey, S256Field, S256Point, Signature
)
from bitcoin.exceptions import BadSignature


class TestFieldElement:
    def test_equal_elements(self):
        a = FieldElement(7, 13)
        b = FieldElement(7, 13)
        assert a == b

    def test_not_equal_elements(self):
        a = FieldElement(7, 13)
        b = FieldElement(8, 13)
        assert a != b

    def test_addition_error(self):
        with pytest.raises(TypeError) as e:
            a = FieldElement(7, 19)
            b = FieldElement(8, 23)
            c = a+b
        assert str(e.value) == 'Cannot add two numbers in different fields.'

    def test_addition(self):
        tests = [
            (19, 7, 8, 15),
            (23, 20, 5, 2),
            (31, 3, 17, 20),
        ]
        for prime, x, y, z in tests:
            a = FieldElement(x, prime)
            b = FieldElement(y, prime)
            c = FieldElement(z, prime)
            assert a+b == c

    def test_substraction_error(self):
        with pytest.raises(TypeError) as e:
            a = FieldElement(20, 31)
            b = FieldElement(3, 29)
            c = a-b
        assert str(e.value) == 'Cannot substract two numbers in different fields.'

    def test_substraction(self):
        tests = [
            (19, 15, 7, 8),
            (23, 2, 20, 5),
            (31, 20, 3, 17),
        ]
        for prime, x, y, z in tests:
            a = FieldElement(x, prime)
            b = FieldElement(y, prime)
            c = FieldElement(z, prime)
            assert a-b == c

    def test_multiplication_error(self):
        with pytest.raises(TypeError) as e:
            a = FieldElement(2, 7)
            b = FieldElement(3, 11)
            c = a*b
        assert str(e.value) == 'Cannot multiply two numbers in different fields.'

    def test_multiplications(self):
        tests = [
            (17, 10, 3, 13),
            (17, 3, 16, 14),
            (17, 15, 15, 4),
            (19, 2, 3, 6),
            (19, 7, 9, 6),
            (19, 12, 17, 14),
            (23, 21, 22, 2),
        ]
        for prime, x, y, z in tests:
            a = FieldElement(x, prime)
            b = FieldElement(y, prime)
            c = FieldElement(z, prime)
            assert a*b == c

    def test_exponentiations(self):
        tests = [
            (13, 3, 3, 1),
            (13, 4, 5, 10),
            (13, 2, 7, 11),
            (17, 15, 7, 8),
            (17, 13, 15, 4),
            (13, 7, -3, 8),
        ]
        for prime, x, exp, y in tests:
            a = FieldElement(x, prime)
            b = FieldElement(y, prime)
            assert a**exp == b

    def test_divisions(self):
        tests = [
            (19, 2, 7, 3),
            (19, 7, 5, 9),
            (19, 10, 5, 2),
            (21, 3, 7, 0),
            (21, 2, 14, 7),
        ]
        for p, x, y, z in tests:
            a = FieldElement(x, p)
            b = FieldElement(y, p)
            c = FieldElement(z, p)
            assert a/b == c


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

    def test_serialize_uncompressed_sec(self):
        tests = [
            S256Point(
                0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c, 
                0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34,
            ),
            S256Point(
                0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 
                0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
            )
        ]
        for p0 in tests:
            serialized = p0.sec()
            p1 = S256Point.parse(serialized)
            assert p0 == p1

    def test_address(self):
        e = 5002
        pub = e * G
        assert pub.address(compressed=False, testnet=True) == 'mmTPbXQFxboEtNRkwfh6K51jvdtHLxGeMA'

        e = 2020**5
        pub = e * G
        assert pub.address(compressed=True, testnet=True) == 'mopVkxp8UhXqRYbCYJsbeE1h1fiF64jcoH'

        e = 0x12345deadbeef
        pub = e * G
        assert pub.address(compressed=True, testnet=False) == '1F1Pn2y6pDb68E5nYJJeba4TLg2U7B6KF1'


class TestSignature:
    def test_der(self):
        signature = Signature(
            0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,
            0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        )

        assert signature.der().hex() == \
            '3045022037206a0610995c58074999cb9767b87af4c4978db68c0' \
            '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
            '119fc9a75bf8e6d0fa65c841c8e2738cdaec'

    def test_parse(self):
        signature_bin = bytes.fromhex(
            '3045022037206a0610995c58074999cb9767b87af4c4978db68c0' \
            '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
            '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
        )

        signature = Signature.parse(signature_bin)

        assert signature == Signature(
            0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,
            0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        )

    def test_parse_bad_signatures(self):
        tests = [
            bytes.fromhex(
                '0345022037206a0610995c58074999cb9767b87af4c4978db68c0' \
                '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
                '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
            ),
            bytes.fromhex(
                '3045202037206a0610995c58074999cb9767b87af4c4978db68c0' \
                '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
                '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
            ),
            bytes.fromhex(
                '30450220ff37206a0610995c58074999cb9767b87af4c4978db68c0' \
                '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
                '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
            ),
            bytes.fromhex(
                '3045022037206a0610995c58074999cb9767b87af4c4978db68c0' \
                '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
                '119fc9a75bf8e6d0fa65c841c8e2738cdaecab'
            ),
            bytes.fromhex(
                '3045022037206a0610995c58074999cb9767b87af4c4978db68c0' \
                '6e8e6e81d282047a7c60321008ca63759c1157ebeaec0d03cecca' \
                '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
            ),
        ]

        for test in tests:
            with pytest.raises(BadSignature):
                Signature.parse(test)


class TestPrivateKey:
    def test_wif(self):
        private_key = PrivateKey(5003)
        assert private_key.wif(compressed=True, testnet=True) == \
            'cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMN8rFTv2sfUK'

        private_key = PrivateKey(2021**5)
        assert private_key.wif(compressed=False, testnet=True) == \
            '91avARGdfge8E4tZfYLoxeJ5sGBdNJQH4kvjpWAxgzczjbCwxic'

        private_key = PrivateKey(0x54321deadbeef)
        assert private_key.wif(compressed=True, testnet=False) == \
            'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgiuQJv1h8Ytr2S53a'
