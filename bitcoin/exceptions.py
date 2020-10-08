class BitcoinError(Exception):
    pass 


class ScriptError(BitcoinError):
    pass


class BadSignature(BitcoinError):
    def __init__(self, *args, **kwargs):
        super().__init__("Bad signature", *args, **kwargs)


class InsufficientStackItems(ScriptError):
    def __init__(self, *args, **kwargs):
        msg = 'Not enough elements on the stack.'
        super().__init__(msg, *args, **kwargs)


class InvalidTransaction(BitcoinError):
    pass 
