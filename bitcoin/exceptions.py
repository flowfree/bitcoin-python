class BitcoinError(Exception):
    def __init__(self, message=None, *args, **kwargs):
        if message is None and hasattr(self, 'message'):
            message = self.message
        super().__init__(message, *args, **kwargs)


class ScriptError(BitcoinError):
    message = 'Failed evaluating the script.'


class StackError(ScriptError):
    message = 'Not enouth elements on the stack.'


class InvalidOpCode(ScriptError):
    message = 'The specified op code has been removed.'


class BadSignature(BitcoinError):
    message = 'Bad signature.'


class InvalidTransaction(BitcoinError):
    message = 'Invalid transaction.'
