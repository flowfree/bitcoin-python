import pytest 

from bitcoin.helpers import (
    decode_num, encode_num, hash160, hash256, 
)
from bitcoin.op import *


# VALUE-PUSHING TESTS
# -------------------------------------------------------------------------


def test_op_0():
    stack = []
    assert op_0(stack=stack) == True
    assert stack == [encode_num(0)]


def test_op_1():
    stack = []
    assert op_1(stack=stack) == True
    assert stack == [encode_num(1)]


def test_op_2():
    stack = []
    assert op_2(stack=stack) == True
    assert stack == [encode_num(2)]


def test_op_3():
    stack = []
    assert op_3(stack=stack) == True
    assert stack == [encode_num(3)]


def test_op_4():
    stack = []
    assert op_4(stack=stack) == True
    assert stack == [encode_num(4)]


def test_op_5():
    stack = []
    assert op_5(stack=stack) == True
    assert stack == [encode_num(5)]


def test_op_6():
    stack = []
    assert op_6(stack=stack) == True
    assert stack == [encode_num(6)]


def test_op_7():
    stack = []
    assert op_7(stack=stack) == True
    assert stack == [encode_num(7)]


def test_op_8():
    stack = []
    assert op_8(stack=stack) == True
    assert stack == [encode_num(8)]


def test_op_9():
    stack = []
    assert op_9(stack=stack) == True
    assert stack == [encode_num(9)]


def test_op_10():
    stack = []
    assert op_10(stack=stack) == True
    assert stack == [encode_num(10)]


def test_op_11():
    stack = []
    assert op_11(stack=stack) == True
    assert stack == [encode_num(11)]


def test_op_12():
    stack = []
    assert op_12(stack=stack) == True
    assert stack == [encode_num(12)]


def test_op_13():
    stack = []
    assert op_13(stack=stack) == True
    assert stack == [encode_num(13)]


def test_op_14():
    stack = []
    assert op_14(stack=stack) == True
    assert stack == [encode_num(14)]


def test_op_15():
    stack = []
    assert op_15(stack=stack) == True
    assert stack == [encode_num(15)]


def test_op_16():
    stack = []
    assert op_16(stack=stack) == True
    assert stack == [encode_num(16)]


def test_op_1negate():
    stack = []
    assert op_1negate(stack=stack) == True
    assert stack == [encode_num(-1)]


# FLOW CONTROL TESTS
# ---------------------------------------------------------


class TestOpIf:
    def test_one(self):
        stack = [encode_num(1)]
        commands = [
            OP_IF, 
                OP_2, 
            OP_ENDIF, 
            OP_3,
        ]
        _ = commands.pop(0)

        assert op_if(stack=stack, commands=commands) == True
        assert stack == []
        assert commands == [OP_2, OP_3]

    def test_two(self):
        stack = [encode_num(1)]
        commands = [
            OP_IF, 
                OP_2, 
            OP_ELSE, 
                OP_3, 
            OP_ENDIF, 
            OP_4,
        ]
        _ = commands.pop(0)

        assert op_if(stack=stack, commands=commands) == True
        assert stack == []
        assert commands == [OP_2, OP_4]

    def test_three(self):
        stack = [encode_num(0)]
        commands = [
            OP_IF, 
                OP_2, 
            OP_ELSE, 
                OP_3, 
            OP_ENDIF, 
            OP_4,
        ]
        _ = commands.pop(0)

        assert op_if(stack=stack, commands=commands) == True
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

        assert op_if(stack=stack, commands=commands) == True
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

        assert op_if(stack=stack, commands=commands) == True
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

        assert op_if(stack=stack, commands=commands) == True
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
        commands = [
            OP_IF, 
                OP_1, 
            OP_ENDIF,
        ]
        _ = commands.pop(0)

        assert op_if(stack=stack, commands=commands) == False

    def test_invalid_script(self):
        stack = [encode_num(1)]
        tests = [
            [OP_IF, OP_1, OP_2],
            [OP_IF, OP_IF, OP_1, OP_ENDIF],
            [OP_IF, OP_1, OP_IF, OP_2, OP_ELSE, OP_ENDIF],
        ]
        for test in tests:
            _ = test.pop(0)
            assert op_if(stack=stack, commands=test) == False


class TestOpNotIf:
    def test_one(self):
        stack = [encode_num(0)]
        commands = [
            OP_NOTIF, 
                OP_2, 
            OP_ENDIF, 
            OP_3,
        ]
        _ = commands.pop(0)

        assert op_notif(stack=stack, commands=commands) == True
        assert stack == []
        assert commands == [OP_2, OP_3]

    def test_two(self):
        stack = [encode_num(1)]
        commands = [
            OP_NOTIF, 
                OP_2, 
            OP_ENDIF, 
            OP_3,
        ]
        _ = commands.pop(0)

        assert op_notif(stack=stack, commands=commands) == True
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

        assert op_notif(stack=stack, commands=commands) == True
        assert stack == []
        assert commands == [
            OP_IF, 
                OP_3, 
            OP_ENDIF, 
            OP_4,
        ]


def test_op_verify():
    stack = [encode_num(1)]
    assert op_verify(stack=stack) == True

    stack = [encode_num(0)]
    assert op_verify(stack=stack) == False


# STACK FUNCTIONS TESTS
# ----------------------------------------------------------------------------


def test_op_toaltstack():
    stack = [encode_num(1), encode_num(2)]
    altstack = []

    op_toaltstack(stack=stack, altstack=altstack)

    assert stack == [encode_num(1)]
    assert altstack == [encode_num(2)]


def test_op_fromaltstack():
    stack = [encode_num(1)]
    altstack = [encode_num(2), encode_num(3)]

    op_fromaltstack(stack=stack, altstack=altstack)

    assert stack == [encode_num(1), encode_num(3)]
    assert altstack == [encode_num(2)]


def test_op_ifdup():
    stack = [encode_num(0)]
    op_ifdup(stack=stack)
    assert stack == [encode_num(0)]

    stack = [encode_num(1)]
    op_ifdup(stack=stack)
    assert stack == [encode_num(1), encode_num(1)]


def test_depth():
    stack = []
    op_depth(stack=stack)
    assert stack == [encode_num(0)]

    stack = [
        encode_num(10), 
        encode_num(20),
    ]
    op_depth(stack=stack)
    assert stack == [
        encode_num(10),
        encode_num(20),
        encode_num(2),
    ]


def test_drop():
    with pytest.raises(ValueError):
        stack = []
        op_drop(stack=stack)

    stack = [encode_num(1), encode_num(2)]
    op_drop(stack=stack)
    assert stack == [encode_num(1)]


def test_op_dup():
    with pytest.raises(ValueError):
        stack = []
        op_dup(stack=stack)

    stack = [0x0001]
    op_dup(stack=stack)
    assert stack == [0x0001, 0x0001]


def test_op_nip():
    with pytest.raises(ValueError):
        stack = [0x0001]
        op_nip(stack=stack)

    stack = [0x0001, 0x0002]
    op_nip(stack=stack)
    assert stack == [0x0002]


def test_op_over():
    with pytest.raises(ValueError):
        stack = [0x0001]
        op_over(stack=stack)

    stack = [0x0001, 0x0002, 0x0003]
    op_over(stack=stack)
    assert stack == [0x0001, 0x0002, 0x0003, 0x0002]


def test_op_rot():
    with pytest.raises(ValueError):
        stack = [0x0001, 0x0002]
        op_rot(stack=stack)

    stack = [0x0001, 0x0002, 0x0003]
    op_rot(stack=stack)
    assert stack == [0x0002, 0x0003, 0x0001]


def test_op_swap():
    with pytest.raises(ValueError):
        stack = [0x0001]
        op_swap(stack=stack)

    stack = [0x0001, 0x0002]
    op_swap(stack=stack)
    assert stack == [0x0002, 0x0001]


def test_op_tuck():
    with pytest.raises(ValueError):
        stack = [0x01]
        op_tuck(stack=stack)

    stack = [0x01, 0x02]
    op_tuck(stack=stack)
    assert stack == [0x02, 0x01, 0x02]

    stack = [0x01, 0x02, 0x03]
    op_tuck(stack=stack)
    assert stack == [0x01, 0x03, 0x02, 0x03]

def test_op_2drop():
    with pytest.raises(ValueError):
        stack = [0x01]
        op_2drop(stack=stack)

    stack = [0x01, 0x02]
    op_2drop(stack=stack)
    assert stack == []

    stack = [0x01, 0x02, 0x03]
    op_2drop(stack=stack)
    assert stack == [0x01]


def test_op_2dup():
    with pytest.raises(ValueError):
        stack = [0x01]
        op_2dup(stack=stack)

    stack = [0x01, 0x02]
    op_2dup(stack=stack)
    assert stack == [0x01, 0x02, 0x01, 0x02]


def test_op_3dup():
    with pytest.raises(ValueError):
        stack = [0x01, 0x02]
        op_3dup(stack=stack)

    stack = [0x01, 0x02, 0x03]
    op_3dup(stack=stack)
    assert stack == [0x01, 0x02, 0x03, 0x01, 0x02, 0x03]


def test_op_2over():
    with pytest.raises(ValueError):
        stack = [0x01, 0x02, 0x03]
        op_2over(stack=stack)

    stack = [0x01, 0x02, 0x03, 0x04]
    op_2over(stack=stack)
    assert stack == [0x01, 0x02, 0x03, 0x04, 0x01, 0x02]


def test_op_2rot():
    with pytest.raises(ValueError):
        stack = [0x01, 0x02, 0x03, 0x04, 0x05]
        op_2rot(stack=stack)

    stack = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
    op_2rot(stack=stack)
    assert stack == [0x03, 0x04, 0x05, 0x06, 0x01, 0x02]


def test_op_2swap():
    with pytest.raises(ValueError):
        stack = [0x01, 0x02, 0x03]
        op_2swap(stack=stack)

    stack = [0x01, 0x02, 0x03, 0x04]
    op_2swap(stack=stack)
    assert stack == [0x03, 0x04, 0x01, 0x02]


# CRYPTO FUNCTIONS TESTS
# ----------------------------------------------------------------------------


class TestOpHash160:
    def test_stack_is_empty(self):
        stack = []
        assert op_hash160(stack=stack) == False

    def test_operation(self):
        x = bytes.fromhex('0001')
        stack = [x]

        assert op_hash160(stack=stack) == True
        assert stack == [hash160(x)]


class TestOpHash256:
    def test_stack_is_empty(self):
        stack = []
        assert op_hash256(stack=stack) == False

    def test_operation(self):
        x = bytes.fromhex('0001')
        stack = [x]

        assert op_hash256(stack=stack) == True
        assert stack == [hash256(x)]
