import pytest 

from bitcoin.signature import Signature
from bitcoin.exceptions import BadSignature


def test_der():
    signature = Signature(
        0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,
        0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
    )

    assert signature.der().hex() == \
        '3045022037206a0610995c58074999cb9767b87af4c4978db68c0' \
        '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
        '119fc9a75bf8e6d0fa65c841c8e2738cdaec'


def test_parse():
    signature_bin = bytes.fromhex(
        '3045022037206a0610995c58074999cb9767b87af4c4978db68c0' \
        '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
        '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
    )

    signature = Signature.parse(signature_bin)

    assert signature == Signature(
        0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,
        0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
    )


def test_parse_bad_signatures():
    tests = [
        bytes.fromhex(
            '0345022037206a0610995c58074999cb9767b87af4c4978db68c0' \
            '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
            '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
        ),
        bytes.fromhex(
            '3045202037206a0610995c58074999cb9767b87af4c4978db68c0' \
            '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
            '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
        ),
        bytes.fromhex(
            '30450220ff37206a0610995c58074999cb9767b87af4c4978db68c0' \
            '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
            '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
        ),
        bytes.fromhex(
            '3045022037206a0610995c58074999cb9767b87af4c4978db68c0' \
            '6e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca' \
            '119fc9a75bf8e6d0fa65c841c8e2738cdaecab'
        ),
        bytes.fromhex(
            '3045022037206a0610995c58074999cb9767b87af4c4978db68c0' \
            '6e8e6e81d282047a7c60321008ca63759c1157ebeaec0d03cecca' \
            '119fc9a75bf8e6d0fa65c841c8e2738cdaec'
        ),
    ]

    for test in tests:
        with pytest.raises(BadSignature):
            Signature.parse(test)
