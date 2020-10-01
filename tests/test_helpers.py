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


def test_int_to_little_endian():
    n = helpers.int_to_little_endian(500, 16)
    assert n.hex() == 'f4010000000000000000000000000000'


def test_little_endian_to_int():
    b = bytes.fromhex('f4010000000000000000000000000000')
    assert helpers.little_endian_to_int(b) == 500