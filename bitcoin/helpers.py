import hashlib 


BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def encode_base58(s):
    num = int.from_bytes(s, 'big')
    prefix = '1' * len([c for c in s if c == 0])
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



