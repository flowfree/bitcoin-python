from .helpers import (
    encode_varints, int_to_little_endian, little_endian_to_int, 
    read_varints
)
from .op import *


class Script(object):
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

    def __add__(self, other):
        return Script(self.cmds + other.cmds)

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

    def evaluate(self, z):
        cmds = self.cmds[:]
        stack = []
        altstack = []
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            if type(cmd) == int:
                operation = OP_CODE_FUNCTIONS[cmd]
                if cmd in [OP_IF, OP_NOTIF]:
                    if not operation(stack, cmds):
                        print(f'Bad op: {cmd}')
                        return False
                elif cmd in [OP_TOALTSTACK, OP_FROMALTSTACK]:
                    if not operation(stack, altstack):
                        print(f'Bad op: {cmd}')
                        return False
                elif cmd in [OP_CHECKSIG, OP_CHECKSIGVERIFY, 
                             OP_CHECKMULTISIG, OP_CHECKMULTISIGVERIFY]:
                    if not operation(stack, z):
                        print(f'Bad op: {cmd}')
                        return False
                else:
                    if not operation(stack):
                        print(f'Bad op: {cmd}')
                        return False
            else:
                stack.append(cmd)
        if len(stack) == 0:
            return False
        if stack.pop() == b'':
            return False
        return True
