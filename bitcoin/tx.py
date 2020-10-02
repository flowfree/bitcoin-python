from .helpers import hash256, little_endian_to_int, read_varints
from .script import Script


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
    def parse(stream, testnet=False):
        version = little_endian_to_int(stream.read(4))
        inputs = []
        num_inputs = read_varints(stream)
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(stream))
        outputs = []
        num_outputs = read_varints(stream)
        for _ in range(num_outputs):
            outputs.append(TxOut.parse(stream))
        sequence = stream.read(4)

        return Tx(version, inputs, outputs, None, testnet=testnet)


class TxIn(object):
    def __init__(self, prev_tx, prev_index, 
                 script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __str__(self):
        return f'{self.prev_tx.hex()}: {self.prev_index}'

    @staticmethod
    def parse(stream, testnet=False):
        prev_tx = stream.read(32)[::-1]
        prev_index = little_endian_to_int(stream.read(4))
        script_sig = Script.parse(stream)
        sequence = little_endian_to_int(stream.read(4))

        return TxIn(prev_tx, prev_index, script_sig, sequence)


class TxOut(object):
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __str__(self):
        return f'{self.amount}: {self.script_pubkey}'

    @staticmethod
    def parse(stream, testnet=False):
        amount = little_endian_to_int(stream.read(8))
        length = read_varints(stream)
        print(length)
        script_pubkey = stream.read(length)

        return TxOut(amount, script_pubkey)
