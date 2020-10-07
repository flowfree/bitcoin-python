from .helpers import (
    encode_varints, int_to_little_endian, little_endian_to_int, 
    read_varints
)
from .op import (
    op_dup, op_hash160, op_hash256
)


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

OP_CODE_FUNCTIONS = {
    0x76: op_dup,
    0xa9: op_hash160,
    0xaa: op_hash256,
}


class Script(object):
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

    @staticmethod
    def parse(stream):
        """
        Read and parse Script from a stream.
        """

        length = read_varints(stream)
        cmds = []
        count = 0
        while count < length:
            current = stream.read(1)
            count += 1
            current_byte = current[0]
            if current_byte > OP_0 and current_byte < OP_PUSHDATA1:
                # For a number between 1-75, the next n bytes are an element
                n = current_byte
                cmds.append(stream.read(n))
                count += n
            elif current_byte == OP_PUSHDATA1:
                # The next byte tells us how many bytes to read
                data_length = little_endian_to_int(stream.read(1))
                cmds.append(stream.read(data_length))
                count += data_length + 1
            elif current_byte == OP_PUSHDATA2:
                # The next two bytes tell us how many bytes to read
                data_length = little_endian_to_int(stream.read(2))
                cmds.append(stream.read(data_length))
                count += data_length + 2
            else:
                # We have an opcode to store
                op_code = current_byte
                cmds.append(op_code)
        if count != length:
            raise SyntaxError('Parsing script failed.')

        return Script(cmds)

    def serialize(self):
        result = b''
        for cmd in self.cmds:
            if type(cmd) == int:
                result += int_to_little_endian(cmd, 1)
            else:
                length = len(cmd)
                if length < 0x4b:
                    result += int_to_little_endian(length, 1)
                elif length >= 0x4c and length < 0x100:
                    result += int_to_little_endian(OP_PUSHDATA1, 1)
                    result += int_to_little_endian(length, 1)
                elif length >= 0x100 and length <= 0x208:
                    result += int_to_little_endian(OP_PUSHDATA2, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError('Too long for a cmd.')
                result += cmd

        length = len(result)
        return encode_varints(length) + result
