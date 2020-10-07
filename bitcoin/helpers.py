import hashlib 


BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result


def hash256(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()


def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])


def little_endian_to_int(b):
    return int.from_bytes(b, 'little')


def int_to_little_endian(n, num_bytes):
    return n.to_bytes(num_bytes, 'little')


def read_varints(stream):
    """
    Reads a variable integer from a stream.
    """
    i = stream.read(1)[0]
    if i == 0xfd:
        return little_endian_to_int(stream.read(2))
    elif i == 0xfe:
        return little_endian_to_int(stream.read(4))
    elif i == 0xff:
        return little_endian_to_int(stream.read(8))
    else:
        return i


def encode_varints(i):
    """
    Encodes an integer as a varint.
    """
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise ValueError(f'Integer too large: {i}')


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
