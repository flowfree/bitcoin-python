from .helpers import hash160, hash256 


# Opcode contants
# Full list is available on https://en.bitcoin.it/wiki/Script
OP_0 = 0x00
OP_PUSHDATA1 = 0x4c
OP_PUSHDATA2 = 0x4d
OP_PUSHDATA4 = 0x4e
OP_1NEGATE = 0x4f
OP_1 = 0x51
OP_2 = 0x52
OP_3 = 0x53
OP_4 = 0x54
OP_5 = 0x55
OP_6 = 0x56
OP_7 = 0x57
OP_8 = 0x58
OP_9 = 0x59
OP_10 = 0x5a
OP_11 = 0x5b
OP_12 = 0x5c
OP_13 = 0x5d
OP_14 = 0x5e
OP_15 = 0x5f
OP_16 = 0x60
OP_NOP = 0x61
OP_IF = 0x63
OP_NOTIF = 0x64
OP_ELSE = 0x67
OP_ENDIF = 0x68
OP_VERIFY = 0x69
OP_RETURN = 0x6a
OP_TOALTSTACK = 0x6b
OP_FROMALTSTACK = 0x6c
OP_IFDUP = 0x73
OP_DEPTH = 0x74
OP_DROP = 0x75
OP_DUP = 0x76
OP_NIP = 0x77
OP_OVER = 0x78
OP_PICK = 0x79
OP_ROLL = 0x7a
OP_ROT = 0x7b
OP_SWAP = 0x7c
OP_TUCK = 0x7d
OP_2DROP = 0x6d
OP_2DUP = 0x6e
OP_3DUP = 0x6f
OP_2OVER = 0x70
OP_2ROT = 0x71
OP_2SWAP = 0x72
OP_CAT = 0x7e           # Note: disabled
OP_SUBSTR = 0x7f        # Note: disabled
OP_LEFT = 0x80          # Note: disabled
OP_RIGHT = 0x81         # Note: disabled
OP_SIZE = 0x82          # Note: disabled
OP_INVERT = 0x83        # Note: disabled
OP_AND = 0x84           # Note: disabled
OP_OR = 0x85            # Note: disabled
OP_XOR = 0x86           # Note: disabled
OP_EQUAL = 0x87
OP_EQUALVERIFY = 0x88
OP_1ADD = 0x8b
OP_1SUB = 0x8c
OP_2MUL = 0x8d          # Note: disabled
OP_2DIV = 0x8e          # Note: disabled
OP_NEGATE = 0x8f
OP_ABS = 0x90
OP_NOT = 0x91
OP_0NOTEQUAL = 0x92
OP_ADD = 0x93
OP_SUB = 0x94
OP_MUL = 0x95           # Note: disabled
OP_DIV = 0x96           # Note: disabled
OP_MOD = 0x97           # Note: disabled
OP_LSHIFT = 0x98        # Note: disabled
OP_RSHIFT = 0x99        # Note: disabled
OP_BOOLAND = 0x9a
OP_BOOLOR = 0x9b
OP_NUMEQUAL = 0x9c
OP_NUMEQUALVERIFY = 0x9d
OP_NUMNOTEQUAL = 0x9e
OP_LESSTHAN = 0x9f
OP_GREATERTHAN = 0xa0
OP_LESSTHANOREQUAL = 0xa1
OP_GREATERTHANOREQUAL = 0xa2
OP_MIN = 0xa3
OP_MAX = 0xa4
OP_WITHIN = 0xa5
OP_RIPEMD160 = 0xa6
OP_SHA1 = 0xa7
OP_SHA256 = 0xa8
OP_HASH160 = 0xa9
OP_HASH256 = 0xaa
OP_CODESEPARATOR = 0xab
OP_CHECKSIG	= 0xac
OP_CHECKSIGVERIFY = 0xad
OP_CHECKMULTISIG = 0xae
OP_CHECKMULTISIGVERIFY = 0xaf
OP_CHECKLOCKTIMEVERIFY = 0xb1
OP_CHECKSEQUENCEVERIFY = 0xb2


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


def op_if(stack, commands, stackval=True):
    if len(stack) < 1:
        return False
    if_commands = []
    else_commands = []
    current_block = if_commands
    found = False
    num_endifs_needed = 1
    while len(commands) > 0:
        command = commands.pop(0) 
        if command in [OP_IF, OP_NOTIF]:
            num_endifs_needed += 1
            current_block.append(command)
        elif num_endifs_needed == 1 and command == OP_ELSE:
            current_block = else_commands
        elif command == OP_ENDIF:
            if num_endifs_needed == 1:
                found = True
                break
            else:
                num_endifs_needed -= 1
                current_block.append(command)
        else:
            current_block.append(command)

    if not found:
        return False

    element = stack.pop()
    if decode_num(element) == 0:
        commands[:0] = else_commands if stackval else if_commands
    else:
        commands[:0] = if_commands if stackval else else_commands
    return True


def op_notif(stack, commands):
    return op_if(stack, commands, stackval=False)


def op_nop():
    """0x61"""
    return True


OP_CODE_FUNCTIONS = {
    OP_0: op_0,
    OP_1: op_1,
    OP_2: op_2,
    OP_3: op_3,
    OP_4: op_4,
    OP_5: op_5,
    OP_6: op_6,
    OP_7: op_7,
    OP_8: op_8,
    OP_9: op_9,
    OP_10: op_10,
    OP_11: op_11,
    OP_12: op_12,
    OP_13: op_13,
    OP_14: op_14,
    OP_15: op_15,
    OP_16: op_16,
    OP_NOP: op_nop,
    OP_IF: op_if,
    OP_DUP: op_dup,
    OP_HASH160: op_hash160,
    OP_HASH256: op_hash256,
}