from .helpers import hash160, hash256 


def encode_num(num):
    if num == 0:
        return b''
    abs_num = abs(num)
    negative = num < 0
    result = bytearray()
    while abs_num:
        result.append(abs_num & 0xff)
        abs_num >>= 8
    if result[-1] & 0x80:
        if negative:
            result.append(0x80)
        else:
            result.append(0)
    elif negative:
        result[-1] = result[-1] | 0x80
    return bytes(result)


def decode_num(element):
    if element == b'':
        return 0
    big_endian = element[::-1]
    if big_endian[0] & 0x80:
        negative = True
        result = big_endian[0] & 0x7f
    else:
        negative = False
        result = big_endian[0]
    for c in big_endian[1:]:
        result <<= 8
        result += c
    if negative:
        return -result
    else:
        return result


def op_0(stack):
    """0x00"""
    stack.append(encode_num(0))
    return True


def op_1(stack):
    """0x51"""
    stack.append(encode_num(1))
    return True


def op_2(stack):
    """0x52"""
    stack.append(encode_num(2))
    return True


def op_3(stack):
    """0x53"""
    stack.append(encode_num(3))
    return True


def op_4(stack):
    """0x54"""
    stack.append(encode_num(4))
    return True


def op_5(stack):
    """0x55"""
    stack.append(encode_num(5))
    return True


def op_6(stack):
    """0x56"""
    stack.append(encode_num(6))
    return True


def op_7(stack):
    """0x57"""
    stack.append(encode_num(7))
    return True


def op_8(stack):
    """0x58"""
    stack.append(encode_num(8))
    return True


def op_9(stack):
    """0x59"""
    stack.append(encode_num(9))
    return True


def op_10(stack):
    """0x5a"""
    stack.append(encode_num(10))
    return True


def op_11(stack):
    """0x5b"""
    stack.append(encode_num(11))
    return True


def op_12(stack):
    """0x5c"""
    stack.append(encode_num(12))
    return True


def op_13(stack):
    """0x5d"""
    stack.append(encode_num(13))
    return True


def op_14(stack):
    """0x5e"""
    stack.append(encode_num(14))
    return True


def op_15(stack):
    """0x5f"""
    stack.append(encode_num(15))
    return True


def op_16(stack):
    """0x60"""
    stack.append(encode_num(16))
    return True


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


def op_nop():
    """0x61"""
    pass
