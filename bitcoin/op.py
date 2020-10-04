from .helpers import hash160, hash256 


def op_dup(stack):
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True


def op_hash160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash160(element))
    return True


def op_hash256(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash256(element))
    return True


OP_CODE_FUNCTIONS = {
    0x76: op_dup,
    0xa9: op_hash160,
    0xaa: op_hash256,
}
