import pytest 

from bitcoin.exceptions import (
    InsufficientStackItems, InvalidTransaction, ScriptError
)
from bitcoin.helpers import (
    decode_num, encode_num, hash160, hash256, 
)
from bitcoin.op import *


# VALUE-PUSHING TESTS
# -------------------------------------------------------------------------


def test_op_0():
    stack = []
    op_0(stack=stack)
    assert stack == [encode_num(0)]


def test_op_1():
    stack = []
    op_1(stack=stack)
    assert stack == [encode_num(1)]


def test_op_2():
    stack = []
    op_2(stack=stack)
    assert stack == [encode_num(2)]


def test_op_3():
    stack = []
    op_3(stack=stack)
    assert stack == [encode_num(3)]


def test_op_4():
    stack = []
    op_4(stack=stack)
    assert stack == [encode_num(4)]


def test_op_5():
    stack = []
    op_5(stack=stack)
    assert stack == [encode_num(5)]


def test_op_6():
    stack = []
    op_6(stack=stack)
    assert stack == [encode_num(6)]


def test_op_7():
    stack = []
    op_7(stack=stack)
    assert stack == [encode_num(7)]


def test_op_8():
    stack = []
    op_8(stack=stack)
    assert stack == [encode_num(8)]


def test_op_9():
    stack = []
    op_9(stack=stack)
    assert stack == [encode_num(9)]


def test_op_10():
    stack = []
    op_10(stack=stack)
    assert stack == [encode_num(10)]


def test_op_11():
    stack = []
    op_11(stack=stack)
    assert stack == [encode_num(11)]


def test_op_12():
    stack = []
    op_12(stack=stack)
    assert stack == [encode_num(12)]


def test_op_13():
    stack = []
    op_13(stack=stack)
    assert stack == [encode_num(13)]


def test_op_14():
    stack = []
    op_14(stack=stack)
    assert stack == [encode_num(14)]


def test_op_15():
    stack = []
    op_15(stack=stack)
    assert stack == [encode_num(15)]


def test_op_16():
    stack = []
    op_16(stack=stack)
    assert stack == [encode_num(16)]


def test_op_1negate():
    stack = []
    op_1negate(stack=stack)
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

        op_if(stack=stack, commands=commands)

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

        op_if(stack=stack, commands=commands)

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

        op_if(stack=stack, commands=commands)

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

        op_if(stack=stack, commands=commands)

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

        op_if(stack=stack, commands=commands)

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

        op_if(stack=stack, commands=commands)

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

        with pytest.raises(ScriptError):
            op_if(stack=stack, commands=commands)

    def test_invalid_script(self):
        stack = [encode_num(1)]
        tests = [
            [OP_IF, OP_1, OP_2],
            [OP_IF, OP_IF, OP_1, OP_ENDIF],
            [OP_IF, OP_1, OP_IF, OP_2, OP_ELSE, OP_ENDIF],
        ]
        for test in tests:
            with pytest.raises(ScriptError) as e:
                _ = test.pop(0)
                op_if(stack=stack, commands=test)
            assert str(e.value) == 'Failed parsing the script.'


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

        op_notif(stack=stack, commands=commands)

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

        op_notif(stack=stack, commands=commands)

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

        op_notif(stack=stack, commands=commands)

        assert stack == []
        assert commands == [
            OP_IF, 
                OP_3, 
            OP_ENDIF, 
            OP_4,
        ]


def test_op_verify():
    stack = [encode_num(1)]
    op_verify(stack=stack)

    with pytest.raises(InvalidTransaction):
        stack = [encode_num(0)]
        op_verify(stack=stack)


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
    with pytest.raises(InsufficientStackItems):
        stack = []
        op_drop(stack=stack)

    stack = [encode_num(1), encode_num(2)]
    op_drop(stack=stack)
    assert stack == [encode_num(1)]


def test_op_dup():
    with pytest.raises(InsufficientStackItems):
        stack = []
        op_dup(stack=stack)

    stack = [0x0001]
    op_dup(stack=stack)
    assert stack == [0x0001, 0x0001]


def test_op_nip():
    with pytest.raises(InsufficientStackItems):
        stack = [0x0001]
        op_nip(stack=stack)

    stack = [0x0001, 0x0002]
    op_nip(stack=stack)
    assert stack == [0x0002]


def test_op_over():
    with pytest.raises(InsufficientStackItems):
        stack = [0x0001]
        op_over(stack=stack)

    stack = [0x0001, 0x0002, 0x0003]
    op_over(stack=stack)
    assert stack == [0x0001, 0x0002, 0x0003, 0x0002]


def test_op_rot():
    with pytest.raises(InsufficientStackItems):
        stack = [0x0001, 0x0002]
        op_rot(stack=stack)

    stack = [0x0001, 0x0002, 0x0003]
    op_rot(stack=stack)
    assert stack == [0x0002, 0x0003, 0x0001]


def test_op_swap():
    with pytest.raises(InsufficientStackItems):
        stack = [0x0001]
        op_swap(stack=stack)

    stack = [0x0001, 0x0002]
    op_swap(stack=stack)
    assert stack == [0x0002, 0x0001]


def test_op_tuck():
    with pytest.raises(InsufficientStackItems):
        stack = [0x01]
        op_tuck(stack=stack)

    stack = [0x01, 0x02]
    op_tuck(stack=stack)
    assert stack == [0x02, 0x01, 0x02]

    stack = [0x01, 0x02, 0x03]
    op_tuck(stack=stack)
    assert stack == [0x01, 0x03, 0x02, 0x03]

def test_op_2drop():
    with pytest.raises(InsufficientStackItems):
        stack = [0x01]
        op_2drop(stack=stack)

    stack = [0x01, 0x02]
    op_2drop(stack=stack)
    assert stack == []

    stack = [0x01, 0x02, 0x03]
    op_2drop(stack=stack)
    assert stack == [0x01]


def test_op_2dup():
    with pytest.raises(InsufficientStackItems):
        stack = [0x01]
        op_2dup(stack=stack)

    stack = [0x01, 0x02]
    op_2dup(stack=stack)
    assert stack == [0x01, 0x02, 0x01, 0x02]


def test_op_3dup():
    with pytest.raises(InsufficientStackItems):
        stack = [0x01, 0x02]
        op_3dup(stack=stack)

    stack = [0x01, 0x02, 0x03]
    op_3dup(stack=stack)
    assert stack == [0x01, 0x02, 0x03, 0x01, 0x02, 0x03]


def test_op_2over():
    with pytest.raises(InsufficientStackItems):
        stack = [0x01, 0x02, 0x03]
        op_2over(stack=stack)

    stack = [0x01, 0x02, 0x03, 0x04]
    op_2over(stack=stack)
    assert stack == [0x01, 0x02, 0x03, 0x04, 0x01, 0x02]


def test_op_2rot():
    with pytest.raises(InsufficientStackItems):
        stack = [0x01, 0x02, 0x03, 0x04, 0x05]
        op_2rot(stack=stack)

    stack = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
    op_2rot(stack=stack)
    assert stack == [0x03, 0x04, 0x05, 0x06, 0x01, 0x02]


def test_op_2swap():
    with pytest.raises(InsufficientStackItems):
        stack = [0x01, 0x02, 0x03]
        op_2swap(stack=stack)

    stack = [0x01, 0x02, 0x03, 0x04]
    op_2swap(stack=stack)
    assert stack == [0x03, 0x04, 0x01, 0x02]


# BITWISE-LOGIC TESTS
# ----------------------------------------------------------------------------


def test_op_equal():
    with pytest.raises(InsufficientStackItems):
        stack = [0x09]
        op_equal(stack=stack)

    stack = [0x09, 0x08] 
    op_equal(stack=stack)
    assert stack == [encode_num(0)]

    stack = [0x09, 0x09] 
    op_equal(stack=stack)
    assert stack == [encode_num(1)]


def test_op_equalverify():
    with pytest.raises(InsufficientStackItems):
        stack = [0x09]
        op_equalverify(stack=stack)

    with pytest.raises(InvalidTransaction):
        stack = [0x09, 0x08] 
        op_equalverify(stack=stack)

    stack = [0x09, 0x09] 
    op_equalverify(stack=stack)


# CRYPTO FUNCTIONS TESTS
# ----------------------------------------------------------------------------


def test_op_hash160():
    with pytest.raises(InsufficientStackItems):
        stack = []
        op_hash160(stack=stack)

    x = bytes.fromhex('0001')
    stack = [x]
    op_hash160(stack=stack)
    assert stack == [hash160(x)]


def test_op_hash256():
    with pytest.raises(InsufficientStackItems):
        stack = []
        op_hash256(stack=stack)

    x = bytes.fromhex('0001')
    stack = [x]
    op_hash256(stack=stack)
    assert stack == [hash256(x)]
