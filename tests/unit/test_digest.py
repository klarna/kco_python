import unittest
from klarnacheckout.digest import create_digester


class TestDigest(unittest.TestCase):

    expected = "MO/6KvzsY2y+F+/SexH7Hyg16gFpsPDx5A2PtLZd0Zs="

    def test_create_digest(self):
        data = '{"eid":1245,"goods_list":[{"artno":"id_1","name":'\
            '"product","price":12345,"vat":25,"qty":1}],"currency":"SEK"'\
            ',"country":"SWE","language":"SV"}'.encode('utf-8')

        digester = create_digester('mySecret')
        self.assertEquals(self.expected, digester(data))
