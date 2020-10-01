from .helpers import hash256, little_endian_to_int


class Tx(object):
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __str__(self):
        """
        String representation of this transaction.
        """
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += f'{tx_in}\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += f'{tx_out}\n'
        
        return f'tx: {self.id()}\n' \
               f'version: {self.version}\n' \
               f'tx_ins:\n{tx_ins}' \
               f'tx_outs:\n{tx_outs}' \
               f'locktime: {self.locktime}'

    def id(self):
        """
        Human-readable hexadecimal of the transaction hash.
        """
        return self.hash.hex()

    def hash(self):
        """
        Binary hash of the legacy serialization.
        """
        return hash256(self.serialize())[::-1]

    @staticmethod
    def parse(stream):
        version_ = stream.read(4)
        self.version = little_endian_to_int(version_)
