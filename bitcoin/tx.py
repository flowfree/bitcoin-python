from io import BytesIO

import requests 

from .exceptions import InvalidTransaction, ScriptError
from .helpers import (
    encode_varints, hash256, int_to_little_endian, little_endian_to_int, 
    read_varints
)
from .script import Script


SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
SIGHASH_ANYONECANPAY = 128


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
        return self.hash().hex()

    def hash(self):
        """
        Binary hash of the legacy serialization.
        """
        return hash256(self.serialize())[::-1]

    def fee(self):
        """
        Returns the fee of this transaction in satoshi.
        """
        input_sum, output_sum = 0, 0
        for tx_in in self.tx_ins:
            input_sum += tx_in.value(self.testnet)
        for tx_out in self.tx_outs:
            output_sum += tx_out.amount
        return input_sum - output_sum

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
        locktime = little_endian_to_int(stream.read(4))

        return Tx(version, inputs, outputs, locktime, testnet=testnet)

    def serialize(self):
        """
        Return the byte serialization of the transaction.
        """
        result = int_to_little_endian(self.version, 4)
        result += encode_varints(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varints(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result

    def sig_hash(self, input_index):
        sig = int_to_little_endian(self.version, 4)
        sig += encode_varints(len(self.tx_ins))
        for i, tx_in in enumerate(self.tx_ins):
            if i == input_index:
                script = TxIn(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    script_sig=tx_in.script_pubkey(self.testnet),
                    sequence=tx_in.sequence,
                )
            else:
                script = TxIn(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    sequence=tx_in.sequence,
                )
            sig += script.serialize()
            sig += encode_varints(len(self.tx_outs))
            for tx_out in self.tx_outs:
                sig += tx_out.serialize()
            sig += int_to_little_endian(self.locktime, 4)
            sig += int_to_little_endian(SIGHASH_ALL, 4)
            h256 = hash256(sig)
            return int.from_bytes(h256, 'big')

    def verify_input(self, input_index):
        tx_in = self.tx_ins[input_index]
        script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
        z = self.sig_hash(input_index)
        script = tx_in.script_sig + script_pubkey
        script.evaluate(z)

    def verify(self):
        """
        Verify this transaction.
        """
        if self.fee() < 0:
            raise InvalidTransaction
        for i in range(len(self.tx_ins)):
            try:
                self.verify_input(i)
            except ScriptError:
                raise InvalidTransaction
        return True


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

    def value(self, testnet=False):
        tx =TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        tx =TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey

    def serialize(self):
        """
        Returns the byte serialization of the transaction input.
        """
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result


class TxOut(object):
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __str__(self):
        return f'{self.amount}: {self.script_pubkey}'

    @staticmethod
    def parse(stream, testnet=False):
        amount = little_endian_to_int(stream.read(8))
        script_pubkey = Script.parse(stream)

        return TxOut(amount, script_pubkey)

    def serialize(self):
        """
        Return the byte serialization of the transaction output.
        """
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result


class TxFetcher:
    cache = {}

    @staticmethod
    def fetch(tx_id, testnet=False, fresh=False):
        if testnet:
            base_url = 'https://blockstream.info/testnet/api'
        else:
            base_url = 'https://blockstream.info/api'

        if fresh or (tx_id not in TxFetcher.cache):
            url = f'{base_url}/tx/{tx_id}/hex'
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError(f'Unexpected response: {response.text}')
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:
                raise ValueError(f'Not the same ID: {tx.id()} vs {tx_id}.')
            TxFetcher.cache[tx_id] = tx
        TxFetcher.cache[tx_id].testnet = testnet

        return TxFetcher.cache[tx_id]
