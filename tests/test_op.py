import pytest 

from bitcoin import helpers
from bitcoin.op import (
    op_dup, op_hash160, op_hash256
)


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
