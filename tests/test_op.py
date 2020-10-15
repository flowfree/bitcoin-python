import pytest 

from bitcoin.exceptions import (
    BadOpCode, InvalidTransaction, ScriptError, StackError
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
            assert str(e.value) == 'Failed evaluating the script.'


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
    with pytest.raises(StackError):
        stack = []
        op_drop(stack=stack)

    stack = [encode_num(1), encode_num(2)]
    op_drop(stack=stack)
    assert stack == [encode_num(1)]


def test_op_dup():
    with pytest.raises(StackError):
        stack = []
        op_dup(stack=stack)

    stack = [0x0001]
    op_dup(stack=stack)
    assert stack == [0x0001, 0x0001]


def test_op_nip():
    with pytest.raises(StackError):
        stack = [0x0001]
        op_nip(stack=stack)

    stack = [0x0001, 0x0002]
    op_nip(stack=stack)
    assert stack == [0x0002]


def test_op_over():
    with pytest.raises(StackError):
        stack = [0x0001]
        op_over(stack=stack)

    stack = [0x0001, 0x0002, 0x0003]
    op_over(stack=stack)
    assert stack == [0x0001, 0x0002, 0x0003, 0x0002]


def test_op_rot():
    with pytest.raises(StackError):
        stack = [0x0001, 0x0002]
        op_rot(stack=stack)

    stack = [0x0001, 0x0002, 0x0003]
    op_rot(stack=stack)
    assert stack == [0x0002, 0x0003, 0x0001]


def test_op_swap():
    with pytest.raises(StackError):
        stack = [0x0001]
        op_swap(stack=stack)

    stack = [0x0001, 0x0002]
    op_swap(stack=stack)
    assert stack == [0x0002, 0x0001]


def test_op_tuck():
    with pytest.raises(StackError):
        stack = [0x01]
        op_tuck(stack=stack)

    stack = [0x01, 0x02]
    op_tuck(stack=stack)
    assert stack == [0x02, 0x01, 0x02]

    stack = [0x01, 0x02, 0x03]
    op_tuck(stack=stack)
    assert stack == [0x01, 0x03, 0x02, 0x03]

def test_op_2drop():
    with pytest.raises(StackError):
        stack = [0x01]
        op_2drop(stack=stack)

    stack = [0x01, 0x02]
    op_2drop(stack=stack)
    assert stack == []

    stack = [0x01, 0x02, 0x03]
    op_2drop(stack=stack)
    assert stack == [0x01]


def test_op_2dup():
    with pytest.raises(StackError):
        stack = [0x01]
        op_2dup(stack=stack)

    stack = [0x01, 0x02]
    op_2dup(stack=stack)
    assert stack == [0x01, 0x02, 0x01, 0x02]


def test_op_3dup():
    with pytest.raises(StackError):
        stack = [0x01, 0x02]
        op_3dup(stack=stack)

    stack = [0x01, 0x02, 0x03]
    op_3dup(stack=stack)
    assert stack == [0x01, 0x02, 0x03, 0x01, 0x02, 0x03]


def test_op_2over():
    with pytest.raises(StackError):
        stack = [0x01, 0x02, 0x03]
        op_2over(stack=stack)

    stack = [0x01, 0x02, 0x03, 0x04]
    op_2over(stack=stack)
    assert stack == [0x01, 0x02, 0x03, 0x04, 0x01, 0x02]


def test_op_2rot():
    with pytest.raises(StackError):
        stack = [0x01, 0x02, 0x03, 0x04, 0x05]
        op_2rot(stack=stack)

    stack = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
    op_2rot(stack=stack)
    assert stack == [0x03, 0x04, 0x05, 0x06, 0x01, 0x02]


def test_op_2swap():
    with pytest.raises(StackError):
        stack = [0x01, 0x02, 0x03]
        op_2swap(stack=stack)

    stack = [0x01, 0x02, 0x03, 0x04]
    op_2swap(stack=stack)
    assert stack == [0x03, 0x04, 0x01, 0x02]


# BITWISE-LOGIC TESTS
# ----------------------------------------------------------------------------


def test_op_equal():
    with pytest.raises(StackError):
        stack = [0x09]
        op_equal(stack=stack)

    stack = [0x09, 0x08] 
    op_equal(stack=stack)
    assert stack == [encode_num(0)]

    stack = [0x09, 0x09] 
    op_equal(stack=stack)
    assert stack == [encode_num(1)]


def test_op_equalverify():
    with pytest.raises(StackError):
        stack = [0x09]
        op_equalverify(stack=stack)

    with pytest.raises(InvalidTransaction):
        stack = [0x09, 0x08] 
        op_equalverify(stack=stack)

    stack = [0x09, 0x09] 
    op_equalverify(stack=stack)


# ARITHMETIC FUNCTIONS TESTS
# ----------------------------------------------------------------------------

def test_op_1add():
    with pytest.raises(StackError):
        stack = []
        op_1add(stack=stack)

    stack = [encode_num(1)]
    op_1add(stack=stack)
    assert stack == [encode_num(2)]


def test_op_1sub():
    with pytest.raises(StackError):
        stack = []
        op_1sub(stack=stack)

    stack = [encode_num(3)]
    op_1sub(stack=stack)
    assert stack == [encode_num(2)]


def test_op_2mul():
    with pytest.raises(BadOpCode):
        op_2mul(stack=[])


def test_op_2div():
    with pytest.raises(BadOpCode):
        op_2div(stack=[])


def test_op_negate():
    with pytest.raises(StackError):
        stack = []
        op_negate(stack=stack)

    tests = [
        (-1, 1),
        (10, -10),
        (2, -2),
        (0, 0),
        (-31, 31),
    ]
    for a, b in tests:
        stack = [encode_num(a)]
        op_negate(stack=stack)
        assert stack == [encode_num(b)]


def test_op_abs():
    with pytest.raises(StackError):
        stack = []
        op_abs(stack=stack)
    
    tests = [
        (-1, 1),
        (10, 10),
        (-2, 2),
        (-0, 0),
        (31, 31),
    ]
    for a, b in tests:
        stack = [encode_num(a)]
        op_abs(stack=stack)
        assert stack == [encode_num(b)]


def test_op_not():
    with pytest.raises(StackError):
        stack = []
        op_not(stack=stack)

    tests = (
        (0, 1),
        (1, 0),
        (2, 0),
        (-1, 0),
        (7, 0),
    )
    for a, b in tests:
        stack = [encode_num(a)]
        op_not(stack=stack)
        assert stack == [encode_num(b)]


def test_op_0notequal():
    with pytest.raises(StackError):
        stack = []
        op_0notequal(stack=stack)

    tests = (
        (0, 0),
        (1, 1),
        (2, 1),
        (-1, 1),
        (-7, 1),
    )
    for a, b in tests:
        stack = [encode_num(a)]
        op_0notequal(stack=stack)
        assert stack == [encode_num(b)]


def test_op_add():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_add(stack=stack)

    tests = (
        (0, 0, 0),
        (1, 1, 2),
        (2, 1, 3),
        (-1, 1, 0),
        (-7, 1, -6),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_add(stack=stack)
        assert stack == [encode_num(c)]


def test_op_sub():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_sub(stack=stack)

    tests = (
        (0, 0, 0),
        (1, 1, 0),
        (2, 1, 1),
        (-1, 1, -2),
        (-7, 1, -8),
        (14, 6, 8),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_sub(stack=stack)
        assert stack == [encode_num(c)]


def test_op_mul():
    with pytest.raises(BadOpCode):
        op_mul(stack=[])


def test_op_div():
    with pytest.raises(BadOpCode):
        op_div(stack=[])


def test_op_mod():
    with pytest.raises(BadOpCode):
        op_mod(stack=[])


def test_op_lshift():
    with pytest.raises(BadOpCode):
        op_lshift(stack=[])


def test_op_rshift():
    with pytest.raises(BadOpCode):
        op_rshift(stack=[])


def test_op_booland():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_booland(stack=stack)

    tests = (
        (0, 0, 0),
        (2, 1, 1),
        (-1, 0, 0),
        (0, 5, 0),
        (7, -1, 1),
        (17, 5, 1),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_booland(stack=stack)
        assert stack == [encode_num(c)]


def test_op_boolor():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_boolor(stack=stack)

    tests = (
        (0, 0, 0),
        (2, 1, 1),
        (-1, 0, 1),
        (0, 5, 1),
        (7, -1, 1),
        (17, 5, 1),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_boolor(stack=stack)
        assert stack == [encode_num(c)]


def test_op_numequal():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_numequal(stack=stack)

    tests = (
        (0, 0, 1),
        (2, 1, 0),
        (-1, 0, 0),
        (5, 5, 1),
        (7, -1, 0),
        (-7, -7, 1),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_numequal(stack=stack)
        assert stack == [encode_num(c)]


def test_op_numequal():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_numequal(stack=stack)

    tests = (
        (0, 0, 1),
        (2, 1, 0),
        (-1, 0, 0),
        (5, 5, 1),
        (7, -1, 0),
        (-7, -7, 1),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_numequal(stack=stack)
        assert stack == [encode_num(c)]


def test_op_numequalverify():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_numequalverify(stack=stack)

    invalid_tests = (
        (2, 1, 0),
        (-1, 0, 0),
        (7, -1, 0),
    )
    for a, b, c in invalid_tests:
        with pytest.raises(InvalidTransaction):
            stack = [encode_num(a), encode_num(b)]
            op_numequalverify(stack=stack)

    valid_tests = (
        (0, 0, 1),
        (5, 5, 1),
        (-7, -7, 1),
    )
    for a, b, c in valid_tests:
        stack = [encode_num(a), encode_num(b)]
        op_numequalverify(stack=stack)


def test_op_numnotequal():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_numnotequal(stack=stack)

    tests = (
        (0, 0, 0),
        (2, 1, 1),
        (-1, 0, 1),
        (5, 5, 0),
        (7, -1, 1),
        (-7, -7, 0),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_numnotequal(stack=stack)
        assert stack == [encode_num(c)]


def test_op_lessthan():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_lessthan(stack=stack)

    tests = (
        (0, 0, 0),
        (2, 1, 0),
        (-1, 0, 1),
        (5, 5, 0),
        (7, -1, 0),
        (-7, -7, 0),
        (13, 27, 1),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_lessthan(stack=stack)
        assert stack == [encode_num(c)]


def test_op_greaterthan():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_greaterthan(stack=stack)

    tests = (
        (0, 0, 0),
        (2, 1, 1),
        (-1, 0, 0),
        (5, 5, 0),
        (7, -1, 1),
        (-7, -7, 0),
        (13, 27, 0),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_greaterthan(stack=stack)
        assert stack == [encode_num(c)]


def test_op_lessthanorequal():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_lessthanorequal(stack=stack)

    tests = (
        (0, 0, 1),
        (2, 1, 0),
        (-1, 0, 1),
        (5, 5, 1),
        (7, -1, 0),
        (-7, -7, 1),
        (13, 27, 1),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_lessthanorequal(stack=stack)
        assert stack == [encode_num(c)]


def test_op_greaterthanorequal():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_greaterthanorequal(stack=stack)

    tests = (
        (0, 0, 1),
        (2, 1, 1),
        (-1, 0, 0),
        (5, 5, 1),
        (7, -1, 1),
        (-7, -7, 1),
        (13, 27, 0),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_greaterthanorequal(stack=stack)
        assert stack == [encode_num(c)]


def test_op_min():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_min(stack=stack)

    tests = (
        (0, 0, 0),
        (2, 1, 1),
        (-1, 0, -1),
        (5, 5, 5),
        (7, -1, -1),
        (-7, -7, -7),
        (13, 27, 13),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_min(stack=stack)
        assert stack == [encode_num(c)]


def test_op_max():
    with pytest.raises(StackError):
        stack = [encode_num(1)]
        op_max(stack=stack)

    tests = (
        (0, 0, 0),
        (2, 1, 2),
        (-1, 0, 0),
        (5, 5, 5),
        (7, -1, 7),
        (-7, -7, -7),
        (13, 27, 27),
    )
    for a, b, c in tests:
        stack = [encode_num(a), encode_num(b)]
        op_max(stack=stack)
        assert stack == [encode_num(c)]


def test_op_within():
    with pytest.raises(StackError):
        stack = [encode_num(1), encode_num(2)]
        op_within(stack=stack)

    tests = (
        (-1, 0, 5, 0),
        (0, 0, 5, 1),
        (1, 0, 5, 1),
        (2, 0, 5, 1),
        (5, 0, 5, 0),
        (6, 0, 5, 0),
    )
    for a, b, c, d, in tests:
        stack = [encode_num(a), encode_num(b), encode_num(c)]
        op_within(stack=stack)
        assert stack == [encode_num(d)]


# CRYPTO FUNCTIONS TESTS
# ----------------------------------------------------------------------------


def test_op_ripemd160():
    with pytest.raises(StackError):
        stack = []
        op_ripemd160(stack=stack)

    stack = [b'abc']
    op_ripemd160(stack=stack)
    assert stack[-1].hex() == '8eb208f7e05d987a9b044a8e98c6b087f15a0bfc'


def test_op_sha1():
    stack = [b'abc']
    op_sha1(stack=stack)
    assert stack[-1].hex() == 'a9993e364706816aba3e25717850c26c9cd0d89d'


def test_op_sha256():
    stack = [b'abc']
    op_sha256(stack=stack)
    assert stack[-1].hex() == 'ba7816bf8f01cfea414140de5dae2223' \
                              'b00361a396177a9cb410ff61f20015ad'


def test_op_hash160():
    with pytest.raises(StackError):
        stack = []
        op_hash160(stack=stack)

    x = bytes.fromhex('0001')
    stack = [x]
    op_hash160(stack=stack)
    assert stack == [hash160(x)]


def test_op_hash256():
    with pytest.raises(StackError):
        stack = []
        op_hash256(stack=stack)

    x = bytes.fromhex('0001')
    stack = [x]
    op_hash256(stack=stack)
    assert stack == [hash256(x)]


def test_op_checksig():
    z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
    sec = bytes.fromhex('04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10'
                        'd006e4da568744d06c61de6d95231cd89026e286df3b6ae4'
                        'a894a3378e393e93a0f45b666329a0ae34')
    sig = bytes.fromhex('3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840'
                        'f404876325a1e8ffe0529a2c022100c7207fee197d27c618'
                        'aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab601')
    stack = [sig, sec]
    op_checksig(stack=stack, z=z)
    assert stack == [encode_num(1)]
