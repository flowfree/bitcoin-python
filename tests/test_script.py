from io import BytesIO

from bitcoin.script import Script


def test_parse():
    stream = BytesIO(bytes.fromhex('6a47304402207899531a52d59a6de200179928ca9'
                                   '00254a36b8dff8bb75f5f5d71b1cdc26125022008'
                                   'b422690b8461cb52c3cc30330b23d574351872b7c'
                                   '361e9aae3649071c1a7160121035d5c93d9ac9688'
                                   '1f19ba1f686f15f009ded7c62efe85a872e6a19b4'
                                   '3c15a2937'))

    script = Script.parse(stream)

    want = bytes.fromhex('304402207899531a52d59a6de200179928ca900254a36b8dff8'
                         'bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc3033'
                         '0b23d574351872b7c361e9aae3649071c1a71601')
    assert script.cmds[0].hex() == want.hex()


def test_serialize():
    x = '6a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71' \
        'b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3' \
        '649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872' \
        'e6a19b43c15a2937'
    stream = BytesIO(bytes.fromhex(x))
    script = Script.parse(stream)

    assert script.serialize().hex() == x