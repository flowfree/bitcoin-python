import pytest

from bitcoin.field_element import FieldElement


def test_equal_elements():
    a = FieldElement(7, 13)
    b = FieldElement(7, 13)
    assert a == b


def test_not_equal_elements():
    a = FieldElement(7, 13)
    b = FieldElement(8, 13)
    assert a != b


def test_addition_error():
    with pytest.raises(TypeError) as e:
        a = FieldElement(7, 19)
        b = FieldElement(8, 23)
        c = a+b
    assert str(e.value) == 'Cannot add two numbers in different fields.'


def test_addition():
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


def test_substraction_error():
    with pytest.raises(TypeError) as e:
        a = FieldElement(20, 31)
        b = FieldElement(3, 29)
        c = a-b
    assert str(e.value) == 'Cannot substract two numbers in different fields.'


def test_substraction():
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


def test_multiplication_error():
    with pytest.raises(TypeError) as e:
        a = FieldElement(2, 7)
        b = FieldElement(3, 11)
        c = a*b
    assert str(e.value) == 'Cannot multiply two numbers in different fields.'


def test_multiplications():
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


def test_exponentiations():
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


def test_divisions():
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
