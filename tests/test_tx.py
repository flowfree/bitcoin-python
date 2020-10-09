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
    def test_fee(self, stream):
        responses.add(
            responses.GET,
            'http://mainnet.programmingbitcoin.com/tx/' \
            'd1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81.hex',
            body='0100000002137c53f0fb48f83666fcfd2fe9f12d13e94ee109c5aeabbfa'
                 '32bb9e02538f4cb000000006a47304402207e6009ad86367fc4b166bc80'
                 'bf10cf1e78832a01e9bb491c6d126ee8aa436cb502200e29e6dd7708ed4'
                 '19cd5ba798981c960f0cc811b24e894bff072fea8074a7c4c012103bc9e'
                 '7397f739c70f424aa7dcce9d2e521eb228b0ccba619cd6a0b9691da796a'
                 '1ffffffff517472e77bc29ae59a914f55211f05024556812a2dd7d8df29'
                 '3265acd8330159010000006b483045022100f4bfdb0b3185c778cf28acb'
                 'af115376352f091ad9e27225e6f3f350b847579c702200d69177773cd2b'
                 'b993a816a5ae08e77a6270cf46b33f8f79d45b0cd1244d9c4c0121031c0'
                 'b0b95b522805ea9d0225b1946ecaeb1727c0b36c7e34165769fd8ed860b'
                 'f5ffffffff027a958802000000001976a914a802fc56c704ce87c42d7c9'
                 '2eb75e7896bdc41ae88aca5515e00000000001976a914e82bd75c9c662c'
                 '3f5700b33fec8a676b6e9391d588ac00000000',
            status=200,
        )

        tx = Tx.parse(stream)
        assert tx.fee() == 40000


class TestTxOut:
    def test_parse(self, monkeypatch):
        monkeypatch.setattr(Script, 'parse', lambda s: Script())

        raw_hex = 'a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac'
        stream = BytesIO(bytes.fromhex(raw_hex))

        tx_out = TxOut.parse(stream)

        assert tx_out.amount == 32454049
        assert type(tx_out.script_pubkey) == Script
