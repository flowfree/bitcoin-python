import pytest 

from bitcoin import helpers
from bitcoin.op import *


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


class TestOpIf:
    def test_one(self):
        stack = [encode_num(1)]
        commands = [OP_IF, OP_2, OP_ENDIF, OP_3]
        _ = commands.pop(0)

        assert op_if(stack, commands) == True
        assert stack == []
        assert commands == [OP_2, OP_3]

    def test_two(self):
        stack = [encode_num(1)]
        commands = [OP_IF, OP_2, OP_ELSE, OP_3, OP_ENDIF, OP_4]
        _ = commands.pop(0)

        assert op_if(stack, commands) == True
        assert stack == []
        assert commands == [OP_2, OP_4]

    def test_three(self):
        stack = [encode_num(0)]
        commands = [OP_IF, OP_2, OP_ELSE, OP_3, OP_ENDIF, OP_4]
        _ = commands.pop(0)

        assert op_if(stack, commands) == True
        assert stack == []
        assert commands == [OP_3, OP_4]

    def test_four(self):
        stack = [
            encode_num(0), 
            encode_num(1),
        ]
        commands = [
            OP_IF,
                OP_2,
            OP_ELSE,
                OP_3,
                OP_IF,
                    OP_4,
                OP_ELSE,
                    OP_5,
                OP_ENDIF,
            OP_ENDIF,
            OP_6,
        ]
        _ = commands.pop(0)

        assert op_if(stack, commands) == True
        assert stack == [encode_num(0)]
        assert commands == [
            OP_2, 
            OP_6,
        ]

    def test_five(self):
        stack = [
            encode_num(1), 
            encode_num(0),
        ]
        commands = [
            OP_IF,
                OP_2,
            OP_ELSE,
                OP_3,
                OP_IF,
                    OP_4,
                OP_ELSE,
                    OP_5,
                OP_ENDIF,
            OP_ENDIF,
            OP_6,
        ]
        _ = commands.pop(0)

        assert op_if(stack, commands) == True
        assert stack == [encode_num(1)]
        assert commands == [
            OP_3,
            OP_IF,
                OP_4,
            OP_ELSE,
                OP_5,
            OP_ENDIF,
            OP_6,
        ]

    def test_six(self):
        stack = [
            encode_num(0), 
            encode_num(1),
        ]
        commands = [
            OP_IF,
                OP_10,
                OP_IF,
                    OP_11,
                OP_ELSE,
                    OP_12,
                OP_ENDIF,
            OP_ELSE,
                OP_13,
            OP_ENDIF,
            OP_14,
        ]
        _ = commands.pop(0)

        assert op_if(stack, commands) == True
        assert stack == [encode_num(0)]
        assert commands == [
            OP_10,
            OP_IF,
                OP_11,
            OP_ELSE,
                OP_12,
            OP_ENDIF,
            OP_14,
        ]

    def test_invalid_stack(self):
        stack = []
        commands = [OP_IF, OP_1, OP_ENDIF]
        _ = commands.pop(0)

        assert op_if(stack, commands) == False

    def test_invalid_script(self):
        stack = [encode_num(1)]
        tests = [
            [OP_IF, OP_1, OP_2],
            [OP_IF, OP_IF, OP_1, OP_ENDIF],
            [OP_IF, OP_1, OP_IF, OP_2, OP_ELSE, OP_ENDIF],
        ]
        for test in tests:
            _ = test.pop(0)
            assert op_if(stack, test) == False


class TestOpNotIf:
    def test_one(self):
        stack = [encode_num(0)]
        commands = [OP_NOTIF, OP_2, OP_ENDIF, OP_3]
        _ = commands.pop(0)

        assert op_notif(stack, commands) == True
        assert stack == []
        assert commands == [OP_2, OP_3]

    def test_two(self):
        stack = [encode_num(1)]
        commands = [OP_NOTIF, OP_2, OP_ENDIF, OP_3]
        _ = commands.pop(0)

        assert op_notif(stack, commands) == True
        assert stack == []
        assert commands == [OP_3]

    def test_three(self):
        stack = [encode_num(1)]
        commands = [
            OP_NOTIF, 
                OP_2, 
            OP_ELSE, 
                OP_IF, 
                    OP_3, 
                OP_ENDIF, 
            OP_ENDIF, 
            OP_4,
        ]
        _ = commands.pop(0)

        assert op_notif(stack, commands) == True
        assert stack == []
        assert commands == [
            OP_IF, 
                OP_3, 
            OP_ENDIF, 
            OP_4,
        ]


def test_op_verify():
    stack = [encode_num(1)]
    assert op_verify(stack) == True

    stack = [encode_num(0)]
    assert op_verify(stack) == False
