import pytest
from bitcoin import FieldElement


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
