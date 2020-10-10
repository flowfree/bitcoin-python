import hashlib 

from .exceptions import (
    InvalidOpCode, InvalidTransaction, ScriptError, StackError
)
from .helpers import (
    decode_num, encode_num, hash160, hash256 
)
from .s256_point import S256Point
from .signature import Signature


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
        raise StackError('num and stack are required.')
    stack.append(encode_num(num))


def op_0(**kwargs):
    """
    Push an empty array of bytes onto the stack.
    """
    op_NUM(num=0, **kwargs)


def op_1(**kwargs):
    """
    Push the number 1 onto the stack.
    """
    op_NUM(num=1, **kwargs)


def op_2(**kwargs):
    """
    Push the number 2 onto the stack.
    """
    op_NUM(num=2, **kwargs)


def op_3(**kwargs):
    """
    Push the number 3 onto the stack.
    """
    op_NUM(num=3, **kwargs)


def op_4(**kwargs):
    """
    Push the number 4 onto the stack.
    """
    op_NUM(num=4, **kwargs)


def op_5(**kwargs):
    """
    Push the number 5 onto the stack.
    """
    op_NUM(num=5, **kwargs)


def op_6(**kwargs):
    """
    Push the number 6 onto the stack.
    """
    op_NUM(num=6, **kwargs)


def op_7(**kwargs):
    """
    Push the number 7 onto the stack.
    """
    op_NUM(num=7, **kwargs)


def op_8(**kwargs):
    """
    Push the number 8 onto the stack.
    """
    op_NUM(num=8, **kwargs)


def op_9(**kwargs):
    """
    Push the number 9 onto the stack.
    """
    op_NUM(num=9, **kwargs)


def op_10(**kwargs):
    """
    Push the number 10 onto the stack.
    """
    op_NUM(num=10, **kwargs)


def op_11(**kwargs):
    """
    Push the number 11 onto the stack.
    """
    op_NUM(num=11, **kwargs)


def op_12(**kwargs):
    """
    Push the number 12 onto the stack.
    """
    op_NUM(num=12, **kwargs)


def op_13(**kwargs):
    """
    Push the number 13 onto the stack.
    """
    op_NUM(num=13, **kwargs)


def op_14(**kwargs):
    """
    Push the number 14 onto the stack.
    """
    op_NUM(num=14, **kwargs)


def op_15(**kwargs):
    """
    Push the number 15 onto the stack.
    """
    op_NUM(num=15, **kwargs)


def op_16(**kwargs):
    """
    Push the number 16 onto the stack.
    """
    op_NUM(num=16, **kwargs)


def op_1negate(**kwargs):
    """
    Push the number -1 onto the stack.
    """
    op_NUM(num=-1, **kwargs)


# FLOW CONTROL FUNCTIONS
# ---------------------------------------------------------


def op_nop(**kwargs):
    """Does nothing"""
    pass


def op_if(stackval=True, **kwargs):
    """
    Remake the commands array to contain only the IF block if the 
    top stack value is true.
    """

    stack = kwargs.get('stack')
    commands = kwargs.get('commands')
    if len(stack) < 1:
        raise StackError

    if_block = []
    else_block = []
    current_block = if_block
    complete = False
    num_endifs_needed = 1
    while len(commands) > 0:
        command = commands.pop(0) 
        if command in [OP_IF, OP_NOTIF]:
            num_endifs_needed += 1
        elif num_endifs_needed == 1 and command == OP_ELSE:
            current_block = else_block
            continue
        elif command == OP_ENDIF:
            if num_endifs_needed == 1:
                complete = True
                break
            num_endifs_needed -= 1
        current_block.append(command)

    if not complete:
        raise ScriptError

    element = stack.pop()
    if decode_num(element) == 0:
        commands[:0] = else_block if stackval else if_block
    else:
        commands[:0] = if_block if stackval else else_block


def op_notif(**kwargs):
    """
    Remake the commands array to contain only the NOTIF block if the 
    top stack value is false.
    """
    op_if(stackval=False, **kwargs)


def op_verify(**kwargs):
    """
    Marks transaction as invalid if top stack value is not true.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    element = stack.pop()
    if decode_num(element) == 0:
        raise InvalidTransaction


def op_return():
    """
    Marks transaction as invalid.
    """
    raise ScriptError('OP_RETURN: Transaction is invalid.')


# STACK FUNCTIONS
# ----------------------------------------------------------------------------


def op_toaltstack(**kwargs):
    """
    Puts the input onto the top of the alt stack. 
    Removes it from the main stack.
    """
    stack = kwargs.get('stack')
    altstack = kwargs.get('altstack')
    if len(stack) < 1:
        raise StackError
    altstack.append(stack.pop())


def op_fromaltstack(**kwargs):
    """
    Puts the input onto the top of the main stack. 
    Removes it from the alt stack.
    """
    stack = kwargs.get('stack')
    altstack = kwargs.get('altstack')
    if len(altstack) < 1:
        raise StackError
    stack.append(altstack.pop())


def op_ifdup(**kwargs):
    """
    If the top stack value is true, duplicate it.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
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
        raise StackError
    stack.pop()


def op_dup(**kwargs):
    """
    Duplicates the top stack item.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    stack.append(stack[-1])


def op_nip(**kwargs):
    """
    Removes the second-to-top stack item.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    del stack[-2]


def op_over(**kwargs):
    """
    Copies the second-to-top stack item to the top.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
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
        raise StackError
    a, b, c = stack[-3], stack[-2], stack[-1]
    stack[-3], stack[-2], stack[-1] = b, c, a


def op_swap(**kwargs):
    """
    The top two items on the stack are swapped.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a, b = stack[-2], stack[-1]
    stack[-2], stack[-1] = b, a


def op_tuck(stack=[], **kwargs):
    """
    The item at the top of the stack is copied and inserted 
    before the second-to-top item.
    """
    if len(stack) < 2:
        raise StackError
    stack.insert(-2, stack[-1])


def op_2drop(**kwargs):
    """
    Removes the top two stack items.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    stack.pop()
    stack.pop()


def op_2dup(**kwargs):
    """
    Duplicates the top two stack items.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a, b = stack[-2], stack[-1]
    stack.append(a)
    stack.append(b)


def op_3dup(**kwargs):
    """
    Duplicates the top three stack items.
    """
    stack = kwargs.get('stack')
    if len(stack) < 3:
        raise StackError
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
        raise StackError
    a, b = stack[-4], stack[-3]
    stack.append(a)
    stack.append(b)


def op_2rot(**kwargs):
    """
    The fifth and sixth items back are moved to the top of the stack.
    """
    stack = kwargs.get('stack')
    if len(stack) < 6:
        raise StackError
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
        raise StackError
    a, b, c, d = stack[-4], stack[-3], stack[-2], stack[-1]
    stack[-4], stack[-3], stack[-2], stack[-1] = c, d, a, b


# SPLICE FUNCTIONS
# ----------------------------------------------------------------------------


def op_cat():
    """
    Concatenates two strings. DISABLED
    """
    raise InvalidOpCode


def op_substr():
    """
    Returns a section of a string. DISABLED
    """
    raise InvalidOpCode


def op_left():
    """
    Keeps only characters left of the specified point in a string. DISABLED
    """
    raise InvalidOpCode


def op_right():
    """
    Keeps only characters right of the specified point in a string. DISABLED
    """
    raise InvalidOpCode


def op_size():
    """
    Pushes the string length of the top element of the stack 
    (without popping it).
    """
    raise NotImplementedError


# BITWISE LOGIC
# ----------------------------------------------------------------------------


def op_invert():
    """
    Flips all of the bits in the input. DISABLED
    """
    raise InvalidOpCode


def op_and():
    """
    Boolean and between each bit in the inputs. DISABLED
    """
    raise InvalidOpCode


def op_or():
    """
    Boolean or between each bit in the inputs. DISABLED
    """
    raise InvalidOpCode


def op_xor():
    """	
    Boolean exclusive or between each bit in the inputs. DISABLED
    """
    raise InvalidOpCode


def op_equal(**kwargs):
    """
    Returns 1 if the inputs are exactly equal, 0 otherwise.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    if a == b:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_equalverify(**kwargs):
    """	
    Same as OP_EQUAL, but runs OP_VERIFY afterward.
    """
    op_equal(**kwargs)
    op_verify(**kwargs)


# ARITHMETIC FUNCTIONS
# ----------------------------------------------------------------------------


def op_1add(**kwargs):
    """
    1 is added to the input.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    b = decode_num(a) + 1
    stack.append(encode_num(b))


def op_1sub(**kwargs):
    """
    1 is subtracted from the input.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    b = decode_num(a) - 1
    stack.append(encode_num(b))


def op_2mul(**kwargs):
    """
    DISABLED
    """
    raise InvalidOpCode


def op_2div(**kwargs):
    """
    DISABLED
    """
    raise InvalidOpCode


def op_negate(**kwargs):
    """
    The sign of the input is flipped.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    b = -1 * decode_num(a)
    stack.append(encode_num(b))


def op_abs(**kwargs):
    """
    The input is made positive.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    b = abs(decode_num(a))
    stack.append(encode_num(b))


def op_not(**kwargs):
    """
    If the input is 0 or 1, it is flipped. Otherwise the output will be 0.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    if a == encode_num(0):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_0notequal(**kwargs):
    """
    Returns 0 if the input is 0. 1 otherwise.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    if a == encode_num(0):
        stack.append(encode_num(0))
    else:
        stack.append(encode_num(1))


def op_add(**kwargs):
    """
    a is added to b.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    c = decode_num(a) + decode_num(b)
    stack.append(encode_num(c))


def op_sub(**kwargs):
    """
    a is subtracted from b.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    c = decode_num(b) - decode_num(a)
    stack.append(encode_num(c))


def op_mul(**kwargs):
    """
    DISABLED
    """
    raise InvalidOpCode


def op_div(**kwargs):
    """
    DISABLED
    """
    raise InvalidOpCode


def op_mod(**kwargs):
    """
    DISABLED
    """
    raise InvalidOpCode


def op_lshift(**kwargs):
    """
    DISABLED
    """
    raise InvalidOpCode


def op_rshift(**kwargs):
    """
    DISABLED
    """
    raise InvalidOpCode


def op_booland(**kwargs):
    """
    If both a and b are not 0, the output is 1. Otherwise 0.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    if decode_num(a) != 0 and decode_num(b) != 0:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_boolor(**kwargs):
    """
    If a or b is not 0, the output is 1. Otherwise 0.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    if decode_num(a) != 0 or decode_num(b) != 0:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_numequal(**kwargs):
    """
    Returns 1 if the numbers are equal, 0 otherwise.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    if a == b:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_numequalverify(**kwargs):
    """
    Same as OP_NUMEQUAL, but runs OP_VERIFY afterward.
    """
    op_numequal(**kwargs)
    op_verify(**kwargs)


def op_numnotequal(**kwargs):
    """
    Returns 1 if the numbers are not equal, 0 otherwise.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    if a != b:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_lessthan(**kwargs):
    """
    Returns 1 if b is less than a, 0 otherwise.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    if decode_num(b) < decode_num(a):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_greaterthan(**kwargs):
    """
    Returns 1 if b is greater than a, 0 otherwise.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    if decode_num(b) > decode_num(a):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_lessthanorequal(**kwargs):
    """
    Returns 1 if b is less than or equal to a, 0 otherwise.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    if decode_num(b) <= decode_num(a):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_greaterthanorequal(**kwargs):
    """
    Returns 1 if b is greater than or equal to a, 0 otherwise.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    if decode_num(b) >= decode_num(a):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_min(**kwargs):
    """
    Returns the smaller of a and b.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    c = min(decode_num(a), decode_num(b))
    stack.append(encode_num(c))


def op_max(**kwargs):
    """
    Returns the larger of a and b.
    """
    stack = kwargs.get('stack')
    if len(stack) < 2:
        raise StackError
    a = stack.pop()
    b = stack.pop()
    c = max(decode_num(a), decode_num(b))
    stack.append(encode_num(c))


def op_within(**kwargs):
    """
    Returns 1 if x is within the specified range (left-inclusive), 0 otherwise.
    """
    stack = kwargs.get('stack')
    if len(stack) < 3:
        raise StackError
    r = decode_num(stack.pop())
    l = decode_num(stack.pop())
    x = decode_num(stack.pop())
    if x >= l and x < r:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


# CRYPTO FUNCTIONS
# ----------------------------------------------------------------------------


def op_ripemd160(**kwargs):
    """
    The input is hashed using RIPEMD-160.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    b = hashlib.new('ripemd160', a).digest()
    stack.append(b)


def op_sha1(**kwargs):
    """
    The input is hashed using SHA-1.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    b = hashlib.sha1(a).digest()
    stack.append(b)


def op_sha256(**kwargs):
    """
    The input is hashed using SHA-256.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    b = hashlib.sha256(a).digest()
    stack.append(b)


def op_hash160(**kwargs):
    """
    The input is hashed twice: first with SHA-256 and then with RIPEMD-160.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    b = hash160(a)
    stack.append(b)


def op_hash256(**kwargs):
    """
    The input is hashed two times with SHA-256.
    """
    stack = kwargs.get('stack')
    if len(stack) < 1:
        raise StackError
    a = stack.pop()
    b = hash256(a)
    stack.append(b)


def op_codeseparator(**kwargs):
    pass


def op_checksig(**kwargs):
    z = kwargs.get('z')
    stack = kwargs.get('stack')

    # Check that there are at least 2 elements on the stack
    if len(stack) < 2:
        raise StackError

    # The top element of the stack is the SEC pubkey
    sec_bin = stack.pop()

    # The next element of the stack is the DER signature
    # Take off the last byte of the signature as that's the hash_type
    sig_bin = stack.pop()[:-1]

    # Parse the serialized pubkey and signature into objects
    signature = Signature.parse(sig_bin)
    pubkey = S256Point.parse(sec_bin)

    # Verify the signature using S256Point.verify()
    # Push an encoded 1 or 0 depending on whether the signature verified
    if pubkey.verify(z, signature):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))


def op_checksigverify(**kwargs):
    raise NotImplementedError


def op_checkmultisig(**kwargs):
    raise NotImplementedError


def op_checkmultisigverify(**kwargs):
    raise NotImplementedError


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

    # Arithmetic functions
    OP_1ADD: op_1add,
    OP_1SUB: op_1sub,
    OP_2MUL: op_2mul,
    OP_2DIV: op_2div,
    OP_NEGATE: op_negate,
    OP_ABS: op_abs,
    OP_NOT: op_not,
    OP_0NOTEQUAL: op_0notequal,
    OP_ADD: op_add,
    OP_SUB: op_sub,
    OP_MUL: op_mul,
    OP_DIV: op_div,
    OP_MOD: op_mod,
    OP_LSHIFT: op_lshift,
    OP_RSHIFT: op_rshift,
    OP_BOOLAND: op_booland,
    OP_BOOLOR: op_boolor,
    OP_NUMEQUAL: op_numequal,
    OP_NUMEQUALVERIFY: op_numequalverify,
    OP_NUMNOTEQUAL: op_numnotequal,
    OP_LESSTHAN: op_lessthan,
    OP_GREATERTHAN: op_greaterthan,
    OP_LESSTHANOREQUAL: op_lessthanorequal,
    OP_GREATERTHANOREQUAL: op_greaterthanorequal,
    OP_MIN: op_min,
    OP_MAX: op_max,
    OP_WITHIN: op_within,

    # Crypto functions
    OP_RIPEMD160: op_ripemd160,
    OP_SHA1: op_sha1,
    OP_HASH256: op_hash256,
    OP_HASH160: op_hash160,
    OP_CODESEPARATOR: op_codeseparator,
    OP_CHECKSIG: op_checksig,
    OP_CHECKSIGVERIFY: op_checksigverify,
    OP_CHECKMULTISIG: op_checkmultisig,
    OP_CHECKMULTISIGVERIFY: op_checkmultisigverify,
}
