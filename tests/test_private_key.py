from bitcoin.private_key import PrivateKey


def test_wif():
    private_key = PrivateKey(5003)
    assert private_key.wif(compressed=True, testnet=True) == \
        'cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMN8rFTv2sfUK'

    private_key = PrivateKey(2021**5)
    assert private_key.wif(compressed=False, testnet=True) == \
        '91avARGdfge8E4tZfYLoxeJ5sGBdNJQH4kvjpWAxgzczjbCwxic'

    private_key = PrivateKey(0x54321deadbeef)
    assert private_key.wif(compressed=True, testnet=False) == \
        'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgiuQJv1h8Ytr2S53a'
