import pytest 

from bitcoin import helpers
from bitcoin.op import (
    decode_num, encode_num,
    op_0, op_1, op_2, op_3, op_4, op_5, op_6, op_7, op_8,
    op_9, op_10, op_11, op_12, op_13, op_14, op_15, op_16,
    op_dup, op_hash160, op_hash256
)


def test_decode_num():
    tests = [
        (b'', 0),
        (b'\x01', 1),
        (b'\x02', 2),
        (b'\x0a', 10),
        (b'\x10', 16),
        (b'\x81', -1),
        (b'\x8d', -13),
    ]
    for x, y in tests:
        assert decode_num(x) == y


def test_encode_num():
    tests = [
        (0, b''),
        (1, b'\x01'),
        (2, b'\x02'),
        (10, b'\x0a'),
        (16, b'\x10'),
        (-1, b'\x81'),
        (-13, b'\x8d'),
    ]
    for x, y in tests:
        assert encode_num(x) == y


def test_op_0():
    stack = []
    assert op_0(stack) == True
    assert stack == [encode_num(0)]


def test_op_1():
    stack = []
    assert op_1(stack) == True
    assert stack == [encode_num(1)]


def test_op_2():
    stack = []
    assert op_2(stack) == True
    assert stack == [encode_num(2)]


def test_op_3():
    stack = []
    assert op_3(stack) == True
    assert stack == [encode_num(3)]


def test_op_4():
    stack = []
    assert op_4(stack) == True
    assert stack == [encode_num(4)]


def test_op_5():
    stack = []
    assert op_5(stack) == True
    assert stack == [encode_num(5)]


def test_op_6():
    stack = []
    assert op_6(stack) == True
    assert stack == [encode_num(6)]


def test_op_7():
    stack = []
    assert op_7(stack) == True
    assert stack == [encode_num(7)]


def test_op_8():
    stack = []
    assert op_8(stack) == True
    assert stack == [encode_num(8)]


def test_op_9():
    stack = []
    assert op_9(stack) == True
    assert stack == [encode_num(9)]


def test_op_10():
    stack = []
    assert op_10(stack) == True
    assert stack == [encode_num(10)]


def test_op_11():
    stack = []
    assert op_11(stack) == True
    assert stack == [encode_num(11)]


def test_op_12():
    stack = []
    assert op_12(stack) == True
    assert stack == [encode_num(12)]


def test_op_13():
    stack = []
    assert op_13(stack) == True
    assert stack == [encode_num(13)]


def test_op_14():
    stack = []
    assert op_14(stack) == True
    assert stack == [encode_num(14)]


def test_op_15():
    stack = []
    assert op_15(stack) == True
    assert stack == [encode_num(15)]


def test_op_16():
    stack = []
    assert op_16(stack) == True
    assert stack == [encode_num(16)]


class TestOpDup:
    def test_stack_is_empty(self):
        stack = []
        assert op_dup(stack) == False

    def test_operation(self):
        stack = [0x0001]
        status = op_dup(stack)

        assert stack == [0x0001, 0x0001]
        assert status == True


class TestOpHash160:
    def test_stack_is_empty(self):
        stack = []
        assert op_hash160(stack) == False

    def test_operation(self):
        x = bytes.fromhex('0001')
        stack = [x]

        assert op_hash160(stack) == True
        assert stack == [helpers.hash160(x)]


class TestOpHash256:
    def test_stack_is_empty(self):
        stack = []
        assert op_hash256(stack) == False

    def test_operation(self):
        x = bytes.fromhex('0001')
        stack = [x]

        assert op_hash256(stack) == True
        assert stack == [helpers.hash256(x)]
