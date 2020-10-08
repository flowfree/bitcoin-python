class BitcoinError(Exception):
    pass 


class ScriptError(BitcoinError):
    pass


class StackError(ScriptError):
    def __init__(self):
        super().__init__('Not enough elements on the stack.')


class BadSignature(BitcoinError):
    def __init__(self):
        super().__init__("Bad signature")


class InvalidTransaction(BitcoinError):
    pass 
