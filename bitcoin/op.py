from .helpers import decode_num, encode_num, hash160, hash256 


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


# VALUE-PUSHING FUNCTIONS
# -------------------------------------------------------------------------


def op_NUM(**kwargs):
    num = kwargs.get('num')
    stack = kwargs.get('stack')
    if num is None or stack is None:
        return False
    stack.append(encode_num(num))
    return True


def op_0(**kwargs):
    """
    Push an empty array of bytes onto the stack.
    """
    return op_NUM(num=0, **kwargs)


def op_1(**kwargs):
    """
    Push the number 1 onto the stack.
    """
    return op_NUM(num=1, **kwargs)


def op_2(**kwargs):
    """
    Push the number 2 onto the stack.
    """
    return op_NUM(num=2, **kwargs)


def op_3(**kwargs):
    """
    Push the number 3 onto the stack.
    """
    return op_NUM(num=3, **kwargs)


def op_4(**kwargs):
    """
    Push the number 4 onto the stack.
    """
    return op_NUM(num=4, **kwargs)


def op_5(**kwargs):
    """
    Push the number 5 onto the stack.
    """
    return op_NUM(num=5, **kwargs)


def op_6(**kwargs):
    """
    Push the number 6 onto the stack.
    """
    return op_NUM(num=6, **kwargs)


def op_7(**kwargs):
    """
    Push the number 7 onto the stack.
    """
    return op_NUM(num=7, **kwargs)


def op_8(**kwargs):
    """
    Push the number 8 onto the stack.
    """
    return op_NUM(num=8, **kwargs)


def op_9(**kwargs):
    """
    Push the number 9 onto the stack.
    """
    return op_NUM(num=9, **kwargs)


def op_10(**kwargs):
    """
    Push the number 10 onto the stack.
    """
    return op_NUM(num=10, **kwargs)


def op_11(**kwargs):
    """
    Push the number 11 onto the stack.
    """
    return op_NUM(num=11, **kwargs)


def op_12(**kwargs):
    """
    Push the number 12 onto the stack.
    """
    return op_NUM(num=12, **kwargs)


def op_13(**kwargs):
    """
    Push the number 13 onto the stack.
    """
    return op_NUM(num=13, **kwargs)


def op_14(**kwargs):
    """
    Push the number 14 onto the stack.
    """
    return op_NUM(num=14, **kwargs)


def op_15(**kwargs):
    """
    Push the number 15 onto the stack.
    """
    return op_NUM(num=15, **kwargs)


def op_16(**kwargs):
    """
    Push the number 16 onto the stack.
    """
    return op_NUM(num=16, **kwargs)


def op_1negate(**kwargs):
    """
    Push the number -1 onto the stack.
    """
    return op_NUM(num=-1, **kwargs)


# FLOW CONTROL FUNCTIONS
# ---------------------------------------------------------


def op_nop(**kwargs):
    """Does nothing"""
    return True


def op_if(stackval=True, **kwargs):
    """
    Remake the commands array to contain only the IF block if the 
    top stack value is true.
    """
    stack = kwargs.get('stack')
    commands = kwargs.get('commands')
    if stack is None or len(stack) < 1:
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


def op_notif(**kwargs):
    """
    Remake the commands array to contain only the NOTIF block if the 
    top stack value is false.
    """
    return op_if(stackval=False, **kwargs)


def op_verify(**kwargs):
    """
    Marks transaction as invalid if top stack value is not true.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        return False
    element = stack.pop()
    return decode_num(element) != 0


def op_return():
    """Marks transaction as invalid."""
    return False


# STACK FUNCTIONS
# ----------------------------------------------------------------------------


def op_toaltstack(**kwargs):
    stack = kwargs.get('stack')
    altstack = kwargs.get('altstack')
    if len(stack) < 1:
        raise ValueError
    altstack.append(stack.pop())


def op_fromaltstack(**kwargs):
    stack = kwargs.get('stack')
    altstack = kwargs.get('altstack')
    if len(altstack) < 1:
        raise ValueError
    stack.append(altstack.pop())


def op_ifdup(**kwargs):
    """
    If the top stack value is true, duplicate it.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise ValueError
    num = decode_num(stack[-1])
    if num != 0:
        stack.append(encode_num(num))


def op_depth(**kwargs):
    """
    Puts the number of stack items onto the stack.
    """
    stack = kwargs.get('stack')
    num = len(stack)
    stack.append(encode_num(num))


def op_drop(**kwargs):
    """
    Removes the top stack item.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise ValueError
    stack.pop()


def op_dup(**kwargs):
    """
    Duplicates the top stack item.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise ValueError
    stack.append(stack[-1])


def op_nip(**kwargs):
    """
    Removes the second-to-top stack item.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise ValueError
    del stack[-2]


def op_over(**kwargs):
    """
    Copies the second-to-top stack item to the top.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise ValueError
    stack.append(stack[-2])


def op_pick(**kwargs):
    raise NotImplementedError


def op_roll(**kwargs):
    raise NotImplementedError


def op_rot(**kwargs):
    """
    The top three items on the stack are rotated to the left.
    """
    stack = kwargs.get('stack')
    if len(stack) < 3:
        raise ValueError
    a, b, c = stack[-3], stack[-2], stack[-1]
    stack[-3], stack[-2], stack[-1] = b, c, a


def op_swap(**kwargs):
    """
    The top two items on the stack are swapped.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise ValueError
    a, b = stack[-2], stack[-1]
    stack[-2], stack[-1] = b, a


def op_tuck(stack=[], **kwargs):
    """
    The item at the top of the stack is copied and inserted 
    before the second-to-top item.
    """
    if len(stack) < 2:
        raise ValueError
    stack.insert(-2, stack[-1])


def op_2drop(**kwargs):
    """
    Removes the top two stack items.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise ValueError
    stack.pop()
    stack.pop()


def op_2dup(**kwargs):
    """
    Duplicates the top two stack items.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise ValueError
    a, b = stack[-2], stack[-1]
    stack.append(a)
    stack.append(b)


def op_3dup(**kwargs):
    """
    Duplicates the top three stack items.
    """
    stack = kwargs.get('stack')
    if len(stack) < 3:
        raise ValueError
    a, b, c = stack[-3], stack[-2], stack[-1]
    stack.append(a)
    stack.append(b)
    stack.append(c)


def op_2over(**kwargs):
    """
    Copies the pair of items two spaces back in the stack to the front.
    """
    stack = kwargs.get('stack')
    if len(stack) < 4:
        raise ValueError
    a, b = stack[-4], stack[-3]
    stack.append(a)
    stack.append(b)


def op_2rot(**kwargs):
    """
    The fifth and sixth items back are moved to the top of the stack.
    """
    stack = kwargs.get('stack')
    if len(stack) < 6:
        raise ValueError
    a = stack.pop(-5)
    b = stack.pop(-5)
    stack.append(b)
    stack.append(a)


def op_2swap(**kwargs):
    """
    Swaps the top two pairs of items.
    """
    stack = kwargs.get('stack')
    if len(stack) < 4:
        raise ValueError
    a, b, c, d = stack[-4], stack[-3], stack[-2], stack[-1]
    stack[-4], stack[-3], stack[-2], stack[-1] = c, d, a, b


# SPLICE FUNCTIONS
# ----------------------------------------------------------------------------


def op_cat():
    """Concatenates two strings. DISABLED"""
    return False


def op_substr():
    """Returns a section of a string. DISABLED"""
    return False


def op_left():
    """
    Keeps only characters left of the specified point in a string. DISABLED
    """
    return False


def op_right():
    """
    Keeps only characters right of the specified point in a string. DISABLED
    """
    return False


def op_size():
    """
    Pushes the string length of the top element of the stack 
    (without popping it).
    """
    raise NotImplementedError


# BITWISE LOGIC
# ----------------------------------------------------------------------------


def op_invert():
    """Flips all of the bits in the input. DISABLED"""
    return False


def op_and():
    """Boolean and between each bit in the inputs. DISABLED"""
    return False


def op_or():
    """Boolean or between each bit in the inputs. DISABLED"""
    return False


def op_xor():
    """	Boolean exclusive or between each bit in the inputs. DISABLED"""
    return False


def op_equal():
    """Returns 1 if the inputs are exactly equal, 0 otherwise."""
    raise NotImplementedError


def op_equalverify():
    """	Same as OP_EQUAL, but runs OP_VERIFY afterward."""
    raise NotImplementedError


# CRYPTO FUNCTIONS
# ----------------------------------------------------------------------------


def op_hash160(**kwargs):
    stack = kwargs.get('stack')
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash160(element))
    return True


def op_hash256(**kwargs):
    stack = kwargs.get('stack')
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash256(element))
    return True


OP_CODE_FUNCTIONS = {
    # Value-pushing functions
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
    OP_1NEGATE: op_1negate,

    # Flow control functions
    OP_NOP: op_nop,
    OP_IF: op_if,
    OP_NOTIF: op_notif,
    OP_VERIFY: op_verify,
    OP_RETURN: op_return,

    # Stack functions
    OP_TOALTSTACK: op_toaltstack,
    OP_FROMALTSTACK: op_fromaltstack,
    OP_IFDUP: op_ifdup,
    OP_DEPTH: op_depth,
    OP_DROP: op_drop,
    OP_DUP: op_dup,
    OP_NIP: op_nip,
    OP_OVER: op_over,
    OP_PICK: op_pick,
    OP_ROLL: op_roll,
    OP_ROT: op_rot,
    OP_SWAP: op_swap,
    OP_TUCK: op_tuck,
    OP_2DROP: op_2drop,
    OP_2DUP: op_2dup,
    OP_3DUP: op_3dup,
    OP_2OVER: op_2over,
    OP_2ROT: op_2rot,
    OP_2SWAP: op_2swap,

    # Splice functions
    OP_CAT: op_cat,
    OP_SUBSTR: op_substr,
    OP_LEFT: op_left,
    OP_RIGHT: op_right,
    OP_SIZE: op_size,

    # Bitwise logic functions
    OP_INVERT: op_invert,
    OP_AND: op_and,
    OP_OR: op_or,
    OP_XOR: op_xor,
    OP_EQUAL: op_equal,
    OP_EQUALVERIFY: op_equalverify,

    # Crypto functions
    OP_HASH160: op_hash160,
    OP_HASH256: op_hash256,
}
