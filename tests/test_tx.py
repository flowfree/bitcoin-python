from io import BytesIO

import pytest
import responses

from bitcoin.script import Script
from bitcoin.tx import Tx, TxIn, TxOut


@pytest.fixture
def raw_tx():
    return bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1' \
                         'd96a3f5f71bf8303c6a989c7d1000000006b483045022100' \
                         'ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf2' \
                         '1320b0277457c98f02207a986d955c6e0cb35d446a89d3f5' \
                         '6100f4d7f67801c31967743a9c8e10615bed01210349fc4e' \
                         '631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213' \
                         'bf016b278afeffffff02a135ef01000000001976a914bc3b' \
                         '654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800' \
                         '000000001976a9141c4bc762dd5423e332166702cb75f40d' \
                         'f79fea1288ac19430600')


@pytest.fixture
def stream(raw_tx):
    return BytesIO(raw_tx)


class TestTx:
    def test_parse_version(self, stream):
        tx = Tx.parse(stream)
        assert tx.version == 1

    def test_parse_inputs(self, stream):
        tx = Tx.parse(stream)

        assert len(tx.tx_ins) == 1
        assert tx.tx_ins[0].prev_tx == bytes.fromhex('d1c789a9c60383bf715f3f6ad9d14b91' \
                                                    'fe55f3deb369fe5d9280cb1a01793f81')
        assert tx.tx_ins[0].prev_index == 0

    def test_parse_outputs(self, stream):
        tx = Tx.parse(stream)

        assert len(tx.tx_outs) == 2
        assert tx.tx_outs[0].amount == 32454049
        assert type(tx.tx_outs[0].script_pubkey) == Script
        assert tx.tx_outs[1].amount == 10011545
        assert type(tx.tx_outs[1].script_pubkey) == Script

    def test_parse_locktime(self, stream):
        tx = Tx.parse(stream)
        assert tx.locktime == 410393

    def test_serialize(self, raw_tx, stream):
        tx = Tx.parse(stream)
        assert tx.serialize() == raw_tx

    @responses.activate
    def test_fee(self, stream, load_raw_tx):
        prev_tx_id = 'd1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81'

        responses.add(
            responses.GET,
            f'https://blockstream.info/api/tx/{prev_tx_id}/hex',
            body=load_raw_tx(f'{prev_tx_id}.txt'),
            status=200,
        )

        tx = Tx.parse(stream)
        assert tx.fee() == 40000

    @responses.activate
    def test_sig_hash(self, stream, load_raw_tx):
        prev_tx_id = 'd1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81'

        responses.add(
            responses.GET,
            f'https://blockstream.info/api/tx/{prev_tx_id}/hex',
            body=load_raw_tx(f'{prev_tx_id}.txt'),
            status=200,
        )

        tx = Tx.parse(stream)
        sig = tx.sig_hash(0)
        assert hex(sig) == '0x27e0c5994dec7824e56dec6b2fcb342' \
                           'eb7cdb0d0957c2fce9882f715e85d81a6'

    @responses.activate
    def test_verify(self, stream, load_raw_tx):
        prev_tx_id = 'd1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81'

        responses.add(
            responses.GET,
            f'https://blockstream.info/api/tx/{prev_tx_id}/hex',
            body=load_raw_tx(f'{prev_tx_id}.txt'),
            status=200,
        )

        tx = Tx.parse(stream)
        assert tx.verify() == True


class TestTxOut:
    def test_parse(self, monkeypatch):
        monkeypatch.setattr(Script, 'parse', lambda s: Script())

        raw_hex = 'a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac'
        stream = BytesIO(bytes.fromhex(raw_hex))

        tx_out = TxOut.parse(stream)

        assert tx_out.amount == 32454049
        assert type(tx_out.script_pubkey) == Script
