import unittest
from modules.cashregister import CashRegister


class CashRegisterTest(unittest.TestCase):
    def test_spravny_dict(self):
        k = CashRegister()
        test_dict_changed = {
            "2e": 1,
            "1e": 0,
            "50c": 0,
            "20c": 0,
            "10c": 0,
            "5c": 0,
            "2c": 0,
            "1c": 0
        }
        test_dict_original = {
            "2e": 0,
            "1e": 0,
            "50c": 0,
            "20c": 0,
            "10c": 0,
            "5c": 0,
            "2c": 0,
            "1c": 0
        }

        k.buffer["2e"] += 1

        self.assertDictEqual(k.buffer, test_dict_changed)
        self.assertDictEqual(k.coins, test_dict_original)


class CashRegisterDataTest(unittest.TestCase):
    def testGetdata(self):
        kasa = CashRegister()
        kasa.buffer["2e"] += 1
        kasa.account = 11
        kasa.coins["2e"] += 1
        data = kasa.getData()
        checkData = {
            "buffer": {'10c': 0,
                       '1c': 0,
                       '1e': 0,
                       '20c': 0,
                       '2c': 0,
                       '2e': 1,
                       '50c': 0,
                       '5c': 0},
            "coins": {'10c': 0,
                      '1c': 0,
                      '1e': 0,
                      '20c': 0,
                      '2c': 0,
                      '2e': 1,
                      '50c': 0,
                      '5c': 0},
            "account": "11"
        }

        self.assertDictEqual(data, checkData)

    def testLoadFromData(self):
        originalKasa = CashRegister()
        originalKasa.account += 10
        originalKasa.coins["1e"] += 5
        originalKasa.coins["50c"] += 7
        originalKasa.coins["5c"] += 10

        data = originalKasa.getData()
        newKasa = CashRegister()
        newKasa.loadFromData(data)

        self.assertEqual(originalKasa, newKasa)


if __name__ == '__main__':
    unittest.main()
