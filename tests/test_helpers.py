from io import BytesIO

from bitcoin import helpers


def test_encode_base58():
    tests = [
        ('7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d',
         '9MA8fRQrT4u8Zj8ZRd6MAiiyaxb2Y1CMpvVkHQu5hVM6'),
        ('eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c', 
         '4fE3H2E6XMp4SsxtwinF7w9a34ooUrwWe4WsW1458Pd'),
        ('c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6', 
         'EQJsjkd6JaGwxrjEhfeqPenqHwrBmPQZjJGNSCHBkcF7'),
    ]
    for test, expected in tests:
        b = bytes.fromhex(test)
        assert helpers.encode_base58(b) == expected


def test_decode_base58():
    addr = 'mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf'
    h160 = helpers.decode_base58(addr).hex()
    want = '507b27411ccf7f16f10297de6cef3f291623eddf'
    assert h160 == want
    got = helpers.encode_base58_checksum(b'\x6f' + bytes.fromhex(h160))
    assert got == addr


def test_int_to_little_endian():
    n = helpers.int_to_little_endian(500, 16)
    assert n.hex() == 'f4010000000000000000000000000000'


def test_little_endian_to_int():
    b = bytes.fromhex('f4010000000000000000000000000000')
    assert helpers.little_endian_to_int(b) == 500


def test_encode_varints():
    assert helpers.encode_varints(255) == b'\xfd\xff\x00'
    assert helpers.encode_varints(555) == b'\xfd\x2b\x02'
    assert helpers.encode_varints(70015) == b'\xfe\x7f\x11\x01\x00'
    assert helpers.encode_varints(112233445566778899) == b'\xff\x13\x0e\xed^\xb9\xbb\x8e\x01'


def test_read_varints():
    tests = [
        (b'\x01\x00\x00', 1),
        (b'\xfd\xff\x00', 255),
        (b'\xfd\x2b\x02', 555),
        (b'\xfe\x7f\x11\x01\x00', 70015),
        (b'\xff\x13\x0e\xed^\xb9\xbb\x8e\x01', 112233445566778899),
    ]
    for x, y in tests:
        stream = BytesIO(x)
        assert helpers.read_varints(stream) == y


def test_decode_num():
    tests = [
        (b'', 0),
        (b'\x01', 1),
        (b'\x02', 2),
        (b'\x0a', 10),
        (b'\x10', 16),
        (b'\x81', -1),
        (b'\x8d', -13),
    ]
    for x, y in tests:
        assert helpers.decode_num(x) == y


def test_encode_num():
    tests = [
        (0, b''),
        (1, b'\x01'),
        (2, b'\x02'),
        (10, b'\x0a'),
        (16, b'\x10'),
        (-1, b'\x81'),
        (-13, b'\x8d'),
    ]
    for x, y in tests:
        assert helpers.encode_num(x) == y
