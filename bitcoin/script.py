from .exceptions import (
    InvalidTransaction, ScriptError,
)
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

    def __str__(self):
        s = ''
        for cmd in self.cmds:
            if type(cmd) == int:
                s += f' {OP_CODE_FUNCTIONS[cmd].__name__.upper()}'
            else:
                s += f' {cmd}'
        return s.strip()

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
        commands = self.cmds[:]
        stack, altstack = [], []

        while len(commands) > 0:
            cmd = commands.pop(0)
            if type(cmd) == int:
                operation = OP_CODE_FUNCTIONS[cmd]
                operation(stack=stack, 
                          altstack=altstack, 
                          commands=commands, z=z)
            else:
                stack.append(cmd)

        if len(stack) == 0 or stack.pop() == b'':
            raise ScriptError

        return True


def p2pkh_script(h160):
    return Script([OP_DUP, OP_HASH160, h160, OP_EQUALVERIFY, OP_CHECKSIG])
